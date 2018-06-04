from Controler.Controler import LidcAnalyzerControler
from PyQt5.QtWidgets import QApplication
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LidcAnalyzerControler()
    window.show()
    sys.exit(app.exec_())