# Image Processing App

Photo Editor is a simple desktop application for photo editing, written in Python using the PyQt5 and OpenCV libraries. 
The application allows you to load photos, resize them, adjust brightness, add rectangles, and save edited photos. 
It also includes the ability to take photos using a camera.

## Features
* **Load Photo:** Load an image from your computer for editing.
* **Take Photo:** Capture an image using a camera and edit it.
* **Display Red Channel:** Show only the red channel of the photo.
* **Display Green Channel:** Show only the green channel of the photo.
* **Display Blue Channel:** Show only the blue channel of the photo.
* **Resize Photo:** Resize the loaded photo.
* **Decrease Brightness:** Decrease the brightness of the photo.
* **Draw Rectangle:** Draw a rectangle to the photo.

## Requirements
- Python 3.8
- pip
- Git

## Installation and Running
### 1. Clone the repository
```sh
git clone https://github.com/ellohar/image-processing-app.git
cd image_processing_app
```
### 2. Create and activate a virtual environment
Using Windows:   
```
python -m venv venv
venv\Scripts\activate
```      
Using 'conda':   
```
conda create --name myenv python=3.8
conda activate myenv
```   
### 3. Install dependencies
`pip install -r requirements.txt`
### 4. Run the application
`python main.py`

## Project Structure
* `start_window.py`: The main application file containing the primary GUI and core editing functions.
* `camera_widget.py`: A module for camera operations, allowing image capture.
* `dialogs.py`: A module containing dialog windows for resizing and adjusting brightness of the image, as well as adding rectangles.
* `utils.py`: Utility functions for image processing.

## Usage Examples
### Loading a Photo
1. Click the "Load Photo" button.
2. Select an image file from your computer.
### Displaying Color Channels
* **Red Channel:** Click the "Red Channel" button to display only the red channel of the photo.
* **Green Channel:** Click the "Green Channel" button to display only the green channel of the photo.
* **Blue Channel:** Click the "Blue Channel" button to display only the blue channel of the photo.
### Resizing a Photo
1. Click the "Resize Photo" button.
2. Set the desired resize factor.
3. Click "OK" to apply the changes.
### Decrease Photo Brightness
1. Click the "Decrease Brightness" button.
2. Decrease the brightness slider to the desired level.
3. Click "OK" to apply the changes.
### Draw a Rectangle
1. Click the "Draw Rectangle" button.
2. Draw a rectangle on the image in the dialog window.
3. Click "OK" to apply the changes.
