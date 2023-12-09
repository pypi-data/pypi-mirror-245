import inspect
import os
import skriba.console

PREVIOUS_FUNCTION = 1


def info(message, markup=False, verbose=False):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")

    logger = skriba.console.get_logger(logger_name=logger_name)
    logger.info(message, extra={"markup": markup})


def debug(message, markup=False, verbose=False):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")

    function_name = inspect.stack()[PREVIOUS_FUNCTION].function
    if verbose:
        message = (
            "[ [blue]{function_name}[/] ]: {message}".format(
                function_name=function_name,
                message=message
            ))

    logger = skriba.console.get_logger(logger_name=logger_name)
    logger.debug(message, extra={"markup": markup})


def warning(message, markup=False, verbose=False):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")

    logger = skriba.console.get_logger(logger_name=logger_name)
    logger.warning(message, extra={"markup": markup})


def critical(message, markup=False, verbose=False):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")

    logger = skriba.console.get_logger(logger_name=logger_name)
    logger.critical(message, extra={"markup": markup})


def error(message, markup=True, verbose=False):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")

    logger = skriba.console.get_logger(logger_name=logger_name)
    logger.error(message, extra={"markup": markup})
