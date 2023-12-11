import os
import threading

from utils.base import FileUtil
from utils.log.LogUtilsConfig import *
from utils.log.LogUtilsModels import LogLevel


def format_log(level: LogLevel, tag: str, message: str) -> str:
    """
    格式化日志
    此函数不受日志级别(down_limit_log_level)限制

    :param level:  日志级别
    :param tag: 日志标签
    :param message: 日志主体
    :return: 格式化后的日志内容
    """
    timestamp = TimeUtil.get_current_date_str()
    return f'{timestamp} {os.getpid()}:{threading.get_ident()} {level.tag()}/{tag}: {message}'


def log(level: LogLevel, tag: str, message: str):
    """
    打印日志
    此函数受日志级别(down_limit_log_level)限制

    :param level:  日志级别
    :param tag: 日志标签
    :param message: 日志主体
    :return:
    """
    # 日志级别低于限制级别时写到文件
    log_str = format_log(level, tag, message)

    # 如果目标文件不是文件夹，先删除（后面会创建）
    if not FileUtil.is_file(log_file_path):
        FileUtil.remove(log_file_path)
    # 如果目标文件不存在，创建
    if not FileUtil.exists(log_file_path):
        FileUtil.create_file(log_file_path, True)

    while level.number() >= write_file_down_limit_log_level.number():
        FileUtil.append(f'{log_file_path}', f'{log_str}\n')
    # 日志级别低于限制级别时不打印
    while level.number() >= down_limit_log_level.number():
        print(log_str)
        break


def v(tag: str, message: str):
    log(LogLevel.VERBOSE, tag, message)


def d(tag: str, message: str):
    log(LogLevel.DEBUG, tag, message)


def i(tag: str, message: str):
    log(LogLevel.INFO, tag, message)


def w(tag: str, message: str):
    log(LogLevel.WARN, tag, message)


def e(tag: str, message: str):
    log(LogLevel.ERROR, tag, message)


def f(tag: str, message: str):
    log(LogLevel.FATAL, tag, message)


if __name__ == '__main__':
    print(format_log(LogLevel.INFO, 'test_tag', 'test_message'))
