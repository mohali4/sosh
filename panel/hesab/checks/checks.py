from ..conf import _C
from ..models import transfer as transfers , vuser , node as nodes
from jdatetime import datetime
from .management import loop

@loop
def check_transfers ():
    for transfer in transfers.objects.all(): 
        if transfer.enable :
            transfer.ensure_tobe()
        else:
            transfer.ensure_tonotbe()


@loop
def check_nodes ():
    for node in nodes.objects.all(): 
        for user_name in node.list(): #type: ignore
            Fuser = vuser.objects.filter(name=user_name)
            if not Fuser.exists():
                node.api.delete(username=user_name)
            else: 
                user = Fuser[0]
                if not transfers.objects.filter(user=user,node=node).enableds().exists():
                    node.api.delete(username=user_name)


@loop
def backup_sqlite_file():
    status = _C('git status')
    if 'db.sqlite3' in status :
        _C('git reset *')
        _C('git add **/db.sqlite3')
        _C(f'git commit -m "auto commit for db.sqlite3 {datetime.now().isoformat()}"')
        _C('git push --set-upstream origin master')
