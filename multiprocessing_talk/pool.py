import time
from multiprocessing import Pool, context
from multiprocessing.managers import SyncManager
from balsa import Balsa, get_logger
from pathlib import Path

from rich import print

from workers import calculate_e, get_dir_info

from multiprocessing_talk import application_name

log = get_logger(application_name)


def main_pool(balsa: Balsa):

    print("=== main_pool ===")
    start = time.time()

    balsa_config = balsa.config_as_dict()

    # `Event` used with multiprocessing need to come from the SyncManager
    sync_manager = SyncManager()
    sync_manager.start()
    e_exit_event = sync_manager.Event()

    # Pool() takes care of "mapping" processes to number of available processor cores
    with Pool() as pool:

        # run the workers using .apply_async()
        e_process = pool.apply_async(calculate_e, args=(e_exit_event, balsa_config))
        dir_path = Path(Path(".").absolute().anchor, "Program Files", "Python310")
        dir_info_result = pool.apply_async(
            get_dir_info,
            args=(dir_path, balsa_config),
        )

        # get the results while displaying a status message
        result = None
        while result is None:
            try:
                result = dir_info_result.get(timeout=2)
            except context.TimeoutError:
                print(f"waiting on dir_info_result for {time.time() - start} seconds ...")
        print(result)

        e_exit_event.set()  # tell calculate_e to stop
        e_value, e_iterations, e_duration = e_process.get()
        print(f"calculated {e_value=} for {e_iterations:,} iterations in {e_duration} seconds")

    print(f"total time: {time.time() - start} seconds")
    print()
