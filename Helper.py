import os.path
from datetime import timedelta
from pathlib import Path


# ---------------------------------------------
#                FILES and PATHS
# ---------------------------------------------
def getNextNumberedFilePath(filePath: Path):
    """
    https://stackoverflow.com/questions/339007/how-do-i-pad-a-string-with-zeroes
    :param filePath:
    :return: first non-existent file name that 4 digit, zero padded number appended
    """
    currentFilePath: Path = filePath
    originFileName = currentFilePath.stem
    originSuffix = currentFilePath.suffix
    originParent = currentFilePath.parent
    counter = 0
    while checkIfExist(currentFilePath):
        counter += 1
        newFileName = f"{originFileName}{counter:04}{originSuffix}"
        currentFilePath = Path(originParent).joinpath(newFileName)
    return currentFilePath


def checkIfExist(filePath):
    return os.path.exists(filePath)


# ---------------------------------------------
#                TIME
# ---------------------------------------------
def seconds_to_hh_mm_ss_milis(time_in_seconds):
    # Convert seconds to timedelta
    # gördüğüm en akla mantığa aykırı time classı bu olabilir.
    # https://ioflood.com/blog/python-timedelta/
    duration = timedelta(seconds=time_in_seconds)

    # Extract hours, minutes, and seconds
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milis = round(duration.microseconds / 1000)

    # Format as "HH:MM:SS"
    formatted_time = "{:02}:{:02}:{:02}.{:03}".format(hours, minutes, seconds, milis)

    return formatted_time
