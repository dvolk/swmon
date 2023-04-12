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


def identify_mantidworkbench64(user_processes):
    for p in user_processes:
        if "/opt/mantidworkbench6.4/bin/mantidworkbench" in p:
            return "mantidworkbench-64"


def identify_mantidworkbench65(user_processes):
    for p in user_processes:
        if "/opt/mantidworkbench6.5/bin/mantidworkbench" in p:
            return "mantidworkbench-65"


def identify_mantidworkbench66(user_processes):
    for p in user_processes:
        if "/opt/mantidworkbench6.6/bin/mantidworkbench" in p:
            return "mantidworkbench-66"


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


def identify_matlab2021b(user_processes):
    for p in user_processes:
        if "/opt/matlab2021b/bin/glnxa64/MATLAB" in p:
            return "matlab-2021b"


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


def identify_jupyter_notebook(user_processes):
    for p in user_processes:
        if "/opt/jupyter/bin/python /opt/jupyter/bin/jupyter-notebook" in p:
            return "jupyter-notebook"


def identify_jupyter_lab(user_processes):
    for p in user_processes:
        if "/opt/jupyter/bin/python /opt/jupyter/bin/jupyter-lab" in p:
            return "jupyter-lab"


def identify_gromacs(user_processes):
    for p in user_processes:
        if "/usr/local/bin/gromacs_bashrc" in p:
            return "gromacs"


def identify_atsas(user_processes):
    for p in user_processes:
        if "/usr/local/bin/atsas/atsas_cli_launcher" in p:
            return "atsas"


def identify_gsas2(user_processes):
    for p in user_processes:
        if "/opt/gsas2/bin/python /opt/gsas2/GSASII/GSASII.py" in p:
            return "gsas2"


def identify_mantidimaging(user_processes):
    for p in user_processes:
        if (
            "/opt/mambaforge/envs/mantidimaging/bin/python3.9 /opt/mambaforge/envs/mantidimaging/bin/mantidimaging"
            in p
        ):
            return "mantidimaging"


def identify_turbovnc(user_processes):
    for p in user_processes:
        if "/opt/TurboVNC/bin/Xvnc" in p:
            return "turbovnc"


def identify_sscanss(user_processes):
    for p in user_processes:
        if "/opt/sscanss2/bin/sscanss" in p:
            return "SScanSS2"


def identify_dlpoly(user_processes):
    for p in user_processes:
        if "java -jar ../java/GUI.jar" in p:
            return "dlpoly"


def identify_jv(user_processes):
    for p in user_processes:
        if "jv" == p:
            return "jv"


def identify_aten(user_processes):
    a = False
    b = False
    for p in user_processes:
        if "/bin/sh /.singularity.d/runscript" in p:
            a = True
        if "/opt/squashfs-root/AppRun" in p:
            b = True
    if a and b:
        return "aten"


def identify_sublime(user_processes):
    for p in user_processes:
        if "/opt/sublime_text/sublime_text" in p:
            return "sublime_text"


def identify_gedit(user_processes):
    for p in user_processes:
        if "/usr/bin/gedit" in p:
            return "gedit"


def identify_emacs(user_processes):
    for p in user_processes:
        if "emacs" in p:
            return "emacs"


def identify_gnuplot(user_processes):
    for p in user_processes:
        if "gnuplot" in p:
            return "gnuplot"


def identify_sftp(user_processes):
    for p in user_processes:
        if "sftp" in p:
            return "sftp"


def identify_risretto(user_processes):
    for p in user_processes:
        if "risretto" in p:
            return "risretto"


def identify_mpirun(user_processes):
    for p in user_processes:
        if "mpirun" in p:
            return "mpirun"


def identify_refnx(user_processes):
    for p in user_processes:
        if "/opt/refnx/bin/python /usr/bin/refnx" in p:
            return "refnx"


def identify_xfce4_terminal(user_processes):
    for p in user_processes:
        if "/usr/bin/xfce4-terminal" == p:
            return "xfce4-terminal"


def identify_vscode(user_processes):
    for p in user_processes:
        if "/usr/share/code/code" in p:
            return "vscode"
