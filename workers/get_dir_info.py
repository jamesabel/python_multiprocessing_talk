from pathlib import Path
import os
import hashlib
import time
from dataclasses import dataclass
from multiprocessing import current_process

from balsa import balsa_clone, get_logger

application_name = __name__

log = get_logger(application_name)


@dataclass
class DirInfo:
    dir_path: Path
    file_count: int = 0
    total_size: int = 0
    hash_str: str = None
    duration: float = None


def get_dir_info(directory_path: Path, balsa_config: dict = None) -> DirInfo:
    """
    Get info of a given directory. Also time the execution.
    :param directory_path: get hash of this directory
    :param balsa_config: balsa config dict (use if not part of a Process.run() )
    :return: a tuple of number of files, hash, and duration (in seconds)
    """

    start = time.time()

    if balsa_config is not None:
        # we're called from process.Pool() so we have to do things that are otherwise in .run()
        balsa = balsa_clone(balsa_config, "get_dir_info_process")
        balsa.init_logger()
        current_process().name = 'get_dir_info_process'

    dir_info = DirInfo(directory_path)

    hash_object = hashlib.sha256()
    bucket_size = 4096  # for speed

    sorted_files = [f for f in directory_path.rglob("*") if f.is_file()]
    for file_path in sorted_files:
        with open(file_path, "rb") as f:
            val = f.read(bucket_size)
            while len(val) > 0:
                hash_object.update(val)
                val = f.read(bucket_size)
        dir_info.total_size += os.path.getsize(file_path)

    dir_info.hash_str = hash_object.hexdigest().lower()
    dir_info.file_count = len(sorted_files)

    dir_info.duration = time.time() - start

    log.info(dir_info)

    return dir_info
