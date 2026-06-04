"""Create words.txt from a public word list using only the standard library."""

import sys
from pathlib import Path
from urllib.request import urlopen

URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"


def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    with urlopen(URL, timeout=30) as response:
        words = sorted({line.decode().strip().lower() for line in response
                        if len(line.strip()) == 5 and line.strip().isalpha()})
    Path("words.txt").write_text("\n".join(words[:count]) + "\n")
    print(f"Wrote {min(count, len(words))} words to words.txt")


if __name__ == "__main__":
    main()
