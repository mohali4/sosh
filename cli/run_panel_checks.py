#!/usr/bin/python3
from pathlib import Path
from .process import service
from .process.log import handlers as H

base_dir = Path(__file__).parent/".."
def run():
    service_name = 'sosh.panel.checkLoop'
    command = f"{base_dir/'venv'/'bin'/'python3'} {base_dir/'node'/'manage.py'}  runchecksloop"
    service(command, service_name, H.file(base_dir/'logs'/f'{service_name}.txt')).run()
