#!/usr/bin/python3
import os
from cli import _C
from cli.form import Form
from pathlib import Path

INSTALL_DIR = Path("/opt/sosh")

if os.getuid() != 0:  # make sure script run as sudo
    _C(f"sudo python3 {__file__}")

def reinstall (form:Form):
    form.exit()

def cleanReinstall (form:Form):
    os.remove(INSTALL_DIR)
    os.mkdir(INSTALL_DIR)
    form.exit()

if os.path.exists(INSTALL_DIR):
    if os.path.isfile(INSTALL_DIR):
        os.remove(INSTALL_DIR)
    else:
        Form(
            "A sosh installation exists what will I do ?",
            ["Reinstall sosh",reinstall],
            ["Clean reinstall sosh",cleanReinstall],
            ["Exit setup",quit]
        )
else :
    os.mkdir(INSTALL_DIR)

_C(f"cp -r ./node ./panel ./cli {INSTALL_DIR}")
_C(f"ln -sf {INSTALL_DIR/'cli'/'run_sosh_cli.py'} /usr/bin/sosh")

print("Run following command for countinue setup:")
print("      sudo sosh ")
