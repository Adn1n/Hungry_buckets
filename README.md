# Hungry Goals 🏀⏱️

## 1. Présentation Générale

### 🎓 Titre du Projet
**Hungry Goals** – Jeu de Basket Arcade en Pygame

### 👥 Contributeurs

| Nom              | Rôle                                                             |
|------------------|------------------------------------------------------------------|
| MOUBARAC Adnan   | Lead développeur, structure du projet, intégration complète      |
| Omar SNANI       | Développeur gameplay, logique de score, système de bonus         |
| Teddy RAME        | Graphiste principal, interface visuelle, animation du jeu        |
| Cylia GOUCEM      | Recherche d’assets visuels, idées de gameplay                    |

### 📝 Description

**Hungry Goals** est un jeu d’arcade où le joueur contrôle un basketteur. Il dispose de **45 secondes** pour **marquer au moins 12 points**. En cas de réussite, un **mode Challenge** se déverrouille, avec un **panier mobile**, des **bonus** qui tombent et plus de difficulté.

### ⭐ Fonctionnalités Principales

- Déplacement du joueur (← →)
- Lancer de ballon avec `Entrée`
- Timer intégré (45s)
- Système de score
- Bonus temporels (plus de temps)
- Mode Challenge avec panier mouvant
- Menu principal et options
- Sons de fond et bruitages
- Transitions animées

### 🛠️ Technologies Utilisées

- **Langage** : Python 3
- **Librairie** : Pygame
- **Outils** :
  - YouTube (musique libre de droit)
  - Logiciels de pixel art (sprites)
  - PyCharm / VSCode

---

## ⚙️ Installation

### Cloner le dépôt :
```bash
git clone https://github.com/Adn1n/Hungry_goals.git
cd Hungry_goals
```

### Installer les dépendances :
```bash
pip install pygame
```

---

## ▶️ Utilisation

### Lancer le jeu :
```bash
python main.py
```

### Contrôles :
- `← →` : Déplacement joueur
- `Entrée` : Tir
- `Échap` : Quitter

---

## 2. Documentation Technique

### 🔁 Algorithme du Jeu

1. Chargement des ressources
2. Affichage du menu principal
3. Sélection du personnage
4. Début du chrono (45s)
5. Détection du tir et mise à jour du score
6. Passage en mode Challenge après 12 points
7. Bonus tombants
8. Fin de partie (victoire ou échec)

---

### 🧩 Fonctions principales

```python
def afficher_texte(ecran, font, texte, position, couleur)
def load_frames(sprite_sheet, row, num_frames, width, height)
def update_animation(frame_index, frames, animation_speed)
def load_combined_frames(sprite_sheet, rows, num_frames_per_row, width, height)
def detect_colored_rect(surface, color)
```

- `main.py` : boucle principale
- `player1.py / player2.py` : comportement des joueurs
- `ball.py` : logique de tir
- `panier.py` : détection de panier
- `bonus_item.py` : gestion du temps bonus
- `menu_screen.py / option_screen.py` : interface
- `music_manager.py / score_manager.py` : sons et score

---

### ⚠️ Gestion des Erreurs et Bugs Connus

- 🎯 Bug : la collision du ballon avec le panier peut être imprécise selon la FPS
- 🔊 Bug : `pygame.mixer` freeze s’il manque un fichier audio
- 📏 Bug : les objets peuvent sortir de l’écran sur petits écrans
- 🌀 Bug : en mode Challenge, le panier peut se bloquer sur un bord

---

## 3. Journal de Bord 🗂️

### 📆 Chronologie

| Date       | Étape                                     |
|------------|-------------------------------------------|
| 03/04/2024 | Initialisation du dépôt                   |
| 05/04/2024 | Création de la structure des fichiers     |
| 08/04/2024 | Ajout du moteur de jeu                    |
| 11/04/2024 | Gestion du score et timer                 |
| 13/04/2024 | Intégration du mode Challenge             |
| 15/04/2024 | Tests finaux et corrections               |

### 👥 Répartition des Tâches

- **Adnan** : structure, moteur, classes principales
- **Omar** : logique gameplay, bonus, collisions
- **Teddy** : sprites, animations, interface visuelle
- **Cylia** : choix des visuels, idées gameplay, organisation

---

## ✅ 4. Tests et Validation

### 🧪 Stratégie

- Tests manuels de chaque fonctionnalité
- Vérification du timer et du score
- Passage automatique au mode Challenge
- Test des collisions et du panier mouvant

---

### 🖼️ Captures attendues

- Écran menu
- Lancer de balle
- Mode Challenge avec panier mobile
- Bonus tombant capturé

---

## 🎓 Licence

Projet réalisé dans le cadre d’un exercice universitaire 2024.  
© Tous droits réservés par les auteurs.
