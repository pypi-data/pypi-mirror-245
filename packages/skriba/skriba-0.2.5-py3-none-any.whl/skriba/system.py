import logging
import os
import skriba.console


def info(message, markup=False):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")

    logger = skriba.console.get_logger(logger_name=logger_name)
    logger.info(message, extra={"markup": markup})


def debug(message, markup=False):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")

    logger = skriba.console.get_logger(logger_name=logger_name)
    logger.debug(message, extra={"markup": markup})


def warning(message, markup=False):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")

    logger = skriba.console.get_logger(logger_name=logger_name)
    logger.warning(message, extra={"markup": markup})


def critical(message, markup=False):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")

    logger = skriba.console.get_logger(logger_name=logger_name)
    logger.critical(message, extra={"markup": markup})


def error(message, markup=True):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")

    logger = skriba.console.get_logger(logger_name=logger_name)
    logger.error(message, extra={"markup": markup})
