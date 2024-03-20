

client = None


def get_client():
    global client
    return client


def set_client(c):
    global client
    client = c
    print("Client set")

