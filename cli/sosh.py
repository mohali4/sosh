from pathlib import Path
base_dir = Path(__file__).parent.parent
import subprocess
import os
from form import Form
from pathlib import Path
from . import _C


def is_service_running(service_name): # Copied from ChatGPT
    try:
        status_output = subprocess.check_output(["systemctl", "is-active", service_name], stderr=subprocess.STDOUT, text=True)
        return status_output.strip() == "active"
    except subprocess.CalledProcessError as e:
        # The 'systemctl' command returned a non-zero exit code, meaning the service is not active.
        return False


def does_service_exist(service_name): # Copied from ChatGPT
    try:
        subprocess.check_output(["systemctl", "status", service_name], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError as e:
        # The 'systemctl' command returned a non-zero exit code, meaning the service does not exist or another error occurred.
        return False

services = []
class service :
    def __init__(self, name, title) -> None:
        self.name = name
        self.title = title
        services.append(self)
    @property
    def running (self):
        return is_service_running(self.name)

    def start (self):
        _C(f"systemctl start {self.name}")
    def stop (self):
        _C(f"systemctl stop {self.name}")


    def formShow (self):
        rows = [
            ["Start",self.start] if not self.running else ["Stop",self.stop]
        ]
        rows += [
            ["Settings",self.EditSettings],
            ["New super user",self.newSuperUser],
            ["Uninstall",self.removeService],
            ["Exit",quit],
        ]
        Form(*rows)

    def EditSettings (self):
        def nano (form):
            _C(f"nano {base_dir/self.title/'setting.json'}")
            form.exit()
        def vim (form):
            _C(f"vim {base_dir/self.title/'setting.json'}")
            form.exit()
        def back (form):
            form.exit()
        Form(
            ['nano',nano],
            ['vim',vim],
            ['Back',back]
        )
    def newSuperUser(self):
        _C(f"python3 {base_dir/self.title/'manage.py'} createsuperuser")

    def removeService (self):
        _C(f"systemctl disable --now {self.name}")
        os.remove(f"/lib/systemd/system/{self.name}.service")

    def installService(self):
        ser = __import__(f"{self.title}.service").SERVICE
        ser = ser.format(workingDir=(base_dir/self.title).__str__(),execStart=(base_dir/"cli"/f"run_{self.title}.py").__str__())
        with open(f"/lib/systemd/system/{self.name}.service","w+") as f:
            f.write(ser)
            f.close()



service(
    "sosh_node",
    "node"
)
service(
    "sosh_panel",
    "panel"
)

FormRows = []

for ser in services:
    row = []
    if does_service_exist(ser.name):
            row = [
                ser.title,
                ser.formShow
            ]
    else:
            row = [
                f"Install {ser.title}",
                ser.installService
            ]
    FormRows.append(row)


Form(
    *[*FormRows,["Exit",quit]]
)


