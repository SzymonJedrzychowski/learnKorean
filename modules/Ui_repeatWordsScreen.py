from PyQt5 import QtCore, QtGui, QtWidgets
from modules import playControl, superMemo
from modules.clickableLabel import QLabelClickable
import time
import random


class Ui_repeatWordsScreen(object):
    """Screent to repeat words"""
    
    def setupUi(self, mainScreen, **kwargs):
        self.screenName = "repeatWordsScreen"
        self.mainScreen = mainScreen
        self.data = self.mainScreen.data

        self.wordToShow = None
        self.secondsDifference = time.localtime().tm_gmtoff
        self.beingPressed = False
        self.playControl = playControl.playControl()

        # Create layout for the screen: start
        self.mainScreen.setObjectName("mainScreen")
        self.mainScreen.setWindowModality(QtCore.Qt.NonModal)
        self.centralwidget = QtWidgets.QWidget(self.mainScreen)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(30, 30, 30, 30)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.englishWordLabel = QtWidgets.QLabel(self.centralwidget)
        self.englishWordLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.englishWordLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.englishWordLabel.setWordWrap(True)
        self.englishWordLabel.setObjectName("englishWordLabel")
        self.horizontalLayout_3.addWidget(self.englishWordLabel)

        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)

        self.koreanWordLabel = QLabelClickable(self.centralwidget)
        self.koreanWordLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.koreanWordLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.koreanWordLabel.setWordWrap(True)
        self.koreanWordLabel.setObjectName("koreanWordLabel")
        self.horizontalLayout_3.addWidget(self.koreanWordLabel)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setMinimumSize(QtCore.QSize(350, 0))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)

        self.submitButton = QtWidgets.QPushButton(self.centralwidget)
        self.submitButton.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.submitButton.setFont(font)
        self.submitButton.setObjectName("submitButton")
        self.horizontalLayout.addWidget(self.submitButton)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.wordsLeftLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.wordsLeftLabel.setFont(font)
        self.wordsLeftLabel.setObjectName("wordsLeftLabel")
        self.horizontalLayout_5.addWidget(self.wordsLeftLabel)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.correctButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.correctButton.setFont(font)
        self.correctButton.setObjectName("correctButton")
        self.verticalLayout_3.addWidget(self.correctButton)

        self.returnButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.returnButton.setFont(font)
        self.returnButton.setObjectName("returnButton")
        self.verticalLayout_3.addWidget(self.returnButton)

        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 4)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.mainScreen.setCentralWidget(self.centralwidget)
        # Create layout for the screen: end

        # Assign functions to buttons
        self.submitButton.clicked.connect(self.submitWord)
        self.correctButton.clicked.connect(self.correctWord)
        self.koreanWordLabel.clicked.connect(self.playCurrentWord)
        self.returnButton.clicked.connect(self.mainScreen.close)

        # Get words to repeat
        self.wordsToRepeat = self.getWordsToRepeat()

        self.retranslateUi(self.mainScreen)
        QtCore.QMetaObject.connectSlotsByName(self.mainScreen)

        # Assign shortcuts to buttons
        self.submitButton.setShortcut("Return")
        self.correctButton.setShortcut("Ctrl+`")
        self.returnButton.setShortcut("Ctrl+Q")

        # Set the first word
        self.setWord()

    def playCurrentWord(self):
        """Play clicked word"""

        koreanWord = self.koreanWordLabel.text()
        if koreanWord != "":
            self.playControl.playSound("data/sounds/{}.mp3".format(koreanWord))

    def getWordsToRepeat(self):
        """Get words that need to be repeated today

        :return list(): list of words to repeat
        """

        wordsToRepeat = []
        currentTime = time.time()

        toEnd = currentTime+self.secondsDifference+3600 * \
            (24-((currentTime+self.secondsDifference)/3600) % 24)

        for i in range(len(self.data["words"])):
            if self.data["words"][i]["count"] == 0:
                break

            if (self.data["words"][i]["date"]+self.data["words"][i]["localTime"] < currentTime and self.data["words"][i]["date"] != 0) or self.data["words"][i]["date"]+self.data["words"][i]["localTime"] < toEnd:
                wordsToRepeat.append(i)

        return wordsToRepeat

    def setWord(self):
        """Set new word to repeat"""

        if self.wordsToRepeat:
            self.wordToShow = random.choice(self.wordsToRepeat)
            self.englishWordLabel.setText(
                self.data["words"][self.wordToShow]["eng"])
            self.koreanWordLabel.setText("")
        else:
            self.englishWordLabel.setText("All words were repeated")
            self.englishWordLabel.setStyleSheet(
                "color: rgb(97, 224, 65); font-size: 18pt")
            self.koreanWordLabel.setText("All words were repeated")
            self.koreanWordLabel.setStyleSheet(
                "color: rgb(97, 224, 65); font-size: 18pt")
            self.wordToShow = None
            self.lineEdit.setEnabled(False)

    def submitWord(self):
        """Submit word"""

        if self.wordToShow == None:
            return

        if not self.beingPressed:
            self.beingPressed = True
            if self.submitButton.text() == "Next":
                self.submitButton.setText("Submit")
                self.lineEdit.setText("")
                self.lineEdit.setStyleSheet(
                    "background: rgb(255, 255, 255); font-size: 18pt")
                self.submitButton.setShortcut("Return")
                self.setWord()
                self.beingPressed = False
                return
            elif self.submitButton.text() == "Repeat":
                word = self.data["words"][self.wordToShow]
                input = self.lineEdit.text()
                if word["han"].split("(")[0] == input:

                    self.data["words"][self.wordToShow] = superMemo.superMemo(
                        0, word)

                    self.data["logs"].append({
                        "wordIndex": self.wordToShow,
                        "correct": 0,
                        "time": int(time.time()),
                        "count": self.data["words"][self.wordToShow]["count"],
                        "nextI": self.data["words"][self.wordToShow]["i"],
                        "ease": self.data["words"][self.wordToShow]["ef"],
                        "localTime": self.secondsDifference,
                        "currentStreak": 0
                    })

                    self.submitButton.setText("Next")
                    self.lineEdit.setStyleSheet(
                        "background: rgb(97, 224, 65); font-size: 18pt")
                    self.submitButton.setShortcut("Return")
                else:
                    self.lineEdit.setText("")
                    self.playControl.playSound(
                        "data/sounds/{}.mp3".format(word["han"]))

            elif self.submitButton.text() == "Submit":
                word = self.data["words"][self.wordToShow]
                input = self.lineEdit.text()
                if word["han"].split("(")[0] == input:

                    self.data["words"][self.wordToShow] = superMemo.superMemo(
                        1, word)

                    self.data["logs"].append({
                        "wordIndex": self.wordToShow,
                        "correct": 1,
                        "time": int(time.time()),
                        "count": self.data["words"][self.wordToShow]["count"],
                        "nextI": self.data["words"][self.wordToShow]["i"],
                        "ease": self.data["words"][self.wordToShow]["ef"],
                        "localTime": self.secondsDifference,
                        "currentStreak": self.data["words"][self.wordToShow]["n"]
                    })

                    self.wordsLeftLabel.setText(
                        "Words left: {}".format(len(self.wordsToRepeat)-1))

                    self.submitButton.setText("Next")
                    self.koreanWordLabel.setText(word["han"])
                    self.lineEdit.setStyleSheet(
                        "background: rgb(97, 224, 65); font-size: 18pt")
                    self.submitButton.setShortcut("Return")

                    self.wordsToRepeat.remove(self.wordToShow)
                    self.playControl.playSound(
                        "data/sounds/{}.mp3".format(word["han"]))
                else:
                    self.submitButton.setText("Repeat")
                    self.koreanWordLabel.setText(word["han"])
                    self.lineEdit.setText("")
                    self.lineEdit.setStyleSheet(
                        "background: rgb(247, 81, 52); font-size: 18pt")
                    self.submitButton.setShortcut("Return")
                    self.playControl.playSound(
                        "data/sounds/{}.mp3".format(word["han"]))

            self.beingPressed = False

    def correctWord(self):
        """Correct the word"""
        if self.submitButton.text() == "Repeat":
            word = self.data["words"][self.wordToShow]
            self.data["words"][self.wordToShow] = superMemo.superMemo(
                1, word)

            self.data["logs"].append({
                "wordIndex": self.wordToShow,
                "correct": 1,
                "time": int(time.time()),
                "count": self.data["words"][self.wordToShow]["count"],
                "nextI": self.data["words"][self.wordToShow]["i"],
                "ease": self.data["words"][self.wordToShow]["ef"],
                "localTime": self.secondsDifference,
                "currentStreak": self.data["words"][self.wordToShow]["n"]
            })

            self.wordsToRepeat.remove(self.wordToShow)
            self.wordsLeftLabel.setText(
                "Words left: {}".format(len(self.wordsToRepeat)))

            self.submitButton.setText("Next")
            self.lineEdit.setStyleSheet(
                "background: rgb(97, 224, 65); font-size: 18pt")
            self.submitButton.setShortcut("Return")

    def retranslateUi(self, mainScreen):
        _translate = QtCore.QCoreApplication.translate
        mainScreen.setWindowTitle(_translate("mainScreen", "Repeat words"))
        self.label.setText(_translate("mainScreen", "Repeat words"))
        self.englishWordLabel.setText(_translate("mainScreen", "English word"))
        self.koreanWordLabel.setText(_translate("mainScreen", "Korean word"))
        self.submitButton.setText(_translate("mainScreen", "Submit"))
        self.wordsLeftLabel.setText(_translate(
            "mainScreen", "Words left: {}".format(len(self.wordsToRepeat))))
        self.correctButton.setText(_translate("mainScreen", "Correct"))
        self.returnButton.setText(_translate("mainScreen", "Return"))
