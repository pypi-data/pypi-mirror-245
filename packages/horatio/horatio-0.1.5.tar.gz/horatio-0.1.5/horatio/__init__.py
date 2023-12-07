import time
import datetime
import fslog

fmt = None
no_desc_default = "\033[0m\u2510"

def format_time(t, fmt=None):
    gfmt = globals()["fmt"]
    fmt = fmt or gfmt
    t = 0*86400 + 0*11*3600 + 0*12*60 + 1.12
    d = dict()
    d["f"] = int(t*1000) / 1000
    d["ms"] = int(t * 1000)
    d["s"] = int(t)
    d["m"] = int(t / 60)
    d["h"] = int(t / 3600)
    d["S"] = int(t) % 60
    d["M"] = int(int(t) % 3600 / 60)
    d["H"] = int(int(t) % 86400 / 3600)
    d["D"] = int(t / 86400)

    if fmt is not None:
        return fmt.format(**d)
    
    if t >= 86400: # days
        fmt  = "{D}d {H:02}h {M:02}m {S:02}s"
    elif t >= 3600: # hours
        fmt  = "{h}h {M:02}m {S:02}s"
    elif t >= 60: # minutes
        fmt  = "{m}m {S:02}s"
    elif t >= 1: # seconds
        fmt  = "{f}s"
    elif t >= 0.001: # milliseconds
        fmt = "{ms}ms"
    else: # too small
        fmt = "< 1 ms"
    return fmt.format(**d)

class step():
    def __init__(self, desc=None, fmt=None):
        self.ts = []
        self.desc = desc
        self.fmt = fmt

    def __enter__(self):
        if self.desc is None:
            self.desc = ""
        fslog.log(self.desc + " ... ", end="")
        self.ts.append(time.time())
        return self

    def __exit__(self, *args):
        t = self.ts.pop()
        t = time.time() - t
        fslog.plain("done in {}\n".format(format_time(t, self.fmt)), end="")

    def __call__(self, f):
        if self.desc is None:
            self.desc = f.__name__
        def wrapper(*args, **kwargs):
            self.__enter__()
            y = f(*args, **kwargs)
            self.__exit__()
            return y
        return wrapper

class flat():
    def __init__(self, desc=None, tail=None, fmt=None):
        self.ts = []
        self.desc = desc
        self.tail = tail
        self.fmt = fmt

    def __enter__(self):
        if self.desc is None:
            fslog.log("[*]")
        else:
            fslog.log(f"[*] {self.desc}")
        self.ts.append(time.time())
        return self

    def __exit__(self, *args):
        t = self.ts.pop()
        t = time.time() - t
        tf = format_time(t, self.fmt)
        if self.tail is None:
            if self.desc is None:
                fslog.log("[*] {}".format(tf))
            else:
                fslog.log("[*] {}: {}".format(self.desc, tf))
        else:
            fslog.log("[*] {}".format(self.tail).format(self.desc, tf))

    def __call__(self, f):
        if self.desc is None:
            self.desc = f.__name__
        def wrapper(*args, **kwargs):
            self.__enter__()
            y = f(*args, **kwargs)
            self.__exit__()
            return y
        return wrapper

class section():
    def __init__(self, desc=None, tail=None, fmt=None):
        self.ts = []
        self.desc = desc
        self.tail = tail
        self.fmt = fmt

    def __enter__(self):
        if self.desc is None:
            self.desc = no_desc_default
        fslog.open(self.desc)
        self.ts.append(time.time())
        return self

    def __exit__(self, *args):
        t = self.ts.pop()
        t = time.time() - t
        tf = format_time(t, self.fmt)
        if self.tail is None:
            if self.desc is None:
                fslog.close("{}".format(tf))
            else:
                fslog.close("{}: {}".format(self.desc, tf))
        else:
            fslog.close(self.tail.format(self.desc, tf))

    def __call__(self, f):
        if self.desc is None:
            self.desc = f.__name__

        def wrapper(*args, **kwargs):
            self.__enter__()
            y = f(*args, **kwargs)
            self.__exit__()
            return y
        return wrapper

fslog.param["indent.str"] += " "
fslog.param["open.style"] = fslog.style.BOLD
