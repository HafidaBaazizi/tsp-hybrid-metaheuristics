# Projet : Hybridation métaheuristique pour le problème du voyageur de commerce (TSP)

## Description
Ce projet a été réalisé dans le cadre du module de métaheuristiques.  
L’objectif est d’étudier et de comparer deux approches pour résoudre le problème du voyageur de commerce (**TSP**) :

- une heuristique gloutonne du **plus proche voisin** ;
- une approche hybride de type **algorithme mémétique**, combinant un **algorithme génétique** et une **recherche locale 2-opt**.

Le projet a été conçu dans un esprit d’**hybridation**, d’**innovation** et d’**expérimentation**, conformément aux consignes de l’enseignant. Il contient un ensemble de **22 instances TSPLIB**, le **code source complet**, les **scripts d’exécution**, les **résultats expérimentaux**, les **figures de synthèse** ainsi qu’un **rapport final en PDF**.

---

## Structure du projet

- `data/tsplib/`  
  Contient les instances TSPLIB utilisées dans l’étude ainsi que le fichier `solutions.txt` regroupant les meilleurs coûts connus (**BKS**) pour les instances testées.

- `src/`  
  Contient l’implémentation principale des différentes composantes algorithmiques : lecture des instances, heuristique gloutonne, algorithme mémétique, recherche locale 2-opt, fonctions utilitaires, etc.

- `scripts/`  
  Contient les scripts permettant d’exécuter automatiquement les expériences et de générer les tableaux de synthèse ainsi que les figures.

- `results/`  
  Regroupe les résultats bruts (`raw_results.csv`), les tableaux de synthèse (`summary_results.csv`) et les figures produites lors des expérimentations.

- `report/`  
  Contient le rapport final du projet en **LaTeX** et en **PDF**, notamment le fichier :  
  `report/tsp_hybrid_report.pdf`

- `assets/`  
  Contient les éléments graphiques utilisés dans le rapport, comme le logo de l’université.

- `demo_results.ipynb`  
  Notebook Python d’exécution et de démonstration contenant une présentation synthétique des résultats, des essais réalisés et des sorties expérimentales principales.

---

## Méthodes utilisées

### 1. Heuristique gloutonne : plus proche voisin
Cette méthode construit une tournée en partant d’une ville initiale, puis en sélectionnant à chaque étape la ville non encore visitée la plus proche.

### 2. Approche hybride : algorithme mémétique
L’approche principale repose sur une hybridation entre :

- un **algorithme génétique** pour l’exploration globale ;
- une **recherche locale 2-opt** pour l’intensification ;
- une **initialisation mixte** (solutions gloutonnes multi-départ + solutions aléatoires) ;
- un mécanisme d’**adaptation du taux de mutation** en cas de stagnation.

Cette hybridation permet d’obtenir de meilleures tournées que l’heuristique gloutonne seule, tout en gardant des temps de calcul raisonnables.

---

## Installation

Dans un terminal placé à la racine du projet :

```bash
pip install -r requirements.txt
