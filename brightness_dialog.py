"""
Module containing a dialog for adjusting brightness percentage.
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel,
                             QLineEdit, QHBoxLayout, QPushButton, QMessageBox)


class BrightnessDialog(QDialog):
    """
        Dialog window for adjusting brightness percentage.

        Attributes:
        - input (QLineEdit): Line edit widget for entering brightness percentage.
        """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Decrease Brightness")
        self.setGeometry(100, 100, 300, 100)

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Enter the percentage to decrease brightness:")
        self.layout.addWidget(self.label)

        self.input = QLineEdit()
        self.layout.addWidget(self.input)

        self.button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.setStyleSheet("font-size: 15px;"
                                     " font-family: Bahnschrift;"
                                     " font-weight: bold;"
                                     " background-color: #f4dbdb;"
                                     " color: #cd4662")
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet("font-size: 15px;"
                                         " font-family: Bahnschrift;"
                                         " font-weight: bold;"
                                         " background-color: #cd4662;"
                                         " color: #f4dbdb")
        self.ok_button.clicked.connect(self.on_ok_clicked)
        self.cancel_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.ok_button)

        self.layout.addLayout(self.button_layout)

    def on_ok_clicked(self):
        try:
            value = float(self.input.text())
            if not (0 <= value <= 100):
                raise ValueError("Value must be between 0 and 100.")
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Error",
                                "Please enter a valid number "
                                "between 0 and 100.")

    def get_value(self):
        return float(self.input.text())
