import time


def get_format_time(timestamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timestamp)))
