__author__ = 'Tien'

import os

full_path = os.path.realpath(__file__)
directory = os.path.dirname(full_path)
def list_file(path):
    str_bat = ""
    #print("tiench: " + str(path))
    for f in os.listdir(path):
        if os.path.isfile(path + "/" + f):
            if f.endswith("mp4") and ".480" not in str(f):
                video = str(path + "/" + f).replace(str(directory) + "/", "").replace(".mp4", "")
                if not os.path.exists(video + ".480.mp4"):
                    print("ffmpeg -i " + video + ".mp4 -vcodec libx264 -preset medium -crf 22 -threads 0 -s 852x480 -acodec copy " + video + ".480.mp4")
                    str_bat += "ffmpeg -i " + video + ".mp4 -vcodec libx264 -preset medium -crf 22 -threads 0 -s 852x480 -acodec copy " + video + ".480.mp4 \n"
        elif os.path.isdir(path + "/" + f):
            str_bat += list_file(path + "/" + f)
    return str_bat
bat = list_file(directory)
file_bat = open("convert.bat", "w")
file_bat.write(bat)
file_bat.close()
