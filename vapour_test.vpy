from vapoursynth import core
video = core.lsmas.LWLibavSource(r'/Users/eddy/Downloads/Torrents/İllegal Hayatlar (2023) 1080p NF WEB-DL [TR] DDP5.1 H.264-TURG.mkv')
clip_fps = 23.976
minute_long_fps = 60*clip_fps
second_range = [*range(0,int(clip_fps))]
video = core.std.SelectEvery(clip=video, cycle=minute_long_fps, offsets=second_range)
#video = core.text.FrameProps(video)
video.set_output()