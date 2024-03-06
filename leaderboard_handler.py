import json
from utils import sort_dictionary
import hashlib

def get_digest(leaderboard):
    return hashlib.sha256(
        f"{json.dumps(leaderboard["words"])},{json.dumps(leaderboard["letters"])}"
        .encode()).hexdigest()

EMPTY_HASH = get_digest({"words": {}, "letters": {}})

def create_leaderboard():
    with open("leaderboard.json", "w") as f:
        json.dump({"words": {}, "letters": {}, "digest": EMPTY_HASH}, f, indent=4)

def open_leaderboard():
    try:
        with open("leaderboard.json", "r") as f:
            leaderboard = json.load(f)
    except FileNotFoundError:
        create_leaderboard()
        leaderboard = open_leaderboard()

    digest = get_digest(leaderboard)
    if digest == leaderboard["digest"]:
        return leaderboard
    else:
        raise RuntimeError("Leaderboard digest doesn't match, file has either been tampered with or an error has occured")
    
    
def update_leaderboard(name: str, words: int, letters: int) -> bool:
    """Updates leaderboard json file with new score if it is higher than the previous score
    Returns True if a new high score was set, False otherwise"""
    updated = False
    leaderboard: dict[str, dict | str] = open_leaderboard()
    previous = leaderboard["words"].get(name, -1)
    if words > previous:
        leaderboard["words"][name] = words
        leaderboard["words"] = sort_dictionary(leaderboard["words"], key=lambda x: x[1], reverse=True)
        updated = True
    previous = leaderboard["letters"].get(name, -1)
    if letters > previous:
        leaderboard["letters"][name] = letters
        leaderboard["letters"] = sort_dictionary(leaderboard["letters"], key=lambda x: x[1], reverse=True)
        updated = True
    if updated:
        leaderboard["digest"] = get_digest(leaderboard)
        with open("leaderboard.json", "w") as f:
            json.dump(leaderboard, f, indent=4)
    return updated 
    
if __name__ == "__main__":
    print(open_leaderboard())
