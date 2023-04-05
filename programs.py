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
            return "EPSR"
        if "/opt/epsr26/EPSR/gui/EPSRshell.jar" in p:
            return "EPSR"


def identify_mantidworkbench65(user_processes):
    for p in user_processes:
        if "/opt/mantidworkbench6.5/bin/mantidworkbench" in p:
            return "mantidworkbench65"


def identify_sasview5(user_processes):
    for p in user_processes:
        if "/opt/sasview5/bin/python" in p:
            return "sasview5"


def identify_libreoffice(user_processes):
    for p in user_processes:
        if "/usr/lib64/libreoffice/program/soffice.bin" in p:
            return "libreoffice"


def identify_matlab2021a(user_processes):
    for p in user_processes:
        if "/opt/matlab2021a/bin/glnxa64/MATLAB" in p:
            return "matlab2021a"
