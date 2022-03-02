from PyQt5 import QtWidgets
from modules import mainScreen
import sys


def main():
    app = QtWidgets.QApplication(sys.argv)
    screen = mainScreen.mainScreen()
    screen.showFullScreen()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
