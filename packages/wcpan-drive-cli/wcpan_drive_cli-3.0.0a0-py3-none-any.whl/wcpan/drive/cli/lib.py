import mimetypes
from pathlib import Path

from wcpan.drive.core.types import Node, MediaInfo, Drive

from ._lib import get_image_info, get_video_info


async def get_media_info(local_path: Path) -> MediaInfo | None:
    type_, _ext = mimetypes.guess_type(local_path)
    if not type_:
        return None

    if type_.startswith("image/"):
        return get_image_info(local_path)

    if type_.startswith("video/"):
        return await get_video_info(local_path)

    return None


async def get_usage(drive: Drive, node: Node) -> int:
    if not node.is_directory:
        return node.size

    rv = 0
    async for _root, _folders, files in drive.walk(node):
        rv += sum((_.size for _ in files))

    return rv
