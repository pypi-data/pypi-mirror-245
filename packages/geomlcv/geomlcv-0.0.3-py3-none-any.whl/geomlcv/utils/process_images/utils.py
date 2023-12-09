import os
from typing import Callable

import cv2
import numpy as np
from skimage.feature import hog
from sklearn.decomposition import PCA


def generate_preprocessed_dir(
    input_dir: str, preprocess_function: Callable, output_dir: str = "images_pcahog"
):
    # Get list of all items in input_dir
    all_items = os.listdir(input_dir)

    # Filter only the folders
    folders = [
        item for item in all_items if os.path.isdir(os.path.join(input_dir, item))
    ]

    # Access to train, test and valid datasets
    for folder in folders:
        folder_dataset = os.path.join(input_dir, folder, "images")
        list_images = os.listdir(folder_dataset)

        # Create dir to save new images
        dir_output = os.path.join(input_dir, folder, output_dir)
        os.makedirs(dir_output)

        for image_name in list_images:
            # Load image
            path_image = os.path.join(folder_dataset, image_name)
            image = cv2.imread(path_image)

            output_image = preprocess_function(image)

            path_output = os.path.join(dir_output, image_name)
            cv2.imwrite(path_output, output_image)


def _pcahog(image):
    # --------------- PCA ---------------
    # Reshape the data to have one pixel per row
    reshaped_data = image.reshape((-1, 3))

    # Apply PCA to reduce to 2 channels
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(reshaped_data)

    # Reshape back to the original shape
    reduced_image = reduced_data.reshape(image.shape[0], image.shape[1], -1)

    # Convert to uint8
    reduced_image_converted = reduced_image.astype(np.uint8)

    # --------------- HOG ---------------
    # Create hog image
    fd, hog_image = hog(
        image,
        orientations=9,
        pixels_per_cell=(8, 8),
        cells_per_block=(2, 2),
        visualize=True,
        channel_axis=-1,
    )

    # Convert hog image to uint8
    hog_image_converted = hog_image.astype(np.uint8)

    # --------------- PCA + HOG ---------------
    pca_hog_image = np.stack(
        (
            reduced_image_converted[:, :, 0],
            reduced_image_converted[:, :, 1],
            hog_image_converted,
        ),
        axis=-1,
    )

    return pca_hog_image


def _svhog(image):
    # Convert to hsv and extract channels
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = hsv_image[:, :, 0], hsv_image[:, :, 1], hsv_image[:, :, 2]  # noqa

    # Create HOG image
    fd, hog_image = hog(
        image,
        orientations=9,
        pixels_per_cell=(8, 8),
        cells_per_block=(2, 2),
        visualize=True,
        multichannel=True,  # TODO: deprecated in latest version
    )

    # Convert hog image to uint8
    # TODO: is this used?
    hog_image_converted = hog_image.astype(np.uint8)

    # Merge s channel, v channel and hog image
    svh_image = np.stack((s, v, hog_image_converted), axis=-1)

    return svh_image
