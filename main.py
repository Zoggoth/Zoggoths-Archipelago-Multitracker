import os
from urllib.request import urlopen
import re
import time
from html import unescape

trackerListFile = open("Tracker List.txt", "r")
text = trackerListFile.read()
trackerListFile.close()
gameList = []
for x in text.splitlines():
    regex = re.match("(.*): (.*)",x)
    gameName = regex[1]
    trackerLink = regex[2]
    worldNumber = re.search(".../\d/\d+", trackerLink)[0]
    gameList.append((worldNumber, gameName, trackerLink))
lastUpdated = {}
try:
    lastUpdateFile = open("Last Updated.txt", "r")
    text = lastUpdateFile.read()
    lastUpdateFile.close()
    for x in text.splitlines():
        try:
            regex = re.search("\((.../\d/\d+)\): (-?\d+)",x)
            lastUpdated[regex[1]] = int(regex[2])
        except TypeError:
            pass
except FileNotFoundError:
    pass
progressionSet = set()
usefulSet = set()
fillerSet = set()
trapSet = set()
unknownSet = set()
for (_, name, _) in gameList:
    try:
        os.mkdir("worlds/{}".format(name))
    except FileExistsError:
        pass
    try:
        progressionFile = open("worlds/{}/progression.txt".format(name),"r")
        text = progressionFile.read()
        progressionFile.close()
        for x in text.splitlines():
            match = re.match("(.*): (.*)",x)
            try:
                match match[2].lower():
                    case "progression": progressionSet.add((name, match[1].lower()))
                    case "useful": usefulSet.add((name, match[1].lower()))
                    case "filler": fillerSet.add((name, match[1].lower()))
                    case "trap": trapSet.add((name, match[1].lower()))
                    case _: unknownSet.add((name, match[1].lower()))
            except IndexError:
                pass
            except TypeError:
                pass
    except FileNotFoundError:
        pass
lastUpdateFile = open("Last Updated.txt", "w")
outputFile = open("output.txt", "w")
progressionPrint = "Progression\n"
usefulPrint = "Useful\n"
fillerPrint = "Filler\n"
trapPrint = "Trap\n"
unknownPrint = "Unknown"
hasunknown = False
DDOSProtectionMode = (len(gameList) > 5)
for (worldNumber, gameName, url) in gameList:
    print("Checking {}".format(gameName))
    lastUpdate = lastUpdated.get(worldNumber, -1)
    newUpdate = lastUpdate
    page = urlopen(url)
    html_bytes = page.read()
    html = unescape(html_bytes.decode("utf-8"))
    matches = re.findall("<tr>\n *<td>(.*)<\/td>\n *<td>(.*)<\/td>\n *<td>(.*)<\/td>\n *<\/tr>",html)
    # You can't parse [X]HTML with regex. Because HTML can't be parsed by regex.
    # TO DO: try using an XML parser instead?
    for (itemName, itemNumber, itemTime) in matches:
        newUpdate = max(newUpdate, int(itemTime))
        if int(itemTime) > lastUpdate:
            if (gameName, itemName.lower()) in progressionSet:
                progressionPrint += "{} ({}): {} x{}\n".format(gameName, worldNumber, itemName, itemNumber)
                continue
            if (gameName, itemName.lower()) in usefulSet:
                usefulPrint += "{} ({}): {} x{}\n".format(gameName, worldNumber, itemName, itemNumber)
                continue
            if (gameName, itemName.lower()) in fillerSet:
                fillerPrint += "{} ({}): {} x{}\n".format(gameName, worldNumber, itemName, itemNumber)
                continue
            if (gameName, itemName.lower()) in trapSet:
                trapPrint += "{} ({}): {} x{}\n".format(gameName, worldNumber, itemName, itemNumber)
                continue
            if not hasunknown:
                hasunknown = True
                unknownPrint += " (Unknown games/items can be added to the worlds folder)\n"
            if (gameName, itemName.lower()) in unknownSet:
                unknownPrint += "{} ({}): {} x{}\n".format(gameName, worldNumber, itemName, itemNumber)
            else:
                unknownPrint += "{} ({}): {} x{}\n".format(gameName, worldNumber, itemName, itemNumber)
                unknownSet.add((gameName, itemName.lower()))
                progressionFile = open("worlds/{}/progression.txt".format(gameName), "a")
                progressionFile.write("\n{}: unknown".format(itemName))
                progressionFile.close()
    lastUpdateFile.write("{} ({}): {}\n".format(gameName, worldNumber, newUpdate))
    if DDOSProtectionMode:
        time.sleep(1)
if not hasunknown:
    unknownPrint += "\n"
print()
print("{}\n{}\n{}\n{}\n{}".format(trapPrint,fillerPrint,usefulPrint,unknownPrint,progressionPrint))
outputFile.write("{}\n{}\n{}\n{}\n{}".format(progressionPrint,unknownPrint,usefulPrint,fillerPrint,trapPrint))
outputFile.close()
lastUpdateFile.close()
print("Output also stored in Output.txt.")
input()
