#!/usr/bin/python3
from run_node_checks import run as chRun
from run_node_server import run as nRun
from multiprocessing import Process
Process(target=chRun).start()
Process(target=nRun).start()
