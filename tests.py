import configparser
import math
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
    print(outPath)
    print(outPath.__str__() == os.path.join(outputFolder, "out_file.mp4"))
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


def mathStuff():
    print(4999 / 5)
    print(999 * 5)


def selectEvenly(chunks: int, arrIn) -> []:
    arrCutEnds = arrIn[1:-1]
    partLength = len(arrCutEnds) / (chunks - 1)
    print(arrIn)
    print(arrCutEnds)
    print(partLength, arrCutEnds[round(partLength)])
    selectedIndexAndValues = {0: arrIn[0]}
    for i in range(1, (chunks - 1)):
        indexRounded = math.ceil(i * partLength)
        print(f"i:{i}, indexRaw:{i * partLength}, indexRounded:{indexRounded}, arr_value:{arrIn[indexRounded]}")
        selectedIndexAndValues[indexRounded] = arrIn[indexRounded]

    selectedIndexAndValues[len(arrIn) - 1] = arrIn[-1]
    keys = []
    values = []
    for key, value in selectedIndexAndValues.items():
        keys.append(key)
        values.append(value)
    print(keys)
    print(values)


def numpyTest():
    import numpy
    # arr = numpy.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    arr = numpy.array([10, 30, 16, 18, 24, 18, 30, 30, 21, 7, 15, 14, 24, 27, 14, 16, 30, 12, 18])
    print(arr)
    start = 1
    end = 3
    width = end - start
    res = (arr - arr.min()) / (arr.max() - arr.min()) * width + start
    res.sort()
    print(res)


if __name__ == '__main__':
    fileNameStuff()
