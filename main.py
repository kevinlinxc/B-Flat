import easygui
import os
from pdf2image import convert_from_path
import shutil
import matplotlib.pyplot as plt
plt.rcParams["keymap.quit"] = ['ctrl+w', 'cmd+w', 'q', 'space']  # enable easy quitting of matplotlib windows
from PIL import Image
import numpy as np
import cv2
import math

track_title = "Use this window to crop the sides of a row of measures. Select the row and hit any key to finish with " \
              "that row. "
left = None
right = None
current_image = None
padding = 10
output_name = "output90.png"


def wipe_directory(path):
    """Deletes files AND folders in a path"""
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        try:
            shutil.rmtree(filepath)
        except OSError:
            os.remove(filepath)


def open_image(path):
    image = Image.open(path)
    image = image.convert('L')  # grayscale mode
    return np.array(image)


def line_contrast(page_image):
    """Helper function for finding the max contrast for every line. Low contrast are likely to be whitespace."""
    line_contr = []
    for line in page_image:  # determine range per line
        line_contr.append(max(line) - min(line))
    return line_contr


def find_rows(line_contr):
    """
    Finds the rows of sheet music on a page.

    returns tuples of y coordinate (start, end) for each row
    """
    detected_rows = []
    row_start = 0
    row_end = 0
    detect_state = 0  # 0 if previous line was not part of a row
    cur_row = 0
    for contrast in line_contr:
        # once a row starts, detect_state becomes 1 and we're waiting for the boundary from 1 to 0
        if contrast < 50 and detect_state == 0:
            row_start = cur_row
        elif contrast >= 50 and detect_state == 0:
            row_start = cur_row
            detect_state = 1
        elif contrast < 50 and detect_state == 1:  # if end of row, evaluate AOI height
            row_end = cur_row
            rowheight = row_start - row_end
            if abs(rowheight) >= 150:
                detected_rows.append((row_start, row_end))
            detect_state = 0
        elif contrast >= 50 and detect_state == 1:
            pass
        else:
            print("unknown situation, help!, detection state: " + str(detect_state))
        cur_row += 1
    return detected_rows


def on_trackbar(var):
    """Callback for trackbar to crop to just the measures"""
    global left
    global right
    left = cv2.getTrackbarPos("left", track_title)
    right = cv2.getTrackbarPos("right", track_title)
    cv2.imshow("current_image", current_image[top:bottom, left:right])


def main():
    global top, bottom, current_image
    # 1. Get the pdf file from the user
    print("Please choose a pdf file you would like to cut up")
    file_path = easygui.fileopenbox()
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    # 2. Convert the pdf to a series of images
    poppler_version = "poppler-21.08.0"
    poppler_path = os.path.join(os.getcwd(), poppler_version, "Library", "bin")
    pages = convert_from_path(file_path, poppler_path=poppler_path)
    temp_path = os.path.join(os.getcwd(), "temp")
    wipe_directory(temp_path)
    saved_rows = []
    num_pages = len(pages)
    for index, page in enumerate(pages):
        page_name = f"{index} - {file_name}.jpg"
        page.save(f"{os.path.join(temp_path, page_name)}", format="jpeg")

    # 3. For each image, find the rows of sheet music
    for i in range(num_pages):
        page_name = f"{i} - {file_name}.jpg"
        image_path = os.path.join(temp_path, page_name)
        img = open_image(os.path.join(os.getcwd(), image_path))
        img_copy = img.copy()
        height = img.shape[0]
        line_contr = line_contrast(img)
        detected_rows = find_rows(line_contr)

        # 4. For each detected row, allow the user to crop it
        for row_index, row in enumerate(detected_rows):
            top = 0 if row[0] - padding < 0 else row[0] - padding
            bottom = height if row[1] + padding > height else row[1] + padding

            cv2.namedWindow(track_title)
            cv2.resizeWindow(track_title, 1000, 240)
            staff_row = img[top:bottom, :]
            rightmost = img.shape[1]
            current_image = img
            cv2.imshow(f"current_image", staff_row)
            track_left_start = left if left else 0
            track_right_start = right if right else rightmost

            cv2.createTrackbar("left", track_title, track_left_start, rightmost, on_trackbar)
            cv2.createTrackbar("right", track_title, track_right_start, rightmost, on_trackbar)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            img[row[0], left:right] = 0
            img[row[1], left:right] = 0
            img[row[0]:row[1], left] = 0
            img[row[0]:row[1], right - 1] = 0

            print(f"top: {top}, bottom: {bottom}, left: {left}, right: {right} for line {row_index} for page {i}")
            saved_rows.append(img_copy[top:bottom, left:right])

        show = plt.imshow(img, cmap='gray')
        wm = plt.get_current_fig_manager()
        wm.window.state('zoomed')
        plt.show()
    cv2.destroyAllWindows()
    max_height = 0
    for row in saved_rows:
        height = row.shape[0]
        max_height = max(height, max_height)
        # cv2.imshow("Results", row)
        # cv2.waitKey(0)
    print(f"Max height: {max_height}")
    final_array = np.ones((max_height, 1)) * 255
    for i in range(len(saved_rows)):
        row_height = saved_rows[i].shape[0]
        height_diff = max_height - row_height
        bot_padding = math.ceil(height_diff / 2)
        top_padding = math.floor(height_diff / 2)
        padded = cv2.copyMakeBorder(saved_rows[i], top_padding, bot_padding, 0, 0, cv2.BORDER_CONSTANT, value=[255])
        final_array = np.hstack([final_array, padded])
    img_rotate_90_clockwise = cv2.rotate(final_array, cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite(output_name, img_rotate_90_clockwise)
    print(f"Saved rows to {output_name}")


if __name__ == '__main__':
    main()