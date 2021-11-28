
import glob
import soundfile as sf
from datetime import datetime
import ffmpy, os,ffmpeg
for file in glob.glob("data/*.ogg"):
    t1 = datetime.now().timestamp()
    temp_dest = path[:path.rfind('.')] + '_temp.wav'
    dest = path[:path.rfind('.')] + '.wav'
    ff = ffmpy.FFmpeg(executable='C:\ffmpeg\bin\ffmpeg.exe', inputs={path: None}, outputs={temp_dest:None})
    ff.run()
