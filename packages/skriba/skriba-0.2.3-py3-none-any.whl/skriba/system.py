import logging
import os
import skriba.console


def info(message):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")
    if logger_name not in logging.Logger.manager.loggerDict:
        skriba.console.setup_logger(
            logger_name=logger_name,
            log_to_term=True,
            log_to_file=True,
            log_file='LOGGER',
            log_level='DEBUG',
        )

    logger = skriba.console.get_logger(logger_name=logger_name)
    logger.info(message)


def debug(message):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")
    if logger_name not in logging.Logger.manager.loggerDict:
        skriba.console.setup_logger(
            logger_name=logger_name,
            log_to_term=True,
            log_to_file=True,
            log_file='LOGGER',
            log_level='DEBUG',
        )

    logger = skriba.console.get_logger(logger_name=logger_name)
    logger.debug(message)


def warning(message):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")
    if logger_name not in logging.Logger.manager.loggerDict:
        skriba.console.setup_logger(
            logger_name=logger_name,
            log_to_term=True,
            log_to_file=True,
            log_file='LOGGER',
            log_level='DEBUG',
        )

    logger = skriba.console.get_logger(logger_name=logger_name)
    logger.warning(message)


def critical(message):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")
    if logger_name not in logging.Logger.manager.loggerDict:
        skriba.console.setup_logger(
            logger_name=logger_name,
            log_to_term=True,
            log_to_file=True,
            log_file='LOGGER',
            log_level='DEBUG',
        )

    logger = skriba.console.get_logger(logger_name=logger_name)
    logger.critical(message)


def error(message):
    logger_name = os.getenv("SKRIBA_LOGGER_NAME")
    if logger_name not in logging.Logger.manager.loggerDict:
        skriba.console.setup_logger(
            logger_name=logger_name,
            log_to_term=True,
            log_to_file=True,
            log_file='LOGGER',
            log_level='DEBUG',
        )

    logger = skriba.console.get_logger(logger_name=logger_name)
    logger.error(message)
