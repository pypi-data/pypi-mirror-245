from concurrent.futures import Executor, ProcessPoolExecutor
import asyncio
import functools
import json
from logging import getLogger
import math
import sys
from typing import Any
from collections.abc import AsyncIterator, Awaitable, Callable
from pathlib import PurePath, Path

from PIL import Image
from wcpan.drive.core.types import Node, ChangeAction, MediaInfo, Drive, CreateHasher
from wcpan.drive.core.exceptions import UnauthorizedError
import yaml


def get_default_config_path() -> Path:
    path = Path("~/.config")
    path = path.expanduser()
    path = path / "wcpan.drive"
    return path


def get_default_data_path() -> Path:
    path = Path("~/.local/share")
    path = path.expanduser()
    path = path / "wcpan.drive"
    return path


def create_executor() -> Executor:
    from multiprocessing import get_start_method

    if get_start_method() == "spawn":
        return ProcessPoolExecutor(initializer=initialize_worker)
    else:
        return ProcessPoolExecutor()


def initialize_worker() -> None:
    from signal import signal, SIG_IGN, SIGINT

    signal(SIGINT, SIG_IGN)


async def get_node_by_id_or_path(drive: Drive, id_or_path: str) -> Node:
    if id_or_path[0] == "/":
        node = await drive.get_node_by_path(PurePath(id_or_path))
    else:
        node = await drive.get_node_by_id(id_or_path)
    return node


async def traverse_node(drive: Drive, node: Node, level: int) -> None:
    if not node.parent_id:
        print_node("/", level)
    elif level == 0:
        top_path = await drive.resolve_path(node)
        print_node(str(top_path), level)
    else:
        print_node(node.name, level)

    if node.is_directory:
        children = await drive.get_children(node)
        for child in children:
            await traverse_node(drive, child, level + 1)


async def trash_node(drive: Drive, id_or_path: str) -> str | None:
    """
    :returns: None if succeed, id_or_path if failed
    """
    node = await get_node_by_id_or_path(drive, id_or_path)
    if not node:
        return id_or_path
    try:
        await drive.move(node, trashed=True)
    except Exception:
        getLogger(__name__).exception("trash failed")
        return id_or_path
    return None


async def wait_for_value[T](k: str, v: Awaitable[T]) -> tuple[str, T]:
    return k, await v


def get_hash(local_path: Path, create_hasher: CreateHasher) -> str:
    from asyncio import run

    CHUNK_SIZE = 64 * 1024

    async def calc():
        hasher = await create_hasher()
        with open(local_path, "rb") as fin:
            while True:
                chunk = fin.read(CHUNK_SIZE)
                if not chunk:
                    break
                await hasher.update(chunk)
        return await hasher.hexdigest()

    return run(calc())


async def chunks_of(
    ag: AsyncIterator[ChangeAction],
    size: int,
) -> AsyncIterator[list[ChangeAction]]:
    chunk: list[ChangeAction] = []
    async for item in ag:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def print_node(name: str, level: int) -> None:
    indention = " " * level
    print(indention + name)


def print_as_yaml(data: Any) -> None:
    yaml.safe_dump(
        data,
        stream=sys.stdout,
        allow_unicode=True,
        encoding=sys.stdout.encoding,
        default_flow_style=False,
    )


def print_id_node_dict(data: Any) -> None:
    pairs = sorted(data.items(), key=lambda _: _[1])
    for id_, path in pairs:
        print(f"{id_}: {path}")


def humanize(n: int) -> str:
    UNIT_LIST = ["", "KiB", "MiB", "GiB", "TiB", "PiB"]
    e = 0
    while n >= 1024:
        n = n // 1024
        e += 1
    return f"{n}{UNIT_LIST[e]}"


def require_authorized[
    **A
](fn: Callable[A, Awaitable[int]]) -> Callable[A, Awaitable[int]]:
    @functools.wraps(fn)
    async def action(*args: A.args, **kwargs: A.kwargs) -> int:
        try:
            return await fn(*args, **kwargs)
        except UnauthorizedError:
            print("not authorized")
            return 1

    return action


def get_image_info(local_path: Path) -> MediaInfo:
    image = Image.open(str(local_path))
    width, height = image.size
    return MediaInfo.image(width=width, height=height)


async def get_video_info(local_path: Path) -> MediaInfo:
    cmd = (
        "ffprobe",
        "-v",
        "error",
        "-show_format",
        "-show_streams",
        "-select_streams",
        "v:0",
        "-print_format",
        "json",
        "-i",
        str(local_path),
    )
    cp = await asyncio.create_subprocess_exec(
        *cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, _err = await cp.communicate()
    data = json.loads(out)
    format_ = data["format"]
    ms_duration = math.floor(float(format_["duration"]) * 1000)
    video = data["streams"][0]
    width = video["width"]
    height = video["height"]
    return MediaInfo.video(width=width, height=height, ms_duration=ms_duration)
