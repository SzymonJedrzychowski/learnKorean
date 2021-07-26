import time
import json
import random
from os import system, name, listdir
import matplotlib.pyplot as plt
from playsound import playsound

# All data is saved with UTC time, difference must be calculated to make the program work correctly in different time-zones.
global SECONDS_DIFFERENCE
SECONDS_DIFFERENCE = time.localtime().tm_gmtoff


def clear():
    """Clear the whole terminal display."""

    if name == 'nt':
        _ = system('cls')

    else:
        _ = system('clear')


def superMemo(answerQuality: int, currentStreak: int, easeRatio: float, interval: int):
    """Returns updatet parameters for the word that was repeated."""

    if answerQuality == 1:
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

        beforeWordTime = time.time()

        answer = input("Repeat: ")
        afterWordTime = time.time()

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
                "timeSpent": round(afterWordTime-beforeWordTime, 1)
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
    toEnd = currentTime-SECONDS_DIFFERENCE+3600*(24-(currentTime/3600) % 24)

    for i in range(len(words)):
        if words[i]["date"] < currentTime and words[i]["date"] != 0:
            toRepeat.append(i)

        elif words[i]["date"] > currentTime and words[i]["date"] < toEnd:
            toRepeatToday.append(i)

    notCorrect = []

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
        print("===\n (0. to exit)\n")
        print("Word: {}\n".format(currentWord["eng"]))

        beforeWordTime = time.time()

        answer = input("Translation: ")
        afterWordTime = time.time()
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
                "timeSpent": round(afterWordTime-beforeWordTime, 1)
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
                "timeSpent": round(afterWordTime-beforeWordTime, 1)
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

                    logs.append({
                        "wordIndex": currentIndex,
                        "correct": 1,
                        "time": int(time.time()),
                        "count": words[currentIndex]["count"],
                        "nextI": words[currentIndex]["i"],
                        "ease": words[currentIndex]["ef"],
                        "timeSpent": round(afterWordTime-beforeWordTime, 1)
                    })

                    toRepeat.remove(currentIndex)

                if currentIndex in notCorrect:
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
                        "timeSpent": round(afterWordTime-beforeWordTime, 1)
                    })

                    notCorrect.remove(currentIndex)

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
                    "timeSpent": round(afterWordTime-beforeWordTime, 1)
                })

                if currentIndex in toRepeat:
                    notCorrect.append(currentIndex)
                    toRepeat.remove(currentIndex)

        print()

        if len(notCorrect+toRepeat) == 0:
            print("All words repeated.")

            _ = input()
            return words, settings, logs


