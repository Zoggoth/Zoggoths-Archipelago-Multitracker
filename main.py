import os
from urllib.request import urlopen
import re
import time
from html import unescape
import webbrowser

trackerListFile = open("Tracker List.txt", "r")
text = trackerListFile.read()
trackerListFile.close()
gameList = []
for x in text.splitlines():
    regex = re.match(r"(.*?) ?(?:\((.*)\))?(?:: )?(http.*)", x)
    gameName = regex[1]
    slotName = "" if regex[2] is None else regex[2]
    trackerLink = regex[3]
    worldID = re.search(r".../\d/\d+", trackerLink)[0]
    gameList.append((worldID, gameName, trackerLink, slotName))
lastUpdated = {}
try:
    lastUpdateFile = open("Last Updated.txt", "r")
    text = lastUpdateFile.read()
    lastUpdateFile.close()
    for x in text.splitlines():
        try:
            regex = re.search(r"\((.../\d/\d+)\): (-?\d+)", x)
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
for (_, name, _, _) in gameList:
    if name != "":
        try:
            os.mkdir("worlds/{}".format(name))
        except FileExistsError:
            pass
        try:
            progressionFile = open("worlds/{}/progression.txt".format(name), "r")
            text = progressionFile.read()
            progressionFile.close()
            for x in text.splitlines():
                match = re.match("(.*): (.*)", x)
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
hasProgression = False
hasUseful = False
hasFiller = False
hasTrap = False
hasUnknown = False
DDOSProtectionMode = (len(gameList) > 5)
for (worldID, gameName, url, slotName) in gameList:
    if slotName != "":
        print("Checking {}".format(slotName))
    elif gameName != "":
        print("Checking {}".format(gameName))
    else:
        print("Checking {}".format(worldID))
    printID = worldID if slotName == "" else slotName
    lastUpdate = lastUpdated.get(worldID, -1)
    newUpdate = lastUpdate
    page = urlopen(url)
    html_bytes = page.read()
    html = unescape(html_bytes.decode("utf-8"))
    matches = re.findall("<tr>\n *<td>(.*)</td>\n *<td>(.*)</td>\n *<td>(.*)</td>\n *</tr>", html)
    # You can't parse [X]HTML with regex. Because HTML can't be parsed by regex.
    # TO DO: try using an XML parser instead?
    for (itemName, itemNumber, itemTime) in matches:
        newUpdate = max(newUpdate, int(itemTime))
        if int(itemTime) > lastUpdate:
            if (gameName, itemName.lower()) in progressionSet:
                progressionPrint += "{} ({}): {} x{}\n".format(gameName, printID, itemName, itemNumber)
                hasProgression = True
                continue
            if (gameName, itemName.lower()) in usefulSet:
                usefulPrint += "{} ({}): {} x{}\n".format(gameName, printID, itemName, itemNumber)
                hasUseful = True
                continue
            if (gameName, itemName.lower()) in fillerSet:
                fillerPrint += "{} ({}): {} x{}\n".format(gameName, printID, itemName, itemNumber)
                hasFiller = True
                continue
            if (gameName, itemName.lower()) in trapSet:
                trapPrint += "{} ({}): {} x{}\n".format(gameName, printID, itemName, itemNumber)
                hasTrap = True
                continue
            if not hasUnknown:
                hasUnknown = True
                unknownPrint += " (Unknown games/items can be added to the worlds folder)\n"
            if (gameName, itemName.lower()) in unknownSet:
                unknownPrint += "{} ({}): {} x{}\n".format(gameName, printID, itemName, itemNumber)
            else:
                unknownPrint += "{} ({}): {} x{}\n".format(gameName, printID, itemName, itemNumber)
                unknownSet.add((gameName, itemName.lower()))
                if gameName != "":
                    progressionFile = open("worlds/{}/progression.txt".format(gameName), "a")
                    progressionFile.write("\n{}: unknown".format(itemName))
                    progressionFile.close()
    lastUpdateFile.write("{} ({}): {}\n".format(gameName, worldID, newUpdate))
    if DDOSProtectionMode:
        time.sleep(1)  # Don't want to get in trouble for hammering the website
progressionPrint = progressionPrint+"\n" if hasProgression else ""
usefulPrint = usefulPrint+"\n" if hasUseful else ""
fillerPrint = fillerPrint+"\n" if hasFiller else ""
trapPrint = trapPrint+"\n" if hasTrap else ""
unknownPrint = unknownPrint+"\n" if hasUnknown else ""
consolePrint = "{}{}{}{}{}".format(trapPrint, fillerPrint, usefulPrint, unknownPrint, progressionPrint)
filePrint = "{}{}{}{}{}".format(progressionPrint, unknownPrint, usefulPrint, fillerPrint, trapPrint)
print()
if consolePrint == "":
    print("No items received")
    outputFile.write("No items received")
else:
    print(consolePrint)
    outputFile.write(filePrint)
outputFile.close()
lastUpdateFile.close()
print("Output also printed to Output.txt.")
print("Open Output.txt? (y/n)")
userInput = input()
if userInput[0].lower() == "y":
    webbrowser.open("output.txt")
