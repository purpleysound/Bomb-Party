import json
from utils import sort_dictionary


def create_leaderboard():
    base_leaderboard = {"words": {}, "letters": {}}
    empty_leaderboard = {2: base_leaderboard.copy(), 3: base_leaderboard.copy()}
    with open("leaderboard.json", "w") as f:
        json.dump(empty_leaderboard, f, indent=4)


def open_leaderboard():
    try:
        with open("leaderboard.json", "r") as f:
            leaderboard = json.load(f)
    except FileNotFoundError:
        create_leaderboard()
        leaderboard = open_leaderboard()
    return leaderboard


def get_leaderboard(difficulty: int):
    return open_leaderboard()[str(difficulty)]
    
    
def update_leaderboard(name: str, words: int, letters: int, difficulty: int) -> bool:
    """Updates leaderboard json file with new score if it is higher than the previous score
    Returns True if a new high score was set, False otherwise"""
    updated = False
    leaderboard: dict[str, dict | str] = get_leaderboard(difficulty)
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
        full_leaderboard = open_leaderboard()
        full_leaderboard[str(difficulty)] = leaderboard
        with open("leaderboard.json", "w") as f:
            json.dump(full_leaderboard, f, indent=4)
    return updated

    
if __name__ == "__main__":
    print(open_leaderboard())
