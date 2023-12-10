# This file is placed in the Public Domain
#
# pylint: disable=C,R


"run"


import inspect
import time


from .command import Commands
from .event   import Event
from .object  import Object
from .storage import Storage
from .thread  import launch
from .utils   import spl


def __dir__():
    return (
        'command',
        'forever',
        'scan'
    )


def command(txt):
    evn = Event()
    evn.txt = txt
    Commands.handle(evn)
    evn.wait()
    return evn


def forever():
    while 1:
        time.sleep(1.0)


def scan(pkg, modstr, initer=False) -> []:
    threads = []
    for modname in spl(modstr):
        module = getattr(pkg, modname, None)
        if not module:
            continue
        for key, cmd in inspect.getmembers(module, inspect.isfunction):
            if key.startswith("cb"):
                continue
            if 'event' in cmd.__code__.co_varnames:
                Commands.add(cmd)
        for key, clz in inspect.getmembers(module, inspect.isclass):
            if key.startswith("cb"):
                continue
            if not issubclass(clz, Object):
                continue
            Storage.add(clz)
        if initer and "init" in dir(module):
            threads.append(launch(module.init, name=f"init {modname}"))
    return threads
