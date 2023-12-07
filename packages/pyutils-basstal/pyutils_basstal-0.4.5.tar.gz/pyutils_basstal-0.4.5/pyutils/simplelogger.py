# ruff: noqa: E501

import os
import logging
import pyutils.shorthand as shd
import sys
import re
from colorama import Fore, Style

######################
######################
#       Log          #
######################
######################

ErrorRaiseExcpetion = False

if sys.version_info >= (3, 9):
    logging.basicConfig(level=logging.INFO, datefmt='%y-%m-%d %H:%M:%S', format='%(message)s', encoding='utf-8')
else:
    logging.basicConfig(level=logging.INFO, datefmt='%y-%m-%d %H:%M:%S', format='%(message)s')


class SimpleLogger(object):
    # 这是原来的 error/warning logger
    _logger = logging.getLogger("error_logger")
    _logger.setLevel(logging.ERROR)
    _logger.handlers.clear()
    _logger.addHandler(logging.StreamHandler(sys.stderr))
    _logger.propagate = False
    # 创建 info logger
    _info_logger = logging.getLogger("info_logger")
    _info_logger.setLevel(logging.INFO)
    _info_logger.handlers.clear()
    _info_logger.addHandler(logging.StreamHandler(sys.stdout))
    _info_logger.propagate = False

    __hanlder_cache = {}

    @staticmethod
    def _color_message(message, color_code, bold=False):
        os.system('')
        # Map color_code to actual color
        color_map = {
            '31': Fore.RED,
            '32': Fore.GREEN,
            '33': Fore.YELLOW,
            '34': Fore.BLUE,
            '35': Fore.MAGENTA,
            '36': Fore.CYAN,
            '37': Fore.WHITE
        }
        # jenkins 无法识别 Fore.RESET，这里将 Fore.RESET 替换为 ''
        color = color_map.get(str(color_code), '')

        if bold:
            return f'{Style.BRIGHT}{color}{message}{Style.RESET_ALL}'
        else:
            return f'{color}{message}{Style.RESET_ALL}'

    @staticmethod
    def _preprocess_message(message: str):
        if not shd.is_win():
            message = message.replace('=>', '➜').replace('<=', '✔')

        return message.rstrip('\r\n')

    @staticmethod
    def info(message, bold=False, color_code=None):
        message = SimpleLogger._preprocess_message(message)
        if color_code is not None or bold is not False:
            message = SimpleLogger._color_message(message, color_code, bold)
        SimpleLogger._info_logger.info(message)

    @staticmethod
    def warning(message, bold=False):
        message = SimpleLogger._preprocess_message(message)
        message = SimpleLogger._color_message(message, 33, bold)
        SimpleLogger._info_logger.warning(message)

    @staticmethod
    def error(message, bold=False):
        if ErrorRaiseExcpetion:
            raise Exception(message)
        message = SimpleLogger._preprocess_message(message)
        message = SimpleLogger._color_message(message, 31, bold)
        SimpleLogger._logger.error(message)

    @staticmethod
    def addFileHandler(file_path):
        if file_path in SimpleLogger.__hanlder_cache:
            return
        file_handler = logging.FileHandler(file_path, encoding='utf-8')

        class NoEscapeSeqFormatter(logging.Formatter):
            _ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')

            def format(self, record):
                record.msg = self._ansi_escape.sub('', record.getMessage())
                return super().format(record)

        file_handler.setFormatter(NoEscapeSeqFormatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S'))
        SimpleLogger.__hanlder_cache[file_path] = file_handler
        SimpleLogger._logger.addHandler(file_handler)
        SimpleLogger._info_logger.addHandler(file_handler)

    @staticmethod
    def removeFileHander(file_path):
        SimpleLogger.removeFileHandler(file_path)

    @staticmethod
    def removeFileHandler(file_path):
        if file_path in SimpleLogger.__hanlder_cache:
            return
        file_handler = SimpleLogger.__hanlder_cache[file_path]
        SimpleLogger._logger.removeHandler(file_handler)
        SimpleLogger._info_logger.removeHandler(file_handler)
        file_handler.close()
        del SimpleLogger.__hanlder_cache[file_path]


logger = SimpleLogger._logger


def info(message, bold=False, color_code=None):
    SimpleLogger.info(str(message), bold, color_code)


def warning(message, bold=False):
    SimpleLogger.warning(str(message), bold)


def error(message, bold=False):
    SimpleLogger.error(str(message), bold)


def __hook__dispatch(assertion, original_func):
    class Restore:
        def __enter__(self):
            def real_hook_func(message, *args):
                """NOTE:ignore any parameters after 'message'

                Args:
                    message (_type_): _description_
                """
                assertion(message)
                original_func(message, *args)
            self.hook_func = real_hook_func
            if original_func == SimpleLogger.warning:
                SimpleLogger.warning = real_hook_func
            elif original_func == SimpleLogger.info:
                SimpleLogger.info = real_hook_func
            elif original_func == SimpleLogger.error:
                SimpleLogger.error = real_hook_func

        def __exit__(self, exception_type, exception_value, traceback):
            if self.hook_func == SimpleLogger.warning:
                SimpleLogger.warning = original_func
            elif self.hook_func == SimpleLogger.info:
                SimpleLogger.info = original_func
            elif self.hook_func == SimpleLogger.error:
                SimpleLogger.error = original_func
    return Restore()


def hook_info(assertion):
    """给 logger.info 加钩子以检测 info 信息是否符合预期"""
    return __hook__dispatch(assertion, SimpleLogger.info)


def hook_warning(assertion):
    """给 logger.warning 加钩子以检测 warning 信息是否符合预期

    Args:
        assertion (func(str)->None): 钩子函数

    Returns:
        class Restore: Restore class that can be used in with statement
    """
    return __hook__dispatch(assertion, SimpleLogger.warning)


def hook_error(assertion):
    """给 logger.error 加钩子

    Args:
        assertion (func(str)->None): 钩子函数

    Returns:
        class Restore: Restore class that can be used in with statement
    """
    return __hook__dispatch(assertion, SimpleLogger.error)
