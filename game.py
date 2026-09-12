"""A small command-line Wordle clone."""

import json
import random
from pathlib import Path

RESET = "\033[0m"
GREEN = "\033[42;30m"
YELLOW = "\033[43;30m"
GRAY = "\033[100;30m"
KEY_COLORS = {"green": GREEN, "yellow": YELLOW, "gray": GRAY}
KEY_RANK = {"gray": 1, "yellow": 2, "green": 3}
KEYBOARD = "qwertyuiop asdfghjkl zxcvbnm"


def load_words(path="words.txt"):
    return {line.strip().lower() for line in Path(path).read_text().splitlines()
            if len(line.strip()) == 5 and line.strip().isalpha()}


def score_guess(guess, answer):
    result = ["gray"] * 5
    remaining = list(answer)
    for i, letter in enumerate(guess):
        if letter == answer[i]:
            result[i] = "green"
            remaining[i] = None
    for i, letter in enumerate(guess):
        if result[i] == "green":
            continue
        if letter in remaining:
            result[i] = "yellow"
            remaining[remaining.index(letter)] = None
    return result


def render(guesses, keyboard):
    print("\n".join(" ".join(f"{KEY_COLORS[s]} {c.upper()} {RESET}" for c, s in zip(word, score))
                    for word, score in guesses))
    print()
    print(" ".join(f"{KEY_COLORS.get(keyboard.get(c), '')}{c.upper()}{RESET if c in keyboard else ''}"
                  for c in KEYBOARD))


def update_stats(stats, won, guess_number=None):
    stats["games_played"] += 1
    if won:
        stats["wins"] += 1
        stats["current_streak"] += 1
        stats["max_streak"] = max(stats["max_streak"], stats["current_streak"])
        stats["guess_distribution"][str(guess_number)] += 1
    else:
        stats["current_streak"] = 0


def main():
    answers = load_words("answers.txt")
    words = load_words() | answers
    if not answers or not words:
        raise SystemExit("answers.txt or words.txt is missing or invalid.")
    stats_path = Path("stats.json")
    default = {"games_played": 0, "wins": 0, "current_streak": 0,
               "max_streak": 0, "guess_distribution": {str(i): 0 for i in range(1, 7)}}
    stats = {**default, **(json.loads(stats_path.read_text()) if stats_path.exists() else {})}
    stats["guess_distribution"] = {**default["guess_distribution"], **stats["guess_distribution"]}
    while True:
        answer, guesses, keyboard = random.choice(tuple(answers)), [], {}
        while len(guesses) < 6:
            render(guesses, keyboard)
            guess = input(f"Guess {len(guesses) + 1}/6: ").strip().lower()
            if len(guess) != 5 or not guess.isalpha() or guess not in words:
                print("Enter a valid five-letter word from the list.")
                continue
            score = score_guess(guess, answer)
            guesses.append((guess, score))
            for letter, status in zip(guess, score):
                if KEY_RANK[status] > KEY_RANK.get(keyboard.get(letter), 0):
                    keyboard[letter] = status
            if guess == answer:
                break
        won = guesses and guesses[-1][0] == answer
        render(guesses, keyboard)
        print(f"Answer: {answer.upper()}" if not won else "You got it!")
        update_stats(stats, won, len(guesses) if won else None)
        stats_path.write_text(json.dumps(stats, indent=2) + "\n")
        print(f"Games: {stats['games_played']}  Wins: {stats['wins']}  "
              f"Streak: {stats['current_streak']}  Max: {stats['max_streak']}")
        print("Distribution: " + " ".join(f"{i}:{stats['guess_distribution'][str(i)]}" for i in range(1, 7)))
        if input("Play again? [y/N] ").strip().lower() != "y":
            break


if __name__ == "__main__":
    main()
