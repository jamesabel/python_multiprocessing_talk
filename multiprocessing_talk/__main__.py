from pathlib import Path

from balsa import Balsa
from ismain import is_main

from multiprocessing_talk import application_name, author, main_process, main_pool


def main():
    balsa = Balsa(
        application_name,
        author,
        log_directory=Path("multiprocessing_talk", "log"),
        delete_existing_log_files=True,
        verbose=False,  # turn verbose on/off to show logging into stdout
    )
    balsa.init_logger()

    main_process(balsa)
    main_pool(balsa)


if is_main():
    main()
