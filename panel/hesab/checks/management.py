def loop (f):
    f.__dict__['loop'] = True
    return f