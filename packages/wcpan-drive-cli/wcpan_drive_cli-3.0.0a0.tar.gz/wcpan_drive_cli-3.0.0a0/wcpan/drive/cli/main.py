import asyncio
import functools
import io
from logging.config import dictConfig
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path, PurePath
from asyncio import as_completed

from wcpan.drive.core.types import Drive
from wcpan.logging import ConfigBuilder

from . import __version__ as VERSION
from ._lib import (
    chunks_of,
    create_executor,
    get_node_by_id_or_path,
    print_as_yaml,
    print_id_node_dict,
    require_authorized,
    trash_node,
    traverse_node,
    wait_for_value,
)
from ._download import download_list
from ._upload import upload_list
from .lib import get_usage
from .interaction import interact
from .cfg import create_drive_from_config


def main(args: list[str] | None = None) -> int:
    if args is None:
        args = sys.argv
    try:
        return asyncio.run(amain(args))
    except KeyboardInterrupt:
        return 1


async def amain(args: list[str]) -> int:
    dictConfig(ConfigBuilder().add("wcpan", level="D").to_dict())

    kwargs = parse_args(args[1:])
    if not kwargs.action:
        await kwargs.fallback_action()
        return 0

    config: str = kwargs.config
    path = Path(config)
    async with create_drive_from_config(path) as drive:
        return await kwargs.action(drive, kwargs)


def parse_args(args: list[str]) -> Namespace:
    parser = ArgumentParser("wcpan.drive.cli")

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"{VERSION}",
    )

    parser.add_argument(
        "--config",
        "-c",
        help=("specify configuration file path"),
    )

    commands = parser.add_subparsers()

    auth_parser = commands.add_parser(
        "auth",
        aliases=["a"],
        help="authorize user",
    )
    auth_parser.set_defaults(action=action_auth)

    sync_parser = commands.add_parser(
        "sync",
        aliases=["s"],
        help="synchronize database",
    )
    add_bool_argument(sync_parser, "verbose", "v")
    sync_parser.set_defaults(action=action_sync)

    find_parser = commands.add_parser(
        "find",
        aliases=["f"],
        help="find files/folders by pattern [offline]",
    )
    add_bool_argument(find_parser, "id_only")
    add_bool_argument(find_parser, "include_trash")
    find_parser.add_argument("pattern", type=str)
    find_parser.set_defaults(action=action_find, id_only=False, include_trash=False)

    info_parser = commands.add_parser(
        "info",
        aliases=["i"],
        help="display file information [offline]",
    )
    info_parser.set_defaults(action=action_info)
    info_parser.add_argument("id_or_path", type=str)

    list_parser = commands.add_parser(
        "list",
        aliases=["ls"],
        help="list folder [offline]",
    )
    list_parser.set_defaults(action=action_list)
    list_parser.add_argument("id_or_path", type=str)

    tree_parser = commands.add_parser(
        "tree",
        help="recursive list folder [offline]",
    )
    tree_parser.set_defaults(action=action_tree)
    tree_parser.add_argument("id_or_path", type=str)

    usage_parser = commands.add_parser(
        "usage",
        aliases=["du"],
        help=("calculate space usage for files, " "recursively for folders [offline]"),
    )
    usage_parser.add_argument("id_or_path", type=str, nargs="+")
    add_bool_argument(usage_parser, "comma")
    usage_parser.set_defaults(action=action_usage, comma=False)

    dl_parser = commands.add_parser(
        "download",
        aliases=["dl"],
        help="download files/folders",
    )
    dl_parser.set_defaults(action=action_download)
    dl_parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=1,
        help=("maximum simultaneously download jobs" " (default: %(default)s)"),
    )
    dl_parser.add_argument("id_or_path", type=str, nargs="+")
    dl_parser.add_argument("destination", type=str)

    ul_parser = commands.add_parser(
        "upload",
        aliases=["ul"],
        help="upload files/folders",
    )
    ul_parser.set_defaults(action=action_upload)
    ul_parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=1,
        help=("maximum simultaneously upload jobs" " (default: %(default)s)"),
    )
    ul_parser.add_argument("source", type=str, nargs="+")
    ul_parser.add_argument("id_or_path", type=str)

    rm_parser = commands.add_parser(
        "remove",
        aliases=["rm"],
        help="trash files/folders",
    )
    rm_parser.set_defaults(action=action_remove)
    rm_parser.add_argument("id_or_path", type=str, nargs="+")

    mv_parser = commands.add_parser(
        "rename",
        aliases=["mv"],
        help="rename file/folder",
    )
    mv_parser.set_defaults(action=action_rename)
    mv_parser.add_argument("source_id_or_path", type=str, nargs="+")
    mv_parser.add_argument("destination_path", type=str)

    mkdir_parser = commands.add_parser(
        "mkdir",
        help="create folder",
    )
    mkdir_parser.set_defaults(action=action_mkdir)
    mkdir_parser.add_argument("path", type=str)

    trash_parser = commands.add_parser(
        "trash",
        help="list trash can",
    )
    add_bool_argument(trash_parser, "flatten")
    trash_parser.set_defaults(
        action=action_trash,
        flatten=False,
    )

    shell_parser = commands.add_parser(
        "shell",
        help="start an interactive shell",
    )
    shell_parser.set_defaults(action=action_shell)
    shell_parser.add_argument("id_or_path", type=str, nargs="?")

    sout = io.StringIO()
    parser.print_help(sout)
    fallback = functools.partial(action_help, sout.getvalue())
    parser.set_defaults(action=None, fallback_action=fallback)

    kwargs = parser.parse_args(args)

    return kwargs


