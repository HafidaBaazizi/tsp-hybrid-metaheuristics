````markdown
# Projet : Hybridation métaheuristique pour le problème du voyageur de commerce (TSP)

## Description
Ce projet a été réalisé dans le cadre du module de métaheuristiques. L’objectif est d’étudier et de comparer deux approches pour résoudre le problème du voyageur de commerce (**Traveling Salesman Problem — TSP**) :

- une heuristique gloutonne du **plus proche voisin** ;
- une approche hybride de type **algorithme mémétique**, combinant un **algorithme génétique** et une **recherche locale 2-opt**.

Le projet a été développé dans un esprit d’**hybridation**, d’**innovation** et d’**expérimentation**, conformément aux consignes de l’enseignant. Il contient un ensemble de **22 instances TSPLIB**, le **code source complet**, les **scripts d’exécution**, les **résultats expérimentaux**, les **figures de synthèse**, un **notebook de démonstration**, ainsi qu’un **rapport final en PDF**.

---

## Structure du projet

### `data/tsplib/`
Contient les instances TSPLIB utilisées dans l’étude ainsi que le fichier `solutions.txt`, qui regroupe les meilleurs coûts connus (**Best Known Solutions — BKS**) pour les instances testées.

### `src/`
Contient l’implémentation principale des différentes composantes algorithmiques : lecture des instances, heuristique gloutonne, algorithme mémétique, recherche locale 2-opt, opérateurs génétiques, calcul des coûts et fonctions utilitaires.

### `scripts/`
Contient les scripts permettant :
- d’exécuter automatiquement les expériences ;
- de générer les fichiers de résultats ;
- de produire les tableaux de synthèse et les figures.

### `results/`
Regroupe les sorties expérimentales du projet :
- `raw_results.csv` : résultats bruts des exécutions ;
- `summary_results.csv` : tableau récapitulatif des performances ;
- `figures/` : figures générées à partir des résultats.

### `report/`
Contient le rapport final du projet en **LaTeX** et en **PDF**, notamment :
- `report/tsp_hybrid_report.pdf`

Le rapport peut également être visible directement à la racine du dépôt si une copie y a été placée pour un accès plus rapide.

### `assets/`
Contient les éléments graphiques utilisés dans le rapport, comme le logo de l’université.

### `demo_results.ipynb`
Notebook Python de démonstration permettant de visualiser une exécution synthétique du projet ainsi qu’un aperçu des principaux résultats obtenus sans relancer immédiatement toutes les expériences.

---

## Prérequis
Avant d’exécuter le projet, il faut disposer de :

- **Python 3.10+** ;
- `pip` installé ;
- les bibliothèques Python listées dans `requirements.txt`.

---

## Installation

1. Cloner le dépôt GitHub :

```bash
git clone <lien-du-repository>
cd tsp_hybrid_project
````

2. Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

## Comment exécuter le projet

Une fois les dépendances installées, le projet peut être exécuté depuis un terminal placé à la racine du dépôt.

### 1. Lancer les expériences

Cette commande exécute les algorithmes sur les instances TSPLIB et enregistre les résultats bruts dans un fichier CSV :

```bash
python scripts/run_experiments.py --data-dir data/tsplib --output results/raw_results.csv --runs 5 --seed 42 --solutions data/tsplib/solutions.txt
```

### 2. Générer la synthèse des résultats

Cette commande produit :

* un tableau récapitulatif ;
* le fichier LaTeX du tableau ;
* les figures de comparaison.

```bash
python scripts/summarize_results.py --input results/raw_results.csv --summary results/summary_results.csv --latex report/tables_generated_results.tex --figure-dir results/figures
```

---

## Exécution via le notebook

Le fichier `demo_results.ipynb` permet également d’explorer le projet de manière plus interactive. Il contient une démonstration de l’exécution Python, un aperçu des résultats et peut être ouvert avec :

* **Jupyter Notebook** ;
* **JupyterLab** ;
* ou **VS Code** avec l’extension Jupyter.

Pour le lancer :

```bash
jupyter notebook demo_results.ipynb
```

Ce notebook est utile pour consulter rapidement les résultats principaux sans relancer immédiatement toutes les expériences.

---

## Résultats et livrables

Conformément à la consigne, ce dépôt contient :

* le **code source complet** ;
* les **instructions d’exécution** ;
* les **résultats expérimentaux** sous forme de fichiers CSV, tableau comparatif et figures ;
* le **rapport final en PDF** ;
* la **source LaTeX** du rapport ;
* un **notebook de démonstration** : `demo_results.ipynb`.

---

## Rapport

Le compte rendu final est disponible dans le dossier `report/` sous le fichier :

```bash
report/tsp_hybrid_report.pdf
```

Selon l’organisation du dépôt, il peut également être accessible directement à la racine du repository si une copie y a été ajoutée.

---

## Remarque

Le notebook `demo_results.ipynb` permet de visualiser rapidement une démonstration de l’exécution du projet ainsi qu’un aperçu des principaux résultats, sans devoir relancer immédiatement toutes les expériences.

---

## Auteur

**Hafida Baazizi**

```
```
