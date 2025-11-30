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

    def guessing_game(self, diff_lvl):
        if diff_lvl not in self.levels:
            print("Please select the correct level")
            return None
        return random.randint(*self.levels[diff_lvl]), self.levels[diff_lvl]

    def get_file_name(self, diff_lvl=None):
        if diff_lvl is None:
            return list(self.file_names.values())
        elif diff_lvl not in self.file_names:
            print("Please select the correct file name")
            return None
        return self.file_names[diff_lvl]

    def get_difficulty_level(self):
        return input("Select level of difficulty (easy, medium, hard, expert): ").lower()

    def play_game(self, diff_lvl):
        rnd_num, (min_num, max_num) = self.guessing_game(diff_lvl)
        attempts = 0
        max_attempts = 15 if diff_lvl == "expert" else 10

        while True:
            try:
                guess = int(input(f"Please select a number between {min_num} and {max_num}: "))
                attempts += 1

                if guess == rnd_num:
                    print("Well done! You have guessed the correct number.")
                    print(f"You took {attempts} attempts.")
                    return attempts
                elif abs(guess - rnd_num) < 5:
                    print("You’re very close!")
                elif guess < rnd_num:
                    print("Guessed number is too low.")
                else:
                    print("Guessed number is too high.")

                if attempts >= max_attempts:
                    print(f"Sorry! You have exceeded {max_attempts} attempts. The correct number was {rnd_num}.")
                    return None
            except ValueError:
                print("Please type in a valid number")

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
        leaderboard = scorecard_sorted[:5]

        print(f"{'Player':<10} {'Score':<10}")
        for item in leaderboard:
            print(f"{item['name'].title():<10} {item['score']:<10}")

    def show_all_leaderboards(self):
        print("\nLeaderboards: \n")
        for file_name in self.get_file_name():
            if os.path.exists(file_name):
                with open(file_name, "r") as f:
                    leaderboard = json.load(f)
                    leaderboard_sorted = sorted(leaderboard, key=lambda x: x["score"])
                    heading = (file_name.split("_")[1].split(".")[0]).title()
                    print("Level: " + heading)
                    for item in leaderboard_sorted[:5]:
                        print(f"{item['name'].title():<10} {item['score']:<30}")
                    print("\n")

    def run(self):
        while True:
            diff_lvl = self.get_difficulty_level()
            if not self.guessing_game(diff_lvl):
                continue

            file_name = self.get_file_name(diff_lvl)
            attempts = self.play_game(diff_lvl)

            if attempts is not None:
                if self.best_score is None or attempts < self.best_score:
                    self.best_score = attempts
                    print("New record for least attempts!")
                self.update_leaderboard(file_name, attempts)

            play_again = input("Do you want to play again? (y/n): ").lower()
            if play_again != "y":
                print(f"Your best attempt this session was {self.best_score if self.best_score else 'No successful'} attempts.")
                self.show_all_leaderboards()
                break


def main():
    name = input("Please type in your name: ")
    game = Game(name)
    game.run()


if __name__ == "__main__":
    main()