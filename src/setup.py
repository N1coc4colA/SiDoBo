import os


def make_directory(fp: str) -> None:
    if not os.path.exists(fp):
        print(f"> Creating directory to store data: {fp}")
        os.mkdir(fp)
        if not os.path.exists(fp):
            print(f"> Failed to create {fp} directory.")
        else:
            print(f"> Created directory {fp}")


def load() -> None:
    make_directory("./logs/")
    make_directory("./resources/")

