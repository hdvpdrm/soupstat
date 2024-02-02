#!/usr/bin/python3
import os
import re
import time as t

morgue_dir = os.path.expanduser("~")+"/.crawl/morgue"
obituary_files = [morgue_dir+"/"+f for f in os.listdir(morgue_dir) if ".txt" in f]

def read(files):
    data = []
    for f in files:
        with open(f,"r") as _f:
            strs = _f.read().split("\n")
            for s in strs:
                if "Time" in s:
                    data.append(s)
                    break
    return data

def parse(data):
    race_class_re = re.compile("\(.*\)")
    race_class = race_class_re.findall(data)[0][1:-1]

    time_re = re.compile("Time:.*")
    _, time = time_re.findall(data)[0].split()

    turns_re = re.compile("Turns:.*,")
    _, turns = turns_re.findall(data)[0][:-1].split()

    return race_class, time, turns


total_turns = 0
hours = minutes = seconds = 0
combo = {}
for line in read(obituary_files):
    race_class, time, turns = parse(line)
    if race_class not in combo.keys():
        combo[race_class] = 1
    else:
        combo[race_class] += 1

    
    total_turns += int(turns)
    hh, mm, ss = time.split(":")
    hours   += int(hh)
    minutes += int(mm)
    seconds += int(ss)


converted_hours   = hours*3600
converted_minutes = minutes*60
seconds += converted_hours+converted_minutes

playing_time = t.strftime('%H:%M:%S', t.gmtime(seconds))

print("total playing time:",playing_time)
print("total turns number:",total_turns)
print("most frequent race-class combo:",max(combo,key=combo.get))
