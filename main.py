import os
from urllib.request import urlopen
import re
import time
from html import unescape
import webbrowser

trackerListFile = open("Tracker List.txt", "r", encoding="utf-8")
text = trackerListFile.read()
trackerListFile.close()
gameList = []
for x in text.splitlines():
    regex = re.match(r"(.*?) ?(?:\((.*)\))?(?:: )?(http.*)", x)
    try:
        gameName = regex[1]
        slotName = "" if regex[2] is None else regex[2]
        trackerLink = regex[3]
        trackerLink = trackerLink.replace("/tracker/", "/generic_tracker/")
        worldID = re.search(r".../\d/\d+", trackerLink)[0]
        gameList.append((worldID, gameName, trackerLink, slotName))
    except TypeError:
        pass
lastUpdated = {}
try:
    lastUpdateFile = open("Last Updated.txt", "r", encoding="utf-8")
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
mcguffinSet = set()
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
            progressionFile = open("worlds/{}/progression.txt".format(name), "r", encoding="utf-8")
            text = progressionFile.read()
            progressionFile.close()
            for x in text.splitlines():
                match = re.match(r"(.*): (.*)", x)
                try:
                    match match[2].lower():
                        case "mcguffin": mcguffinSet.add((name, match[1].lower()))
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
lastUpdatePrint = ""
mcguffinPrint = "McGuffin\n"
progressionPrint = "Progression\n"
usefulPrint = "Useful\n"
fillerPrint = "Filler\n"
trapPrint = "Trap\n"
unknownPrint = "Unknown"
hasMcguffin = False
hasProgression = False
hasUseful = False
hasFiller = False
hasTrap = False
hasUnknown = False
DDOSProtectionMode = (len(gameList) > 5)  # Don't want to get in trouble for hammering the website
lastWebsiteCheck = 0
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
    if DDOSProtectionMode:  # If checking large numbers of trackers, limit to 1 per second
        timeToSleep = lastWebsiteCheck - time.time() + 1
        if timeToSleep > 0:
            time.sleep(timeToSleep)
    page = None
    failcount = 0
    maxfails = 5
    timeout = 3
    while failcount < maxfails:
        try:
            if failcount > 0:
                print("Connection took too long. Retrying ({})".format(failcount))
            lastWebsiteCheck = time.time()
            page = urlopen(url, timeout=timeout)
            break
        except TimeoutError:
            failcount += 1
            timeout += 1
    if failcount == maxfails:
        print("failed {} times. In the interest of finishing, this one will be skipped".format(failcount))
        lastUpdatePrint += "{} ({}): {}\n".format(gameName, worldID, lastUpdate)
        continue
    if failcount >= 1:
        print("retrying worked!")
    html_bytes = page.read()
    html = unescape(html_bytes.decode("utf-8"))
    matches = re.findall("<tr>\n *<td>(.*)</td>\n *<td>(.*)</td>\n *<td>(.*)</td>\n *</tr>", html)
    # You can't parse [X]HTML with regex. Because HTML can't be parsed by regex.
    # TO DO: try using an XML parser instead?
    # silasary: I'd recommend using BeautifulSoup, it's much better for parsing HTML
    for (itemName, itemNumber, itemTime) in matches:
        newUpdate = max(newUpdate, int(itemTime))
        if int(itemTime) > lastUpdate:
            if (gameName, itemName.lower()) in mcguffinSet:
                mcguffinPrint += "{} ({}): {} x{}\n".format(gameName, printID, itemName, itemNumber)
                hasMcguffin = True
                continue
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
                    progressionFile = open("worlds/{}/progression.txt".format(gameName), "a", encoding="utf-8")
                    progressionFile.write("\n{}: unknown".format(itemName))
                    progressionFile.close()
    lastUpdatePrint += "{} ({}): {}\n".format(gameName, worldID, newUpdate)
mcguffinPrint = mcguffinPrint+"\n" if hasMcguffin else ""
progressionPrint = progressionPrint+"\n" if hasProgression else ""
usefulPrint = usefulPrint+"\n" if hasUseful else ""
fillerPrint = fillerPrint+"\n" if hasFiller else ""
trapPrint = trapPrint+"\n" if hasTrap else ""
unknownPrint = unknownPrint+"\n" if hasUnknown else ""
consolePrint = "{}{}{}{}{}{}".format(trapPrint, fillerPrint, usefulPrint, unknownPrint, progressionPrint, mcguffinPrint)
filePrint = "{}{}{}{}{}{}".format(progressionPrint, unknownPrint, usefulPrint, fillerPrint, trapPrint, mcguffinPrint)
print()
outputFile = open("output.txt", "w", encoding="utf-8")
outputFile2 = open("old output/{}.txt".format(time.strftime("%Y-%m-%d %H-%M-%S")), "w", encoding="utf-8")
if consolePrint == "":
    print("No items received")
    outputFile.write("No items received")
    outputFile2.write("No items received")
else:
    print(consolePrint)
    outputFile.write(filePrint)
    outputFile2.write(filePrint)
outputFile.close()
outputFile2.close()
lastUpdateFile = open("Last Updated.txt", "w", encoding="utf-8")
lastUpdateFile.write(lastUpdatePrint)
lastUpdateFile.close()
print("Output also printed to Output.txt.")
print("Open Output.txt? (y/n)")
userInput = input()
if userInput[0].lower() == "y":
    webbrowser.open("output.txt")
