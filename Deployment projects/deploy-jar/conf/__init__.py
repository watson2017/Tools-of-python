# - * - coding: utf-8 - * -

import logbook
import sys
from logbook import Logger, FileHandler, StreamHandler

# 日志文件
logFile = "rk-bd.log"

# 设置UTC时间格式为本地时间格式
logbook.set_datetime_format("local")

# 日志输出到标准输出设备，应用整个程序范围
StreamHandler(
    sys.stdout,
    level=logbook.DEBUG,
    format_string="[{record.time:%Y-%m-%d %H:%M:%S}] {record.level_name}: {record.filename}:{record.lineno} {record.message}",
    encoding="utf-8").push_application()

# 日志输出到文件，应用整个程序范围
FileHandler(
    logFile,
    level=logbook.INFO,
    format_string="[{record.time:%Y-%m-%d %H:%M:%S}] {record.level_name}: {record.filename}:{record.lineno} {record.message}",
    encoding="utf-8",
    bubble=True).push_application()

log = Logger(__name__)
