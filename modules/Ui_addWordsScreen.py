import time
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from gtts import gTTS
from functools import partial


class Ui_addWordsScreen(object):
    """Screen to add words"""

    def setupUi(self, mainScreen, **kwargs):
        self.screenName = "addWordsScreen"
        self.mainScreen = mainScreen
        self.data = self.mainScreen.data

        # Create layout for the screen: start
        self.mainScreen.setObjectName("mainScreen")
        self.centralwidget = QtWidgets.QWidget(self.mainScreen)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(30, 30, 30, 30)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.koreanWordLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.koreanWordLabel.setFont(font)
        self.koreanWordLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.koreanWordLabel.setObjectName("koreanWordLabel")
        self.verticalLayout_5.addWidget(self.koreanWordLabel)

        self.koreanWord = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.koreanWord.setFont(font)
        self.koreanWord.setObjectName("koreanWord")
        self.verticalLayout_5.addWidget(self.koreanWord)

        self.horizontalLayout.addLayout(self.verticalLayout_5)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.englishWordLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.englishWordLabel.setFont(font)
        self.englishWordLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.englishWordLabel.setObjectName("englishWordLabel")
        self.verticalLayout_3.addWidget(self.englishWordLabel)

        self.englishWord = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.englishWord.setFont(font)
        self.englishWord.setObjectName("englishWord")
        self.verticalLayout_3.addWidget(self.englishWord)

        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout)

        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        self.minimumIndexLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.minimumIndexLabel.setFont(font)
        self.minimumIndexLabel.setObjectName("minimumIndexLabel")
        self.verticalLayout_6.addWidget(self.minimumIndexLabel)

        self.maximumIndexLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.maximumIndexLabel.setFont(font)
        self.maximumIndexLabel.setObjectName("maximumIndexLabel")
        self.verticalLayout_6.addWidget(self.maximumIndexLabel)

        self.horizontalLayout_2.addLayout(self.verticalLayout_6)

        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.inputIndexLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.inputIndexLabel.setFont(font)
        self.inputIndexLabel.setObjectName("inputIndexLabel")
        self.horizontalLayout_4.addWidget(self.inputIndexLabel)

        self.inputIndex = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.inputIndex.setFont(font)
        self.inputIndex.setObjectName("inputIndex")
        self.limits = self.calculateLimits()
        validator = QtGui.QIntValidator(self.limits[0], self.limits[1])
        self.inputIndex.setValidator(validator)
        self.horizontalLayout_4.addWidget(self.inputIndex)

        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.submitButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.submitButton.setFont(font)
        self.submitButton.setObjectName("submitButton")
        self.verticalLayout_2.addWidget(self.submitButton)

        self.returnButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.returnButton.setFont(font)
        self.returnButton.setObjectName("returnButton")
        self.verticalLayout_2.addWidget(self.returnButton)

        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 3)
        self.verticalLayout.setStretch(3, 3)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.mainScreen.setCentralWidget(self.centralwidget)
        # Create layout for the screen: end

        # Assign functions to buttons
        self.submitButton.clicked.connect(self.submitWord)
        self.returnButton.clicked.connect(self.mainScreen.close)

        self.retranslateUi(self.mainScreen)
        QtCore.QMetaObject.connectSlotsByName(self.mainScreen)

        # Assign shortcuts to buttons
        self.returnButton.setShortcut("Ctrl+Q")
        self.submitButton.setShortcut("Ctrl+A")

        # Set text on lables with index
        self.minimumIndexLabel.setText(
            "Minimum Index: {}".format(self.limits[0]))
        self.maximumIndexLabel.setText(
            "Maximum Index: {}".format(self.limits[1]))

    def calculateLimits(self):
        """Calculate limits for the adding of the words

        :return list(lowerLimit, higherLimit): limits
        """
        lastDay = list(self.data["logsSave"].keys())[-1]
        lowerLimit = sum(self.data["logsSave"][lastDay]["5"])
        higherLimit = len(self.data["words"])
        return [lowerLimit, higherLimit]

    def submitWord(self):
        """Submit new word to be added"""

        koreanWord = self.koreanWord.text()
        englishWord = self.englishWord.text()
        wordIndex = int(self.inputIndex.text())

        # Prevent adding if any places is empty
        if koreanWord == "" or englishWord == "" or wordIndex == "" or wordIndex < self.limits[0] or wordIndex > self.limits[1]:
            self.submitButton.setText("Error")
        else:
            # Create sound file if no file with such korean word is already in sounds directory
            if not os.path.isfile("data/sounds/{}.mp3".format(koreanWord)):
                tts = gTTS(koreanWord, lang="ko")
                tts.save("data/sounds/{}.mp3".format(koreanWord))
                print("[SOUND FILE: {}]     Created sound file: {}.mp3".format(
                    time.strftime("%H:%M:%S"), koreanWord))
            self.data["words"].insert(wordIndex, {
                                      "han": koreanWord, "eng": englishWord, "currentStreak": 0, "easeFactor": 2.5, "nextInterval": 0, "count": 0, "date": 0, "localTime": 0})
            self.submitButton.setText("Word added")
            self.koreanWord.setText("")
            self.englishWord.setText("")
        QtCore.QTimer.singleShot(3000, partial(
            self.mainScreen.changeButtonText, self.submitButton, "Submit"))

    def retranslateUi(self, mainScreen):
        _translate = QtCore.QCoreApplication.translate
        mainScreen.setWindowTitle(_translate("mainScreen", "MainWindow"))
        self.label.setText(_translate("mainScreen", "Add words"))
        self.koreanWordLabel.setText(_translate("mainScreen", "Korean"))
        self.englishWordLabel.setText(_translate("mainScreen", "English"))
        self.minimumIndexLabel.setText(
            _translate("mainScreen", "Minimum Index: 0"))
        self.maximumIndexLabel.setText(
            _translate("mainScreen", "Maximum Index: 0"))
        self.inputIndexLabel.setText(_translate("mainScreen", "Your index:"))
        self.submitButton.setText(_translate("mainScreen", "Submit"))
        self.returnButton.setText(_translate("mainScreen", "Return"))
