import time
import json
import random
from os import system, name
import matplotlib.pyplot as plt

def clear(): 

    if name == 'nt': 
        _ = system('cls')  
    else: 
        _ = system('clear')

def superMemo(answerQuality:int, currentStreak:int, easeRatio:float, interval:int):

    if answerQuality == 1:
        if currentStreak == 0:
            interval = 1
        elif currentStreak == 1:
            interval = 6
        else:
            interval = interval*easeRatio

        easeRatio = easeRatio+0.2
        if easeRatio < 1.3:
            easeRatio = 1.3
            
        currentStreak += 1

    else:
        currentStreak = 0
        interval = 1
        easeRatio -= 0.1

    return currentStreak, easeRatio, interval

def learnNewWords(words, settings, logs):

    clear()

    wordsToLearn = []
    wordIndex = 0
    while len(wordsToLearn) < settings["maxWords"]:
        if words[wordIndex]["count"] == 0:
            wordsToLearn.append(wordIndex)

        wordIndex+=1
        if wordIndex==len(words):
            break

    isLastCorrect = True
    while True:

        clear()

        print("To learn: {}\n".format(len(wordsToLearn)))
        print("===\n\n")
        
        if isLastCorrect:
            currentIndex = random.choice(wordsToLearn)
            currentWord = words[currentIndex]
        print("Word: " + currentWord["han"])
        print()
        print("Translation: " + currentWord["eng"])
        print()
        t1 = time.time()
        lastWord = input("Repeat: ")
        t2 = time.time()
        print()
        if lastWord == currentWord["han"].split("(")[0]:
            print("Correct!")
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
                "timeSpent": round(t2-t1, 1)
            })
            wordsToLearn.remove(currentIndex)
            a = input()
        else:
            words[currentIndex]["count"] += 1
            words[currentIndex]["ef"] -= 0.1
            if words[currentIndex]["ef"] < 2:
                words[currentIndex]["ef"] = 2
            print("Incorrect!")
            logs.append({
                "wordIndex": currentIndex,
                "correct": 0,
                "time": int(time.time()),
                "count": words[currentIndex]["count"],
                "nextI": 0,
                "ease": words[currentIndex]["ef"],
                "timeSpent": round(t2-t1, 1)
            })
            isLastCorrect = False
            a = input()
        print()
        if len(wordsToLearn) == 0:
            print("===")
            print("Learning has ended.")
            a = input()
            return words, settings, logs

