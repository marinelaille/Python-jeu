# highscore.py,
import json
import os

SCORES_FILE = "highscores.json"
MAX_ENTRIES = 5

def load_scores():
    """Charge la liste des meilleurs scores depuis le fichier JSON."""
    if not os.path.exists(SCORES_FILE):
        return []
    try:
        with open(SCORES_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_scores(scores):
    """Sauvegarde la liste des scores dans le fichier JSON."""
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f)

def update_scores(new_score):
    """
    Ajoute new_score à la liste, trie par ordre décroissant,
    ne garde que les MAX_ENTRIES meilleures valeurs et renvoie la liste.
    """
    scores = load_scores()
    scores.append(new_score)
    scores = sorted(scores, reverse=True)[:MAX_ENTRIES]
    save_scores(scores)
    return scores
