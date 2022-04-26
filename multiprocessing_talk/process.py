import time
from multiprocessing import Process, Event, SimpleQueue
from balsa import Balsa, get_logger, balsa_clone
from pathlib import Path
from typing import Tuple, Union

from rich import print

from workers import calculate_e, get_dir_info, DirInfo

from multiprocessing_talk import application_name

log = get_logger(application_name)


class CalculateE(Process):
    def __init__(self, logging_config: dict):

        self.logging_config = logging_config

        self._result_queue = SimpleQueue()  # must use a multiprocessing mechanism to return the result
        self._result = None  # type: Union[Tuple[float, int, float], None]
        self.exit_event = Event()

        # it's recommended to name the process
        super().__init__(name="calculate_e_process")

    def run(self):

        balsa_log = balsa_clone(self.logging_config, self.name)  # must be in .run()
        balsa_log.init_logger()

        returned_e_value = calculate_e(self.exit_event)
        log.info("done calculating e!")
        self._result_queue.put(returned_e_value)  # return the value in the Queue

    def get(self) -> Tuple[float, int, float]:
        # get the value of the computation (with typing)
        if self._result is None:
            self._result = self._result_queue.get()  # will block until done
        return self._result


class GetDirInfo(Process):
    def __init__(self, dir_path: Path, logging_config: dict):

        self.dir_path = dir_path
        self.logging_config = logging_config

        self._result_queue = SimpleQueue()  # must use a multiprocessing mechanism to return the result
        self._result = None  # type: Union[DirInfo, None]

        # naming the process is recommended
        super().__init__(name="get_dir_info_process")

    def run(self):

        balsa_log = balsa_clone(self.logging_config, self.name)  # must be in .run()
        balsa_log.init_logger()

        dir_info = get_dir_info(self.dir_path)
        log.info(f"got info from {dir_info.file_count} files!")
        self._result_queue.put(dir_info)  # return the value in the Queue

    def get(self) -> DirInfo:
        # get the value of the computation (with typing)
        if self._result is None:
            self._result = self._result_queue.get()  # will block until done
        return self._result


def main_process(balsa: Balsa):

    print("=== main_process ===")
    start = time.time()

    balsa_config = balsa.config_as_dict()

    # create and start worker processes
    log.info(f"starting {application_name}")
    e_process = CalculateE(balsa_config)  # pass in log config
    e_process.start()  # calculates e

    dir_path = Path(Path(".").absolute().anchor, "Program Files", "Python310")  # just point to some large set of files

    if dir_path.exists():
        dir_info_process = GetDirInfo(dir_path, balsa_config)
        dir_info_process.start()

        # request exit from "e" process and wait for dir info
        while dir_info_process.is_alive():
            dir_info_process.join(2)
            print(f"waiting on dir_info_result for {time.time() - start} seconds ...")

        # get the results
        print(dir_info_process.get())
        e_process.exit_event.set()
        e_value, e_iterations, e_duration = e_process.get()
        print(f"calculated {e_value=} for {e_iterations:,} iterations in {e_duration} seconds")
    else:
        print(f'{dir_path} does not exist - please modify "dir_path" this example to point to a valid directory')

    print(f"total time: {time.time() - start} seconds")
    print()
