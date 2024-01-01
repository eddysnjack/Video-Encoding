import functools
import os
import vapoursynth as vpSynth

import Helper


def getClipLSmash(filePath, crop: tuple = None) -> vpSynth.VideoNode:
    """
    :param filePath: absoulute file path that will be open
    :param crop: tuple for crop. it should contain integer crop values ordered as left, right, top, bottom
    :return: vapoursynth.VideoNode object
    """
    clip = vpSynth.core.lsmas.LWLibavSource(filePath)
    if crop is not None:
        clip = vpSynth.core.std.Crop(clip, left=crop[0], right=crop[1], top=crop[2], bottom=crop[3])
    return clip


def SelectEverySecondFromEachMinute(filePath, crop: tuple = None) -> vpSynth.VideoNode:
    """
    This function select 1 second long clips from each minute long of chunks from the video file
    and return the combination of those clips.
    it's useful to use CRF mode and get estimation optimum bitrate for a movie.
    :param filePath: absoulute file path that will be open
    :param crop: tuple for crop. it should contain integer crop values ordered as left, right, top, bottom
    :return: vapoursynth.VideoNode object
    """
    clip = vpSynth.core.lsmas.LWLibavSource(filePath)
    clip_fps_rounded = round(getFpsValue(clip))
    minute_long_fps_rounded = round(60 * clip_fps_rounded)
    second_range = [*range(0, int(clip_fps_rounded))]
    # http://www.vapoursynth.com/doc/functions/video/selectevery.html#selectevery
    clip = vpSynth.core.std.SelectEvery(clip=clip, cycle=minute_long_fps_rounded, offsets=second_range, modify_duration=False)
    if crop is not None:
        clip = vpSynth.core.std.Crop(clip, left=crop[0], right=crop[1], top=crop[2], bottom=crop[3])
    return clip


def getFpsValue(clip: vpSynth.VideoNode) -> int:
    """
    https://www.vapoursynth.com/doc/pythonreference.html#VideoNode.fps
    :param clip:
    :return:
    """
    return round(clip.fps.numerator / clip.fps.denominator, 3)


# TIME STAMP STUFF
def ShowTime(clip, font_size=20, x=10, y=10, color="white"):
    """
    Show the current time on the video clip.

    Parameters:
    - clip: Input video clip.
    - font_size: (Waiting to be implemented) Font size for the text (default is 20).
    - x, y: (Waiting to be implemented) Position of the text on the screen (default is (10, 10)).
    - color: (Waiting to be implemented) Text color (default is "white").

    Returns:
    A new video clip with the current time displayed.
    """

    def update_time(n, clip):
        frame = clip.get_frame(n)
        frameTimeLength = frame.props["_DurationNum"] / frame.props["_DurationDen"]
        secondsPassed = n * frameTimeLength
        return vpSynth.core.text.Text(clip[n], Helper.seconds_to_hh_mm_ss_milis(secondsPassed))

    return vpSynth.core.std.FrameEval(clip, functools.partial(update_time, clip=clip))


def writeClipToNull(clip: vpSynth.VideoNode):
    """
    it writes the clip to null. usefull for imwri clip. imwri already defining file properties. we are just requesting frames here.
    :param clip:
    :return: None

    PS: looping over "clip.get_frame(index)" as mentioned here https://forum.doom9.org/showthread.php?p=1885855
        for frame in range(len(clip)):
            clip.get_frame(frame)
    is not requesting frames all the time. this method is more reliable in my experience.
    """
    # https://stackoverflow.com/questions/2929899/cross-platform-dev-null-in-python
    f = open(os.devnull, "wb")
    clip.output(f)


def writeClipToPngFiles(clip, outFolderPath):
    outFilePath = os.path.join(outFolderPath, "image%06d.png")
    clip = vpSynth.core.resize.Bicubic(clip, format=vpSynth.RGB24)
    imageWRIResponse = vpSynth.core.imwri.Write(clip, 'PNG64', str(outFilePath))
    writeClipToNull(imageWRIResponse)


if __name__ == '__main__':
    pass
