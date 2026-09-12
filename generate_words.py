"""Create words.txt from a public word list using only the standard library."""

import sys
from pathlib import Path
from urllib.request import urlopen

ANSWERS_URL = "https://raw.githubusercontent.com/3b1b/videos/master/_2022/wordle/data/possible_words.txt"
GUESSES_URL = "https://raw.githubusercontent.com/Kinkelin/WordleCompetition/main/data/official/official_allowed_guesses.txt"


def main():
    def fetch(url):
        with urlopen(url, timeout=30) as response:
            return {line.decode().strip().lower() for line in response
                    if len(line.strip()) == 5 and line.strip().isalpha()}

    answers = fetch(ANSWERS_URL)
    guesses = fetch(GUESSES_URL) | answers
    Path("answers.txt").write_text("\n".join(sorted(answers)) + "\n")
    Path("words.txt").write_text("\n".join(sorted(guesses)) + "\n")
    print(f"Wrote {len(answers)} answers and {len(guesses)} valid guesses")


if __name__ == "__main__":
    main()
