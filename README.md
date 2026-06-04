# terminal-wordle

A command-line Wordle game for Python 3. It uses only the standard library.

## Run

```powershell
python game.py
```

`words.txt` contains one five-letter word per line. To create a fresh list of
about 2,000 five-letter words, run:

```powershell
python generate_words.py
```

The generator downloads an open English word list with `urllib`, filters it,
and writes the first 2,000 entries. `stats.json` is created automatically.

## Project phases

1. Foundation: word-list generation and repository documentation.
2. Core gameplay: six guesses, validation, repeated-letter scoring, and the keyboard.
3. Persistence and polish: JSON statistics, replay flow, ANSI rendering, and final checks.
