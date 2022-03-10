import time
from multiprocessing import Pool, context
from multiprocessing.managers import SyncManager
from balsa import Balsa, get_logger
from pathlib import Path

from rich import print

from workers import calculate_e, get_dir_info

from multiprocessing_talk import application_name, author

log = get_logger(application_name)


def main_pool(balsa: Balsa):

    print("=== main_pool ===")
    start = time.time()

    sync_manager = SyncManager()
    sync_manager.start()

    balsa_config = balsa.config_as_dict()

    exit_event = sync_manager.Event()  # event needs to come from the SyncManager
    with Pool() as pool:

        # run the workers using .apply_async()
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

        # get the results
        print(e_result.get())
        r = None
        while r is None:
            try:
                r = dir_info_result.get(timeout=1)
            except context.TimeoutError:
                print(f"waiting on dir_info_result {time.time() - start} ...")
        print(r)

        print(f"total time: {time.time() - start} seconds")
        print()
