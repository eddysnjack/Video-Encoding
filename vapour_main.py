# Everything missing for macOS install on the documents can be found here:
# https://forum.doom9.org/showthread.php?t=175522
import errno
import os.path
import sys

import vapoursynth
from vapoursynth import core as vpCore, VideoNode as vpClip
import configparser
import subprocess
import shutil
import CustomClipFunctions
import Helper
from pathlib import Path
from view.view import Preview as vpPreview


# =======================================================================
#                               ENCODE PART
# =======================================================================
def updateFunction(currentFrame, totalFrames):
    print(currentFrame, totalFrames)


def startEncoding(clip, outFilePath):
    ffmpeg = shutil.which("ffmpeg")
    # https://trac.ffmpeg.org/wiki/Encode/H.265
    # ffmpeg -i input -c:v libx265 -crf 26 -preset fast -c:a aac -b:a 128k output.mp4
    ffmpeg_cmd = [ffmpeg, "-i", "-",
                  "-c:v", "libx265",
                  "-crf", "23",
                  "-preset", "fast",
                  outFilePath]
    process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=subprocess.STDOUT)
    clip.output(process.stdin, y4m=True, progress_update=updateFunction)

    # # https://forum.videohelp.com/threads/392480-Easy-way-to-encode-vpy-scripts
    # # https://gist.github.com/rlaphoenix/8cc734e08f765490d9cc48f2f3006e22
    # # https://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running
    # # https://stackoverflow.com/questions/18421757/live-output-from-subprocess-command
    # --------
    # universal_newlines parametresi önemli. yoksa ffmpeg güncelleme satırını göremiyoruz.
    # --------
    # universal_newlines = True option doesnt working with "clip.output"
    # will figure this later for output. for now vapoursynth "progress_update" is enough for me.

    # with open("test.log", "w") as log_file:
    #     #     process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE)
    #     #     for command_line_out in iter(lambda: process.stdout.read(1), b""):
    #     #         sys.stdout.buffer.write(command_line_out)
    #     #         log_file.write(command_line_out)
    #     # Start the subprocess with pipes for stdout and stderr
    #     process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)
    #     clip.output(process.stdin, y4m=True)
    #     process.communicate()
    #     # Read and print live output line by line
    #     # for line in process.stdout:
    #     #     print(line, end='')
    #     #     log_file.write(line.encode("utf-8"))
    #     #     log_file.flush()  # Ensure the log is flushed to the file immediately
    #


def getConfig(section=None):
    parser = configparser.ConfigParser()
    parser.read("config.data")
    if section is not None:
        return parser[section]
    return parser


def getClip(filePath) -> vpClip:
    return CustomClipFunctions.selectEverySecondFromEachMinute(filePath, (0, 0, 104, 104))


def mainFunc():
    generalConfig = getConfig("General")
    inputFilePathInstance = Path(generalConfig.get("inputFilePath"))
    outFolderPath = generalConfig.get("outputFolder")
    clip = CustomClipFunctions.getClipLSmash(inputFilePathInstance)
    outFilePath = os.path.join(outFolderPath, "out_file.mp4")
    safeOutFilePath = Helper.getNextNumberedFilePath(Path(outFilePath))
    clip = CustomClipFunctions.printCustomInfoToFrames(clip, 7, inputFilePathInstance.name)
    clip = CustomClipFunctions.splitAndSelect(clip, 20)
    CustomClipFunctions.writeClipToPngFiles(clip, outFolderPath, imageNamePrefix=inputFilePathInstance.name)
    # startEncoding(clip, safeOutFilePath)
    # vpPreview(clip)


if __name__ == '__main__':
    # to get rid of shadowing variable name warnings
    mainFunc()
