from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
import clipboard


class Ui_mainMenu(object):
    """Screen for main menu"""
    
    def setupUi(self, mainScreen, **kwargs):
        self.screenName = "mainMenuScreen"
        self.mainScreen = mainScreen
        self.data = self.mainScreen.data

        # Create layout for the screen: start
        self.mainScreen.setObjectName("mainScreen")
        self.centralwidget = QtWidgets.QWidget(self.mainScreen)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setContentsMargins(30, 30, 30, 30)
        self.verticalLayout_7.setObjectName("verticalLayout_7")

        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_7.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)

        self.learnWordsButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.learnWordsButton.setFont(font)
        self.learnWordsButton.setObjectName("learnWordsButton")
        self.verticalLayout_7.addWidget(self.learnWordsButton)

        self.repeatWordsButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.repeatWordsButton.setFont(font)
        self.repeatWordsButton.setObjectName("repeatWordsButton")
        self.verticalLayout_7.addWidget(self.repeatWordsButton)

        self.viewLogsButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.viewLogsButton.setFont(font)
        self.viewLogsButton.setObjectName("viewLogsButton")
        self.verticalLayout_7.addWidget(self.viewLogsButton)

        self.searchWordsButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.searchWordsButton.setFont(font)
        self.searchWordsButton.setObjectName("searchWordsButton")
        self.verticalLayout_7.addWidget(self.searchWordsButton)

        self.modifySetButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.modifySetButton.setFont(font)
        self.modifySetButton.setObjectName("modifySetButton")
        self.verticalLayout_7.addWidget(self.modifySetButton)

        self.generateQuizletDataButton = QtWidgets.QPushButton(
            self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.generateQuizletDataButton.setFont(font)
        self.generateQuizletDataButton.setObjectName(
            "generateQuizletDataButton")
        self.verticalLayout_7.addWidget(self.generateQuizletDataButton)

        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.saveButton.setFont(font)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout_6.addWidget(self.saveButton)

        self.quitButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.quitButton.setFont(font)
        self.quitButton.setObjectName("quitButton")
        self.horizontalLayout_6.addWidget(self.quitButton)

        self.verticalLayout_7.addLayout(self.horizontalLayout_6)
        self.gridLayout_2.addLayout(self.verticalLayout_7, 0, 0, 1, 1)
        self.mainScreen.setCentralWidget(self.centralwidget)
        # Create layout for the screen: end

        # Assign functions to buttons
        self.learnWordsButton.clicked.connect(
            partial(self.mainScreen.useScreen, self.mainScreen.learnWordsScreen))
        self.repeatWordsButton.clicked.connect(
            partial(self.mainScreen.useScreen, self.mainScreen.repeatScreen))
        self.viewLogsButton.clicked.connect(
            partial(self.mainScreen.useScreen, self.mainScreen.viewLogsScreen))
        self.searchWordsButton.clicked.connect(
            partial(self.mainScreen.useScreen, self.mainScreen.searchWordsScreen))
        self.modifySetButton.clicked.connect(
            partial(self.mainScreen.useScreen, self.mainScreen.modifySetScreen))
        self.generateQuizletDataButton.clicked.connect(
            self.generateQuizletData)
        self.saveButton.clicked.connect(partial(self.mainScreen.saveData, self.saveButton))
        self.quitButton.clicked.connect(
            partial(self.mainScreen.useScreen, self.mainScreen.quitScreen))

        self.retranslateUi(self.mainScreen)
        QtCore.QMetaObject.connectSlotsByName(self.mainScreen)

        # Assign shortcuts to buttons
        self.learnWordsButton.setShortcut("Ctrl+1")
        self.repeatWordsButton.setShortcut("Ctrl+2")
        self.viewLogsButton.setShortcut("Ctrl+3")
        self.searchWordsButton.setShortcut("Ctrl+4")
        self.modifySetButton.setShortcut("Ctrl+5")
        self.generateQuizletDataButton.setShortcut("Ctrl+6")
        self.quitButton.setShortcut("Ctrl+Q")
        self.saveButton.setShortcut("Ctrl+S")

    def generateQuizletData(self):
        """Generate string with word to repeat in quizlet and copy it to clipboard"""

        data = ""
        for i in self.data["words"]:
            if i["n"] > 0 and i["n"] < 3:
                data += "{}	{}\n".format(i["han"], i["eng"])
        clipboard.copy(data)

        self.generateQuizletDataButton.setText("Copied!")
        QtCore.QTimer.singleShot(3000, partial(
            self.mainScreen.changeButtonText, self.generateQuizletDataButton, "Generate quizlet data"))

    def retranslateUi(self, mainScreen):
        _translate = QtCore.QCoreApplication.translate
        mainScreen.setWindowTitle(_translate("mainScreen", "Learn Korean"))
        self.label.setText(_translate("mainScreen", "Learn Korean"))
        self.learnWordsButton.setText(_translate("mainScreen", "Learn words"))
        self.repeatWordsButton.setText(
            _translate("mainScreen", "Repeat words"))
        self.viewLogsButton.setText(_translate("mainScreen", "View logs"))
        self.searchWordsButton.setText(
            _translate("mainScreen", "Search words"))
        self.modifySetButton.setText(_translate("mainScreen", "Modify set"))
        self.generateQuizletDataButton.setText(
            _translate("mainScreen", "Generate quizlet data"))
        self.saveButton.setText(_translate("mainScreen", "Save"))
        self.quitButton.setText(_translate("mainScreen", "Quit"))
