"""Module that contains functions for identifying programs.

Functions that take a list of user processes and
return the name of the identified program (or none)."""


def identify_firefox(user_processes):
    for p in user_processes:
        if "/usr/lib64/firefox/firefox" in p:
            return "firefox"


def identify_epsr(user_processes):
    for p in user_processes:
        if "/opt/epsr26/EPSR/bin/epsr" in p:
            return "EPSR-26"
        if "/opt/epsr26/EPSR/gui/EPSRshell.jar" in p:
            return "EPSR-25"


def identify_mantidworkbench65(user_processes):
    for p in user_processes:
        if "/opt/mantidworkbench6.5/bin/mantidworkbench" in p:
            return "mantidworkbench-65"


def identify_mantidworkbenchnightly(user_processes):
    for p in user_processes:
        if "/opt/mantidworkbenchnightly/bin/mantidworkbench" in p:
            return "mantidworkbench-nightly"


def identify_sasview5(user_processes):
    for p in user_processes:
        if "/opt/sasview5/bin/python" in p:
            return "sasview-5"


def identify_libreoffice(user_processes):
    for p in user_processes:
        if "/usr/lib64/libreoffice/program/soffice.bin" in p:
            return "libreoffice"


def identify_matlab2021a(user_processes):
    for p in user_processes:
        if "/opt/matlab2021a/bin/glnxa64/MATLAB" in p:
            return "matlab-2021a"


def identify_xvnc(user_processes):
    for p in user_processes:
        if "/usr/bin/Xvnc" in p:
            return "Xvnc"


def identify_xfwm4(user_processes):
    for p in user_processes:
        if "xfwm4" in p:
            return "xfwm4"


def identify_dissolve(user_processes):
    for p in user_processes:
        if "bin/dissolve-gui" in p:
            return "dissolve"


def identify_fiji(user_processes):
    for p in user_processes:
        if "/opt/Fiji.app/ImageJ-linux64" in p:
            return "Fiji"


def identify_gudpy(user_processes):
    for p in user_processes:
        if "/opt/GudPy/gudpy" in p:
            return "GudPy"


def identify_gudrun(user_processes):
    for p in user_processes:
        if "GudrunGUI/GudrunGUI_4.jar" in p:
            return "GudRun"


def identify_mcstas(user_processes):
    for p in user_processes:
        if "/usr/local/bin/mcstas_launcher" in p:
            return "mcstas"


def identify_horace(user_processes):
    for p in user_processes:
        if "/opt/matlab2021b/bin/glnxa64/MATLAB -r horace_on" in p:
            return "horace"


def identify_mathematica(user_processes):
    for p in user_processes:
        if "/opt/mathematica12/Executables/Mathematica" in p:
            return "mathematica"


def identify_fullprof(user_processes):
    for p in user_processes:
        if "/usr/local/bin/FullProf_Suite/tfp" in p:
            return "fullprof"