def showLogs(words, logs):
    while True:
        clear()
        print("0. Exit")
        print("1. Words daily")
        print("2. Words type daily.")
        print("3. Words from previous day daily.")
        print("4. Accuracy daily")
        print("5. Accuracy hours")
        print("6. Word types")
        print("7. Ease factor")

        answer = input()

        if answer == "0":
            break

        elif answer == "1":
            log = {}
            d0 = (int(time.time())+SECONDS_DIFFERENCE)//(3600*24)

            for i in logs:
                day = str(int((i["time"]+SECONDS_DIFFERENCE)//(3600*24)-d0))

                if day not in log.keys():
                    log[day] = [[], []]

                if i["wordIndex"] not in log[day][0] and i["count"] == 1 and i["nextI"] == 0:
                    log[day][0].append(i["wordIndex"])

                elif i["nextI"] > 0 and i["wordIndex"] not in log[day][1]:
                    log[day][1].append(i["wordIndex"])

            log2 = {}

            for j, i in enumerate(words):
                day = str(int((i["date"]+SECONDS_DIFFERENCE)//(3600*24)-d0))

                if int(day) >= 0:
                    if day not in log2.keys():
                        log2[day] = []

                    log2[day].append(j)

            old = []
            new = []
            toRepeat = []

            days = list(log.keys())+list(log2.keys())

            if days.count("0") > 1:
                days.remove("0")

            days = [int(i) for i in days]
            days.sort()

            for i in range(days[0], days[-1]):
                if i not in days:
                    days.append(i)

            days.sort()
            days = [str(i) for i in days]

            for i in days:
                if i in log.keys():
                    old.append(len(log[i][1]))
                    new.append(len(log[i][0]))

                else:
                    old.append(0)
                    new.append(0)

                if i in log2.keys():
                    toRepeat.append(len(log2[i]))

                else:
                    toRepeat.append(0)

            fig, ax = plt.subplots()
            tickNumber = int(len(days)/10)
            ticks = []

            if not tickNumber:
                tickNumber = 1

            for i in days:
                if int(i) % tickNumber == 0:
                    ticks.append(i)

                else:
                    ticks.append("")

            ax.bar(days, new, label="new words")
            ax.bar(days, old, label="repeated words", bottom=new)
            ax.bar(days, toRepeat, label="repeat in future", bottom=[
                   new[i]+old[i] for i in range(len(days))], tick_label=ticks)

            ax.legend()

        elif answer == "2":
            log = {}
            wordsLog = {}
            d0 = (int(time.time())+SECONDS_DIFFERENCE)//(3600*24)

            for i in logs:
                day = str(int((i["time"]+SECONDS_DIFFERENCE)//(3600*24)-d0))

                if day not in log.keys():
                    log[day] = []

                if i["wordIndex"] not in wordsLog:
                    wordsLog[i["wordIndex"]] = {
                        "array": [], "index": 0, "streak": 0}

                if i["correct"] == 1 and i["count"] > 1:
                    log[day].append(i["wordIndex"])
                    wordsLog[i["wordIndex"]]["array"].append(i["count"])

            for i in log.keys():
                log[i].sort()

            for i in log.keys():
                for j in range(len(log[i])):
                    if wordsLog[log[i][j]]["index"] == 0:
                        wordsLog[log[i][j]]["streak"] = 1
                        value = 0

                    else:
                        if wordsLog[log[i][j]]["array"][wordsLog[log[i][j]]["index"]] - wordsLog[log[i][j]]["array"][wordsLog[log[i][j]]["index"]-1] > 1:
                            value = wordsLog[log[i][j]]["streak"]
                            wordsLog[log[i][j]]["streak"] = 0

                        else:
                            value = wordsLog[log[i][j]]["streak"]
                            wordsLog[log[i][j]]["streak"] += 1

                    wordsLog[log[i][j]]["index"] += 1
                    log[i][j] = value

            days = [int(i) for i in log.keys()]
            firstDay = min(days)*-1
            toShow = []

            for i in range(firstDay+1):
                toShow.append([0, 0, 0, 0, 0, 0])

            for i in days:
                for j in log[str(i)]:
                    if j > 4:
                        toShow[i+firstDay][5] += 1

                    else:
                        toShow[i+firstDay][j] += 1

            fig, ax = plt.subplots()
            tickNumber = int(len(days)/10)
            ticks = []

            if not tickNumber:
                tickNumber = 1

            for i in days:
                if int(i) % tickNumber == 0:
                    ticks.append(i)

                else:
                    ticks.append("")

            if len(toShow) > len(days):
                toShow.pop()

            ax.bar(days, [i[0] for i in toShow], label="0")
            ax.bar(days, [i[1] for i in toShow], label="1",
                   bottom=[i[0] for i in toShow])
            ax.bar(days, [i[2] for i in toShow], label="2",
                   bottom=[i[0]+i[1] for i in toShow])
            ax.bar(days, [i[3] for i in toShow], label="3",
                   bottom=[i[0]+i[1]+i[2] for i in toShow])
            ax.bar(days, [i[4] for i in toShow], label="4",
                   bottom=[i[0]+i[1]+i[2]+i[3] for i in toShow])
            ax.bar(days, [i[5] for i in toShow], label=">4", bottom=[
                   i[0]+i[1]+i[2]+i[3]+i[4] for i in toShow])

            ax.legend()

        elif answer == "3":
            log = {}
            wordsLog = {}
            d0 = (int(time.time())+SECONDS_DIFFERENCE)//(3600*24)

            for i in logs:
                day = str(int((i["time"]+SECONDS_DIFFERENCE)//(3600*24)-d0))

                if day not in log.keys():
                    log[day] = []

                if i["correct"] == 1 and i["count"] > 1:
                    log[day].append(i["wordIndex"])

            for i in log.keys():
                log[i].sort()

            for i in log.keys():
                for j in log[i]:
                    if j not in wordsLog:
                        wordsLog[j] = []

                    wordsLog[j].append(int(i))

            days = [int(i) for i in log.keys()]
            previous = {}

            for i in days:
                previous[str(i)] = []

            for i in wordsLog.keys():
                count = 0
                for j in range(len(wordsLog[i])):
                    if j != 0:
                        if wordsLog[i][j-1]+1 == wordsLog[i][j]:
                            count += 1

                        else:
                            count = 0

                    previous[str(wordsLog[i][j])].append(count)

            firstDay = min(days)*-1
            toShow = []

            for i in range(firstDay+1):
                toShow.append([0, 0, 0, 0, 0, 0])

            for i in days:
                for j in previous[str(i)]:
                    if j > 4:
                        toShow[i+firstDay][5] += 1

                    else:
                        toShow[i+firstDay][j] += 1

            fig, ax = plt.subplots()
            tickNumber = int(len(days)/10)
            ticks = []

            if not tickNumber:
                tickNumber = 1

            for i in days:
                if int(i) % tickNumber == 0:
                    ticks.append(i)

                else:
                    ticks.append("")

            if len(toShow) > len(days):
                toShow.pop()

            ax.bar(days, [i[0] for i in toShow], label="0")
            ax.bar(days, [i[1] for i in toShow], label="1",
                   bottom=[i[0] for i in toShow])
            ax.bar(days, [i[2] for i in toShow], label="2",
                   bottom=[i[0]+i[1] for i in toShow])
            ax.bar(days, [i[3] for i in toShow], label="3",
                   bottom=[i[0]+i[1]+i[2] for i in toShow])
            ax.bar(days, [i[4] for i in toShow], label="4",
                   bottom=[i[0]+i[1]+i[2]+i[3] for i in toShow])
            ax.bar(days, [i[5] for i in toShow], label=">4", bottom=[
                   i[0]+i[1]+i[2]+i[3]+i[4] for i in toShow])

            ax.legend()

        elif answer == "4":
            log = {}
            d0 = (logs[0]["time"]+SECONDS_DIFFERENCE)//(3600*24)

            for i in logs:
                day = str(int((i["time"]+SECONDS_DIFFERENCE)//(3600*24)-d0))

                if day not in log.keys():
                    log[day] = []

                log[day].append(i["correct"])

            days = []
            toShow = []

            for i in log.keys():
                days.append(int(i))
                toShow.append(log[i].count(
                    1)/(log[i].count(1)+log[i].count(0)))

            for i in range(max(days)):
                if i not in days:
                    days.append(i)
                    toShow.append(0)

            toShow = [x for _, x in sorted(zip(days, toShow))]
            days.sort()
            tickNumber = int(len(days)/5)
            ticks = []

            if not tickNumber:
                tickNumber = 1

            for i in days:
                if i % tickNumber == 0:
                    ticks.append(i)

                else:
                    ticks.append("")

            avg7 = []
            avg3 = []

            for i in range(len(toShow)):
                avg3.append(sum(toShow[max(0, i-2):i+1])/min(i+1, 3))
                avg7.append(sum(toShow[max(0, i-6):i+1])/min(i+1, 7))

            fig, ax = plt.subplots()

            ax.plot(days, avg3, label="3 day average", color='red')
            ax.plot(days, avg7, label="7 day average", color='green')
            ax.bar(days, toShow, tick_label=ticks, label="accuracy daily")

            ax.legend()

        elif answer == "5":
            log = {}

            for i in range(96):
                log[i] = []

            for i in logs:
                log[(i["time"]+SECONDS_DIFFERENCE) %
                    (3600*24)//900].append(i["correct"])

            toShow = []
            hrs = []

            for i in log.keys():
                if i % 4 == 0:
                    hrs.append("{}:00".format(i//4))

                else:
                    hrs.append("{}:{}".format(i//4, 15*(i % 4)))

                if len(log[i]) > 0:
                    toShow.append(log[i].count(
                        1)/(log[i].count(0)+log[i].count(1)))

                else:
                    toShow.append(0)

            hrsToShow = []

            for i, j in enumerate(hrs):
                if i % 2 == 0:
                    hrsToShow.append(j)
                else:
                    hrsToShow.append("")

            fig, ax = plt.subplots()
            plt.xticks(rotation=90)

            ax.bar(hrs, toShow, label="accuracy hourly", tick_label=hrsToShow)

            ax.legend()

        elif answer == "6":
            toShow = ["1", "2", "3", "4", "5+"]
            toShowData = [0, 0, 0, 0, 0]

            for i in words:
                if i["n"] == 1:
                    toShowData[0] += 1

                elif i["n"] == 2:
                    toShowData[1] += 1

                elif i["n"] == 3:
                    toShowData[2] += 1

                elif i["n"] == 4:
                    toShowData[3] += 1

                elif i["n"] > 4:
                    toShowData[4] += 1

            fig, ax = plt.subplots()

            for i in range(len(toShow)):
                ax.bar(toShow[i], toShowData[i])

        elif answer == "7":
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

            fig, ax = plt.subplots()

            ax.bar([str(i) for i in toShow], toShowData)

        plt.show()


def main():
    """Main function."""

    with open("data.json", "r") as rd:
        data = json.load(rd)
        words = data["words"]
        settings = data["settings"]
        logs = data["logs"]

    allFiles = listdir('saves')

    try:
        if (int(allFiles[-1].split("-")[1].strip(".json"))+SECONDS_DIFFERENCE)//(3600*24) != int((time.time()+SECONDS_DIFFERENCE)//(24*3600)):
            with open("saves/dataSave-{}.json".format(int(time.time())), "w") as sv:
                json.dump(data, sv)
    except:
        with open("saves/dataSave-{}.json".format(int(time.time())), "w") as sv:
            json.dump(data, sv)

    today = time.localtime()

    if today.tm_mday != settings["date"][2] or today.tm_mon != settings["date"][1]:
        settings["date"] = today
        settings["words"] = 0

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
            words, settings, logs = learnNewWords(words, settings, logs)

        elif dec == "2":
            words, settings, logs = repeat(words, settings, logs)

        elif dec == "3":
            showLogs(words, logs)

    with open("data.json", "w") as sv:
        data["words"] = words
        data["settings"] = settings
        data["logs"] = logs
        json.dump(data, sv)


main()
