import time
import json
import random
from os import system, name
import matplotlib.pyplot as plt
from playsound import playsound
from fileOperations import *

# All data is saved with UTC time, difference must be calculated to make the program work correctly in different time-zones.
global SECONDS_DIFFERENCE
SECONDS_DIFFERENCE = time.localtime().tm_gmtoff

def clear():
    """Clear the whole terminal display."""

    if name == 'nt':
        _ = system('cls')

    else:
        _ = system('clear')


def superMemo(answer: int, currentStreak: int, easeRatio: float, interval: int):
    """Returns updatet parameters for the word that was repeated."""

    if answer == 1:
        if currentStreak == 0:
            interval = 1

        elif currentStreak == 1:
            interval = 6

        else:
            interval = round(interval*easeRatio, 2)

        easeRatio = round(easeRatio+0.05, 2)
        if easeRatio < 1.3:
            easeRatio = 1.3

        currentStreak += 1

    else:
        currentStreak = 0
        interval = 1
        easeRatio = max(0, round(easeRatio-0.3, 2))

    return currentStreak, easeRatio, interval


def learnNewWords(words: list, settings: dict, logs: list):
    """Full process of learning new words."""

    clear()

    wordsToLearn = []
    alreadyLearned = []
    wordIndex = 0
    isLastCorrect = True

    if settings["maxWords"]-settings["words"] <= 0:
        while True:
            print("You have already accomplished your goal ({} words, while your limit is: {}).\n".format(
                settings["words"], settings["maxWords"]))
            print("Do you want to continue? (1 - y/2 - n)\n")

            decision = input("Your decision: ")
            print("\n===\n")

            if decision == "1":
                print("Another {} words will be prepared for learning.".format(
                    settings["maxWords"]))
                print(
                    "Remember that you can always stop learning by inputing 0 when asked to repeat a word.\n")

                _ = input("Press enter to continue...")
                break

            else:
                print("You will return to main menu.\n")

                _ = input("Press enter to continue...")
                return words, settings, logs

        while len(wordsToLearn) < settings["maxWords"]:
            if words[wordIndex]["count"] == 0:
                wordsToLearn.append(wordIndex)

            wordIndex += 1
            
            if wordIndex == len(words):
                break

    else:
        while len(wordsToLearn) < settings["maxWords"]-settings["words"]:
            if words[wordIndex]["count"] == 0:
                wordsToLearn.append(wordIndex)

            wordIndex += 1
            
            if wordIndex == len(words):
                break

    while True:

        clear()

        print("LEARNING. Words to learn: {}".format(len(wordsToLearn)))
        print("0 - abort session")
        print("1 - repeat new words\n")
        print("===\n")

        if isLastCorrect:
            currentIndex = random.choice(wordsToLearn)
            currentWord = words[currentIndex]

        print("Word: {}\n".format(currentWord["han"]))
        print("Translation: {}\n".format(currentWord["eng"]))
        playsound("sounds/korean_{}.mp3".format(currentIndex))

        answer = input("Repeat: ")

        print("\n===\n")

        if answer == "0":
            print("Learning has ended with {} words remaining.\n".format(
                len(wordsToLearn)))
            print("Words learned:")

            for i, j in enumerate(alreadyLearned):
                print("{}. {} - {}".format(i+1,
                                           words[j]["han"], words[j]["eng"]))

            _ = input("\nPress Enter to continue...")
            return words, settings, logs

        if answer == "1":

            clear()

            print("Words from this session:\n".format(len(wordsToLearn)))

            for i, j in enumerate(alreadyLearned):
                print("{}. {} - {}".format(i+1,
                                           words[j]["han"], words[j]["eng"]))

            _ = input("\nPress Enter to continue...")

        elif answer == currentWord["han"].split("(")[0]:
            print("Correct!\n")

            isLastCorrect = True
            words[currentIndex]["date"] = int(time.time())
            words[currentIndex]["count"] += 1

            logs.append({
                "wordIndex": currentIndex,
                "correct": 1,
                "time": int(time.time()),
                "count": words[currentIndex]["count"],
                "nextI": 0,
                "ease": words[currentIndex]["ef"],
                "localTime": SECONDS_DIFFERENCE,
                "currentStreak": 0
            })

            settings["words"] += 1

            alreadyLearned.append(currentIndex)
            wordsToLearn.remove(currentIndex)
            userInput = input(
                "Press Enter to continue...\nor 1 to replay the sound.\n")

            while True:
                if userInput == "1":
                    playsound("sounds/korean_{}.mp3".format(currentIndex))
                    pass

                else:
                    break

                userInput = input()

        else:
            print("Incorrect!\n")
            print("Try again.\n")

            isLastCorrect = False
            userInput = input(
                "Press Enter to continue...\nor 1 to replay the sound.\n")

            while True:
                if userInput == "1":
                    playsound("sounds/korean_{}.mp3".format(currentIndex))
                    pass

                else:
                    break

                userInput = input()

        if len(wordsToLearn) == 0:
            print("\n===\n")
            print("Learning has ended.\n")
            print("Words learned:")

            for i, j in enumerate(alreadyLearned):
                print("{}. {} - {}".format(i+1,
                                           words[j]["han"], words[j]["eng"]))

            userInput = input("Press Enter to continue...\n")
            return words, settings, logs


