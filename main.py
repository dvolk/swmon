"""Check services on platform host."""

import json
from multiprocessing import Pool
import logging
import datetime
import subprocess
import pathlib

import pymongo
import argh

import programs

logging.basicConfig(level=logging.DEBUG)


mongodb = pymongo.MongoClient("mongodb://localhost")
workspaces = mongodb["ada"]["workspaces"]


def get_active_workspaces():
    """
    Return workspaces active in the last 10 minutes.
    """
    time_now = datetime.datetime.utcnow()
    ws = workspaces.find({"state": "CLAIMED"})
    for w in ws:
        last_activity = w.get("parameters", {}).get("last_activity")
        if last_activity and type(last_activity) == str:
            last_activity_time = datetime.datetime.strptime(
                last_activity, "%Y-%m-%d %H:%M:%S"
            )
            last_activity_ago = (time_now - last_activity_time).seconds
            print(last_activity_ago)
            if last_activity_ago < 600:
                # serialize weird types to string
                for k, v in w.items():
                    if type(v) not in [str, int, float, list, dict]:
                        w[k] = str(v)
                yield w


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
    ws = list(get_active_workspaces())
    ws = get_running(ws)
    pathlib.Path("saved").mkdir(exist_ok=True)
    filename = f"saved/{datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S')}.json"
    with open(filename, "w") as f:
        f.write(json.dumps(ws, indent=4))


def out1(filename):
    ws = json.loads(pathlib.Path(filename).read_text())
    ws = identify_programs(ws)
    for w in ws:
        pass


if __name__ == "__main__":
    argh.dispatch_commands([run, out1])
