
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import math

HEADER_KEYS = {
    'NAME', 'TYPE', 'COMMENT', 'DIMENSION', 'EDGE_WEIGHT_TYPE', 'EDGE_WEIGHT_FORMAT',
    'DISPLAY_DATA_TYPE'
}
SECTION_KEYS = {'NODE_COORD_SECTION', 'EDGE_WEIGHT_SECTION', 'DISPLAY_DATA_SECTION', 'EOF'}
ALL_KEYS = HEADER_KEYS | SECTION_KEYS

@dataclass
class TSPInstance:
    name: str
    dimension: int
    edge_weight_type: str
    distance_matrix: List[List[int]]
    coords: Optional[List[Tuple[float, float]]] = None

def _tokens(text: str) -> List[str]:
    return text.replace(':', ' : ').split()

def _extract_sections(text: str):
    toks = _tokens(text)
    headers: Dict[str, str] = {}
    sections: Dict[str, List[str]] = {}
    i = 0
    current_section = None
    while i < len(toks):
        tok = toks[i]
        if tok == 'EOF':
            break
        if tok in SECTION_KEYS:
            current_section = tok
            sections[current_section] = []
            i += 1
            while i < len(toks) and toks[i] not in SECTION_KEYS:
                sections[current_section].append(toks[i])
                i += 1
            continue
        if current_section is None and tok in HEADER_KEYS:
            key = tok
            i += 1
            if i < len(toks) and toks[i] == ':':
                i += 1
            vals = []
            while i < len(toks) and toks[i] not in ALL_KEYS:
                vals.append(toks[i])
                i += 1
            headers[key] = ' '.join(vals)
            continue
        i += 1
    return headers, sections

def _geo_to_radians(value: float) -> float:
    deg = int(value)
    minutes = value - deg
    return math.pi * (deg + 5.0 * minutes / 3.0) / 180.0

def _geo_distance(a: Tuple[float, float], b: Tuple[float, float]) -> int:
    lat1 = _geo_to_radians(a[0])
    lon1 = _geo_to_radians(a[1])
    lat2 = _geo_to_radians(b[0])
    lon2 = _geo_to_radians(b[1])
    RRR = 6378.388
    q1 = math.cos(lon1 - lon2)
    q2 = math.cos(lat1 - lat2)
    q3 = math.cos(lat1 + lat2)
    dij = int(RRR * math.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0)
    return dij

def _att_distance(a: Tuple[float, float], b: Tuple[float, float]) -> int:
    xd = a[0] - b[0]
    yd = a[1] - b[1]
    rij = math.sqrt((xd * xd + yd * yd) / 10.0)
    tij = int(rij)
    return tij + 1 if tij < rij else tij

def _euc_distance(a: Tuple[float, float], b: Tuple[float, float]) -> int:
    return int(round(math.dist(a, b)))

def _coords_from_section(tokens: List[str], n: int) -> List[Tuple[float, float]]:
    coords = []
    idx = 0
    for _ in range(n):
        idx += 1  # node id
        x = float(tokens[idx]); idx += 1
        y = float(tokens[idx]); idx += 1
        coords.append((x, y))
    return coords

def _build_from_coords(coords: List[Tuple[float, float]], ew_type: str) -> List[List[int]]:
    n = len(coords)
    m = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if ew_type == 'EUC_2D':
                d = _euc_distance(coords[i], coords[j])
            elif ew_type == 'GEO':
                d = _geo_distance(coords[i], coords[j])
            elif ew_type == 'ATT':
                d = _att_distance(coords[i], coords[j])
            else:
                raise ValueError(f'Unsupported coordinate edge weight type: {ew_type}')
            m[i][j] = d
            m[j][i] = d
    return m

def _explicit_matrix(tokens: List[str], n: int, fmt: str) -> List[List[int]]:
    vals = [int(float(x)) for x in tokens]
    m = [[0] * n for _ in range(n)]
    k = 0
    if fmt == 'LOWER_DIAG_ROW':
        for i in range(n):
            for j in range(i + 1):
                m[i][j] = vals[k]
                m[j][i] = vals[k]
                k += 1
    elif fmt == 'UPPER_ROW':
        for i in range(n):
            for j in range(i + 1, n):
                m[i][j] = vals[k]
                m[j][i] = vals[k]
                k += 1
    elif fmt == 'FULL_MATRIX':
        for i in range(n):
            for j in range(n):
                m[i][j] = vals[k]
                k += 1
    else:
        raise ValueError(f'Unsupported explicit format: {fmt}')
    return m

def load_tsp_instance(path: str | Path) -> TSPInstance:
    text = Path(path).read_text(encoding='utf-8')
    headers, sections = _extract_sections(text)
    name = headers.get('NAME', Path(path).stem)
    n = int(headers['DIMENSION'])
    ew_type = headers['EDGE_WEIGHT_TYPE']
    fmt = headers.get('EDGE_WEIGHT_FORMAT', '')

    coords = None
    if 'NODE_COORD_SECTION' in sections:
        coords = _coords_from_section(sections['NODE_COORD_SECTION'], n)
    elif 'DISPLAY_DATA_SECTION' in sections:
        coords = _coords_from_section(sections['DISPLAY_DATA_SECTION'], n)

    if ew_type in {'EUC_2D', 'GEO', 'ATT'}:
        if coords is None:
            raise ValueError(f'Coordinates not found for instance {name}')
        distance_matrix = _build_from_coords(coords, ew_type)
    elif ew_type == 'EXPLICIT':
        distance_matrix = _explicit_matrix(sections['EDGE_WEIGHT_SECTION'], n, fmt)
    else:
        raise ValueError(f'Unsupported edge weight type: {ew_type}')

    return TSPInstance(name=name, dimension=n, edge_weight_type=ew_type, distance_matrix=distance_matrix, coords=coords)
