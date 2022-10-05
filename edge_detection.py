import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from skimage.morphology import binary_dilation


def find_edge(img_path, plot=False):
    img = cv.imread(img_path)
    edges = cv.Canny(img,255/3,255)
    edge_dilate = binary_dilation(edges)
    edge_dilate = edge_dilate.astype(np.uint8)
    edge_dilate *= 255
    edge_image = cv.imwrite('gray_images/gray.png', edge_dilate)
    
    if plot:
        plt.subplot(121),plt.imshow(img,cmap = 'gray')
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(edge_dilate,cmap = 'gray')
        plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
        plt.show()

    return edge_dilate

def is_accessible(row, col, i, j, visited, binary_img):
    return 0 <= i and i < row and 0 <= j and j < col and not visited[i][j] and binary_img[i][j] == 0

def BFS(row, col, i, j, visited, island, binary_img):
    # Utility function to do BFS for a 2D boolean matrix. Uses only the 4 neighbors as adjacent vertices
    rowNbr = [-1, 0, 1, 0]
    colNbr = [0, -1, 0, 1]
    q = []
    q.append((i,j))
    visited[i][j] = True

    while len(q) != 0:
        x,y = q.pop(0)
        for k in range(len(rowNbr)):
            if is_accessible(row, col, x + rowNbr[k], y + colNbr[k], visited, binary_img):
                island.append((x + rowNbr[k], y + colNbr[k]))
                visited[(x) + rowNbr[k]][y + colNbr[k]] = True
                q.append((x + rowNbr[k], y + colNbr[k]))

def findIslands(edge_path):
    # height, width, number of channels in image
    edge_img = cv.imread(edge_path)
    binary_img = cv.cvtColor(edge_img, cv.COLOR_BGR2GRAY)
    row = binary_img.shape[0]
    col = binary_img.shape[1]
    # Make a bool array to mark visited cells. Initially all cells are unvisited
    visited = [[False for j in range(col)]for i in range(row)]
    # Initialize count as 0 and traverse through cells of given matrix
    index = 0
    islands = []
    for i in range(row):
        for j in range(col):
            # If a cell with value 0 is not visited yet, then new island found
            if visited[i][j] == False and binary_img[i][j] == 0:
                # Visit all cells in this island and increment island count
                island = []
                BFS(row, col, i, j, visited, island, binary_img)
                if len(island) > 0:
                    islands.append(island)
                index += 1
    return islands

def draw_islands(edge_img_path, islands):
    edge_img = cv.imread(edge_img_path)
    binary_img = cv.cvtColor(edge_img, cv.COLOR_BGR2GRAY)
    island_mask = np.zeros(binary_img.shape)
    for island in islands:
        for point in island:
            island_mask[point[0], point[1]] = 255
        island_mask = island_mask.astype(np.uint8)
    island_mask_img = cv.imwrite('island_images/islands.png',island_mask)
    return island_mask



# img_path = "example_images/brighton_8_apple.png"
# find_edge(img_path)
#Edge image saved as gray_images/gray.png
#Find the Islands!
# islands = findIslands("gray_images/gray.png")

#Draw the Islands (More of test function)
# draw_islands("gray_images/gray.png", islands)
