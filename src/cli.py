import sys

from src.rover import run_scenario


def main(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    x, y, orientation = run_scenario(text)
    print(f"Position finale : ({x}, {y}) Orientation : {orientation}")


if __name__ == "__main__":
    main(sys.argv[1])
