import configparser
import os.path
from pathlib import Path

import CustomClipFunctions


def writeConfigSection(section: str):
    parser = configparser.ConfigParser()
    parser.read("config.data")
    print(dict(parser[section].items()))


def fileNameStuff():
    inputFilePath = "/Users/eddy/Downloads/test_input_file.mkv"
    outputFolder = "OutputFolder/"
    outPath = Path(os.path.join(outputFolder, "out_file.mp4"))
    print(outPath.name)
    print(outPath.stem)
    print(outPath.suffix)
    print(getNextNumberedFilePath(outPath))


def getNextNumberedFilePath(filePath: Path):
    """
    https://stackoverflow.com/questions/339007/how-do-i-pad-a-string-with-zeroes
    :param filePath:
    :return: first non-existent file name that 4 digit, zero padded number appended
    """
    currentFilePath: Path = filePath
    counter = 0
    while (checkIfExist(currentFilePath)):
        newFileName = f"{currentFilePath.stem}{counter:04}{currentFilePath.suffix}"
        currentFilePath = Path(currentFilePath.parent).joinpath(newFileName)
    return currentFilePath


def checkIfExist(filePath):
    return os.path.exists(filePath)


def dateTimeTest():
    from datetime import timedelta

    def seconds_to_hh_mm_ss(seconds):
        # Convert seconds to timedelta
        duration = timedelta(seconds=seconds)

        # Extract hours, minutes, and seconds
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Format as "HH:MM:SS"
        formatted_time = "{:02}:{:02}:{:02}".format(hours, minutes, seconds)

        return formatted_time

    # Example usage:
    duration_in_seconds = 145  # Change this to your actual duration
    formatted_time = seconds_to_hh_mm_ss(duration_in_seconds)
    print(formatted_time)


if __name__ == '__main__':
    dateTimeTest()
