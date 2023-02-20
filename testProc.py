from processSupervisor import SetProcess
import time


proc = SetProcess("test")


def preSet():
    msg = "this is a test message"
    imgPaths = [{"name": "testPic", "path": "649587E8BA57F26BCD245A91B5223C9C.png"}, {"name": "lty", "path": "IMG_2005(20230214-233503).JPEG"}]
    filePaths = [{"name": "testFil", "path": "testFil.txt"}]
    proc.configer(msg, imgPaths, filePaths, timer=1)


def processing():
    for i in range(0, 50):
        print(i)
        proc.set_epoch(i, 50)
        time.sleep(1)


def postSet():
    print("Nice!!!")
    ...


if __name__ == "__main__":
    preSet()
    processing()
    postSet()
