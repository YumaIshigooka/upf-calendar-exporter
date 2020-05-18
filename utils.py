import html
from datetime import datetime
from os import path

NEWLINE = '\n'


def print_progress_bar(iteration: int, total: int, fill: str = '█') -> None:
    """
    prints a progress bar

    :param iteration: current progress
    :param total: total progress
    :param fill: char to mark filled progress, defaults to █
    """
    filled = iteration
    unfilled = total - filled
    bar = fill * filled + '-' * unfilled
    print('|{}| {}/{}'.format(bar, filled, total))


def print_separator():
    print("**********************************************************************************")


def ask_date(text: str) -> datetime:
    """
    asks for a valid datetime until given one, and returns it

    :param text: question/hint
    :return: datetime object set to time of user input
    """
    dt = None

    valid = False  # while loop controller
    while not valid:
        print(text)
        date_entry = input('date in YYYY-MM-DD format (year in 4 digits, month in 2 digits, day in 2 digits): ')
        try:
            dt = datetime.strptime(date_entry, "%Y-%m-%d")
            print(dt)
            valid = True  # stop asking
        except ValueError:
            print("date is not valid, use correct format")

    return dt


def ask_path() -> str:
    """
    asks for a valid directory path until given one

    :return: path of valid existing directory
    """
    while True:  # ask until return
        path_input = input("directory path: ")

        if path.isdir(path_input):
            return path_input

        print("incorrect path... try again!")


def get_date(date: datetime) -> str:
    return date.strftime('%m/%d/%Y')  # Google Calendar format


def get_time(date: datetime) -> str:
    return date.strftime('%I:%M %p')  # Google Calendar format


def replace_entities(text: str) -> str:
    """
    given a string, replaces all html entities (if any) by standard chars

    :param text: a string
    :return: same string with all html entities replaced by standard chars
    """
    return html.unescape(text)
