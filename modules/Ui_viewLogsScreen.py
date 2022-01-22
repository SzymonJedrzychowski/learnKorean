from PyQt5 import QtCore, QtGui, QtWidgets
import time
from functools import partial


class Ui_viewLogsScreen(object):
    """Screen to view logs"""

    def __init__(self):
        self.deliberateZero = False
    
    def setupUi(self, mainScreen, **kwargs):
        self.screenName = "viewLogsScreen"
        self.mainScreen = mainScreen
        self.data = mainScreen.data

        d0 = (int(time.time())+time.localtime().tm_gmtoff)//(3600*24)
        self.firstDay = (self.data["logs"][0]["time"] +
                         self.data["logs"][0]["localTime"])//(3600*24)-d0
        self.lastDay = max([self.data["words"][i]["date"]+self.data["words"][i]["localTime"]
                           for i in range(len(self.data["words"]))])//(3600*24)-d0

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

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.wordsDailyButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.wordsDailyButton.setFont(font)
        self.wordsDailyButton.setObjectName("wordsDailyButton")
        self.verticalLayout_4.addWidget(self.wordsDailyButton)

        self.wordsTypesDailyButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.wordsTypesDailyButton.setFont(font)
        self.wordsTypesDailyButton.setObjectName("wordsTypesDailyButton")
        self.verticalLayout_4.addWidget(self.wordsTypesDailyButton)

        self.wordsFromPreviousDaysDailyButton = QtWidgets.QPushButton(
            self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.wordsFromPreviousDaysDailyButton.setFont(font)
        self.wordsFromPreviousDaysDailyButton.setObjectName(
            "wordsFromPreviousDaysDailyButton")
        self.verticalLayout_4.addWidget(self.wordsFromPreviousDaysDailyButton)

        self.accuracyDailyButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.accuracyDailyButton.setFont(font)
        self.accuracyDailyButton.setObjectName("accuracyDailyButton")
        self.verticalLayout_4.addWidget(self.accuracyDailyButton)

        self.wordsTypesHistoryButton = QtWidgets.QPushButton(
            self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.wordsTypesHistoryButton.setFont(font)
        self.wordsTypesHistoryButton.setObjectName("wordsTypesHistoryButton")
        self.verticalLayout_4.addWidget(self.wordsTypesHistoryButton)

        self.horizontalLayout_2.addLayout(self.verticalLayout_4)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        self.startLimitLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.startLimitLabel.setFont(font)
        self.startLimitLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.startLimitLabel.setObjectName("startLimitLabel")
        self.verticalLayout_6.addWidget(self.startLimitLabel)

        self.startLimit = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.startLimit.setFont(font)
        self.startLimit.setObjectName("startLimit")
        validator = QtGui.QIntValidator(self.firstDay, self.lastDay)
        self.startLimit.setValidator(validator)
        self.verticalLayout_6.addWidget(self.startLimit)

        self.endLimitLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.endLimitLabel.setFont(font)
        self.endLimitLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.endLimitLabel.setObjectName("endLimitLabel")
        self.verticalLayout_6.addWidget(self.endLimitLabel)

        self.endLimit = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.endLimit.setFont(font)
        self.endLimit.setObjectName("endLimit")
        self.endLimit.setValidator(validator)
        self.verticalLayout_6.addWidget(self.endLimit)

        self.verticalLayout_3.addLayout(self.verticalLayout_6)

        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)

        self.returnButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.returnButton.setFont(font)
        self.returnButton.setObjectName("returnButton")
        self.verticalLayout_5.addWidget(self.returnButton)

        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)

        self.verticalLayout_3.addLayout(self.verticalLayout_5)
        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 1)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 4)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.mainScreen.setCentralWidget(self.centralwidget)
        # Create layout for the screen: end

        # Assign functions to buttons
        self.returnButton.clicked.connect(self.mainScreen.close)
        self.wordsDailyButton.clicked.connect(
            partial(self.useGraphScreen, "wordsDaily"))
        self.wordsTypesDailyButton.clicked.connect(
            partial(self.useGraphScreen, "wordsTypesDaily"))
        self.wordsFromPreviousDaysDailyButton.clicked.connect(
            partial(self.useGraphScreen, "wordsFromPreviousDaysDaily"))
        self.accuracyDailyButton.clicked.connect(
            partial(self.useGraphScreen, "accuracyDaily"))
        self.wordsTypesHistoryButton.clicked.connect(
            partial(self.useGraphScreen, "wordsTypesHistory"))

        self.retranslateUi(self.mainScreen)
        QtCore.QMetaObject.connectSlotsByName(self.mainScreen)

        # Assign shortcuts to buttons
        self.returnButton.setShortcut("Ctrl+Q")
        self.wordsDailyButton.setShortcut("Ctrl+1")
        self.wordsTypesDailyButton.setShortcut("Ctrl+2")
        self.wordsFromPreviousDaysDailyButton.setShortcut("Ctrl+3")
        self.accuracyDailyButton.setShortcut("Ctrl+4")
        self.wordsTypesHistoryButton.setShortcut("Ctrl+5")

    def useGraphScreen(self, name):
        """Use specific graph screen

        :param name: name of graph that needs to be used
        """

        self.mainScreen.useScreen(self.mainScreen.graphScreen, graphType=name, graphLimits=[
                                  self.startLimit.text(), self.endLimit.text()])

    def setGraphLimits(self):
        """Set limits for graphs in input boxes"""

        if self.mainScreen.graphLimits != None:
            if self.mainScreen.graphLimits[0] != self.firstDay:
                self.startLimit.setText(str(self.mainScreen.graphLimits[0]))
            if self.mainScreen.graphLimits[1] != self.lastDay and (self.mainScreen.graphLimits[1] != 0 or (self.mainScreen.graphLimits[1] == 0 and self.deliberateZero == True)):
                self.endLimit.setText(str(self.mainScreen.graphLimits[1]))

    def retranslateUi(self, mainScreen):
        _translate = QtCore.QCoreApplication.translate
        mainScreen.setWindowTitle(_translate("mainScreen", "View logs"))
        self.label.setText(_translate("mainScreen", "View logs"))
        self.wordsDailyButton.setText(_translate("mainScreen", "Words daily"))
        self.wordsTypesDailyButton.setText(
            _translate("mainScreen", "Words type daily"))
        self.wordsFromPreviousDaysDailyButton.setText(
            _translate("mainScreen", "Words from previous days daily"))
        self.accuracyDailyButton.setText(
            _translate("mainScreen", "Accuracy daily"))
        self.wordsTypesHistoryButton.setText(
            _translate("mainScreen", "Word types history"))
        self.startLimitLabel.setText(_translate(
            "mainScreen", "Start limit ({})".format(self.firstDay)))
        self.endLimitLabel.setText(_translate(
            "mainScreen", "End limit (0/{})".format(self.lastDay)))
        self.returnButton.setText(_translate("mainScreen", "Return"))