def add_bool_argument(
    parser: ArgumentParser,
    name: str,
    short_name: str | None = None,
) -> None:
    flag = name.replace("_", "-")
    pos_flags = ["--" + flag]
    if short_name:
        pos_flags.append("-" + short_name)
    neg_flag = "--no-" + flag
    parser.add_argument(*pos_flags, dest=name, action="store_true")
    parser.add_argument(neg_flag, dest=name, action="store_false")


async def action_help(message: str) -> None:
    print(message)


async def action_auth(drive: Drive, args: Namespace) -> int:
    url = await drive.get_oauth_url()
    print("Access the following URL to authorize user:\n")
    print(url)
    print("")
    print("Paste the redireced URL or provided code here:")
    answer = input("")
    await drive.set_oauth_token(answer)
    return 0


@require_authorized
async def action_sync(drive: Drive, args: Namespace) -> int:
    chunks = chunks_of(drive.sync(), 100)
    async for changes in chunks:
        if not args.verbose:
            print(len(changes))
        else:
            for change in changes:
                print_as_yaml(change)
    return 0


async def action_find(drive: Drive, args: Namespace) -> int:
    nodes = await drive.find_nodes_by_regex(args.pattern)
    if not args.include_trash:
        nodes = (_ for _ in nodes if not _.is_trashed)
    nodes = (wait_for_value(_.id, drive.resolve_path(_)) for _ in nodes)
    nodes = await asyncio.gather(*nodes)
    nodes = dict(nodes)

    if args.id_only:
        for id_ in nodes:
            print(id_)
    else:
        print_id_node_dict(nodes)

    return 0


async def action_info(drive: Drive, args: Namespace) -> int:
    from dataclasses import asdict

    node = await get_node_by_id_or_path(drive, args.id_or_path)
    print_as_yaml(asdict(node))
    return 0


async def action_list(drive: Drive, args: Namespace) -> int:
    node = await get_node_by_id_or_path(drive, args.id_or_path)
    nodes = await drive.get_children(node)
    nodes = {_.id: _.name for _ in nodes}
    print_id_node_dict(nodes)
    return 0


async def action_tree(drive: Drive, args: Namespace) -> int:
    node = await get_node_by_id_or_path(drive, args.id_or_path)
    await traverse_node(drive, node, 0)
    return 0


async def action_usage(drive: Drive, args: Namespace) -> int:
    node_list = (get_node_by_id_or_path(drive, _) for _ in args.id_or_path)
    node_list = await asyncio.gather(*node_list)
    node_list = (get_usage(drive, _) for _ in node_list)
    node_list = await asyncio.gather(*node_list)

    for usage, src in zip(node_list, args.id_or_path):
        if args.comma:
            label = f"{usage:,}"
        else:
            label = f"{usage}"
        print(f"{label} - {src}")
    return 0


@require_authorized
async def action_download(drive: Drive, args: Namespace) -> int:
    with create_executor() as pool:
        g = (get_node_by_id_or_path(drive, _) for _ in args.id_or_path)
        ag = (await _ for _ in as_completed(g))
        node_list = [_ async for _ in ag if not _.is_trashed]
        dst = Path(args.destination)

        ok = await download_list(node_list, dst, drive=drive, pool=pool, jobs=args.jobs)

    return 0 if ok else 1


@require_authorized
async def action_upload(drive: Drive, args: Namespace) -> int:
    with create_executor() as pool:
        node = await get_node_by_id_or_path(drive, args.id_or_path)
        src_list = [Path(_) for _ in args.source]

        ok = await upload_list(src_list, node, drive=drive, pool=pool, jobs=args.jobs)

    return 0 if ok else 1


@require_authorized
async def action_remove(drive: Drive, args: Namespace) -> int:
    g = (trash_node(drive, _) for _ in args.id_or_path)
    ag = (await _ for _ in as_completed(g))
    rv = [_ async for _ in ag if _ is not None]
    if not rv:
        return 0
    print("trash failed:")
    print_as_yaml(rv)
    return 1


@require_authorized
async def action_rename(drive: Drive, args: Namespace) -> int:
    from wcpan.drive.core.lib import move_node

    async def rename(id_or_path: str, dst: str) -> PurePath:
        node = await get_node_by_id_or_path(drive, id_or_path)
        path = await drive.resolve_path(node)
        node = await move_node(drive, path, PurePath(dst))
        path = await drive.resolve_path(node)
        return path

    node_list = (rename(_, args.destination_path) for _ in args.source_id_or_path)
    await asyncio.gather(*node_list)
    return 0


@require_authorized
async def action_mkdir(drive: Drive, args: Namespace) -> int:
    path = PurePath(args.path)
    parent_path = path.parent
    name = path.name
    parent_node = await drive.get_node_by_path(parent_path)
    await drive.create_directory(name, parent_node, exist_ok=True)
    return 0


async def action_trash(drive: Drive, args: Namespace) -> int:
    node_list = await drive.get_trashed_nodes(args.flatten)
    rv = [
        {
            "id": _.id,
            "name": _.name,
            "modified": str(_.ctime),
        }
        for _ in node_list
    ]
    print_as_yaml(rv)
    return 0


async def action_shell(drive: Drive, args: Namespace) -> int:
    if not args.id_or_path:
        node = await drive.get_root()
    else:
        node = await get_node_by_id_or_path(drive, args.id_or_path)

    if not node or not node.is_directory:
        print(f"{args.id_or_path} is not a folder")
        return 1

    interact(drive, node)
    return 0
