import random
import getpass
import platform


def create_logger():
    logger = None  # future logging core
    session = random.randint(10 ** 14, 10 ** 15)
    return logger, session


def logging(time, type_message, message):
    print(f'time: {str(time)[:-3]}; '
          f'session: id{SESSION}; '
          f'type: {type_message}; '
          f'platform: {platform.platform()}; '
          f'user: {getpass.getuser()}; '
          f'message: {message}')


LOGGER, SESSION = create_logger()
