from multiprocessing import Event, current_process
import math

from balsa import get_logger, balsa_clone

from multiprocessing_talk import application_name

log = get_logger(application_name)


def calculate_e(exit_event: Event, balsa_config: dict = None) -> float:
    """
    calculate "e"

    :param exit_event: Event that controls when to exit
    :param balsa_config: balsa config dict
    :return: the value of e
    """

    if balsa_config is not None:
        # we're called from process.Pool() so we have to do things that are otherwise in .run()
        balsa = balsa_clone(balsa_config, "e_process")
        balsa.init_logger()
        current_process().name = 'e_process'

    k = 1.0
    e_value = 0.0
    iteration = 0
    # check the exit event every so often
    while iteration % 1000 != 0 or not exit_event.is_set():
        e_value += 1.0 / k
        k *= iteration + 1
        iteration += 1

    assert math.isclose(e_value, math.e)  # just a check

    log.info(f"{e_value=}")

    return e_value
