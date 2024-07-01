"""
Initializes a PyQt5 application and starts the main window.
"""
import sys
from PyQt5.QtWidgets import QApplication
from start_window import StartWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartWindow()
    sys.exit(app.exec_())
