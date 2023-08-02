import requests
import json

__all__ =[
    'ip',
    'port',
    'create',
    'delete',
    'list',
    'update',
    'exists',
    'onlines'
]


def ip (node):
    res = requests.get(f"http://{node.address}/ip", headers={'mohali-secret':node.secret} )
    return res.text

def port (node):
    res = requests.get(f"http://{node.address}/port", headers={'mohali-secret':node.secret} )
    return res.text

def create(node,**user_data):
    body = json.dumps(user_data)
    res = requests.post(f"http://{node.address}/create", body, headers={'mohali-secret':node.secret})
    return res.text == 'success'

def delete(node,**user_data):
    body = json.dumps(user_data)
    res = requests.post(f"http://{node.address}/delete", body, headers={'mohali-secret':node.secret})
    return res.text == 'success'

def list(node):
    res = requests.get(f"http://{node.address}/list", headers={'mohali-secret':node.secret} )
    return json.loads(res.text)

def update(node,**user_data):
    body = json.dumps(user_data)
    res = requests.post(f"http://{node.address}/update", body, headers={'mohali-secret':node.secret})
    return res.text == 'success'

def onlines(node):
    res = requests.get(f"http://{node.address}/onlines", headers={'mohali-secret':node.secret})
    return json.loads(res.text)

def exists(node,acc):
    return acc.username in list(node)