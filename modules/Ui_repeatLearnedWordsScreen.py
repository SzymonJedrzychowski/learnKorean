from json.tool import main
from PyQt5 import QtCore, QtGui, QtWidgets
from modules import playControl
from modules.clickableLabel import QLabelClickable
import time


class Ui_repeatLearnedWordsScreen(object):
    """Screen to repeat learned words"""
    
    def setupUi(self, mainScreen, **kwargs):
        self.screenName = "repeatLearnedWordsScreen"
        self.mainScreen = mainScreen
        self.data = mainScreen.data

        self.playControl = playControl.playControl()
        self.secondsDifference = time.localtime().tm_gmtoff

        # Create layout for the screen: start
        self.mainScreen.setObjectName("mainScreen")
        self.centralwidget = QtWidgets.QWidget(self.mainScreen)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(30, 30, 30, 30)
        self.verticalLayout.setObjectName("verticalLayout")

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Korean", "English"])
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.verticalLayout.addWidget(self.tableWidget)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.koreanWordLabel = QLabelClickable(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.koreanWordLabel.sizePolicy().hasHeightForWidth())
        self.koreanWordLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.koreanWordLabel.setFont(font)
        self.koreanWordLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.koreanWordLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.koreanWordLabel.setWordWrap(True)
        self.koreanWordLabel.setObjectName("koreanWordLabel")
        self.horizontalLayout_3.addWidget(self.koreanWordLabel)

        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)

        self.englishWordLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.englishWordLabel.sizePolicy().hasHeightForWidth())
        self.englishWordLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.englishWordLabel.setFont(font)
        self.englishWordLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.englishWordLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.englishWordLabel.setWordWrap(True)
        self.englishWordLabel.setObjectName("englishWordLabel")
        self.horizontalLayout_3.addWidget(self.englishWordLabel)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.returnButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.returnButton.setFont(font)
        self.returnButton.setObjectName("returnButton")
        self.verticalLayout.addWidget(self.returnButton)

        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.mainScreen.setCentralWidget(self.centralwidget)
        # Create layout for the screen: end

        # Assign functions to buttons (and table rows)
        self.tableWidget.cellClicked.connect(self.showFullText)
        self.returnButton.clicked.connect(self.mainScreen.close)
        self.koreanWordLabel.clicked.connect(self.playCurrentWord)

        self.retranslateUi(self.mainScreen)
        QtCore.QMetaObject.connectSlotsByName(self.mainScreen)

        # Assign shortcuts to buttons
        self.returnButton.setShortcut("Ctrl+Q")

        # Load data to table
        self.loadData()

    def playCurrentWord(self):
        """Play clicked word"""

        koreanWord = self.koreanWordLabel.text()
        if koreanWord != "":
            self.playControl.playSound(
                "data/sounds/{}.mp3".format(koreanWord))

    def showFullText(self, item):
        """Show clicked word in the labels"""

        koreanWord = self.tableWidget.item(item, 0).text()
        englishWord = self.tableWidget.item(item, 1).text()

        self.koreanWordLabel.setText(koreanWord)
        self.englishWordLabel.setText(englishWord)

    def loadData(self):
        """Load data of words learned today"""

        currentTime = time.time()
        fromStart = currentTime+self.secondsDifference+3600 * \
            (24-((currentTime+self.secondsDifference)/3600) % 24)-3600*24
        todayLearned = []
        for i in reversed(self.data["logs"]):
            if i["time"]+i["localTime"] < fromStart:
                break
            if i["count"] == 1 and i["correct"] == 1:
                todayLearned.append(i["wordIndex"])

        self.tableWidget.setRowCount(len(todayLearned))

        for row, word in enumerate(reversed(todayLearned)):
            koreanWord = QtWidgets.QTableWidgetItem(
                self.data["words"][word]["han"])
            englishWord = QtWidgets.QTableWidgetItem(
                self.data["words"][word]["eng"])
            self.tableWidget.setItem(row, 0, koreanWord)
            self.tableWidget.setItem(row, 1, englishWord)

    def retranslateUi(self, mainScreen):
        _translate = QtCore.QCoreApplication.translate
        mainScreen.setWindowTitle(_translate(
            "mainScreen", "Repeat learned words"))
        self.koreanWordLabel.setText(_translate("mainScreen", ""))
        self.englishWordLabel.setText(_translate("mainScreen", ""))
        self.returnButton.setText(_translate("mainScreen", "Return"))
