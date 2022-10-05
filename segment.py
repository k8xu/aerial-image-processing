from find_green_pixels import *
from edge_detection import *


def segment(image_path):
    green_pixel_mask = find_green_pixels(image_path)

    edge_image = find_edge(image_path)

    edge_image[green_pixel_mask == 255] = 255
    edge_save_path = "edges_after_removing_green.png"
    cv2.imwrite(edge_save_path, edge_image)

    islands = findIslands(edge_save_path)
    # island_mask = draw_islands(edge_save_path, islands)

    for island in islands:
        island = np.array(island)
        min_area_rect = cv2.minAreaRect(island)

        box = cv.boxPoints(min_area_rect)
        box = np.int0(box)
        cv2.imwrite("box.png", box)
        cv.drawContours(edge_image,[box],0,(0,0,255),2)
        break


file_name = "brighton_8_apple.png"
image_path = f"example_images/{file_name}"

segment(image_path)
