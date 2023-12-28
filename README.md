# Video-Encoding

Video Encoding Scripts I use time to time.

## VapourSynth

Everything missing for macOS install on the documents can be found here:
https://forum.doom9.org/showthread.php?t=175522

### My Installation Journey

-----------
I'm familiar with avisynth but since It's hard to work with on macOS and I was curious about vapoursynth I decided to use vapoursynth.
First thing i did was to read the vapoursynt documentation. i installed xcode and instal via brew but I couldnt install the wrapper. itried
`pip install vapoursynth` and it give me an error about clang and wheel build. I'm guessing it was trying to compile the C source, which I did download and check the error line
but it was gibberish to me. That turns out to be a dead end. Then I try to search differently, luckliy I came accross to doom9 forum. which helped me a lot.
Even though I know doom9 it didnt came my mind to chech there. Then I follow the instructions from the op guy and also the guide in his website(https://www.l33tmeatwad.com/vapoursynth101)
(Wirdly enough I cant remember how I found the website...anyway), I install the vapoursynth.pkg, I download the lsmash plugin.

as op mentioned vapoursynth.pkg had its own python instance.
> INFO: To access the python environment for the VapourSynth.framework just run vspython in terminal.

so i try to find it via:
`where vspython`
which turn out to be in `/usr/local/bin/vspython`   
For pycharm i change the interpereter to python instance in that directory and it worked.
I also installed VapourSynth Editor, which is really nice.

**PS**:
I have to remove brew installation since it was causing confusion for vspipe command.
there was two vspipe locations in the path and I want to use the one in `/usr/local/bin` instead of the one in `/opt/homebrew/bin`

#### Encoding

-----------
I was looking for a way to simply encode the script. ffmpeg was already installed in my system and seems like with vspipe it is possible to pass
frames into x265 or ffmpeg executables via pipeline. But I dont like to write long commands on terminal i just want to do with python. Simple search give me an idea to how can i pass vapoursynth frames to the subprocess created in python.
That's nice for now. Handling output of ffmpeg or x265 is little bit confusing RN but i think we can figure out that later.