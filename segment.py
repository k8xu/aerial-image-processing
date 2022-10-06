from find_green_pixels import *
from edge_detection import *
import matplotlib.patches as patches


def segment(image_path, plot=False):
    edge_image = find_edge(image_path)
    green_pixel_mask = find_green_pixels(image_path)

    edge_image[green_pixel_mask == 255] = 255
    edge_save_path = "edges_after_removing_green.png"
    cv2.imwrite(edge_save_path, edge_image)

    islands = findIslands(edge_save_path)
    building_mask = np.zeros(edge_image.shape)

    rects = []
    for island_coords in islands:
        island = np.array(island_coords)
        min_area_rect = cv2.minAreaRect(island)
        
        center, dim, rotation = min_area_rect
        center_x, center_y = center
        width, height = dim

        contour_area = cv.contourArea(island)
        
        # Detect potential buildings in islands
        if abs(width - height) < 10 and contour_area > 0.5 * width * height:
            rects.append(min_area_rect)
            for island_x, island_y in island:
                building_mask[island_x][island_y] = 255
        
        cv2.imwrite("building_mask.png", building_mask)
    
    if plot:
        fig, [ax0, ax1, ax2] = plt.subplots(1, 3)

        ax0.imshow(edge_image, interpolation='none')
        ax1.imshow(edge_image, interpolation='none')
        ax1.imshow(building_mask, cmap='Blues', interpolation='none', alpha=0.3)

        rect_to_use = rects[20]
        center, dim, rotation = rect_to_use
        center_x, center_y = center
        width, height = dim
        box = cv.boxPoints(rect_to_use)
        rect = patches.Rectangle(box[0], width, height, angle=rotation, edgecolor='r', linewidth=1, facecolor='none')
        ax2.imshow(edge_image, interpolation='none')
        ax2.add_patch(rect)

        plt.show()


file_name = "brighton_8_apple.png"
image_path = f"example_images/{file_name}"

segment(image_path, plot=True)
