import os
import time
def name_change(file):
    localtime = time.asctime(time.localtime(time.time()))
    os.rename(file, localtime+'.png')

name_change("New.png")
