import time
import glob
import os
import sys
import re
import codecs
import yaml
import operator
from os.path import dirname, exists

justonce = False
def tail(thefile, past):
    if not past:
        thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.5)
            continue
        line = line.rstrip("\n").rstrip("\r")
        if line != "":
            yield line


if __name__ == "__main__":
    with open("config.yml", "r") as config:
        conf = yaml.load(config, Loader=yaml.SafeLoader)
    print("VRC Log Viewer : Original https://github.com/27Cobalter/vrc_log_viewer/releases \r\n Edit ver : Zuwaii-")
    print("load config")
    reg = []
    for pattern in conf["reg"]:
        print("  " + pattern)
        reg.append(re.compile(pattern))

    vrcdir = os.environ["USERPROFILE"] + "\\AppData\\LocalLow\\VRChat\\VRChat\\"
    logfile = vrcdir + conf["logfile"]
    if logfile == vrcdir:
        logfiles = glob.glob(vrcdir + "output_log_*.txt")
        logfiles.sort(key=os.path.getctime, reverse=True)
        logfile = logfiles[0]
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if exists(path):
            logfile = path

    with open(logfile, "r", encoding="utf-8") as f:
        print("open logfile : ", logfile)
        loglines = tail(f, conf["past"])
        if justonce == False:
            justonce == True
            f = codecs.open('alllog.txt','a+','utf-8')
            f.write("-----------------------------------------------------------------------------reopened-----------------------------------------------------------\r\n")
            f.close()
        for line in loglines:
            for pattern in reg:
                match = pattern.match(line)
                if not match:
                    continue
                message = ""
                for group in match.groups():
                    message = message + group + " "
                print(message) 
                f = codecs.open('alllog.txt','a+','utf-8')
                f.write("%s \r\n" % message)
                f.close()
