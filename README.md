# Projet : Hybridation métaheuristique pour le problème du voyageur de commerce (TSP)

## Description
Ce projet a été réalisé dans le cadre du module de métaheuristiques. Il porte sur le problème du voyageur de commerce (**TSP**) et compare deux approches :

- une heuristique gloutonne du **plus proche voisin** ;
- une approche hybride de type **algorithme mémétique**, combinant un **algorithme génétique** et une **recherche locale 2-opt**.

Le projet comprend le **code source**, les **instances TSPLIB**, les **résultats expérimentaux**, les **figures**, un **notebook de démonstration** et le **rapport final en PDF**.

---

## Structure du projet

### `data/tsplib/`
Ce dossier contient :
- les instances TSPLIB utilisées dans les expériences ;
- le fichier `solutions.txt`, qui regroupe les meilleurs coûts connus (**BKS**) des instances testées.

### `src/`
Ce dossier contient l’implémentation principale du projet :
- lecture des instances ;
- heuristique gloutonne ;
- algorithme mémétique ;
- recherche locale 2-opt ;
- fonctions de coût et outils utilitaires.

### `scripts/`
Ce dossier contient les scripts principaux du projet :
- `run_experiments.py` : lance les expériences sur les instances TSPLIB et produit les résultats bruts ;
- `summarize_results.py` : construit les fichiers de synthèse à partir des résultats bruts et génère les figures.

### `results/`
Ce dossier contient les sorties expérimentales :
- `raw_results.csv` : résultats bruts des exécutions ;
- `summary_results.csv` : tableau récapitulatif final ;
- `figures/` : figures générées à partir des résultats ;
- `histories/` : historiques d’exécution ou données intermédiaires utiles pour l’analyse.

### `report/`
Ce dossier contient les fichiers du rapport :
- la source LaTeX du compte rendu ;
- le fichier `tables_generated_results.tex`, qui correspond au tableau généré automatiquement et inséré dans le rapport ;
- le rapport final en PDF : `report/tsp_hybrid_report.pdf`.

### `assets/`
Ce dossier contient les éléments graphiques utilisés dans le projet, comme le logo de l’université.

### `demo_results.ipynb`
Ce notebook permet de visualiser une démonstration du projet, d’explorer une partie des résultats et d’avoir un aperçu rapide du fonctionnement global sans relancer immédiatement toutes les expériences.

---

## Prérequis
Pour exécuter le projet, il faut disposer de :
- **Python 3.10+**
- `pip`
- les bibliothèques listées dans `requirements.txt`

---

## Installation

Cloner le dépôt puis installer les dépendances :

```bash
git clone <lien-du-repository>
cd tsp_hybrid_project
pip install -r requirements.txt
````

---

## Exécution du projet

### 1. Lancer les expériences

Cette commande exécute les algorithmes sur les instances TSPLIB et enregistre les résultats bruts :

```bash
python scripts/run_experiments.py --data-dir data/tsplib --output results/raw_results.csv --runs 5 --seed 42 --solutions data/tsplib/solutions.txt
```

### 2. Générer la synthèse

Cette commande lit les résultats bruts et produit :

* le fichier récapitulatif `results/summary_results.csv` ;
* les figures dans `results/figures/` ;
* le tableau LaTeX `report/tables_generated_results.tex`, utilisé directement dans le rapport final.

```bash
python scripts/summarize_results.py --input results/raw_results.csv --summary results/summary_results.csv --latex report/tables_generated_results.tex --figure-dir results/figures
```

---

## Exécution via le notebook

Le notebook `demo_results.ipynb` peut être ouvert avec Jupyter Notebook, JupyterLab ou VS Code.

```bash
jupyter notebook demo_results.ipynb
```

Il permet de consulter rapidement une démonstration du projet et un aperçu des résultats principaux.

---

## Rapport

Le rapport final est disponible ici :

```bash
report/tsp_hybrid_report.pdf
```

Selon l’organisation du dépôt, une copie peut aussi être visible directement à la racine du repository.

---

## Livrables

Le dépôt contient :

* le code source ;
* les instructions d’exécution ;
* les résultats expérimentaux ;
* les figures ;
* le rapport final en PDF ;
* la source LaTeX du rapport ;
* le notebook `demo_results.ipynb`.

---

## Auteur

**Hafida Baazizi**

