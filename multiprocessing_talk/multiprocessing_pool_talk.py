import time
from multiprocessing import Pool
from multiprocessing.managers import SyncManager
from balsa import Balsa, get_logger
from pathlib import Path

from rich import print

from workers import calculate_e, get_dir_info

from multiprocessing_talk import application_name, author

log = get_logger(application_name)


def main_pool():

    sync_manager = SyncManager()
    sync_manager.start()

    balsa = Balsa(
        application_name,
        author,
        log_directory="log",
        delete_existing_log_files=True,
        verbose=True,
    )
    balsa.init_logger()
    balsa_config = balsa.config_as_dict()

    exit_event = sync_manager.Event()
    with Pool() as pool:

        e_result = pool.apply_async(calculate_e, args=(exit_event, balsa_config))

        dir_path = Path(Path(".").absolute().anchor, "Program Files", "Python310")
        dir_info_result = pool.apply_async(
            get_dir_info,
            args=(dir_path, balsa_config),
        )

        # give the user some visual feedback that something is going on
        print('countdown to "e" begins ...')
        for count_down in range(3, -1, -1):
            print(count_down)
            time.sleep(1)
        exit_event.set()

        print(e_result.get())
        print(dir_info_result.get())
