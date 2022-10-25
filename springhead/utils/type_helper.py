def get_type(name):
    t = __builtins__.get(name)
    if isinstance(t, type):
        return t
    raise ValueError(name)
