# swmon

swmon connects to workspaces and analyses the programs used

## Install

```
git clone https://github.com/dvolk/swmon
cd swmon
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

## Usage

define the `MONGO_URI` and `MONGO_DB` environmental variables.

To get the data:

```
python3 main.py run
```

It will be saved in saved/YYYYmmdd-HHMMSS.json

To print out a table with the running programs

```
python3 main.py out1 saved/YYYYmmdd-HHMMSS.json
```
