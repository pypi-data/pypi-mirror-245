


# 声明区域
from enum import Enum


class LogLevel(Enum):
    """
    日志级别
    """
    VERBOSE = 0, 'V'
    DEBUG = 1, 'D'
    INFO = 2, 'I'
    WARN = 3, 'W'
    ERROR = 4, 'E'
    FATAL = 5, 'F'

    def __str__(self):
        return self.name

    def number(self) -> int:
        return self.value[0]

    def tag(self) -> str:
        return self.value[1]