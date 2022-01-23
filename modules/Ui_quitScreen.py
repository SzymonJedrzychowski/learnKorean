from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial


class Ui_quitScreen(object):
    """Screen for quiting the app"""

    def setupUi(self, mainScreen, **kwargs):
        self.screenName = "quitScreen"
        self.mainScreen = mainScreen

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

        self.returnButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.returnButton.setFont(font)
        self.returnButton.setObjectName("returnButton")
        self.horizontalLayout.addWidget(self.returnButton)

        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.saveButton.setFont(font)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)

        self.quitButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.quitButton.setFont(font)
        self.quitButton.setObjectName("quitButton")
        self.horizontalLayout.addWidget(self.quitButton)

        self.verticalLayout.addLayout(self.horizontalLayout)

        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.mainScreen.setCentralWidget(self.centralwidget)
        # Create layout for the screen: end

        # Assign functions to buttons
        self.returnButton.clicked.connect(
            partial(self.mainScreen.useScreen, self.mainScreen.mainMenuScreen))
        self.saveButton.clicked.connect(
            partial(self.mainScreen.saveData, self.saveButton))
        self.quitButton.clicked.connect(self.mainScreen.close)

        self.retranslateUi(self.mainScreen)
        QtCore.QMetaObject.connectSlotsByName(self.mainScreen)

        # Assign shortcuts to buttons
        self.returnButton.setShortcut("Ctrl+R")
        self.saveButton.setShortcut("Ctrl+S")
        self.quitButton.setShortcut("Ctrl+Q")

    def retranslateUi(self, mainScreen):
        _translate = QtCore.QCoreApplication.translate
        mainScreen.setWindowTitle(_translate("mainScreen", "MainWindow"))
        self.label.setText(_translate(
            "mainScreen", "Are you sure you want to quit? All unsaved data will be lost."))
        self.returnButton.setText(_translate("mainScreen", "Return"))
        self.saveButton.setText(_translate("mainScreen", "Save and quit"))
        self.quitButton.setText(_translate("mainScreen", "Quit"))
