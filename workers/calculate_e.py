from multiprocessing import Event, current_process
import math
import time
from typing import Tuple

from balsa import get_logger, balsa_clone

application_name = __name__

log = get_logger(application_name)


def calculate_e(exit_event: Event, balsa_config: dict = None) -> Tuple[float, int, float]:
    """
    calculate "e"

    :param exit_event: Event that controls when to exit
    :param balsa_config: balsa config dict
    :return: the value of e and the run time
    """

    start = time.time()

    if balsa_config is not None:
        # we're called from process.Pool() so we have to do things that are otherwise in .run()
        balsa = balsa_clone(balsa_config, "calculate_e_process")
        balsa.init_logger()
        current_process().name = 'e_process'

    k = 1.0
    e_value = 0.0
    iteration = 0
    # run a minimum number of times (for required accuracy), and check the exit event every so often
    while iteration < 1000000 or iteration % 1000 != 0 or not exit_event.is_set():
        e_value += 1.0 / k
        k *= iteration + 1
        iteration += 1

    assert math.isclose(e_value, math.e)  # just a check

    duration = time.time() - start

    log.info(f"{e_value=},{iteration=},{duration=}")

    return e_value, iteration, duration
