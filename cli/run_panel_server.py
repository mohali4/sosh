#!/usr/bin/python3
from pathlib import Path
import json
import os
from .process.log import handlers as H
from process import service
base_dir = Path(__file__).parent/".."
def run():
    os.chdir(base_dir/"panel")
    service_name = "sosh.panel.server"
    settings = json.loads(open(base_dir/"panel"/"setting.json",'r').read())
    command = f"{base_dir/'venv'/'bin'/'python3'} -m gunicorn ketab.wsgi:application -b {settings['listen']}:{settings['port']}"
    service(command, service_name, H.file(base_dir/'logs'/f'{service_name}.txt')).run()