"""Check services on platform host."""

import json
from multiprocessing import Pool
import logging
import datetime
import subprocess
import pathlib
import collections
import os

import pymongo
import argh

import programs

logging.basicConfig(level=logging.DEBUG)


def get_active_workspaces(mongo_url, mongo_db):
    """
    Return workspaces active in the last 10 minutes.
    """
    mongodb = pymongo.MongoClient(mongo_url)
    workspaces = mongodb[mongo_db]["workspaces"]

    time_now = datetime.datetime.now()
    ws = workspaces.find({"state": "CLAIMED"})
    info = list()
    for w in ws:1
        last_activity = w.get("parameters", {}).get("last_activity")
        if not last_activity or not type(last_activity) == str:
            print(
                "workspace {w.get('_id')} belonging to {w.get('owner')} doesn't have last_activity"
            )
            continue
        last_activity_time = datetime.datetime.strptime(
            last_activity, "%Y-%m-%d %H:%M:%S"
        )
        last_activity_ago = (time_now - last_activity_time).seconds
        print(last_activity_ago)
        info.append([w.get("owner"), w.get("name"), last_activity, last_activity_ago])
        if last_activity_ago < 600:
            # serialize weird types to string
            for k, v in w.items():
                if type(v) not in [str, int, float]:
                    w[k] = str(v)
            yield w
    import tabulate

    print(tabulate.tabulate(info))


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
    out = subprocess.check_output(cmd)
    ps = [x.strip() for x in out.decode().strip().split("\n")[1:]]
    w["user_processes"] = ps
    return w


def get_running(ws):
    with Pool(5) as p:
        ret = p.map(get_running_1, ws)
    return ret


progs = [
    programs.identify_firefox,
    programs.identify_epsr,
    programs.identify_mantidworkbench65,
    programs.identify_sasview5,
    programs.identify_libreoffice,
    programs.identify_matlab2021a,
]


def identify_programs(ws):
    for w in ws:
        w["found_programs"] = list()
        up = w["user_processes"]
        for p in progs:
            found_program = p(up)
            if found_program:
                w["found_programs"].append(found_program)
    return ws


def run():
    """Main pipeline:

    we get the list of active workspaces,
    connect to them over ssh to get the process list
    go over the process list to identify running programs
    save the data to a json file.
    """
    mongo_url = os.environ.get("MONGO_URL")
    mongo_db = os.environ.get("MONGO_DB")
    if not mongo_url or not mongo_db:
        print("You must define MONGO_URL and MONGO_DB environmental variables. Exiting.")
        return

    ws = list(get_active_workspaces(mongo_url, mongo_db))
    ws = get_running(ws)
    pathlib.Path("saved").mkdir(exist_ok=True)
    filename = f"saved/{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    print(f"saving to {filename}")
    with open(filename, "w") as f:
        f.write(json.dumps(ws, indent=4))


def out1(filename):
    """Print a table showing frequency of programs found at a certain time."""
    ws = json.loads(pathlib.Path(filename).read_text())
    print(f"analysing {len(ws)} workspaces")

    ws = identify_programs(ws)
    progs = collections.defaultdict(int)
    for w in ws:
        for p in w.get("found_programs", list()):
            progs[p] += 1

    import tabulate

    print(
        tabulate.tabulate(
            list(progs.items()),
            headers=["program name", "count"],
            tablefmt="simple_outline",
        )
    )


if __name__ == "__main__":
    argh.dispatch_commands([run, out1])
