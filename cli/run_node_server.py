#!/usr/bin/python3
from pathlib import Path
import json
import os
from .process import service
from .process.log import handlers as H

base_dir = Path(__file__).parent/".."
def run():
    service_name = 'sosh.node.server'
    os.chdir(base_dir/"node")
    settings = json.loads(open(base_dir/"node"/"setting.json",'r').read())
    command = f"{base_dir/'venv'/'bin'/'python3'} -m gunicorn ketab.wsgi:application -b {settings['listen']}:{settings['port']}"
    service(command, service_name, H.file(base_dir/'logs'/f'{service_name}.txt')).run()
