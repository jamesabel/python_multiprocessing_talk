import time
from multiprocessing import Process, Event, Queue
from balsa import Balsa, get_logger, balsa_clone

from rich import print

from workers import calculate_e

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
        log.info(f"{returned_e_value=}")
        self.result.put(returned_e_value)  # return the value in the Queue


def main():

    balsa = Balsa(
        application_name,
        author,
        log_directory="log",
        delete_existing_log_files=True,
        verbose=True,
    )
    balsa.init_logger()

    log.info(f"starting {application_name}")
    worker_process = CalculateE(balsa.config_as_dict())  # pass in log config
    worker_process.start()  # calculates e

    # give the user some visual feedback that something is going on
    print("countdown begins ...")
    for count_down in range(4, -1, -1):
        print(count_down)
        time.sleep(1)

    worker_process.exit_event.set()  # request exit
    worker_process.join()

    e = worker_process.result.get(timeout=1)  # only works once
    print(f"{e=}")
