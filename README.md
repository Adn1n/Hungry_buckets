# Hungry Buckets 

## 1. Contributeurs

Le projet **Hungry Buckets** a été réalisé par une équipe de quatre étudiants de l'EFREI :

- **Adnan Moubarac** : Principal développeur de la physique du jeu (logique des rebonds, score, équation de trajectoire, POO, optimisation finale).
- **Omar Snani** : Responsable interface utilisateur et manche finale (menus, transitions, logique de victoire/défaite, panier mobile).
- **Cylia Goucem** : Testeuse, rédactrice et coordinatrice de suivi (README, carnet de bord, PPT, validation fonctionnelle).
- **Teddy Rame** : Designer graphique (sprites, visuels IA, cohérence visuelle, support de présentation).

---

## 2. Présentation du Jeu

**Hungry Buckets** est un jeu 2D d'adresse basé sur la physique. Le joueur doit marquer des paniers en lançant des balles via la **souris** (clic-glisser) avec angle et puissance ajustables.

###  Deux Manches :

- **Manche 1** : Panier statique repositionné après chaque panier marqué. Objectif : **12 points minimum**.
- **Manche 2 (finale)** : Débloquée si score suffisant. Le panier **change de position toutes les 2 secondes**.

###  Style
Ambiance cyber, animations fluides, visuels générés par IA.

---

## 3. Fonctionnalités Clés

-  **Tir basé sur la physique** : angle, vitesse initiale, gravité, rebonds gérés.
-  **Prévisualisation de tir** : affichage en temps réel de la trajectoire via des points violets.
-  **Panier dynamique** : mouvement aléatoire après réussite (manche 1) ou toutes les 2s (manche 2).
-  **Choix de personnage** : deux personnages animés au choix (Tyson & Axel).
-  **Menus complets** : menu principal, options, sélection du personnage, écran de fin.
-  **Design personnalisé** : sprites IA, esthétique cyber, barre de chargement animée.

---

## 4. Technologies Utilisées

- **Python 3**
- **Pygame**
- **Git / GitHub**
- **Discord / WhatsApp**
- **Outils IA** : génération de sprites/personnages

---

## 5. Installation

### Prérequis

- Python 3.8+
- `pip` installé

###  Cloner le dépôt

```bash
git clone https://github.com/Adn1n/Hungry_buckets.git
cd Hungry_buckets
```

###  Installer les dépendances

```bash
pip install pygame
```

### ▶ Lancer le jeu

```bash
python src/utils/main.py
```

> ⚠️ Le dossier `assets/` (images & musiques) doit être à la racine du projet.

---

## 6. Utilisation

- Naviguer dans les menus avec la souris
- Choisir un personnage
- **Clic-glisser** pour viser, **relâcher** pour tirer
- Atteindre **12 points** → accéder à la manche finale
- Continuer à marquer jusqu’à la fin du chrono

---

## 7. Documentation Technique

### Algorithme Général

1. Lancer le jeu (écran de chargement)
2. Menu principal → sélection de personnage
3. Manche 1 : tir & score avec panier repositionné
4. Si `score ≥ 12` : passage à la manche 2
5. Manche 2 : panier se déplace toutes les 2s
6. Fin de partie : écran victoire/défaite + score

### Fonctionnalités Principales (Modules)

- **Moteur physique** : angle, force, gravité, rebonds
- **Trajectoire** : calcul et affichage dynamique
- **Sprites** : joueurs animés, effets visuels
- **Menus** : transitions fluides, gestion des états
- **Score** : comptabilisé uniquement si la balle entre par le haut

---

## 8. Gestion des Entrées et des Erreurs

- Empêche les tirs hors écran
- Détection précise des collisions
- Exception prévue si `high_scores.txt` est manquant
- Score uniquement validé sur tir « propre »

---

## 9. Bugs Connus

- Collisions latérales parfois approximatives (selon rebond)
- Résolutions petites peuvent altérer la visualisation de trajectoire

---

## 10. Journal de Bord (extraits)

- **03/02/2025** : Brainstorming initial, contraintes du projet
- **10/02** : Prototype plateforme (type Mario), premiers tests Pygame
- **15/02 → 03/03** : Mini-jeux individuels (canon, shoot, saut)
- **03/03** : Partage des jeux → projet plateforme lancé
- **17 → 24/03** : Déplacements, tirs, intégration assets
- **04/04** : Pivot → jeu de basket « Hungry Buckets »
- **14 → 21/04** : Trajectoire, mécanique de tir, panier
- **28/04** : Transitions, rebonds, sprites animés
- **05/05** : Bonus pendules, panier mouvant, finalisation
- **10/05** : Tests finaux, rendu, README, PPT

---

## 11. Tests et Validation

### Méthodes

-  Tests unitaires : fonctions de trajectoire
-  Tests fonctionnels : menus, collisions, rebonds
-  Tests utilisateurs : jouabilité, intuitivité

### Résultats

-  Score uniquement sur tir par le haut
-  Prévisualisation précise
-  Menus réactifs

---

## 12. Répartition des Tâches

| Membre   | Tâches clés |
|----------|-------------|
| Cylia    | Documentation, carnet, tests |
| Teddy    | Design graphique, IA, présentation |
| Omar     | UI, transitions, manche finale |
| Adnan    | Tir, architecture, POO, trajectoire |

---

## 13. Problèmes Rencontrés et Solutions

| Problème                        | Solution apportée                                 |
|--------------------------------|----------------------------------------------------|
| Code complexe à gérer          | Passage en POO, modules clairs                    |
| Collisions imprécises          | Ajustements manuels + recherche de ressources     |
| Difficulté de coordination     | Outils de suivi (Discord, GitHub, planning)       |
| Incohérences de trajectoire    | Unification des formules tir & affichage          |

---

## 14. Améliorations Futures

- Ajouter un écran de crédits
- Intégrer des missions avec objectifs
- Skins personnalisables pour les personnages
- Ajouter une musique de fond complète et des effets sonores

---

## 15. Conclusion

Ce projet transverse a été une aventure intense, mêlant apprentissage, créativité et travail d'équipe. Chaque membre a contribué avec ses compétences pour produire un jeu original, esthétique, et techniquement solide.

Il nous a préparés à affronter des projets plus complexes, tout en mettant en lumière l’importance de la planification, de la communication, et de l’adaptation.

---
