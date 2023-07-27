import os
import os.path
import io
import subprocess
import logging
import re

dir = "/sda/res"  # 你的视频文件所在目录
rtmp = "?streamname=live_11001546_4006607&key=xxxxxxxxxxxxxxxxx&schedule=rtmp&pflag=1"  # 填你的串流密钥
fps = "25"  # 默认即可
found_start_file = True
start_file = "23.mp4"  # 指定起始文件名 这里可以填你想从第几集播放的上一集名称，比如你想从第二集播放，这里就填第一集的名字， 然后把 found_start_file 的值改成 false。

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
    print("programmer start !!!")
    global found_start_file  # 将变量声明为全局变量
    logging.basicConfig(filename='playback.log', level=logging.INFO, format='%(asctime)s - %(message)s')
    nameList = listDir(dir)
    nameList.sort()
    while True:
        for file in nameList:
            filename = os.path.basename(file)
            if not found_start_file:
                if filename == start_file:
                    found_start_file = True
                continue
            logging.info("当前播放的是：" + filename)
            command = 'ffmpeg -re -i "' + file + '" -vcodec copy -acodec aac -ar 44100 -strict -2  -r ' + fps + ' -f flv "rtmp://live-push.bilivideo.com/live-bvc/' + rtmp + '"'
            subprocess.run(command, shell=True)
          

if __name__ == '__main__':
    main()
