import random
import json
import os

class Game:
    def __init__(self, name):
        self.name = name
        self.best_score = None
        self.levels = {
            "easy": (10, 100),
            "medium": (10, 250),
            "hard": (10, 500),
            "expert": (10, 1000)
        }
        self.file_names = {
            "easy": "scorecard_easy.json",
            "medium": "scorecard_medium.json",
            "hard": "scorecard_hard.json",
            "expert": "scorecard_expert.json"
        }
        self.current_number = None
        self.attempts = 0
        self.max_attempts = 0
        self.diff_lvl = None

    def start_game(self, diff_lvl):
        if diff_lvl not in self.levels:
            return {"error": "Invalid difficulty level"}
        
        self.diff_lvl = diff_lvl
        self.current_number, (min_num, max_num) = random.randint(*self.levels[diff_lvl]), self.levels[diff_lvl]
        self.attempts = 0
        self.max_attempts = 15 if diff_lvl == "expert" else 10

        return {
            "message": f"Game started at {diff_lvl} level",
            "min": min_num, 
            "max": max_num,
            "max_attempts": self.max_attempts
        }

    def make_guess(self, guess):
        if self.current_number is None:
            return {"error": "Game not started"}
        
        self.attempts += 1
        attempts_left = self.max_attempts - self.attempts

        if guess == self.current_number:
            result = {"message": "Correct!", "attempts": self.attempts, "attempts_left": attempts_left}
            self.update_leaderboard(self.get_file_name(self.diff_lvl), self.attempts)
            return result
        elif abs(guess - self.current_number) < 5:
            result = {"message": "You’re very close!", "attempts_left": attempts_left}
        elif guess < self.current_number:
            result = {"message": "Too low", "attempts_left": attempts_left}
        else:
            result = {"message": "Too high", "attempts_left": attempts_left}

        if self.attempts >= self.max_attempts:
            result = {"message": f"Out of attempts! Correct number was {self.current_number}", "attempts_left": 0}
            return result

        return result

    def get_file_name(self, diff_lvl=None):
        if diff_lvl is None:
            return list(self.file_names.values())
        return self.file_names.get(diff_lvl)

    def update_leaderboard(self, file_name, attempts):
        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                scorecard = json.load(f)
        else:
            scorecard = []

        scorecard.append({"name": self.name, "score": attempts})

        with open(file_name, "w") as f:
            json.dump(scorecard, f, indent=4)

        scorecard_sorted = sorted(scorecard, key=lambda x: x["score"])
        return scorecard_sorted[:5]

    def show_all_leaderboards(self):
        leaderboards = {}
        for file_name in self.get_file_name():
            if os.path.exists(file_name):
                with open(file_name, "r") as f:
                    leaderboard = json.load(f)
                    leaderboard_sorted = sorted(leaderboard, key=lambda x: x["score"])
                    heading = (file_name.split("_")[1].split(".")[0]).title()
                    leaderboards[heading] = leaderboard_sorted[:5]
                    print(leaderboards)
                    
        return leaderboards