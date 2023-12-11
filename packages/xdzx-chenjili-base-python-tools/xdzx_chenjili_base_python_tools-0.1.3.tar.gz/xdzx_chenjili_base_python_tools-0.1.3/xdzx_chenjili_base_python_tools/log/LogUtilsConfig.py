from utils.base import TimeUtil
from utils.log.LogUtilsModels import LogLevel

# 最低打印日志的级别
down_limit_log_level = LogLevel.VERBOSE
# 最低写入文件的日志级别
write_file_down_limit_log_level = LogLevel.INFO
# 日志文件存放目录
log_file_path = f'./files/log/{TimeUtil.get_current_date_str()}'
