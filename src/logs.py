import os
from datetime import datetime


class Logs:
    def __init__(self):
        self._can_log: bool = os.path.exists("./logs/")
        self._file = open("./logs/log.log", "a") if self._can_log else None
        self.local: list = []

    def message(self, msg: str) -> None:
        if not self._can_log:
            return

        dt = datetime.now().strftime("%H:%M:%S/%d/%m/%Y")

        out = f"[{dt}] | " + msg + "\n"
        self._file.write(out)
        self.local.append(out)
        print(out)


logs = None


def log(msg: str) -> None:
    global logs
    logs.message(msg)


def get_logs() -> list:
    global logs
    return logs.local


def load() -> None:
    global logs
    logs = Logs()

