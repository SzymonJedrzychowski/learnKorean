import json
import time
import os
from modules import Ui_mainMenu, Ui_learnWordsScreen, Ui_repeatLearnedWordsScreen, Ui_repeatWordsScreen, Ui_viewLogsScreen, Ui_graphScreen, Ui_searchWordsScreen, Ui_modifySetScreen,  Ui_addWordsScreen, Ui_removeWordsScreen, Ui_modifyWordsScreen, Ui_quitScreen
from modules import fileOperations
from PyQt5 import QtWidgets, QtCore
from functools import partial
from gtts import gTTS


class mainScreen(QtWidgets.QMainWindow):
    """Main screen for the application that will be changed to other screens"""

    def __init__(self, parent=None):
        super(mainScreen, self).__init__(parent)
        self.currentScreenName = None
        self.data = None
        self.previousSaveLenghts = [0, 0, False]
        self.logsSaveLogsLength = 0
        self.graphLimits = None

        # Screens used in the application
        self.mainMenuScreen = Ui_mainMenu.Ui_mainMenu()
        self.learnWordsScreen = Ui_learnWordsScreen.Ui_learnWordsScreen()
        self.repeatLearnedScreen = Ui_repeatLearnedWordsScreen.Ui_repeatLearnedWordsScreen()
        self.repeatScreen = Ui_repeatWordsScreen.Ui_repeatWordsScreen()
        self.viewLogsScreen = Ui_viewLogsScreen.Ui_viewLogsScreen()
        self.graphScreen = Ui_graphScreen.Ui_graphScreen()
        self.searchWordsScreen = Ui_searchWordsScreen.Ui_searchWordsScreen()
        self.modifySetScreen = Ui_modifySetScreen.Ui_modifySetScreen()
        self.addWordsScreen = Ui_addWordsScreen.Ui_addWordsScreen()
        self.removeWordsScreen = Ui_removeWordsScreen.Ui_removeWordsScreen()
        self.modifyWordsScreen = Ui_modifyWordsScreen.Ui_modifyWordsScreen()
        self.quitScreen = Ui_quitScreen.Ui_quitScreen()

        # Check if directories are present and create empty ones if they are missing
        self.checkDirectories()

        # Loading data
        self.loadData()

        # Create missing sounds
        self.createSounds()

        # Starting with main menu screen
        self.useScreen(self.mainMenuScreen, data=self.data)

    def checkDirectories(self):
        """Check if necessary directories are present, if not create empty ones"""

        if os.path.isdir("data"):
            if not os.path.isdir("data/json"):
                os.mkdir("data/json")
                print("[DIRECTORY: {}]      Directory data/json was created".format(
                    time.strftime("%H:%M:%S")))
            if not os.path.isdir("data/sounds"):
                os.mkdir("data/sounds")
                print("[DIRECTORY: {}]      Directory data/sounds was created".format(
                    time.strftime("%H:%M:%S")))
        else:
            os.mkdir("data")
            print("[DIRECTORY: {}]      Directory data was created".format(
                time.strftime("%H:%M:%S")))
            os.mkdir("data/json")
            print("[DIRECTORY: {}]      Directory data/json was created".format(
                time.strftime("%H:%M:%S")))
            os.mkdir("data/sounds")
            print("[DIRECTORY: {}]      Directory data/sounds was created".format(
                time.strftime("%H:%M:%S")))

    def loadData(self):
        """Load data from local file and compare it to online one"""

        # Check if file data.json exists
        if os.path.isfile("data/json/data.json"):
            with open("data/json/data.json") as f:
                data = json.load(f)
        else:
            # Create file with 0 time to download new file
            data = {"time": 0}
            with open("data/json/data.json", "w") as f:
                json.dump(data, f)

        # Try downloading new file from discord
        try:
            result = fileOperations.load(data["time"])

            if len(result) == 1:
                print("[DATA FILE: {}]      File loaded successfuly".format(
                    time.strftime("%H:%M:%S")))
            elif result[1] == 1:
                print("[DATA FILE: {}]      Data was already up to date".format(
                    time.strftime("%H:%M:%S")))
            else:
                print("[DATA FILE: {}]      Problems with data and time consistency".format(
                    time.strftime("%H:%M:%S")))
                exit()

        except Exception as ex:
            print("[EXCEPTION: {}]      {}".format(
                time.strftime("%H:%M:%S"), ex))
            exit()

        # Load the file again.
        with open("data/json/data.json") as f:
            self.data = json.load(f)

        self.previousSaveLenghts = [
            len(self.data["words"]), len(self.data["logs"]), False]
        self.logsSaveLogsLength = len(self.data["logs"])

    def saveData(self, buttonToChange):
        """Save data and upload it to discord

        :param buttonToChange: object of button which text will be changed during saving process
        """

        buttonToChange.setText("Saving...")
        buttonToChange.repaint()
        try:
            self.data["time"] = int(time.time())

            if len(self.data["logs"]) != self.previousSaveLenghts[1] or len(self.data["words"]) != self.previousSaveLenghts[0] or self.previousSaveLenghts[2]:
                with open("data/json/data.json", "w") as sv:
                    json.dump(self.data, sv)
                fileOperations.save()
                print("[DATA FILE: {}]      Data was saved".format(
                    time.strftime("%H:%M:%S")))
                self.previousSaveLenghts = [
                    len(self.data["words"]), len(self.data["logs"]), False]
                buttonToChange.setText("Saved")
                self.wordModified = False
            else:
                buttonToChange.setText("No data to save")
                print("[DATA FILE: {}]      There was no updates to be saved".format(
                    time.strftime("%H:%M:%S")))
            QtCore.QTimer.singleShot(3000, partial(
                self.changeButtonText, buttonToChange, "Save"))

        except Exception as ex:
            print("[EXCEPTION: {}]      {}".format(
                time.strftime("%H:%M:%S"), ex))

    def createSounds(self):
        """Create missing sounds"""

        wordsLength = len(self.data["words"])
        for i, word in enumerate(self.data["words"]):
            if not os.path.isfile("data/sounds/{}.mp3".format(word["han"])):
                tts = gTTS(word["han"], lang="ko")
                tts.save("data/sounds/{}.mp3".format(word["han"]))
                print("[SOUND FILE: {}]     ({}/{})   Created sound file: {}.mp3".format(
                    time.strftime("%H:%M:%S"), i+1, wordsLength, word["han"]))

    def useScreen(self, screen, **kwargs):
        """Open new screen

        :param screen: object of screen that needs to be used
        """

        screen.setupUi(self, **kwargs)
        self.currentScreenName = screen.screenName
        if self.currentScreenName == "viewLogsScreen":
            self.viewLogsScreen.setGraphLimits()
        elif self.currentScreenName == "graphScreen":
            self.graphLimits = kwargs.get("graphLimits")
            if self.graphLimits[0] != "":
                self.graphLimits[0] = int(self.graphLimits[0])
            if self.graphLimits[1] != "":
                self.graphLimits[1] = int(self.graphLimits[1])

    def saveLogs(self):
        """Modify logsSave after learning or repeating words"""

        d0 = (int(time.time())+time.localtime().tm_gmtoff)//(3600*24)

        firstDay = (self.data["logs"][0]["time"] +
                    self.data["logs"][0]["localTime"])//(3600*24)
        if str(d0-firstDay) not in self.data["logsSave"]:
            self.data["logsSave"][str(d0-firstDay)] = {"1": [0, 0], "2": [0, 0, 0, 0, 0, 0], "3": [
                0, 0, 0, 0, 0, 0], "4": [0, 0], "5": [0, 0, 0, 0, 0]}
        day = "-1"
        for i in self.data["logs"][self.logsSaveLogsLength:]:
            day = str(d0-firstDay)
            # FOR 1
            if i["correct"] != 0:
                if i["count"] == 1:
                    self.data["logsSave"][day]["1"][0] += 1
                else:
                    self.data["logsSave"][day]["1"][1] += 1

            # FOR 2
            if i["count"] != 1 and i["correct"] != 0:
                if i["currentStreak"] < 6:
                    self.data["logsSave"][day]["2"][i["currentStreak"]-1] += 1
                else:
                    self.data["logsSave"][day]["2"][5] += 1

            # FOR 4
            if i["count"] != 1:
                if i["correct"] == 1:
                    self.data["logsSave"][day]["4"][0] += 1
                self.data["logsSave"][day]["4"][1] += 1

        if day == "-1":
            return

        # FOR 5
        self.data["logsSave"][day]["5"] = [0, 0, 0, 0, 0]
        for i in self.data["words"]:
            if i["currentStreak"] != 0:
                self.data["logsSave"][day]["5"][min(
                    i["currentStreak"], 5)-1] += 1

        # FOR 3
        todayWords = {}
        finalTodayWords = {}
        toRemove = []
        for j, i in enumerate(reversed(self.data["logs"])):
            wordDay = (i["time"]+time.localtime().tm_gmtoff)//(3600*24)
            if i["correct"] == 0 or i["count"] == 1:
                continue
            if wordDay == d0:
                if i["wordIndex"] not in todayWords:
                    todayWords[i["wordIndex"]] = [wordDay]
            elif i["wordIndex"] in todayWords:
                if todayWords[i["wordIndex"]][-1] == wordDay+1:
                    todayWords[i["wordIndex"]].append(wordDay)
                else:
                    finalTodayWords[i["wordIndex"]
                                    ] = todayWords[i["wordIndex"]]
                    toRemove = [i["wordIndex"]]
            for l in toRemove:
                del todayWords[l]
                toRemove = []
            if not todayWords and wordDay != d0:
                break

        allDays = [0, 0, 0, 0, 0, 0]
        for i in finalTodayWords:
            allDays[min(len(finalTodayWords[i])-1, 5)] += 1
        self.data["logsSave"][day]["3"] = allDays

        self.logsSaveLogsLength = len(self.data["logs"])

    def checkSoundFiles(self):
        """Remove usused sound files after quiting the app"""

        allWords = set()
        with open("data/json/data.json") as f:
            data = json.load(f)
        for i in data["words"]:
            allWords.add(i["han"]+".mp3")
        for i in os.listdir("data/sounds"):
            if not i in allWords:
                print("[SOUND FILE: {}]     Removing unused sound file: {}".format(
                    time.strftime("%H:%M:%S"), i))
                os.remove("data/sounds/{}".format(i))

    def closeEvent(self, event):
        """Decide next screen after using close/return button"""

        if self.currentScreenName == "repeatLearnedWordsScreen":
            self.useScreen(self.learnWordsScreen, data=self.data)
            event.ignore()
        elif self.currentScreenName == "graphScreen":
            self.useScreen(self.viewLogsScreen, data=self.data)
            event.ignore()
        elif self.currentScreenName in ["addWordsScreen", "removeWordsScreen", "modifyWordsScreen"]:
            self.useScreen(self.modifySetScreen, data=self.data)
            event.ignore()
        elif self.currentScreenName != "mainMenuScreen":
            if self.currentScreenName in ["learnWordsScreen", "repeatWordsScreen"]:
                self.saveLogs()
            elif self.currentScreenName == "viewLogsScreen":
                self.graphLimits = None
            elif self.currentScreenName == "quitScreen":
                self.checkSoundFiles()
                event.accept()
                return
            self.useScreen(self.mainMenuScreen, data=self.data)
            event.ignore()
        else:
            self.useScreen(self.quitScreen)
            event.ignore()

    def changeButtonText(self, buttonToChange, text: str):
        """Change text on button

        :param buttonToChange: button that will get the text changed,
        :param text: new text for the button
        """

        try:
            buttonToChange.setText(text)
        except:
            pass