def repeat(words, settings, logs):
    clear()
    toRepeat = []
    toRepeatToday = []
    now = time.time()
    toEnd = now+3600*4
    for i in range(len(words)):
        if words[i]["date"] < now and words[i]["date"] != 0:
            toRepeat.append(i)
        elif words[i]["date"] > now and words[i]["date"]<toEnd:
            toRepeatToday.append(i)
    if not toRepeat:
        firstWord = words[0]["date"]
        for i in range(1, len(words)):
            if words[i]["date"] < firstWord and words[i]["date"] != 0:
                firstWord = words[i]["date"]
        firstWordTime = time.localtime(firstWord)
        date = [firstWordTime.tm_mday, firstWordTime.tm_mon, firstWordTime.tm_hour, firstWordTime.tm_min]
        if len(str(date[1])) == 1:
            date[1] = "0" + str(date[1])
        if len(str(date[3])) == 1:
            date[3] = "0" + str(date[3])
    notCorrect = []
    if len(toRepeat) == 0:
        print("No words to repeat.\nFirst word to repeat at: {}.{} - {}:{}\nThere is {} to repeat today.".format(date[0], date[1], date[2], date[3], len(toRepeatToday)))
        print("Do you want to repeat them earlier? (Y/N)")
        a = input()
        if a == "Y":
            toRepeat = toRepeatToday
        else:
            return words, settings, logs
    while True:
        clear()
        print("Words to repeat: {}".format(len(notCorrect+toRepeat)))
        print()
        currentIndex = random.choice(toRepeat+notCorrect)
        currentWord = words[currentIndex]
        print("===\n (0. to exit)\n")
        print("Word: " + currentWord["eng"] + "\n")
        t1 = time.time()
        answer = input("Translation: ")
        t2 = time.time()
        print()
        if answer == "0":
            return words, settings, logs
        elif answer == currentWord["han"].split("(")[0] and currentIndex in toRepeat:
            print("Correct!")
            words[currentIndex]["n"], words[currentIndex]["ef"], words[currentIndex]["i"] = superMemo(1, currentWord["n"], currentWord["ef"], currentWord["i"])
            words[currentIndex]["date"] = int(time.time())+words[currentIndex]["i"]*24*3600
            words[currentIndex]["count"] += 1
            logs.append({
                "wordIndex": currentIndex,
                "correct": 1,
                "time": int(time.time()),
                "count": words[currentIndex]["count"],
                "nextI": words[currentIndex]["i"],
                "ease": words[currentIndex]["ef"],
                "timeSpent": round(t2-t1, 1)
            })
            toRepeat.remove(currentIndex)
            a = input()
        elif answer == currentWord["han"].split("(")[0] and currentIndex in notCorrect:
            print("Correct!")
            words[currentIndex]["n"], words[currentIndex]["ef"], _ = superMemo(1, currentWord["n"], currentWord["ef"], currentWord["i"])
            words[currentIndex]["count"] += 1
            logs.append({
                "wordIndex": currentIndex,
                "correct": 1,
                "time": int(time.time()),
                "count": words[currentIndex]["count"],
                "nextI": words[currentIndex]["i"],
                "ease": words[currentIndex]["ef"],
                "timeSpent": round(t2-t1, 1)
            })
            notCorrect.remove(currentIndex)
            a = input()
        else:
            print("Incorrect!")
            print()
            print("Correct answer: " + currentWord["han"])
            really = input()
            if really == "`":
                if currentIndex in toRepeat:
                    words[currentIndex]["n"], words[currentIndex]["ef"], words[currentIndex]["i"] = superMemo(1, currentWord["n"], currentWord["ef"], currentWord["i"])
                    words[currentIndex]["date"] = int(time.time())+words[currentIndex]["i"]*24*3600
                    words[currentIndex]["count"] += 1
                    logs.append({
                        "wordIndex": currentIndex,
                        "correct": 1,
                        "time": int(time.time()),
                        "count": words[currentIndex]["count"],
                        "nextI": words[currentIndex]["i"],
                        "ease": words[currentIndex]["ef"],
                        "timeSpent": round(t2-t1, 1)
                    })
                    toRepeat.remove(currentIndex)
                if currentIndex in notCorrect:
                    words[currentIndex]["n"], words[currentIndex]["ef"], _ = superMemo(1, currentWord["n"], currentWord["ef"], currentWord["i"])
                    words[currentIndex]["count"] += 1
                    logs.append({
                        "wordIndex": currentIndex,
                        "correct": 1,
                        "time": int(time.time()),
                        "count": words[currentIndex]["count"],
                        "nextI": words[currentIndex]["i"],
                        "ease": words[currentIndex]["ef"],
                        "timeSpent": round(t2-t1, 1)
                    })
                    notCorrect.remove(currentIndex)
            else:   
                words[currentIndex]["n"], words[currentIndex]["ef"], words[currentIndex]["i"] = superMemo(0, currentWord["n"], currentWord["ef"], currentWord["i"])
                words[currentIndex]["date"] = int(time.time())+words[currentIndex]["i"]*24*3600
                words[currentIndex]["count"] += 1
                logs.append({
                    "wordIndex": currentIndex,
                    "correct": 0,
                    "time": int(time.time()),
                    "count": words[currentIndex]["count"],
                    "nextI": words[currentIndex]["i"],
                    "ease": words[currentIndex]["ef"],
                    "timeSpent": round(t2-t1, 1)
                })
                if currentIndex in toRepeat:
                    notCorrect.append(currentIndex)
                    toRepeat.remove(currentIndex)
        print()
        if len(notCorrect+toRepeat) == 0:
            print("All words repeated.")
            a = input()
            return words, settings, logs

