import json
from utils import sort_dictionary
import hashlib

def get_digest(leaderboard):
    return hashlib.sha256(json.dumps(leaderboard["leaderboard"]).encode()).hexdigest()

EMPTY_HASH = get_digest({"leaderboard": {}})

def create_leaderboard():
    with open("leaderboard.json", "w") as f:
        json.dump({"words": {}, "digest": EMPTY_HASH}, f, indent=4)

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
    
    
def update_leaderboard(name, score):
    leaderboard = open_leaderboard()
    leaderboard["leaderboard"][name] = score
    leaderboard["leaderboard"] = sort_dictionary(leaderboard["leaderboard"], key=lambda x: x[1], reverse=True)
    leaderboard["digest"] = get_digest(leaderboard)
    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f, indent=4)
    return leaderboard
    
if __name__ == "__main__":
    print(open_leaderboard())
