def get_type(name: str):
    t = __builtins__.get(name)
    if isinstance(t, type):
        return t
    else:
        return name
