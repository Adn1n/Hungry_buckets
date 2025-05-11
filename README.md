# Hungry Goals 🏀⏱️

## 1. Présentation du Projet

### Résumé
Le jeu **Hungry Goals** repose sur un gameplay simple et efficace : le joueur déplace un basketteur horizontalement (`← →`) et tente de tirer (`Entrée` ou souris) dans un panier. L’objectif est de marquer **12 points en 45 secondes** pour débloquer une **seconde manche plus difficile** avec un panier en mouvement. Des bonus tombants permettent de gagner du temps. Inspiré de « Angry Birds », ce jeu addictif propose une rejouabilité forte avec un design **cyber** stylisé.

### Contraintes Techniques
- Utilisation de **Python** avec la **bibliothèque Pygame**
- Implémentation d’une **équation de trajectoire physique** : angle, vitesse, poids, temps
- Rétroactions : conditions de victoire/défaite, messages et conseils au joueur

### Objectifs Pédagogiques
- Travailler en mode projet
- Appliquer les connaissances de Python et de physique
- Développer autonomie, collaboration, créativité, capacité à s’auto-former

---

## 2. Organisation de l'Équipe

| Membre           | Rôle                                                                 |
|------------------|----------------------------------------------------------------------|
| Cylia GOUCEM     | Testeuse, présentation, rédaction du carnet                          |
| Teddy RAME       | Game design, création et gestion des images                          |
| Omar SNANI       | Interfaces, logique bonus, codage manche finale                      |
| MOUBARAC Adnan   | Chef de projet, structure, algorithmes, équation de trajectoire      |

### Communication
- Discord, GitHub, WhatsApp  
- Réunions hebdomadaires + échanges permanents

---

## 3. Journal de Bord

- **3 fév. 2025** : Brainstorming idées
- **10 fév.** : Premiers tests Pygame
- **15 fév.** : Mini-jeux d’entraînement
- **3 mars** : Début projet plateforme
- **17–24 mars** : Graphismes + mécanique de tir
- **10 avril** : Pivot vers Hungry Goals
- **14–21 avril** : Ajout du panier, tir à trajectoire
- **28 avril** : Interface, menu, sons, bonus
- **5 mai** : Panier mobile toutes les 2s, derniers raffinements
- **7 mai** : Ajout des conditions de victoire, README et finalisation

---

## 4. Suivi Technique

- Initial : jeu de plateforme abandonné
- Final : jeu de basket avec deux manches et physique de tir
- Organisation en fichiers modulaires (`ball.py`, `player.py`, `bonus_item.py`, etc.)

---

## 5. Fonctionnalités Principales

- Déplacement latéral
- Tir avec **entrée** ou **clic souris**  
  ➜ Affichage dynamique de **la trajectoire en fonction de l’angle et la force**
- Score, timer (45s)
- Bonus temporels tombants
- Mode Challenge avec panier mouvant
- Sons, musiques, interface animée

---

## 6. Technologies Utilisées

- **Langage** : Python 3
- **Librairie** : Pygame
- **Outils** :
  - YouTube (sons)
  - Logiciels pixel art
  - PyCharm / VSCode

---

## 7. Installation

```bash
git clone https://github.com/Adn1n/Hungry_goals.git
cd Hungry_goals
pip install pygame
```

---

## 8. Utilisation

```bash
python main.py
```

### Contrôles

- `← →` : Déplacement joueur  
- `Entrée` : Tir  
- **Souris** : Viser et tirer avec affichage de trajectoire  
- `Échap` : Quitter

---

## 9. Documentation Technique

### Algorithme du Jeu

1. Chargement des ressources
2. Affichage menu principal
3. Sélection joueur
4. Lancement timer
5. Viseur souris + tir
6. Vérification collision panier
7. Score, bonus, passage en manche 2
8. Fin du jeu, affichage résultat

### Fonctions principales

```python
def afficher_texte(ecran, font, texte, position, couleur)
def load_frames(sprite_sheet, row, num_frames, width, height)
def update_animation(frame_index, frames, animation_speed)
def load_combined_frames(sprite_sheet, rows, num_frames_per_row, width, height)
def detect_colored_rect(surface, color)
```

---

## 10. Gestion des Erreurs et Bugs Connus

- 🎯 Collision panier imprécise selon FPS
- 🔊 Plantage possible si fichier audio manquant (`pygame.mixer`)
- 📏 Bonus qui sortent de l’écran selon la résolution
- 🌀 Panier parfois bloqué en bordure en mode Challenge

---

## 11. Tests et Validation

- Tests manuels sur chaque fonctionnalité
- Tests de score, timer, trajectoire, collision, bonus
- Mode Challenge vérifié avec panier mouvant toutes les 2s

---

### Captures attendues

- Écran menu  
- Trajectoire affichée avant tir  
- Panier mouvant  
- Bonus tombant

---
