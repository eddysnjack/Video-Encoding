import os

import vapoursynth as vs
import functools

from datetime import timedelta


def seconds_to_hh_mm_ss_milis(time_in_seconds):
    # Convert seconds to timedelta
    duration = timedelta(seconds=time_in_seconds)  # gördüğüm en akla mantığa aykırı time classı bu olabilir.

    # Extract hours, minutes, and seconds
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milis = round(duration.microseconds / 1000)

    # Format as "HH:MM:SS"
    formatted_time = "{:02}:{:02}:{:02}.{:03}".format(hours, minutes, seconds, milis)

    return formatted_time


def ShowTime(clip, font_size=20, x=10, y=10, color="white"):
    """
    Show the current time on the video clip.

    Parameters:
    - clip: Input video clip.
    - font_size: Font size for the text (default is 20).
    - x, y: Position of the text on the screen (default is (10, 10)).
    - color: Text color (default is "white").

    Returns:
    A new video clip with the current time displayed.
    """

    def update_time(n, clip):
        print(n, clip.get_frame(n).props)
        frame = clip.get_frame(n)
        frameTimeLength = frame.props["_DurationNum"] / frame.props["_DurationDen"]
        secondsPassed = n * frameTimeLength
        return vs.core.text.Text(clip[n], seconds_to_hh_mm_ss_milis(secondsPassed))

    return vs.core.std.FrameEval(clip, functools.partial(update_time, clip=base_clip))


def writeClipToNull(clip: vs.VideoNode):
    """
    it writes the clip to null. usefull for imwri clip. imwri already defining file properties we are just requesting frames here.
    :param clip:
    :return: None
    """
    # https://stackoverflow.com/questions/2929899/cross-platform-dev-null-in-python
    f = open(os.devnull, "wb")
    clip.output(f)


vs_core = vs.core
base_clip = vs_core.std.BlankClip(format=vs.YUV420P8, length=200, color=[255, 128, 128])
clip = base_clip

# Add current time to each frame
clip_with_time = ShowTime(clip)
# writeClipToNull(clip_with_time)

#
# for index in range(0, len(clip)):
#     frame = clip.get_frame(index)
#     frameTimeLength = frame.props["_DurationNum"] / frame.props["_DurationDen"]
#     secondsPassed = index * frameTimeLength
#
#     print(seconds_to_hh_mm_ss(secondsPassed))


# Display the clip with current time
clip_with_time.set_output()
