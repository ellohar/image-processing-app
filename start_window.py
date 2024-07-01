"""
Main application window for an Image Processing App using PyQt5.

Imports necessary modules and defines the StartWindow class which initializes
the main UI with buttons to load an image, connect to a camera, and navigate
between different editing modes. Also includes methods for displaying images,
editing images (resizing, adjusting brightness, drawing rectangles), and
displaying individual color channels.

Main application window for an Image Processing App using PyQt5.

Imports necessary modules and defines the StartWindow class which initializes
the main UI with buttons to load an image, connect to a camera, and navigate
between different editing modes. Also includes methods for displaying images,
editing images (resizing, adjusting brightness, drawing rectangles), and
displaying individual color channels.
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QFileDialog,
                             QMessageBox, QSizePolicy, QDialog)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image
from camera_widget import CameraWidget
from utils import correct_image_orientation
import cv2
import numpy as np
from resize_dialog import ResizeDialog
from brightness_dialog import BrightnessDialog
from rectangle_dialog import RectangleDialog


def create_button(text, slot):
    """
        Create a QPushButton with customized styling and connect it to a slot function.

        Args:
        - text (str): Text to display on the button.
        - slot (function): Function to connect to the button's clicked signal.

        Returns:
        - QPushButton: Configured button object.
        """
    button = QPushButton(text)
    button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    if text == 'Back':
        button.setStyleSheet(
            "font-size: 15px; font-family: Bahnschrift; font-weight: bold;"
            " background-color: #cd4662; color: #f4dbdb;")
    elif text == 'Load Image' or text == 'Connect to Camera':
        button.setStyleSheet(
            "font-size: 20px; font-family: Bahnschrift; font-weight: bold;"
            " background-color: #f4dbdb; color: #cd4662;")
    else:
        button.setStyleSheet(
            "font-size: 15px; font-family: Bahnschrift; font-weight: bold;"
            " background-color: #f4dbdb; color: #cd4662;")

    button.clicked.connect(slot)
    return button


class StartWindow(QMainWindow):
    """
        Main window class for the Image Processing App.

        Attributes:
        - pil_image (PIL.Image): Currently loaded image in PIL format.
        - load_image_button (QPushButton): Button to load an image.
        - connect_camera_button (QPushButton): Button to connect to a camera.
        - image_label (QLabel): Label to display loaded images.
        - back_button (QPushButton): Button to navigate back.
        - continue_button (QPushButton): Button to continue to edit mode.
        - camera_widget (CameraWidget): Widget to display camera feed.
        - layout (QVBoxLayout): Layout for main window.
        """
    def __init__(self):
        """
                Initialize the main window with buttons and layout.
                """
        super().__init__()
        self.setWindowTitle('Image Processing App')
        self.setGeometry(100, 100, 800, 600)

        self.main_widget = QWidget()
        self.main_widget.setStyleSheet("background-color: #f4f2ef;")
        self.setCentralWidget(self.main_widget)

        self.load_image_button = None
        self.connect_camera_button = None
        self.image_label = None
        self.back_button = None
        self.continue_button = None
        self.camera_widget = None

        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        self.pil_image = None  # Keep track of the loaded image
        self.init_ui()
        self.show()

    def display_image(self, pil_image):
        """
            Display the given PIL image on the GUI.

            Args:
            - pil_image (PIL.Image.Image): The PIL image to display.

            This method clears the current layout, sets the given image as the current
            image to display, converts it to QImage format, scales it to fit the window,
            and adds it to the GUI. Navigation buttons are then added for user interaction.
            """
        try:
            self.clear_layout(self.layout)
            self.pil_image = pil_image

            q_img = QImage(pil_image.tobytes(), pil_image.width,
                           pil_image.height, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)

            self.image_label = QLabel()
            self.image_label.setAlignment(Qt.AlignCenter)

            window_width = self.size().width()
            window_height = self.size().height()

            scaled_pixmap = pixmap.scaled(window_width, window_height,
                                          Qt.KeepAspectRatio)

            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setScaledContents(False)

            self.layout.addWidget(self.image_label)

            self.add_navigation_buttons()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to display image: {e}")

    def init_ui(self):
        """
                Initialize the user interface with load image and connect to camera buttons.
                """
        self.clear_layout(self.layout)

        self.load_image_button = create_button('Load Image', self.load_image)
        self.connect_camera_button = create_button('Connect to Camera',
                                                   self.connect_to_camera)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_image_button)
        button_layout.addWidget(self.connect_camera_button)

        self.layout.addLayout(button_layout)

    def add_navigation_buttons(self):
        """
                Add navigation buttons (Back and Continue) to the current layout.
                """
        self.back_button = create_button('Back', self.release_camera_and_back)
        self.continue_button = create_button('Continue', self.edit_mode)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.continue_button)

        self.layout.addStretch()
        self.layout.addLayout(button_layout)

    def load_image(self):
        """
                Open a file dialog to load an image file and display it.
                """
        try:
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName(self, 'Open Image',
                                                       '', 'Image Files (*.png *.jpg *.bmp)')
            if file_path:
                pil_image = Image.open(file_path)
                pil_image = correct_image_orientation(pil_image)
                self.display_image(pil_image)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load image: {e}")

    def connect_to_camera(self):
        """
                Connect to a camera and display the camera feed.
                """
        try:
            self.clear_layout(self.layout)
            self.camera_widget = CameraWidget(self)
            self.layout.addWidget(self.camera_widget)
        except Exception as e:
            QMessageBox.critical(self, "Error",
                                 f"Failed to connect to camera: {e}")

    def release_camera_and_back(self):
        """
                Release the camera (if connected) and navigate back to the main UI.
                """
        if self.camera_widget:
            self.camera_widget.release_camera()
        self.init_ui()

    def clear_layout(self, layout):
        """
                Clear all widgets from a given layout.

                Args:
                - layout (QLayout): Layout to clear.
                """
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())
            self.main_widget.setStyleSheet("background-color: #f4f2ef;")

    def create_edit_buttons(self):
        """
                Create buttons for different editing modes.

                Returns:
                - list: List of tuples (button_text, handler_function).
                """
        edit_buttons = [
            ("Display Red Channel", lambda: self.display_channel('R')),
            ("Display Green Channel", lambda: self.display_channel('G')),
            ("Display Blue Channel", lambda: self.display_channel('B')),
            ("Resize the Image", lambda: self.resize_image()),
            ("Decrease Brightness", lambda: self.decrease_brightness()),
            ("Draw a Blue Rectangle", lambda: self.draw_rectangle()),
            ("Back", self.release_camera_and_back)
        ]
        return edit_buttons

    def edit_mode(self):
        """
                Switch to edit mode UI with image display and editing buttons.
                """
        self.clear_layout(self.layout)

        main_layout = QHBoxLayout()

        image_layout = QVBoxLayout()
        image_container = QWidget()
        image_container.setLayout(image_layout)
        image_container.setSizePolicy(QSizePolicy.Expanding,
                                      QSizePolicy.Expanding)

        if self.pil_image:  # Check if there's an image to display
            q_img = QImage(self.pil_image.tobytes(), self.pil_image.width,
                           self.pil_image.height, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            image_label = QLabel()
            image_label.setPixmap(pixmap.scaled(self.size().width() // 2,
                                                self.size().height(), Qt.KeepAspectRatio,
                                                Qt.SmoothTransformation))
            image_label.setAlignment(Qt.AlignCenter)
            image_label.setSizePolicy(QSizePolicy.Expanding,
                                      QSizePolicy.Expanding)
            image_layout.addWidget(image_label)

        buttons_container = QWidget()
        buttons_container.setSizePolicy(QSizePolicy.Minimum,
                                        QSizePolicy.Expanding)
        buttons_layout = QVBoxLayout()
        buttons_container.setLayout(buttons_layout)

        edit_buttons = self.create_edit_buttons()

        # All buttons except the last one
        for button_text, handler in edit_buttons[:-1]:
            button = create_button(button_text, handler)
            buttons_layout.addWidget(button)

        # The last button (Back button)
        back_button_text, back_button_handler = edit_buttons[-1]
        back_button = create_button(back_button_text, back_button_handler)
        buttons_layout.addWidget(back_button)

        main_layout.addWidget(image_container, 3)
        main_layout.addWidget(buttons_container, 1)

        self.layout.addLayout(main_layout)

    def display_channel(self, channel):
        """
                Display an individual color channel of the loaded image.

                Args:
                - channel (str): Color channel to display ('R', 'G', 'B').
                """
        self.clear_layout(self.layout)

        main_layout = QHBoxLayout()

        image_layout = QVBoxLayout()
        image_container = QWidget()
        image_container.setLayout(image_layout)
        image_container.setSizePolicy(QSizePolicy.Expanding,
                                      QSizePolicy.Expanding)

        if self.pil_image:
            # Convert PIL image to OpenCV format (BGR)
            cv_image = cv2.cvtColor(np.array(self.pil_image),
                                    cv2.COLOR_RGB2BGR)

            # Split channels
            red_channel, green_channel, blue_channel = cv2.split(cv_image)

            # Create an image with only the selected channel
            if channel == 'R':
                channel_image = cv2.merge((red_channel,
                                           np.zeros_like(red_channel),
                                           np.zeros_like(red_channel)))
            elif channel == 'G':
                channel_image = cv2.merge((np.zeros_like(green_channel),
                                           green_channel,
                                           np.zeros_like(green_channel)))
            elif channel == 'B':
                channel_image = cv2.merge((np.zeros_like(blue_channel),
                                           np.zeros_like(blue_channel),
                                           blue_channel))
            else:
                return  # Exit if channel is not recognized

            # Convert channel image to QImage for display
            q_img = QImage(channel_image.data, channel_image.shape[1],
                           channel_image.shape[0], channel_image.strides[0],
                           QImage.Format_RGB888)

            pixmap = QPixmap.fromImage(q_img)
            image_label = QLabel()
            image_label.setPixmap(pixmap.scaled(self.size().width() // 2,
                                                self.size().height(),
                                                Qt.KeepAspectRatio,
                                                Qt.SmoothTransformation))
            image_label.setAlignment(Qt.AlignCenter)
            image_label.setSizePolicy(QSizePolicy.Expanding,
                                      QSizePolicy.Expanding)
            image_layout.addWidget(image_label)

        buttons_container = QWidget()
        buttons_container.setSizePolicy(QSizePolicy.Minimum,
                                        QSizePolicy.Expanding)
        buttons_layout = QVBoxLayout()
        buttons_container.setLayout(buttons_layout)

        edit_buttons = self.create_edit_buttons()

        # All buttons except the last one
        for button_text, handler in edit_buttons[:-1]:
            button = create_button(button_text, handler)
            buttons_layout.addWidget(button)

        # The last button
        back_button_text, back_button_handler = edit_buttons[-1]
        back_button = create_button(back_button_text, back_button_handler)
        buttons_layout.addWidget(back_button)

        main_layout.addWidget(image_container, 3)
        main_layout.addWidget(buttons_container, 1)

        self.layout.addLayout(main_layout)

    def resize_image(self):
        """
                Open a dialog to resize the loaded image based on user input.
                """
        if not self.pil_image:
            return

        dialog = ResizeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            resize_type, width, height, keep_aspect_ratio = dialog.get_values()

            # Check for valid input
            if resize_type == 'percent':
                if width <= 0 or height <= 0 or width > 300 or height > 300:
                    QMessageBox.warning(self, "Error",
                                        "Size in percent must be"
                                        " greater than 0 and less than 300.")
                    return
                new_width = int(self.pil_image.width * width / 100)
                new_height = int(self.pil_image.height * height / 100)
            else:
                if (width <= 0 or height <= 0 or
                        width > 10000 or height > 10000):
                    QMessageBox.warning(self, "Error",
                                        "Size in pixels must be "
                                        "greater than 0 and less than 10000.")
                    return
                new_width = width
                new_height = height

            if keep_aspect_ratio:
                aspect_ratio = self.pil_image.width / self.pil_image.height
                if new_width / aspect_ratio < new_height:
                    new_height = int(new_width / aspect_ratio)
                else:
                    new_width = int(new_height * aspect_ratio)

            print(f"Original size: ({self.pil_image.width},"
                  f" {self.pil_image.height})")
            print(f"New size: ({new_width}, {new_height})")

            # Convert PIL image to OpenCV format (BGR)
            cv_image = cv2.cvtColor(np.array(self.pil_image),
                                    cv2.COLOR_RGB2BGR)

            # Resize the image
            resized_image = cv2.resize(cv_image, (new_width, new_height),
                                       interpolation=cv2.INTER_AREA)

            # Convert back to PIL format
            resized_pil_image = Image.fromarray(cv2.cvtColor(resized_image,
                                                             cv2.COLOR_BGR2RGB))

            # Display the resized image
            self.display_image(resized_pil_image)

    def decrease_brightness(self):
        """
                Open a dialog to adjust the brightness of the loaded image based on user input.
                """
        dialog = BrightnessDialog(self)
        if dialog.exec_():
            try:
                decrease_value = dialog.get_value()
                self.apply_brightness_decrease(decrease_value)
            except Exception as e:
                print(f"Error in decrease_brightness: {e}")
                QMessageBox.critical(self, "Error",
                                     f"Failed to retrieve brightness"
                                     f" value: {str(e)}")

    def apply_brightness_decrease(self, decrease_value):
        """
                Apply a decrease in brightness to the loaded image.

                Args:
                - decrease_value (float): Value between 0 and 100 representing the
                  percentage decrease in brightness.
                """
        try:
            # Ensure decrease_value is within valid range
            if not (0 <= decrease_value <= 100):
                raise ValueError("Brightness decrease value "
                                 "must be between 0 and 100.")

            cv_img = np.array(self.pil_image)
            factor = 1 - decrease_value / 100.0
            cv_img = cv_img * factor
            cv_img = np.clip(cv_img, 0, 255).astype(np.uint8)
            self.pil_image = Image.fromarray(cv_img)
            self.display_image(self.pil_image)
        except Exception as e:
            print(f"Error applying brightness decrease: {e}")
            QMessageBox.critical(self, "Error",
                                 f"Failed to decrease brightness: {str(e)}")

    def draw_rectangle(self):
        """
                Open a dialog to draw a blue rectangle on the loaded image based on user input.
                """
        dialog = RectangleDialog(self)
        if dialog.exec_():
            coordinates = dialog.get_coordinates()
            self.apply_draw_rectangle(coordinates)

    def apply_draw_rectangle(self, coordinates):
        """
                Draw a blue rectangle on the loaded image using given coordinates.

                Args:
                - coordinates (tuple): Tuple containing (x, y, width, height) of the rectangle.
                """
        try:
            x, y, width, height = coordinates
            cv_img = np.array(self.pil_image)

            # Draw the filled rectangle with a blue color (BGR format)
            cv2.rectangle(cv_img, (x, y), (x + width, y + height),
                          (0, 0, 255), -1)  # -1 fill the rectangle

            self.pil_image = Image.fromarray(cv_img)
            self.display_image(self.pil_image)
        except Exception as e:
            print(f"Error drawing rectangle: {e}")
            QMessageBox.critical(self, "Error", f"Failed to "
                                                f"draw rectangle: {str(e)}")