def repeat(words, settings, logs):
    """Repeat all words for given day."""

    clear()

    toRepeat = []
    toRepeatToday = []

    currentTime = time.time()
    toEnd = currentTime+SECONDS_DIFFERENCE+3600*(24-((currentTime+SECONDS_DIFFERENCE)/3600) % 24)
    
    allWordsLastDifference = {}

    for i in logs:
        allWordsLastDifference[i["wordIndex"]] = i["localTime"]

    for i in range(len(words)):
        if i not in allWordsLastDifference:
            continue 

        if words[i]["date"]+allWordsLastDifference[i] < currentTime and words[i]["date"] != 0:
            toRepeat.append(i)

        elif words[i]["date"]+allWordsLastDifference[i] > currentTime and words[i]["date"]+allWordsLastDifference[i] < toEnd:
            toRepeatToday.append(i)

    notCorrect = []

    if settings["repeatAll"] == 1:
        if toRepeatToday:
            toRepeat = toRepeat + toRepeatToday

    if not toRepeat:
        firstWordTime = words[0]["date"]

        for i in range(1, len(words)):
            if words[i]["date"] < firstWordTime and words[i]["date"] != 0:
                firstWordTime = words[i]["date"]

        firstWordTimeTime = time.localtime(firstWordTime)
        date = [firstWordTimeTime.tm_mday, firstWordTimeTime.tm_mon,
                firstWordTimeTime.tm_hour, firstWordTimeTime.tm_min]

        if len(str(date[1])) == 1:
            date[1] = "0" + str(date[1])

        if len(str(date[3])) == 1:
            date[3] = "0" + str(date[3])

        if settings["repeatAll"] == 1:
            if toRepeatToday:
                toRepeat = toRepeatToday

            else:
                print("No words to repeat.\nFirst word to repeat at: {}.{} - {}:{}\n".format(
                    date[0], date[1], date[2], date[3]))

                _ = input("Press enter to continue...")
                return words, settings, logs

    while True:

        clear()

        currentIndex = random.choice(toRepeat+notCorrect)
        currentWord = words[currentIndex]

        print("Words to repeat: {}\n".format(len(notCorrect+toRepeat)))
        print("===\n(0. to exit)\n")
        print("Word: {}\n".format(currentWord["eng"]))

        answer = input("Translation: ")
        print()

        if answer == "0":
            return words, settings, logs

        elif answer == currentWord["han"].split("(")[0] and currentIndex in toRepeat:
            print("Correct!")
            playsound("sounds/korean_{}.mp3".format(currentIndex))

            words[currentIndex]["n"], words[currentIndex]["ef"], words[currentIndex]["i"] = superMemo(
                1, currentWord["n"], currentWord["ef"], currentWord["i"])
            words[currentIndex]["date"] = int(
                time.time())+int(words[currentIndex]["i"]*24*3600)
            words[currentIndex]["count"] += 1

            logs.append({
                "wordIndex": currentIndex,
                "correct": 1,
                "time": int(time.time()),
                "count": words[currentIndex]["count"],
                "nextI": words[currentIndex]["i"],
                "ease": words[currentIndex]["ef"],
                "localTime": SECONDS_DIFFERENCE,
                "currentStreak": words[currentIndex]["n"]
            })

            toRepeat.remove(currentIndex)

            userInput = input(
                "Press Enter to continue...\nor 1 to replay the sound.\n")

            while True:
                if userInput == "1":
                    playsound("sounds/korean_{}.mp3".format(currentIndex))
                    pass

                else:
                    break

                userInput = input()

        elif answer == currentWord["han"].split("(")[0] and currentIndex in notCorrect:
            print("Correct!")
            playsound("sounds/korean_{}.mp3".format(currentIndex))

            words[currentIndex]["n"], words[currentIndex]["ef"], _ = superMemo(
                1, currentWord["n"], currentWord["ef"], currentWord["i"])
            words[currentIndex]["count"] += 1

            logs.append({
                "wordIndex": currentIndex,
                "correct": 1,
                "time": int(time.time()),
                "count": words[currentIndex]["count"],
                "nextI": words[currentIndex]["i"],
                "ease": words[currentIndex]["ef"],
                "localTime": SECONDS_DIFFERENCE,
                "currentStreak": 1
            })

            notCorrect.remove(currentIndex)

            userInput = input(
                "Press Enter to continue...\nor 1 to replay the sound.\n")

            while True:
                if userInput == "1":
                    playsound("sounds/korean_{}.mp3".format(currentIndex))
                    pass

                else:
                    break

                userInput = input()

        else:
            print("Incorrect!\n")
            print("Correct answer: " + currentWord["han"])
            playsound("sounds/korean_{}.mp3".format(currentIndex))

            userInput = input(
                "Press Enter to continue...\nor 1 to replay the sound.\n")

            while True:
                if userInput == "1":
                    playsound("sounds/korean_{}.mp3".format(currentIndex))
                    pass

                else:
                    break

                userInput = input()

            if userInput == "`":
                if currentIndex in toRepeat:
                    words[currentIndex]["n"], words[currentIndex]["ef"], words[currentIndex]["i"] = superMemo(
                        1, currentWord["n"], currentWord["ef"], currentWord["i"])
                    words[currentIndex]["date"] = int(
                        time.time())+words[currentIndex]["i"]*24*3600
                    words[currentIndex]["count"] += 1

                    toRepeat.remove(currentIndex)

                elif currentIndex in notCorrect:
                    words[currentIndex]["n"], words[currentIndex]["ef"], _ = superMemo(
                        1, currentWord["n"], currentWord["ef"], currentWord["i"])
                    words[currentIndex]["count"] += 1

                    notCorrect.remove(currentIndex)

                logs.append({
                    "wordIndex": currentIndex,
                    "correct": 1,
                    "time": int(time.time()),
                    "count": words[currentIndex]["count"],
                    "nextI": words[currentIndex]["i"],
                    "ease": words[currentIndex]["ef"],
                    "localTime": SECONDS_DIFFERENCE,
                    "currentStreak": words[currentIndex]["n"]
                })

            else:
                words[currentIndex]["n"], words[currentIndex]["ef"], words[currentIndex]["i"] = superMemo(
                    0, currentWord["n"], currentWord["ef"], currentWord["i"])
                words[currentIndex]["date"] = int(
                    time.time())+words[currentIndex]["i"]*24*3600
                words[currentIndex]["count"] += 1

                logs.append({
                    "wordIndex": currentIndex,
                    "correct": 0,
                    "time": int(time.time()),
                    "count": words[currentIndex]["count"],
                    "nextI": words[currentIndex]["i"],
                    "ease": words[currentIndex]["ef"],
                    "localTime": SECONDS_DIFFERENCE,
                    "currentStreak": 0
                })

                if currentIndex in toRepeat:
                    notCorrect.append(currentIndex)
                    toRepeat.remove(currentIndex)

        print()

        if len(notCorrect+toRepeat) == 0:
            print("All words repeated.")

            _ = input()
            return words, settings, logs


