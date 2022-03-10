import time
from multiprocessing import Process, Event, Queue
from balsa import Balsa, get_logger, balsa_clone
from pathlib import Path

from rich import print

from workers import calculate_e, get_dir_info

from multiprocessing_talk import application_name, author

log = get_logger(application_name)


class CalculateE(Process):
    def __init__(self, logging_config: dict):

        self.logging_config = logging_config

        # can not merely return the result in .run() as a class variable
        self.result = Queue()
        self.exit_event = Event()

        # it's recommended to name the process
        super().__init__(name="calculate_e_process")

    def run(self):

        balsa_log = balsa_clone(self.logging_config, self.name)  # must be in .run()
        balsa_log.init_logger()

        returned_e_value = calculate_e(self.exit_event)
        log.info("done calculating e!")
        self.result.put(returned_e_value)  # return the value in the Queue


class GetDirInfo(Process):
    def __init__(self, dir_path: Path, logging_config: dict):

        self.dir_path = dir_path
        self.logging_config = logging_config

        # can not merely return the result in .run() as a class variable
        self.result = Queue()

        # it's recommended to name the process
        super().__init__(name="get_dir_info_process")

    def run(self):

        balsa_log = balsa_clone(self.logging_config, self.name)  # must be in .run()
        balsa_log.init_logger()

        dir_info = get_dir_info(self.dir_path)
        log.info(f"got info from {dir_info.file_count} files!")
        self.result.put(dir_info)  # return the value in the Queue


def main():

    balsa = Balsa(
        application_name,
        author,
        log_directory="log",
        delete_existing_log_files=True,
        verbose=True,
    )
    balsa.init_logger()
    balsa_config = balsa.config_as_dict()

    log.info(f"starting {application_name}")
    e_process = CalculateE(balsa_config)  # pass in log config
    e_process.start()  # calculates e

    program_files = Path(Path(".").absolute().anchor, "Program Files")
    dir_info_process = GetDirInfo(Path(program_files, "Python310"), balsa_config)
    dir_info_process.start()

    # give the user some visual feedback that something is going on
    print('countdown to "e" begins ...')
    for count_down in range(4, -1, -1):
        print(count_down)
        time.sleep(1)

    e_process.exit_event.set()  # request exit
    e_process.join()
    e = e_process.result.get(timeout=1)  # only works once
    print(f"{e=}")

    while dir_info_process.is_alive():
        print(f"waiting on {dir_info_process.name} ...")
        dir_info_process.join(3)
    dir_info = dir_info_process.result.get()
    print(f"{dir_info=}")
