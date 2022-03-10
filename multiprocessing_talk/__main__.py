from ismain import is_main
from multiprocessing_talk import main_process, main_pool

from balsa import Balsa

from multiprocessing_talk import application_name, author


def main():
    balsa = Balsa(
        application_name,
        author,
        log_directory="log",
        delete_existing_log_files=True,
        verbose=False,  # turn verbose on/off to show logging into stdout
    )
    balsa.init_logger()

    main_process(balsa)
    main_pool(balsa)


if is_main():
    main()
