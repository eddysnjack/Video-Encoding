from vapoursynth import core as vpCore, VideoNode as vpClip


def SelectEverySecondFromEachMinute(filePath) -> vpClip:
    """
    This function select 1 second long clips from each minute long of chunks from the video file
    and return the combination of those clips.
    it's useful to use CRF mode and get estimation optimum bitrate for a movie.
    :param filePath: absoulute file path that will be open
    :return: vapoursynth.VideoNode object
    """
    clip = vpCore.lsmas.LWLibavSource(filePath)
    clip_fps_rounded = round(getFpsValue(clip))
    minute_long_fps_rounded = round(60 * clip_fps_rounded)
    second_range = [*range(0, int(clip_fps_rounded))]
    # http://www.vapoursynth.com/doc/functions/video/selectevery.html#selectevery
    clip = vpCore.std.SelectEvery(clip=clip, cycle=minute_long_fps_rounded, offsets=second_range, modify_duration=False)
    # clip.set_output() #VSEdit needs this, otherwise it would not run
    return clip


def getFpsValue(clip: vpClip) -> int:
    """
    https://www.vapoursynth.com/doc/pythonreference.html#VideoNode.fps
    :param clip:
    :return:
    """
    return round(clip.fps.numerator / clip.fps.denominator, 3)


if __name__ == '__main__':
    pass
