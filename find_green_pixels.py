import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import binary_opening, binary_erosion


def find_green_pixels(image_path, save_mask_path=None, plot=False):
    image = cv2.imread(image_path)
    num_rows, num_cols, _ = image.shape

    pixel_mask = np.zeros((num_rows, num_cols))

    for i in range(num_rows):
        for j in range(num_cols):
            pixel_rgb = image[i][j]
            r, g, b = pixel_rgb

            # This works for brighton_8 trees and grass
            # if r < 130 and 30 < g and g < 130 and b < 130:
            #     if (g > r + 1 and g > b + 1) or (g > r + 7 and g > b - 10) or (g > b + 7 and g > r - 10):
            #         pixel_mask[i][j] = 255

            # Try to isolate grass only
            if r < 130 and 45 < g and g < 130 and b < 130:
                if (g > r + 6 and g > b + 6) or (g > r + 7 and g > b - 2) or (g > b + 7 and g > r - 2):
                    pixel_mask[i][j] = 255

    # pixel_mask = binary_opening(pixel_mask) # This works for brighton_8 trees and grass
    pixel_mask = binary_erosion(pixel_mask) # Try to isolate grass only
    pixel_mask = pixel_mask.astype(np.uint8)
    pixel_mask *= 255

    # Save green pixel mask
    if save_mask_path is not None:
        cv2.imwrite(save_mask_path, pixel_mask)

    # Overlay green pixel mask on original image
    if plot:
        plt.figure()
        plt.subplot(1, 2, 1)
        plt.imshow(image, interpolation='none')
        plt.subplot(1, 2, 2)
        plt.imshow(image, interpolation='none')
        plt.imshow(pixel_mask, cmap='Greens', interpolation='none', alpha=0.3)
        plt.show()

    return pixel_mask


# Test the function
# file_name = "brighton_8_apple.png"
# file_name = "bpgbc_8_apple.png"
# image_path = f"example_images/{file_name}"
# save_mask_path = f"{file_name}"

# find_green_pixels(image_path, save_mask_path)
