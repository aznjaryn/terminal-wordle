# terminal-wordle

A command-line Wordle game for Python 3. It uses only the standard library.

## Run

```powershell
python game.py
```

`answers.txt` contains the smaller curated answer pool, while `words.txt`
contains the larger accepted-guess pool. To refresh both lists, run:

```powershell
python generate_words.py
```

The generator downloads an open English word list with `urllib`, filters it,
The generator downloads Wordle-style lists, filters them to five-letter words,
and writes both files. `stats.json` is created automatically.

## Project phases

1. Foundation: Wordle-style answer and guess lists.
2. Core gameplay: six guesses, validation, repeated-letter scoring, and the keyboard.
3. Persistence and polish: JSON statistics, replay flow, ANSI rendering, and final checks.
