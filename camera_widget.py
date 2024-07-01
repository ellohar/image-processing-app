"""
Module contains the CameraWidget class and supporting functions
for a PyQt5 widget that displays live camera feed and allows capturing photos.
"""
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout,
                             QPushButton, QMessageBox, QSizePolicy)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
import cv2
import tempfile
from PIL import Image
from utils import correct_image_orientation


def create_button(text, slot):
    button = QPushButton(text)
    button.setStyleSheet("font-size: 15px; font-family: Bahnschrift;"
                         " font-weight: bold;"
                         " background-color: #f4dbdb; color: #cd4662")
    button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    button.clicked.connect(slot)
    return button


class CameraWidget(QWidget):
    """
        Widget to display live camera feed and capture photos.

        Attributes:
        - parent (QWidget): Parent widget that manages this CameraWidget.
        - cap (cv2.VideoCapture): OpenCV VideoCapture object for camera access.
        - image_label (QLabel): Widget to display the captured image.
        - capture_button (QPushButton): Button to capture a photo from the camera.
        - timer (QTimer): Timer for continuous frame updates from the camera.
        """
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.cap = None
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.capture_button = create_button('Capture Photo',
                                            self.capture_photo)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addStretch()
        layout.addWidget(self.capture_button, alignment=Qt.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.start_camera()

    def start_camera(self):
        """
                Starts the camera by initializing VideoCapture and starting the timer for frame updates.
                Displays an error message if the camera fails to initialize.
                """
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise Exception("Failed to connect to camera.")
            self.timer.start(10)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"{e}")

    def update_frame(self):
        """
                Updates the camera feed by reading a frame, converting it to RGB format,
                and displaying it on the image_label widget.
                """
        try:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = QImage(frame, frame.shape[1], frame.shape[0],
                               QImage.Format_RGB888)
                self.image_label.setPixmap(QPixmap.fromImage(image))
        except Exception as e:
            QMessageBox.critical(self, "Error",
                                 f"Failed to update frame: {e}")

    def capture_photo(self):
        """
                Captures a photo from the camera, saves it as a temporary file,
                and displays the captured image using the parent widget's display_image method.
                """
        try:
            ret, frame = self.cap.read()
            if ret:
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        suffix='.jpg')
                cv2.imwrite(temp_file.name, frame)
                temp_file.close()

                pil_image = Image.open(temp_file.name)
                pil_image = correct_image_orientation(pil_image)
                self.parent.display_image(pil_image)
        except Exception as e:
            QMessageBox.critical(self, "Error",
                                 f"Failed to capture photo: {e}")

    def release_camera(self):
        if self.cap is not None:
            self.timer.stop()
            self.cap.release()
