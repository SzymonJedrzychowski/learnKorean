import os
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
from gtts import gTTS


class Ui_modifyWordsScreen(object):
    """Screen to search words"""

    def setupUi(self, mainScreen, **kwargs):
        self.screenName = "modifyWordsScreen"
        self.mainScreen = mainScreen
        self.data = mainScreen.data

        self.item = None

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
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)

        self.tableView = QtWidgets.QTableView(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.tableView.setFont(font)
        self.tableView.setObjectName("tableView")

        self.verticalLayout.addWidget(self.tableView)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.koreanWordLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.koreanWordLabel.sizePolicy().hasHeightForWidth())
        self.koreanWordLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.koreanWordLabel.setFont(font)
        self.koreanWordLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.koreanWordLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.koreanWordLabel.setWordWrap(True)
        self.koreanWordLabel.setObjectName("koreanWordLabel")
        self.horizontalLayout_4.addWidget(self.koreanWordLabel)

        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)

        self.englishWordLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.englishWordLabel.sizePolicy().hasHeightForWidth())
        self.englishWordLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.englishWordLabel.setFont(font)
        self.englishWordLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.englishWordLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.englishWordLabel.setWordWrap(True)
        self.englishWordLabel.setObjectName("englishWordLabel")
        self.horizontalLayout_4.addWidget(self.englishWordLabel)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.koreanWord = QtWidgets.QLineEdit(self.centralwidget)
        self.koreanWord.setObjectName("koreanWord")
        self.horizontalLayout_2.addWidget(self.koreanWord)

        self.englishWord = QtWidgets.QLineEdit(self.centralwidget)
        self.englishWord.setObjectName("englishWord")
        self.horizontalLayout_2.addWidget(self.englishWord)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.changeLanguageButton = QtWidgets.QPushButton(self.centralwidget)
        self.changeLanguageButton.setObjectName("changeLanguageButton")
        self.horizontalLayout.addWidget(self.changeLanguageButton)

        self.submitButton = QtWidgets.QPushButton(self.centralwidget)
        self.submitButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.submitButton)

        self.returnButton = QtWidgets.QPushButton(self.centralwidget)
        self.returnButton.setObjectName("returnButton")
        self.horizontalLayout.addWidget(self.returnButton)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(2, 3)
        self.verticalLayout.setStretch(3, 2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        mainScreen.setCentralWidget(self.centralwidget)
        # Create layout for the screen: end

        # Create ability to display only parts of the set

        # Create model with all words
        self.model = QtGui.QStandardItemModel(len(self.data["words"]), 1)
        self.model.setHorizontalHeaderLabels(["Korean", "English"])

        for row, word in enumerate(self.data["words"]):
            koreanWord = QtGui.QStandardItem(word["han"])
            englishWord = QtGui.QStandardItem(word["eng"])
            self.model.setItem(row, 0, koreanWord)
            self.model.setItem(row, 1, englishWord)

        # Create filter that searches words based on the first column
        self.filter = QtCore.QSortFilterProxyModel()
        self.filter.setSourceModel(self.model)
        self.filter.setFilterKeyColumn(0)
        self.filter.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)

        # Connect filter to input
        self.lineEdit.textChanged.connect(self.filter.setFilterRegExp)

        # Connect model to the table
        self.tableView.setModel(self.filter)
        self.tableView.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        self.tableView.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)

        # Assign functions to buttons (and table rows)
        self.tableView.clicked.connect(self.showFullText)
        self.changeLanguageButton.clicked.connect(self.changeLanguageSearch)
        self.submitButton.clicked.connect(self.submitWordChange)
        self.returnButton.clicked.connect(mainScreen.close)

        self.retranslateUi(mainScreen)
        QtCore.QMetaObject.connectSlotsByName(mainScreen)

        # Asign shortcuts to buttons
        self.changeLanguageButton.setShortcut("Ctrl+1")
        self.returnButton.setShortcut("Ctrl+Q")

    def changeLanguageSearch(self):
        """Change language of filter to filter based on the other column"""

        current = self.changeLanguageButton.text()
        if current == "Korean":
            self.changeLanguageButton.setText("English")
            self.filter.setFilterKeyColumn(1)
        else:
            self.changeLanguageButton.setText("Korean")
            self.filter.setFilterKeyColumn(0)
        self.changeLanguageButton.setShortcut("Ctrl+1")

    def showFullText(self, item):
        """Show clicked word in the labels"""

        currentValues = [[self.filter.index(row, 0).data(), self.filter.index(
            row, 1).data()] for row in range(self.filter.rowCount())]

        koreanWord = currentValues[item.row()][0]
        englishWord = currentValues[item.row()][1]

        self.koreanWordLabel.setText(koreanWord)
        self.englishWordLabel.setText(englishWord)

        self.koreanWord.setText(koreanWord)
        self.englishWord.setText(englishWord)

        self.item = item

    def submitWordChange(self):
        """Modify currently selected word"""

        koreanWord = self.koreanWordLabel.text()
        englishWord = self.englishWordLabel.text()
        newKoreanWord = self.koreanWord.text()
        newEnglishWord = self.englishWord.text()
        if koreanWord == "":
            return
        if newKoreanWord == "" or newEnglishWord == "":
            return
        for i, word in enumerate(self.data["words"]):
            if word["han"] == koreanWord:
                if word["eng"] == englishWord:
                    self.data["words"][i]["han"] = newKoreanWord
                    self.data["words"][i]["eng"] = newEnglishWord
                    self.koreanWordLabel.setText("")
                    self.englishWordLabel.setText("")
                    self.koreanWord.setText("")
                    self.englishWord.setText("")
                    self.submitButton.setText("Word was modified")
                    if not os.path.isfile("data/sounds/{}.mp3".format(newKoreanWord)):
                        tts = gTTS(newKoreanWord, lang="ko")
                        tts.save("data/sounds/{}.mp3".format(newKoreanWord))
                        print("[SOUND FILE: {}]     Created sound file: {}.mp3".format(
                            time.strftime("%H:%M:%S"), newKoreanWord))
                    QtCore.QTimer.singleShot(3000, partial(
                        self.mainScreen.changeButtonText, self.submitButton, "Submit"))
                    self.filter.setData(self.filter.index(
                        self.item.row(), 0), newKoreanWord)
                    self.filter.setData(self.filter.index(
                        self.item.row(), 1), newEnglishWord)
                    self.tableView.repaint()
                    self.mainScreen.previousSaveLenghts[2] = True
                    return

    def retranslateUi(self, mainScreen):
        _translate = QtCore.QCoreApplication.translate
        mainScreen.setWindowTitle(_translate("mainScreen", "MainWindow"))
        self.label.setText(_translate("mainScreen", "Search words"))
        self.koreanWordLabel.setText(_translate("mainScreen", ""))
        self.submitButton.setText(_translate("mainScreen", "Submit"))
        self.englishWordLabel.setText(_translate("mainScreen", ""))
        self.changeLanguageButton.setText(_translate("mainScreen", "Korean"))
        self.returnButton.setText(_translate("mainScreen", "Return"))
