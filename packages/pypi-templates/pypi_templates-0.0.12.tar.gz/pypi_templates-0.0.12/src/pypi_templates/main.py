import os
from pathlib import Path

HERE = Path(__file__).parent.resolve()
PROJECT_NAME = os.path.basename(HERE)


def main():
    print(f"you are use {PROJECT_NAME} now")


def add_one(number):
    return number + 1


if __name__ == "__main__":
    main()
