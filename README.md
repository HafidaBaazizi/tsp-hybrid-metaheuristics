# Projet : Hybridation metaheuristique pour le probleme du voyageur de commerce (TSP)

## Description
Ce projet a ete realise dans le cadre du module de metaheuristiques. L'objectif est de resoudre le probleme du voyageur de commerce (TSP) en comparant :

- une heuristique gloutonne du plus proche voisin ;
- une approche hybride de type algorithme memetique, combinant un algorithme genetique et une recherche locale 2-opt.

Le depot contient un jeu de **22 instances TSPLIB** de tailles variees, le **code source**, les **instructions d'execution**, les **resultats experimentaux** et le **rapport PDF**.

## Structure du projet
- `data/tsplib/` : instances TSPLIB et fichier des meilleurs couts connus.
- `src/` : implementation des algorithmes.
- `scripts/` : scripts d'execution et de synthese.
- `results/` : resultats bruts, table de synthese et figures.
- `report/` : rapport en LaTeX et en PDF.
- `assets/` : logo de l'universite.

## Methodes utilisees
### 1. Heuristique gloutonne : plus proche voisin
Une ville de depart est choisie, puis on visite iterativement la ville non encore visitee la plus proche.

### 2. Hybridation retenue : algorithme memetique
L'approche principale combine :
- un algorithme genetique pour l'exploration globale ;
- une recherche locale 2-opt pour l'intensification ;
- une initialisation mixte (gloutonne multi-depart + solutions aleatoires) ;
- un taux de mutation adapte en cas de stagnation.

## Installation
Dans un terminal place a la racine du projet :

```bash
pip install -r requirements.txt
```

## Execution
### Option 1 : terminal
```bash
python scripts/run_experiments.py --data-dir data/tsplib --output results/raw_results.csv --runs 2 --seed 42 --solutions data/tsplib/solutions.txt
python scripts/summarize_results.py --input results/raw_results.csv --summary results/summary_results.csv --latex report/tables_generated_results.tex --figure-dir results/figures
```

### Option 2 : Windows
Double-cliquer sur `run_project.bat`.

## Livrables
Conformement a la consigne, ce depot contient :
- le code source avec instructions d'execution ;
- les resultats experimentaux sous forme de tableau comparatif ;
- le rapport final en PDF.

## Rapport
Le compte rendu final est disponible ici : `report/tsp_hybrid_report.pdf`.

## Auteur
**Hafida Baazizi**
