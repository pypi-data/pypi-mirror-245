from typing import TypedDict, Any, NotRequired
from pathlib import Path
from functools import partial
from importlib import import_module
from contextlib import asynccontextmanager

from yaml import safe_load
from wcpan.drive.core import create_drive


class FunctionDict(TypedDict):
    name: str
    args: NotRequired[list[Any]]
    kwargs: NotRequired[dict[str, Any]]


class DriveDict(TypedDict):
    file: FunctionDict
    file_middleware: NotRequired[list[FunctionDict]]
    snapshot: FunctionDict
    snapshot_middleware: NotRequired[list[FunctionDict]]


class MainDict(TypedDict):
    version: int
    drive: DriveDict


@asynccontextmanager
async def create_drive_from_config(path: Path):
    with path.open("r") as fin:
        main: MainDict = safe_load(fin)

    version = main["version"]
    if version != 2:
        raise RuntimeError("wrong version")

    drive = main["drive"]
    file_ = _deserialize(drive["file"])
    file_middleware = [_deserialize(_) for _ in drive.get("file_middleware", [])]
    snapshot = _deserialize(drive["snapshot"])
    snapshot_middleware = [
        _deserialize(_) for _ in drive.get("snapshot_middleware", [])
    ]

    async with create_drive(
        file=file_,
        file_middleware=file_middleware,
        snapshot=snapshot,
        snapshot_middleware=snapshot_middleware,
    ) as drive:
        yield drive


def _deserialize(fragment: FunctionDict):
    name = fragment["name"]
    args = fragment.get("args", [])
    kwargs = fragment.get("kwargs", {})

    base, name = name.rsplit(".", 1)
    module = import_module(base)
    function = getattr(module, name)

    bound = partial(function, *args, **kwargs)
    return bound
