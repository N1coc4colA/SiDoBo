from datetime import datetime

from src.logs import log
import src.shared as shared


availables: dict = {}
reserved: dict = {}
sum = 0


def reserve_timeslot(date, time, uid, year) -> bool:
    if date not in availables:
        return False

    if time not in availables[date]:
        return False

    availables[date].remove(time)

    if date not in reserved:
        reserved[date] = []

    reserved[date].append([time, uid, "", year])

    log(f"Reserved timeslot: {date} - {time} - {uid} - {year}")
    return True


def cancel_timeslot(date, time, uid) -> bool:
    if date not in reserved:
        return False

    target = None
    for e in reserved[date]:
        if e[0] == time and e[1] == uid:
            reserved[date].remove(e)

            if date not in availables:
                availables[date] = []
            if time not in availables[date]:
                availables[date].append(time)

            log(f"Cancelled timeslot: {date} - {time} - {uid} - {e[3]}")
            return True

    return False


def update_timeslot(date, time, message) -> bool:
    if date not in reserved:
        return False

    target = None
    for e in reserved[date]:
        if e[0] == time:
            e[2] = message
            return True

    return False


def add_timeslot(date, time) -> bool:
    if date not in availables:
        availables[date] = []

    if time in availables[date]:
        return False

    availables[date].append(time)

    log(f"Added timeslot: {date} - {time}")
    return True


async def remove_timeslot(date, time, reason) -> None:
    must_notify = False

    copy = None
    if date in reserved:
        found = False
        for e in reserved[date]:
            if e[0] == time:
                found = True
                copy = e

        reserved[date].remove(copy)
        must_notify = found

    if date in availables:
        availables[date].remove(time)

    log(f"Removed timeslot: {date} - {time} - {must_notify}")

    await shared.get_client().dm_cancelled(date, time, copy)
    if must_notify:
        await shared.get_client().dm_reservation_cancelled(date, time, copy[1], reason)


def get_availables(date) -> list:
    return [] if date not in availables else availables[date]


def get_reserved(date) -> list:
    if date not in reserved:
        return []

    return reserved[date]


def query(uid) -> list:
    out = []

    for date in reserved:
        print(f"Date: {date}")
        for entry in reserved[date]:
            print(f"{date} - {entry[0]} {entry[2]}")
            if str(entry[1]) == str(uid):
                out.append((date + " - " + entry[0], entry[2],))

    return out


def query_by_date(date, uid) -> list:
    if date not in reserved:
        return []

    out = []

    for entry in reserved[date]:
        if entry[1] == uid:
            out.append(entry[0])

    return out


def cleanup() -> None:
    dt = datetime.now()
    to_remove = []
    for d in availables:
        if d < dt:
            to_remove.append(d)

    for d in to_remove:
        availables.remove(d)

    to_remove = []
    for d in reserved:
        sum += len(reserved[d])
        to_remove.append(d)

    for d in to_remove:
        reserved.remove(d)


def get_data(date, time) -> list:
    for e in reserved[date]:
        if e[0] == time:
            return e

    return ["", "", "", 0]

