"""
Module containing a dialog for resizing images with options to maintain aspect ratio.
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QRadioButton, QLabel, QLineEdit, QPushButton,
                             QCheckBox, QMessageBox)
import re


class ResizeDialog(QDialog):
    """
        Dialog window for resizing images. Provides options for resizing by percent or pixels,
        maintaining aspect ratio, and validating input values.
        """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Resize Image")
        self.setGeometry(100, 100, 300, 200)

        self.image_width = parent.pil_image.width
        self.image_height = parent.pil_image.height

        self.resize_type = 'pixels'
        self.keep_aspect_ratio = True

        self.layout = QVBoxLayout(self)

        # Resize type selection
        self.resize_type_layout = QHBoxLayout()
        self.percent_radio = QRadioButton("Percent")
        self.pixel_radio = QRadioButton("Pixels")
        self.pixel_radio.setChecked(True)
        self.percent_radio.toggled.connect(self.on_radio_button_toggled)
        self.pixel_radio.toggled.connect(self.on_radio_button_toggled)
        self.resize_type_layout.addWidget(self.percent_radio)
        self.resize_type_layout.addWidget(self.pixel_radio)

        self.layout.addLayout(self.resize_type_layout)

        # Width and height input
        self.width_label = QLabel("Width:")
        self.width_input = QLineEdit(str(self.image_width))
        self.height_label = QLabel("Height:")
        self.height_input = QLineEdit(str(self.image_height))

        self.width_input.textChanged.connect(self.on_width_changed)
        self.height_input.textChanged.connect(self.on_height_changed)

        self.layout.addWidget(self.width_label)
        self.layout.addWidget(self.width_input)
        self.layout.addWidget(self.height_label)
        self.layout.addWidget(self.height_input)

        # Aspect ratio checkbox
        self.aspect_ratio_checkbox = QCheckBox("Maintain Aspect Ratio")
        self.aspect_ratio_checkbox.setChecked(True)
        self.layout.addWidget(self.aspect_ratio_checkbox)

        # OK and Cancel buttons
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

    def on_radio_button_toggled(self):
        """
                Slot function called when radio buttons (Percent or Pixels) are toggled.
                Updates the resize type attribute and resets width and height inputs accordingly.
                """
        if self.percent_radio.isChecked():
            self.resize_type = 'percent'
            self.width_input.setText("100")
            self.height_input.setText("100")
        else:
            self.resize_type = 'pixels'
            self.width_input.setText(str(self.image_width))
            self.height_input.setText(str(self.image_height))

    def on_width_changed(self, text):
        """
                Slot function called when width input field is changed.
                Adjusts the height input field based on the width value to maintain aspect ratio,
                if 'Maintain Aspect Ratio' checkbox is checked.
                """
        if self.resize_type == 'percent':
            if self.validate_input(text):
                self.height_input.blockSignals(True)
                self.height_input.setText(text)
                self.height_input.blockSignals(False)
        elif (self.resize_type == 'pixels' and
              self.aspect_ratio_checkbox.isChecked()):
            if self.validate_input(text):
                new_width = int(text)
                aspect_ratio = self.image_height / self.image_width
                new_height = int(new_width * aspect_ratio)
                self.height_input.blockSignals(True)
                self.height_input.setText(str(new_height))
                self.height_input.blockSignals(False)

    def on_height_changed(self, text):
        """
                Slot function called when height input field is changed.
                Adjusts the width input field based on the height value to maintain aspect ratio,
                if 'Maintain Aspect Ratio' checkbox is checked.
                """
        if self.resize_type == 'percent':
            if self.validate_input(text):
                self.width_input.blockSignals(True)
                self.width_input.setText(text)
                self.width_input.blockSignals(False)
        elif (self.resize_type == 'pixels' and
              self.aspect_ratio_checkbox.isChecked()):
            if self.validate_input(text):
                new_height = int(text)
                aspect_ratio = self.image_width / self.image_height
                new_width = int(new_height * aspect_ratio)
                self.width_input.blockSignals(True)
                self.width_input.setText(str(new_width))
                self.width_input.blockSignals(False)

    def on_ok_clicked(self):
        if (not self.validate_input(self.width_input.text()) or
                not self.validate_input(self.height_input.text())):
            QMessageBox.warning(self, "Error",
                                "Invalid input."
                                " Please enter numeric values only.")
            return
        self.accept()

    def validate_input(self, text):
        return bool(re.match(r"^\d+$", text))

    def get_values(self):
        """
                Returns the current values of resize type, width, height, and
                whether aspect ratio should be maintained.
                """
        return self.resize_type, int(self.width_input.text()), int(
            self.height_input.text()), self.aspect_ratio_checkbox.isChecked()
