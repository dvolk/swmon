"""Check services on platform host."""

import json
from multiprocessing import Pool
import logging
import datetime
import subprocess
import pathlib
import collections
import os
import inspect

import pymongo
import argh


logging.basicConfig(level=logging.DEBUG)


def get_active_workspaces(mongo_url, mongo_db, cutoff_seconds):
    """
    Return workspaces active in the last `cutoff_seconds`.

    Negative `cutoff_seconds` mean unlimited time
    """
    mongodb = pymongo.MongoClient(mongo_url)
    workspaces = mongodb[mongo_db]["workspaces"]

    time_now = datetime.datetime.now()
    ws = workspaces.find({"state": "CLAIMED"})
    info = list()
    for w in ws:
        last_activity = w.get("parameters", {}).get("last_activity")
        if not last_activity or not type(last_activity) == str:
            logging.warning(
                "workspace {w.get('_id')} belonging to {w.get('owner')} doesn't have last_activity"
            )
            continue
        last_activity_time = datetime.datetime.strptime(
            last_activity, "%Y-%m-%d %H:%M:%S"
        )
        last_activity_ago = (time_now - last_activity_time).seconds
        info.append([w.get("owner"), w.get("name"), last_activity, last_activity_ago])
        if cutoff_seconds < 0 or last_activity_ago < cutoff_seconds:
            # serialize weird types to string
            for k, v in w.items():
                if type(v) not in [str, int, float]:
                    w[k] = str(v)
            yield w

    import tabulate

    print(
        tabulate.tabulate(
            info,
            headers=["owner", "name", "last activity", "last activity ago"],
            tablefmt="simple_outline",
        )
    )


def get_running_1(w):
    hostname = w["hostname"]
    owner = w["owner"]
    cmd = [
        "ssh",
        "-oUserKnownHostsFile=/dev/null",
        "-oStrictHostKeyChecking=no",
        "-i platform-key",
        f"root@{hostname}",
        f"ps -wwo command -U {owner}",
    ]

    try:
        out = subprocess.check_output(cmd, timeout=10)
    except subprocess.CalledProcessError:
        logging.exception("ssh command error:")
        w["user_processes"] = list()
        return w
    except subprocess.TimeoutExpired:
        logging.exception("ssh command timeout:")
        w["user_processes"] = list()
        return w

    ps = [x.strip() for x in out.decode().strip().split("\n")[1:]]
    w["user_processes"] = ps
    return w


def get_running(ws):
    with Pool(10) as p:
        ret = p.map(get_running_1, ws)
    return ret


def identify_programs(ws):
    import programs

    progs = [x[1] for x in inspect.getmembers(programs, inspect.isfunction)]

    for w in ws:
        w["found_programs"] = list()
        up = w["user_processes"]
        for p in progs:
            found_program = p(up)
            if found_program:
                w["found_programs"].append(found_program)
    return ws


def run(last_activity_cutoff_seconds=600):
    """Main pipeline:

    we get the list of active workspaces,
    connect to them over ssh to get the process list
    go over the process list to identify running programs
    save the data to a json file.
    """
    mongo_url = os.environ.get("MONGO_URL")
    mongo_db = os.environ.get("MONGO_DB")
    if not mongo_url or not mongo_db:
        print(
            "You must define MONGO_URL and MONGO_DB environmental variables. Exiting."
        )
        return

    ws = list(get_active_workspaces(mongo_url, mongo_db, last_activity_cutoff_seconds))
    ws = get_running(ws)
    date = datetime.datetime.now().strftime("%Y%m%d")
    pathlib.Path("saved/").mkdir(exist_ok=True)
    pathlib.Path(f"saved/{date}").mkdir(exist_ok=True)
    time = datetime.datetime.now().strftime("%H%M%S")
    filename = f"saved/{date}/{time}.json"
    print(f"saving to {filename}")
    data = {
        "date": date,
        "time": time,
        "last_activity_cutoff_seconds": last_activity_cutoff_seconds,
        "workspaces": ws,
    }
    with open(filename, "w") as f:
        f.write(json.dumps(data, indent=4))


def make_count(ws):
    progs = collections.defaultdict(int)
    for w in ws:
        for p in w.get("found_programs", list()):
            progs[p] += 1
    progs = sorted(progs.items(), key=lambda x: -x[1])
    return dict(progs)


def out1(filename):
    """Print a json dict showing frequency of programs found at a certain time."""
    ws = json.loads(pathlib.Path(filename).read_text())
    ws["workspaces"] = identify_programs(ws["workspaces"])
    progs = make_count(ws["workspaces"])
    return json.dumps(
        {
            "date": ws["date"],
            "time": ws["time"],
            "last_activity_cutoff_seconds": ws["last_activity_cutoff_seconds"],
            "count": progs,
        },
        indent=4,
    )


def out2(filename):
    """Print a table showing frequency of programs found at a certain time."""
    ws = json.loads(pathlib.Path(filename).read_text())
    print(f"analysing {len(ws['workspaces'])} workspaces")
    ws["workspaces"] = identify_programs(ws["workspaces"])
    progs = make_count(ws["workspaces"])

    import tabulate

    return tabulate.tabulate(
        list(progs.items()),
        headers=["program name", "count"],
        tablefmt="simple_outline",
    )


if __name__ == "__main__":
    argh.dispatch_commands([run, out1, out2])
