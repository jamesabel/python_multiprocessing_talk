from pathlib import Path
import os
import hashlib
import time
from typing import Tuple


def get_dir_info(directory_path: Path) -> Tuple[int, int, str, float]:
    """
    Get info of a given directory. Also time the execution.
    :param directory_path: get hash of this directory
    :return: a tuple of number of files, hash, and duration (in seconds)
    """

    start = time.time()

    hash_object = hashlib.sha256()
    bucket_size = 4096  # for speed

    sorted_files = [f for f in directory_path.rglob("*") if f.is_file()]
    total_size = 0
    for file_path in sorted_files:
        with open(file_path, "rb") as f:
            val = f.read(bucket_size)
            while len(val) > 0:
                hash_object.update(val)
                val = f.read(bucket_size)
        total_size += os.path.getsize(file_path)

    hash_str = hash_object.hexdigest().lower()

    duration = time.time() - start

    return len(sorted_files), total_size, hash_str, duration