def showLogs(words, logs, logsSave):
    incorrectLimits = False
    while True:
        clear()

        d0 = (int(time.time())+SECONDS_DIFFERENCE)//(3600*24)
        allWordsLastDifference = {}

        for i in logs:
            allWordsLastDifference[i["wordIndex"]] = i["localTime"]
        
        firstDay = (logs[0]["time"]+logs[0]["localTime"])//(3600*24)
        lastDay = max([words[i]["date"]+allWordsLastDifference[i] for i in range(len(allWordsLastDifference))])//(3600*24)

        print("0. Exit")
        print("1. Words daily")
        print("2. Words type daily")
        print("3. Words from previous day daily")
        print("4. Accuracy daily")
        print("5. Accuracy hours")
        print("6. Word types")
        print("7. Word types history")
        print("8. Ease factor")

        print("\nLimits: {}:{} <- only for 1.".format(firstDay-d0, lastDay-d0))
        if incorrectLimits:
            incorrectLimits = False
            print("\nIncorrect limits. Try again.\n")

        answer = input()
        limits = []

        if len(answer.split(" ")) == 2:
            limits = answer.split(" ")[1]
            answer = answer.split(" ")[0]
            if limits.count(":") != 1:
                incorrectLimits = True
                continue

        if answer == "0":
            break

        if answer in [str(i) for i in range(1, 9)]:
            fig, ax = plt.subplots()

        if answer in ["1", "2", "3", "4", "7"]:

            if limits:
                if limits[0] == ":":
                    limits = [str(firstDay-d0), limits.split(":")[1]]
                elif limits.split(":")[1] == "":
                    limits = [limits.split(":")[0], 0]
                else:
                    limits = limits.split(":")
            else:
                limits = [str(firstDay-d0), 0]

            if answer == "1":
                days = [str(i-d0) for i in range(firstDay, int(lastDay+1))]
                if limits[1] == 0:
                    limits[1] = str(lastDay-d0)

            else:
                days = [str(i-d0) for i in range(firstDay, d0+1)]
                if limits[1] == 0:
                    limits[1] = "0"

            if int(limits[0])>=int(limits[1]):
                incorrectLimits = True
                continue
            elif limits[0] in days and limits[1] in days:
                days = [str(i) for i in range(int(limits[0]), int(limits[1])+1)]
            else:
                incorrectLimits = True
                continue
            
            tickNumber = int(len(days)/10)
            ticks = []

            if not tickNumber:
                tickNumber = 1

            for i in days:
                if int(i) % tickNumber == 0:
                    ticks.append(i)

                else:
                    ticks.append("")

        if answer == "1":
            wordsLog = []

            for i in days:
                if str(int(i)-(firstDay-d0)) in logsSave.keys():
                    wordsLog.append(logsSave[str(int(i)-(firstDay-d0))]["1"]+[0])
                else:
                    wordsLog.append([0,0,0])
    
            for j, i in enumerate(words):
                try:
                    day = str(int((i["date"]+allWordsLastDifference[j])//(3600*24)-d0))

                    wordsLog[days.index(day)][2] += 1
                except:
                    pass

            ax.bar(days, [i[0] for i in wordsLog], label="new words")
            ax.bar(days, [i[1] for i in wordsLog], label="repeated words", bottom=[i[0] for i in wordsLog])
            ax.bar(days, [i[2] for i in wordsLog], label="words to repeat", bottom=[i[0]+i[1] for i in wordsLog], tick_label=ticks)
                
        elif answer == "2":
            wordsLog = []

            for i in days:
                wordsLog.append(logsSave[str(int(i)-(firstDay-d0))]["2"])

            ax.bar(days, [i[0] for i in wordsLog], label="0")
            ax.bar(days, [i[1] for i in wordsLog], label="1", bottom=[i[0] for i in wordsLog])
            ax.bar(days, [i[2] for i in wordsLog], label="2", bottom=[i[0]+i[1] for i in wordsLog])
            ax.bar(days, [i[3] for i in wordsLog], label="3", bottom=[i[0]+i[1]+i[2] for i in wordsLog])
            ax.bar(days, [i[4] for i in wordsLog], label="4", bottom=[i[0]+i[1]+i[2]+i[3] for i in wordsLog])
            ax.bar(days, [i[5] for i in wordsLog], label="5+", bottom=[i[0]+i[1]+i[2]+i[3]+i[4] for i in wordsLog], tick_label=ticks)

        elif answer == "3":
            toDisplay = []
            
            for i in days:
                toDisplay.append(logsSave[str(int(i)-(firstDay-d0))]["3"])
            
            ax.bar(days, [i[0] for i in toDisplay], label="0")
            ax.bar(days, [i[1] for i in toDisplay], label="1", bottom=[i[0] for i in toDisplay])
            ax.bar(days, [i[2] for i in toDisplay], label="2", bottom=[i[0]+i[1] for i in toDisplay])
            ax.bar(days, [i[3] for i in toDisplay], label="3", bottom=[i[0]+i[1]+i[2] for i in toDisplay])
            ax.bar(days, [i[4] for i in toDisplay], label="4", bottom=[i[0]+i[1]+i[2]+i[3] for i in toDisplay])
            ax.bar(days, [i[5] for i in toDisplay], label="5+", bottom=[i[0]+i[1]+i[2]+i[3]+i[4] for i in toDisplay], tick_label=ticks)          
                
        elif answer == "4":
            toDelete = 0
            if int(days[0])-6 > firstDay-d0:
                toDelete = 6
                days = [str(i) for i in range(int(days[0])-6, int(days[0]))]+days
            elif int(days[0])>firstDay-d0:
                toDelete = firstDay-d0-int(days[0])
                days = [str(i) for i in range(int(days[0]), int(days[0]))]+days

            wordsLog = []
            for i in days:
                wordsLog.append(logsSave[str(int(i)-(firstDay-d0))]["4"])

            accuracyDaily = [i[0]/i[1] if i[1] > 0 else 0 for i in wordsLog]
            average3 = [sum(accuracyDaily[max(0, i-2):i+1])/min(i+1, 3) for i in range(len(accuracyDaily))]
            average7 = [sum(accuracyDaily[max(0, i-6):i+1])/min(i+1, 7) for i in range(len(accuracyDaily))]

            if accuracyDaily[-1] == 0:
                average3[-1] = None
                average7[-1] = None

            for _ in range(0, toDelete):
                days.pop(0)
                accuracyDaily.pop(0)
                average3.pop(0)
                average7.pop(0)

            ax.plot(days, average3, label="3 day average", color='red')
            ax.plot(days, average7, label="7 day average", color='black')
            ax.bar(days, accuracyDaily, tick_label=ticks, label="accuracy daily")

        elif answer == "5":
            toShow = []
            for i in range(96):
                if logsSave["hours"][i][1] > 0:
                    toShow.append(logsSave["hours"][i][0]/logsSave["hours"][i][1])
                else:
                    toShow.append(0)

            hrs = []

            for i in range(96):
                if i % 4 == 0:
                    hrs.append("{}:00".format(i//4))

                else:
                    hrs.append("{}:{}".format(i//4, 15*(i % 4)))

            hrsToShow = []

            for i, j in enumerate(hrs):
                if i % 2 == 0:
                    hrsToShow.append(j)
                else:
                    hrsToShow.append("")

            plt.xticks(rotation=90)

            ax.bar(hrs, toShow, label="accuracy hourly", tick_label=hrsToShow)

        elif answer == "6":
            toShow = ["1", "2", "3", "4", "5+"]
            toShowData = [0, 0, 0, 0, 0]

            for i in words:
                if i["n"] == 0:
                    continue

                toShowData[min(i["n"]-1, 4)] += 1

            for i in range(len(toShow)):
                ax.bar(toShow[i], toShowData[i])

        elif answer == "7":
            toDisplay = []
            if sum(logsSave[str(int(days[-1])-(firstDay-d0))]["7"]) == 0:
                for i in words:
                    logsSave[str(int(days[-1])-(firstDay-d0))]["7"][min(i["n"], 5)-1] += 1

            for i in days:
                toDisplay.append(logsSave[str(int(i)-(firstDay-d0))]["7"])

            ax.bar(days, [i[0] for i in toDisplay], label="1")
            ax.bar(days, [i[1] for i in toDisplay], label="2", bottom = [i[0] for i in toDisplay])
            ax.bar(days, [i[2] for i in toDisplay], label="3", bottom = [i[0]+i[1] for i in toDisplay])
            ax.bar(days, [i[3] for i in toDisplay], label="4", bottom = [i[0]+i[1]+i[2] for i in toDisplay])
            ax.bar(days, [i[4] for i in toDisplay], label="5+", bottom = [i[0]+i[1]+i[2]+i[3] for i in toDisplay], tick_label=ticks)

        elif answer == "8":
            allEf = []

            for i in words:
                if i["count"] > 0:
                    allEf.append(i["ef"])

            allEf.sort()
            toShow = []
            ef = min(allEf)

            while ef <= max(allEf):
                toShow.append(round(ef, 2))
                ef += .05

            toShowData = [0 for i in range(len(toShow))]

            for i in allEf:
                toShowData[toShow.index(i)] += 1

            ax.bar([str(i) for i in toShow], toShowData)

        if answer in [str(i) for i in range(1, 9)]:
            if answer not in ["6", "8"]:
                ax.legend()
            
            plt.show()


def saveLogs(logs, logStart, logsSave, words):
    d0 = (int(time.time())+SECONDS_DIFFERENCE)//(3600*24)

    firstDay = (logs[0]["time"]+logs[0]["localTime"])//(3600*24)
    if str(d0-firstDay) not in logsSave:
        logsSave[str(d0-firstDay)] = {"1": [0,0], "2": [0,0,0,0,0,0], "3": [0,0,0,0,0,0], "4": [0, 0], "7": [0,0,0,0,0]}

    for i in logs[logStart:]:
        day = d0-firstDay
        #FOR 1
        if i["correct"] != 0:
            if i["count"] == 1:
                logsSave[day]["1"][0] += 1     
            else:
                logsSave[day]["1"][1] += 1

        #FOR 2
        if i["count"] != 1 and i["correct"] != 0:
            if i["currentStreak"] < 6:
                logsSave[day]["2"][i["currentStreak"]-1] += 1
            else:
                logsSave[day]["2"][5] += 1

        #FOR 4
        if i["count"] != 1:
            if i["correct"] == 1:
                logsSave[day]["4"][0] += 1
            logsSave[day]["4"][1] += 1

        #FOR HOURS
        if i["count"] != 1:
            if i["correct"] == 1:
                logsSave["hours"][(i["time"]+SECONDS_DIFFERENCE) %
                        (3600*24)//900][0] += 1
            logsSave["hours"][(i["time"]+SECONDS_DIFFERENCE) %
                        (3600*24)//900][1] += 1
    
    #FOR 7
    logsSave[day]["7"] = [0,0,0,0,0]
    for i in words:
        if i["n"] != 0:
            logsSave[day]["7"][min(i["n"], 5)-1] += 1
    
    #FOR 3
    todayWords = {}
    finalTodayWords = {}
    toRemove = []
    for j, i in enumerate(reversed(logs)):
        wordDay = (i["time"]+SECONDS_DIFFERENCE)//(3600*24)
        if i["correct"] == 0 or i["count"] == 1:
            continue
        if wordDay == d0:
            if i["wordIndex"] not in todayWords:
                todayWords[i["wordIndex"]] = [wordDay]
        elif i["wordIndex"] in todayWords:
            if todayWords[i["wordIndex"]][-1] == wordDay+1:
                todayWords[i["wordIndex"]].append(wordDay)
            else:
                finalTodayWords[i["wordIndex"]] = todayWords[i["wordIndex"]]
                toRemove = [i["wordIndex"]]
        for l in toRemove:
            del todayWords[l]
            toRemove = []
        if not todayWords and wordDay != d0:
            break
    
    allDays = [0,0,0,0,0,0]
    for i in finalTodayWords:
        allDays[min(len(finalTodayWords[i])-1, 5)] += 1
    logsSave[day]["3"] = allDays
    
    return logsSave


def main():
    """Main function."""

    clear()
    try:
        with open("data.json", "r") as rd:
            lastFileTime = json.load(rd)["settings"]["time"]
    except:
        lastFileTime = 0


    try:
        result = load(lastFileTime)
        if result == True:
            print("Files are in sync...")
        
        elif result == False:
            print("File from this machine is older than from web...\nManage the files correctly before running program...\n")
            
            _ = input("Press enter to exit the program...")
            exit()
        
        else:
            print("Newest file was was downloaded...\n")

    except Exception as ex:
        print(ex)
        print("There was problem downloading file...\nMake sure you have internet connection...\n")
        
        _ = input("Press enter to exit the program...")
        exit()

    with open("data.json", "r") as rd:
        data = json.load(rd)
        words = data["words"]
        settings = data["settings"]
        logs = data["logs"]
        logsSave = data["logsSave"]
        logsLength = len(logs)

    today = time.localtime()[0:3]

    if today[0]*365+today[1]*30+today[2] > settings["date"][0]*365+settings["date"][1]*30+settings["date"][2]:
        settings["date"] = today
        settings["words"] = 0

    _ = input("Press enter to continue...")

    while True:
        clear()
        print("0. Exit")
        print("1. Learn")
        print("2. Repeat")
        print("3. Logs\n")

        dec = input("Your action: ")

        if dec == "0":
            break
        
        elif dec == "1":
            logsLen = len(logs)
            words, settings, logs = learnNewWords(words, settings, logs)
            logsSave = saveLogs(logs, logsLen, logsSave, words)

        elif dec == "2":
            logsLen = len(logs)
            words, settings, logs = repeat(words, settings, logs)
            logsSave = saveLogs(logs, logsLen, logsSave, words)

        elif dec == "3":
            showLogs(words, logs, logsSave)

    settings["time"] = int(time.time())
    if len(logs) > logsLength:
        with open("data.json", "w") as sv:
            data["words"] = words
            data["settings"] = settings
            data["logs"] = logs
            data["logsSave"] = data["logsSave"]
            json.dump(data, sv)

        save(settings["time"])

        clear()
        print("Data was saved...")
    else:
        clear()
        print("Data was not saved, as there was no updates to it...")
    
    _ = input("Press enter to exit the program...")

main()
