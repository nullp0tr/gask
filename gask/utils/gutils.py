def elapsed_time(start_time, end_time):
    delta_time = end_time - start_time
    days, seconds = divmod(delta_time.total_seconds(), 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return days, hours, int(minutes), int(seconds)


def parse_time(seconds):
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return days, hours, minutes, seconds
