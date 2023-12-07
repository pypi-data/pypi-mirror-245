from .config.sqlt import get_sqlt, STATUS, ARG, OUT, ERR, SqlData
from .config.status import Status
from .config.arg import Arg
from .config.out import Out, Err


def table_init():
    with get_sqlt() as sqlt:
        sqlt.createTable(ARG, Arg.colmap.keys(), Arg.colmap, key='task')
        sqlt.createTable(STATUS, Status.colmap.keys(), Status.colmap, key='task')
        sqlt.commit()


def set_arg(arg, reload_status):
    with get_sqlt() as sqlt:
        sqlt.delete(ARG, where=f"task='{arg.task}'")
        sqlt.insert(ARG, SqlData([arg.get()]))
        if reload_status:
            sqlt.delete(STATUS, where=f"task='{arg.task}'")
        sqlt.commit()


def saveOut(task, sd, ed,running_seconds, out):
    with get_sqlt() as sqlt:
        outer = Out(task, sd, ed, running_seconds,out)
        sqlt.create_insert(OUT, [outer.get()], colmap=Out.colmap)
        sqlt.commit()


def saveErr(task, i, sd, ed,running_seconds, outerr):
    with get_sqlt() as sqlt:
        errer = Err(i, task, sd, ed,running_seconds, outerr)
        sqlt.create_insert(ERR, [errer.get()], colmap=Err.colmap)
        sqlt.commit()


def setStatus(status):
    with get_sqlt() as sqlt:
        sqlt.delete(STATUS, where=f"task='{status.task}'")
        sqlt.insert(STATUS, SqlData([status.get()]))
        sqlt.commit()
