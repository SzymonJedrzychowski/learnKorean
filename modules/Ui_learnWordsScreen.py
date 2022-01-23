import time
from PyQt5 import QtCore, QtGui, QtWidgets
from modules import playControl
from modules.clickableLabel import QLabelClickable
from functools import partial


class Ui_learnWordsScreen(object):
    """Screen to learn words"""

    def setupUi(self, mainScreen, **kwargs):
        self.screenName = "learnWordsScreen"
        self.mainScreen = mainScreen
        self.data = mainScreen.data

        self.playControl = playControl.playControl()
        self.secondsDifference = time.localtime().tm_gmtoff
        self.beingPressed = False

        # Create layout for the screen: start
        mainScreen.setObjectName("mainScreen")
        font = QtGui.QFont()
        font.setPointSize(18)
        mainScreen.setFont(font)
        self.centralwidget = QtWidgets.QWidget(mainScreen)
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
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(
            self.label, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")

        self.koreanWordLabel = QLabelClickable(self.centralwidget)
        self.koreanWordLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.koreanWordLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.koreanWordLabel.setWordWrap(True)
        self.koreanWordLabel.setObjectName("koreanWordLabel")
        self.horizontalLayout_7.addWidget(self.koreanWordLabel)

        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)

        self.englishWordLabel = QtWidgets.QLabel(self.centralwidget)
        self.englishWordLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.englishWordLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.englishWordLabel.setWordWrap(True)
        self.englishWordLabel.setObjectName("englishWordLabel")
        self.horizontalLayout_7.addWidget(self.englishWordLabel)

        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setMinimumSize(QtCore.QSize(350, 0))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_6.addWidget(self.lineEdit)

        self.submitButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.submitButton.sizePolicy().hasHeightForWidth())
        self.submitButton.setSizePolicy(sizePolicy)
        self.submitButton.setMinimumSize(QtCore.QSize(150, 0))
        self.submitButton.setObjectName("submitButton")
        self.horizontalLayout_6.addWidget(self.submitButton)

        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.todayLearnedLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.todayLearnedLabel.setFont(font)
        self.todayLearnedLabel.setObjectName("todayLearnedLabel")
        self.horizontalLayout.addWidget(self.todayLearnedLabel)

        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.repeatWordsButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.repeatWordsButton.setFont(font)
        self.repeatWordsButton.setObjectName("repeatWordsButton")
        self.verticalLayout_4.addWidget(self.repeatWordsButton)

        self.returnButton = QtWidgets.QPushButton(self.centralwidget)
        self.returnButton.setObjectName("returnButton")
        self.verticalLayout_4.addWidget(self.returnButton)

        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 4)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        mainScreen.setCentralWidget(self.centralwidget)
        # Create layout for the screen: end

        # Assign functions to buttons
        self.submitButton.clicked.connect(self.submitWord)
        self.repeatWordsButton.clicked.connect(
            partial(mainScreen.useScreen, mainScreen.repeatLearnedScreen))
        self.koreanWordLabel.clicked.connect(self.playCurrentWord)
        self.returnButton.clicked.connect(mainScreen.close)

        # Get words learned today
        self.todayLearned = self.getTodayLearned()

        self.retranslateUi(mainScreen)
        QtCore.QMetaObject.connectSlotsByName(mainScreen)

        self.submitButton.setShortcut("Return")
        self.repeatWordsButton.setShortcut("Ctrl+R")
        self.returnButton.setShortcut("Ctrl+Q")

        # Run functions to get words and set first word to learn
        self.wordsToLearn = self.getWordsToLearn()
        self.setWord()

    def playCurrentWord(self):
        """Play clicked word"""

        koreanWord = self.koreanWordLabel.text()
        if koreanWord != "":
            self.playControl.playSound("data/sounds/{}.mp3".format(koreanWord))

    def getTodayLearned(self):
        """Get list of words that were learned today

        :return list(): list of learned words
        """

        currentTime = time.time()
        fromStart = currentTime+self.secondsDifference+3600 * \
            (24-((currentTime+self.secondsDifference)/3600) % 24)-3600*24
        todayLearned = []
        for i in reversed(self.data["logs"]):
            if i["time"]+i["localTime"] < fromStart:
                return todayLearned
            if i["count"] == 1 and i["correct"] == 1:
                todayLearned.append(i["wordIndex"])
        return todayLearned

    def getWordsToLearn(self):
        """Get list of words to learn

        :return list(): list of words to learn
        """

        wordsToLearn = []
        for i in range(len(self.data["words"])):
            if self.data["words"][i]["count"] == 0:
                wordsToLearn.append(i)

        return wordsToLearn

    def setWord(self):
        """Set text of labels to new word"""

        word = self.data["words"][self.wordsToLearn[0]]
        self.koreanWordLabel.setText(word["han"])
        self.englishWordLabel.setText(word["eng"])

    def submitWord(self):
        """Submit word"""

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

            word = self.data["words"][self.wordsToLearn[0]]
            input = self.lineEdit.text()
            if word["han"].split("(")[0] == input:

                self.data["words"][self.wordsToLearn[0]
                                   ]["date"] = int(time.time())
                self.data["words"][self.wordsToLearn[0]]["count"] = 1
                self.data["words"][self.wordsToLearn[0]
                                   ]["localTime"] = self.secondsDifference

                self.data["logs"].append({
                    "wordIndex": self.wordsToLearn[0],
                    "correct": 1,
                    "time": int(time.time()),
                    "count": 1,
                    "nextI": 0,
                    "ease": self.data["words"][self.wordsToLearn[0]]["ef"],
                    "localTime": self.secondsDifference,
                    "currentStreak": 0
                })

                self.submitButton.setText("Next")
                self.lineEdit.setStyleSheet(
                    "background: rgb(97, 224, 65); font-size: 18pt")
                self.submitButton.setShortcut("Return")
                self.todayLearned.append(self.wordsToLearn[0])
                self.todayLearnedLabel.setText(
                    "Today learned: {}".format(len(self.todayLearned)))
                self.playControl.playSound(
                    "data/sounds/{}.mp3".format(word["han"]))
                self.wordsToLearn.pop(0)

            else:
                self.lineEdit.setText("")
                self.submitButton.setText("Repeat")
                self.lineEdit.setStyleSheet(
                    "background: rgb(247, 81, 52); font-size: 18pt")
                self.submitButton.setShortcut("Return")
                self.playControl.playSound(
                    "data/sounds/{}.mp3".format(word["han"]))

            self.beingPressed = False

    def retranslateUi(self, mainScreen):
        _translate = QtCore.QCoreApplication.translate
        mainScreen.setWindowTitle(_translate("mainScreen", "Learn words"))
        self.label.setText(_translate("mainScreen", "Learn words"))
        self.koreanWordLabel.setText(_translate("mainScreen", ""))
        self.englishWordLabel.setText(_translate("mainScreen", ""))
        self.submitButton.setText(_translate("mainScreen", "Submit"))
        self.todayLearnedLabel.setText(_translate(
            "mainScreen", "Today learned: {}".format(len(self.todayLearned))))
        self.repeatWordsButton.setText(
            _translate("mainScreen", "Repeat words"))
        self.returnButton.setText(_translate("mainScreen", "Return"))
