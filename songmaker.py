from MidiFile3 import MIDIFile
from random import randint
import subprocess
import json
from pprint import pprint

import os.path


def createFile():
    dataList = []
    theSong = MIDIFile(1)
    track = 0
    channel = 0
    duration = 1
    volume = 100
    theSong.addTrackName(track, 0, "track1")
    theSong.addTempo(track, 0, 120)
    theSong.addNote(track, channel, 60, 0, 1, volume)

    with open('counting.json') as data_file:
        json1_data = json.load(data_file)

    for i in range(1, 5):

        time = 25 / 16 * i
        pitch = choosePitchByLearning(json1_data)

        if pitch > 71:
            pass
        else:
            theSong.addNote(track, channel, pitch, time, duration, volume)
            dataList.append("n" + str(pitch))

    binfile = open("output.mid", 'wb')
    theSong.writeFile(binfile)
    binfile.close()
    playFile('output.mid', dataList,json1_data)


def playFile(filename, listtt, json1_data):
    subprocess.call(['timidity', filename])

    decision = input("yes or no?")

    if (decision == "yes"):

        for x in listtt:
            json1_data[x] = json1_data[x] + 1
    else:

        for x in listtt:
            json1_data[x] = json1_data[x] - 1

    pprint(json1_data)
    with open('counting.json', 'w') as fp:
        json.dump(json1_data, fp)

    createFile()


def choosePitchByLearning(dict):
    total = 0
    chosen = 0
    for key, value in dict.items():
        total = total + value


    for i in range(1, 12):
        thisChance = dict["n" + str(60 + i)]
        if randint(0, total + 1) <= thisChance:

            chosen = 60+i
            break

        else:
            total = total - dict["n" + str(60 + i)]
        pprint("n" + str(60 + i)+" "+str(thisChance) + " " + str(total))
    return chosen


createFile()
