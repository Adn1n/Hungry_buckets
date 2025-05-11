import os

class ScoreManager:
    def __init__(self, path="high_scores.txt"):
        self.path = path

    def load_high_score(self):
        if not os.path.exists(self.path):
            return 0
        with open(self.path, "r") as f:
            line = f.readline().strip()
            return int(line) if line.isdigit() else 0

    def save_high_score(self, score):
        with open(self.path, "w") as f:
            f.write(f"{score}\n")