def showLogs(logs):
    clear()
    print("0. Exit")
    print("1. Words daily")
    print("2. Words hours")
    print("3. Accuracy daily")
    print("4. Accuracy hours")
    print("5. Time daily")
    print("6. Time hours")
    answer = input()
    if answer == "0":
        pass
    elif answer == "1":
        log = {}
        d0 = (int(time.time())+7200)//(3600*24)
        for i in logs:
            day = str(int((i["time"]+7200)//(3600*24)-d0))
            if day not in log.keys():
                log[day] = [[], []]
            if i["wordIndex"] not in log[day][0] and i["count"]==1 and i["nextI"] == 0:
                log[day][0].append(i["wordIndex"])
            elif i["nextI"] > 0 and i["wordIndex"] not in log[day][1]:
                log[day][1].append(i["wordIndex"])

        log2 = {}
        for j, i in enumerate(words):
            day = str(int((i["date"]+7200)//(3600*24)-d0))
            
            if int(day)>=0:
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
        if not tickNumber:
            tickNumber = 1
        ticks = []
        for i in days:
            if int(i)%tickNumber==0:
                ticks.append(i)
            else:
                ticks.append("")

        ax.bar(days, new, label="new words")
        ax.bar(days, old, label="repeated words", bottom=new)
        ax.bar(days, toRepeat, label="repeat in future", bottom=[new[i]+old[i] for i in range(len(days))], tick_label=ticks)
        ax.legend()
    elif answer == "3":
        log = {}
        d0 = (logs[0]["time"]+7200)//(3600*24)
        for i in logs:
            day = str(int((i["time"]+7200)//(3600*24)-d0))
            if day not in log.keys():
                log[day] = []
            log[day].append(i["correct"])
        days = []
        toShow = []

        for i in log.keys():
            days.append(int(i))
            toShow.append(log[i].count(1)/(log[i].count(1)+log[i].count(0)))

        for i in range(max(days)):
            if i not in days:
                days.append(i)
                toShow.append(0)

        toShow = [x for _,x in sorted(zip(days, toShow))]
        days.sort()
        tickNumber = int(len(days)/5)
        if not tickNumber:
            tickNumber = 1
        ticks = []
        for i in days:
            if i%tickNumber==0:
                ticks.append(i)
            else:
                ticks.append("")

        fig, ax = plt.subplots()
        ax.bar(days, toShow, tick_label=ticks, label="accuracy daily")
        ax.legend()
    elif answer == "4":
        log = {}
        for i in range(96):
            log[i] = []
        for i in logs:
            log[(i["time"]+7200)%(3600*24)//900].append(i["correct"])
        toShow = []
        hrs = []
        for i in log.keys():
            if i%4 == 0:
                hrs.append("{}:00".format(i//4))
            else:    
                hrs.append("{}:{}".format(i//4, 15*(i%4)))
            if len(log[i]) > 0:
                toShow.append(log[i].count(1)/(log[i].count(0)+log[i].count(1)))
            else:
                toShow.append(0)
        hrsToShow = []
        for i, j in enumerate(hrs):
            if i%2==0:
                hrsToShow.append(j)
            else:
                hrsToShow.append("")
        fig, ax = plt.subplots()
        plt.xticks(rotation=90)
        ax.bar(hrs, toShow, label="accuracy hourly", tick_label=hrsToShow)
        ax.legend()
    plt.show()
        
    a = input()

with open("data.json", "r") as rd:
    data = json.load(rd)
    words = data["words"]
    settings = data["settings"]
    logs = data["logs"]

today = time.localtime()

if today.tm_mday != settings["today"]["date"][2] or today.tm_mon != settings["today"]["date"][1]:
    settings["today"]["date"] = today
    settings["today"]["words"] = 0

while True:
    clear()
    print("0. Exit")
    print("1. Learn")
    print("2. Repeat")
    print("3. Logs")
    dec = input()
    if dec == "0":
        break
    elif dec == "1":
        words, settings, logs = learnNewWords(words, settings, logs)
    elif dec == "2":
        words, settings, logs = repeat(words, settings, logs)
    elif dec == "3":
        showLogs(logs)

with open("data.json", "w") as sv:
    data["words"] = words
    data["settings"] = settings
    data["logs"] = logs
    data = json.dump(data, sv)