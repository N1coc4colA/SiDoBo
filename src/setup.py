import os

def load():
    if not os.path.exists("./resources/"):
        print("Creating directory to store data: ./resources")
        os.mkdir("./resources/")
        if not os.path.exists("./resources/"):
            print("Failed to create resources directory.")

