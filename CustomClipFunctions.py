import functools
import math
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


def splitAndSelect(clip: vpSynth.VideoNode, chunkCount: int) -> vpSynth.VideoNode:
    if len(clip) < chunkCount:
        return clip
    indexes = Helper.selectEvenly(chunkCount, len(clip))
    resultClip: vpSynth.VideoNode = None
    for i in range(0, len(indexes)):
        if resultClip is not None:
            resultClip += clip[indexes[i]]
        else:
            resultClip = clip[indexes[i]]
    return resultClip


def selectEverySecondFromEachMinute(filePath, crop: tuple = None) -> vpSynth.VideoNode:
    """
    This function select 1 second long clips from each minute long of chunks from the video file
    and return the combination of those clips.
    it's useful to use CRF mode and get estimation optimum bitrate for a movie.
    :param filePath: absoulute file path that will be open
    :param crop: tuple for crop. it should contain integer crop values ordered as left, right, top, bottom
    :return: vapoursynth.VideoNode object
    """
    clip = vpSynth.core.lsmas.LWLibavSource(filePath)
    clip_fps_rounded = round(getFpsValueUpTo3DecimalPoint(clip))
    minute_long_fps_rounded = round(60 * clip_fps_rounded)
    one_second_range = [*range(0, int(clip_fps_rounded))]
    # http://www.vapoursynth.com/doc/functions/video/selectevery.html#selectevery
    clip = vpSynth.core.std.SelectEvery(clip=clip, cycle=minute_long_fps_rounded, offsets=one_second_range, modify_duration=False)
    if crop is not None:
        clip = vpSynth.core.std.Crop(clip, left=crop[0], right=crop[1], top=crop[2], bottom=crop[3])
    return clip


def getFpsValueUpTo3DecimalPoint(clip: vpSynth.VideoNode) -> int:
    """
    https://www.vapoursynth.com/doc/pythonreference.html#VideoNode.fps
    :param clip:
    :return:
    """
    return round(clip.fps.numerator / clip.fps.denominator, 3)


# TIME STAMP STUFF
def showTime(clip, font_size=20, x=10, y=10, color="white", alignMent=7):
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

    def update_time(n, inner_clip, inner_alignment):
        frame = inner_clip.get_frame(n)
        frameTimeLength = frame.props["_DurationNum"] / frame.props["_DurationDen"]
        secondsPassed = n * frameTimeLength
        return vpSynth.core.text.Text(inner_clip[n], Helper.seconds_to_hh_mm_ss_milis(secondsPassed), alignment=inner_alignment)

    return vpSynth.core.std.FrameEval(clip, functools.partial(update_time, inner_clip=clip, inner_alignment=alignMent))


def showFrameNumb(clip: vpSynth.VideoNode, alignMent=7):
    def updateFrame(n, inner_clip, inner_alignment):
        return vpSynth.core.text.Text(inner_clip[n], n, alignment=inner_alignment)

    return vpSynth.core.std.FrameEval(clip, functools.partial(updateFrame, inner_clip=clip, inner_alignment=alignMent))


def printTimeAndFrameNumber(clip: vpSynth.VideoNode, alignment=7, customClipName=""):
    def updateFrame(n, inner_clip, inner_alignment, inner_customClipName):
        frame = inner_clip.get_frame(n)
        frameTimeLength = frame.props["_DurationNum"] / frame.props["_DurationDen"]
        secondsPassed = n * frameTimeLength
        timeStamp = Helper.seconds_to_hh_mm_ss_milis(secondsPassed)
        frameLabel = f"{timeStamp}\n{n}" if inner_customClipName == "" else f"{inner_customClipName}\n{timeStamp}\n{n}"
        return vpSynth.core.text.Text(inner_clip[n], frameLabel, alignment=inner_alignment)

    return vpSynth.core.std.FrameEval(clip, functools.partial(updateFrame, inner_clip=clip, inner_alignment=alignment, inner_customClipName=customClipName))


def printCustomInfoToFrames(clip: vpSynth.VideoNode, alignment=7, customClipName=""):
    def updateFrame(n, inner_clip, inner_alignment, inner_customClipName):
        frame = inner_clip.get_frame(n)
        frameTimeLength = frame.props["_DurationNum"] / frame.props["_DurationDen"]
        secondsPassed = n * frameTimeLength
        timeStamp = Helper.seconds_to_hh_mm_ss_milis(secondsPassed)
        frameLabel = prettyPrintInfo(timeStamp, n, f"{frame.width}x{frame.height}", inner_customClipName)
        return vpSynth.core.text.Text(inner_clip[n], frameLabel, alignment=inner_alignment)

    return vpSynth.core.std.FrameEval(clip, functools.partial(updateFrame, inner_clip=clip, inner_alignment=alignment, inner_customClipName=customClipName))


def prettyPrintInfo(timeStamp: str, frameCount: int, resolution: str, fileName: str = ""):
    frameLabel = "-"
    if fileName == "":
        frameLabel = f"{timeStamp}\n{resolution}\n{frameCount}"
    else:
        frameLabel = f"{fileName}\n{resolution}\n{timeStamp}\n{frameCount}"
    return frameLabel


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


def writeClipToPngFiles(clip: vpSynth.VideoNode, outFolderPath, imageNamePrefix="image"):
    outFilePath = os.path.join(outFolderPath, f"{imageNamePrefix}%06d.png")
    # https://www.vapoursynth.com/doc/functions/video/resize.html
    # bkz: Resize error 3074: no path between colorspaces (2/2/2 => 1/1/1). May need to specify additional colorspace parameters.
    # matrix bilgisi ise frame içerisindeymiş. kodu incelemem gerekti.
    # https://github.com/vapoursynth/vapoursynth/blob/9a489169f8c77b5c2b30733794beac9bf3274c25/src/core/textfilter.cpp#L552
    # https://www.vapoursynth.com/doc/apireference.html#reserved-frame-properties
    if clip.get_frame(0).props["_Matrix"] == vpSynth.MATRIX_UNSPECIFIED:
        clip = vpSynth.core.resize.Bicubic(clip, format=vpSynth.RGB24, matrix_in=vpSynth.MATRIX_BT709)
    else:
        clip = vpSynth.core.resize.Bicubic(clip, format=vpSynth.RGB24)
    imageWRIResponse = vpSynth.core.imwri.Write(clip, 'PNG64', str(outFilePath))
    writeClipToNull(imageWRIResponse)


if __name__ == '__main__':
    pass
