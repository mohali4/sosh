def _C (c:str,**wargs) -> str:
    import subprocess
    from shlex import split
    result = subprocess.run(split(c) , stdout=subprocess.PIPE, **wargs)
    return result.stdout.decode() #type: ignore
def clearScrean():
    import os
    os.system('clear')