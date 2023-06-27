import os
import os.path
import io
import subprocess
import logging

dir = "/sda/res"  # 你的视频文件所在目录
rtmp = "?streamname=live_11001546_4006607&key=xxxxxxxx&schedule=rtmp&pflag=1"  # 填你的串流密钥
fps = "25"  # 默认即可
start_time = "00:01:30"  # 填你的跳过片头时间
duration_time = "00:43:30"  # 填你的视频持续时间长


# 下面方法是查询你的视频目录下的所有视频文件
def listDir(dirTemp):
    nameList = []
    if not os.path.exists(dirTemp):
        print("file or directory doesn't exist")
        return
    fileList = os.listdir(dirTemp)
    for fileName in fileList:
        absPath = os.path.join(dirTemp, fileName)
        if os.path.isfile(absPath):
            nameList.append(absPath)
    return nameList


def getfilename(file):
    tmpint = file.rfind('/')
    filename = file[tmpint + 1:]
    return filename


def main():
    logging.basicConfig(filename='playback.log', level=logging.INFO, format='%(asctime)s - %(message)s')
    nameList = listDir(dir)
    nameList.sort()
    while True:
        for file in nameList:
            filename = os.path.basename(file)
            logging.info("当前播放的是：" + filename)
            command = 'ffmpeg -re -ss "' + start_time + '" -to "' + duration_time + '" -i "' + file + '" -vcodec copy -acodec copy   -b:a 128k -r ' + fps + ' -f flv "rtmp://live-push.bilivideo.com/live-bvc/' + rtmp + '"'
            subprocess.run(command, shell=True)


main()
