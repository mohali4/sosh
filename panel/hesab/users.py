

class bridge :

    def toapp (nameornames): #type: ignore
        if isinstance(nameornames,str):
            return nameornames[:-4]
        elif isinstance(nameornames,list) or isinstance(nameornames,tuple):
            return [bridge.toapp(name) for name in nameornames] #type: ignore


    def tolinux (nameornames): #type: ignore
        if isinstance(nameornames,str):
            return nameornames+"_vpn" #type: ignore
        elif isinstance(nameornames,list) or isinstance(nameornames,tuple):
            return [bridge.tolinux(name) for name in nameornames] #type: ignore


