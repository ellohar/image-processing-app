"""
Module for image processing utilities including image orientation correction.
"""
from PIL import ExifTags


def correct_image_orientation(image):
    """
        Corrects the orientation of an image based on its Exif metadata.

        Args:
        - image (PIL.Image.Image): The input PIL image.

        Returns:
        - PIL.Image.Image: The corrected PIL image.
        """
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass
    return image
