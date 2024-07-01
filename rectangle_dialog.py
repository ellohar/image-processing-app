"""
Module containing a dialog for specifying rectangle coordinates.
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit,
                             QHBoxLayout, QPushButton, QMessageBox)


class RectangleDialog(QDialog):
    """
        Dialog window for specifying rectangle coordinates.

        Attributes:
        - coordinates (tuple): Tuple containing (x, y, width, height) of the rectangle.
        """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.coordinates = None
        self.setWindowTitle("Draw Blue Rectangle")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout(self)

        parent_width = parent.pil_image.width
        parent_height = parent.pil_image.height

        self.label_x = QLabel(f"X Coordinate (0 to {parent_width}):")
        self.input_x = QLineEdit()
        self.input_x.setPlaceholderText(f"0 to {parent_width}")
        self.layout.addWidget(self.label_x)
        self.layout.addWidget(self.input_x)

        self.label_y = QLabel(f"Y Coordinate (0 to {parent_height}):")
        self.input_y = QLineEdit()
        self.input_y.setPlaceholderText(f"0 to {parent_height}")
        self.layout.addWidget(self.label_y)
        self.layout.addWidget(self.input_y)

        self.label_width = QLabel("Width (positive value):")
        self.input_width = QLineEdit()
        self.input_width.setPlaceholderText("positive value")
        self.layout.addWidget(self.label_width)
        self.layout.addWidget(self.input_width)

        self.label_height = QLabel("Height (positive value):")
        self.input_height = QLineEdit()
        self.input_height.setPlaceholderText("positive value")
        self.layout.addWidget(self.label_height)
        self.layout.addWidget(self.input_height)

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
            x = int(self.input_x.text())
            y = int(self.input_y.text())
            width = int(self.input_width.text())
            height = int(self.input_height.text())

            parent_width = self.parent().pil_image.width
            parent_height = self.parent().pil_image.height

            if not (0 <= x <= parent_width) or not (0 <= y <= parent_height):
                raise ValueError(f"Coordinates must be "
                                 f"within the image dimensions: "
                                 f"width 0-{parent_width},"
                                 f" height 0-{parent_height}.")
            if width <= 0 or height <= 0:
                raise ValueError("Width and height must be positive values.")
            if x + width > parent_width or y + height > parent_height:
                raise ValueError("Rectangle must be within image boundaries.")

            self.coordinates = (x, y, width, height)
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def get_coordinates(self):
        return self.coordinates
