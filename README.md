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

It will be saved in `saved/YYYYmmdd/HHMMSS.json`

To print out a table with the running programs:

```
python3 main.py out1 saved/YYYYmmdd/HHMMSS.json
```

## Identified programs

- [x] Firefox
- [x] EPSR
- [x] Mantid 6.5
- [x] Mantid nightly
- [x] Sasview 5
- [x] Libreoffice
- [x] Matlab 2021a
- [x] Xvnc
- [x] Xfwm4
- [x] ATSAS
- [x] Aten
- [ ] Cambridge Structural Database System (CSD-System) - Has multiple execs, Sanghamitra has said they use Conquest and Mercury in particular
- [x] CSD crossminer
- [x] DL_Poly
- [x] Dissolve
- [x] Fiji
- [x] FullProf
- [x] GROMACS
- [x] GSAS-II
- [x] GudPy
- [x] GudRun
- [x] Horace - this is a matlab toolbox but the word horace might be in the process name somewhere
- [x] Jupyter notebook + Jupyter lab
- [ ] LAMMPS
- [x] MDANSE
- [x] Mantid Imaging
- [x] Mathematica
- [x] McStas
- [x] SScanSS 2
