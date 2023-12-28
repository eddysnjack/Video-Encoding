# Everything missing for macOS install on the documents can be found here:
# https://forum.doom9.org/showthread.php?t=175522
import os.path
from vapoursynth import core
import configparser
import subprocess
import shutil


# =======================================================================
#                       ENCODE PART
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
    process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    clip.output(process.stdin, y4m=True, progress_update=updateFunction)
    process.communicate()

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


def getClip(filePath):
    clip = core.lsmas.LWLibavSource(filePath)
    clip_fps = 23.976
    minute_long_fps = 60 * clip_fps
    second_range = [*range(0, int(clip_fps))]
    # http://www.vapoursynth.com/doc/functions/video/selectevery.html#selectevery
    clip = core.std.SelectEvery(clip=clip, cycle=minute_long_fps, offsets=second_range, modify_duration=False)
    # clip.set_output() #VSEdit needs this, otherwise it would not run
    return clip


def mainFunc():
    generalConfig = getConfig("General")
    inputFilePath = generalConfig.get("inputFilePath")
    clip = getClip(inputFilePath)
    startEncoding(clip, os.path.join(generalConfig.get("outputFolder"), "out_file.mp4"))


if __name__ == '__main__':
    # to get rid of shadowing variable name warnings
    mainFunc()
