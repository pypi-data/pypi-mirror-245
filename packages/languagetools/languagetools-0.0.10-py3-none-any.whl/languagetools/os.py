import os
import tempfile
import pytesseract
import pyautogui
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import time
from PIL import Image
import random
import cairosvg
import numpy as np
import io

# DISABLED as it doesn't work. I don't know why.
# import matplotlib
# matplotlib.use('agg') # all images will be just rasterized and sent up, not interactive

import matplotlib.pyplot as plt

def screenshot(show=True):
    temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    os.system(f"screencapture -x {temp_file.name}")
    
    # Open the image file with PIL
    img = Image.open(temp_file.name)

    # Delete the temporary file
    os.remove(temp_file.name)

    if show:
        # Show the image using matplotlib
        plt.imshow(np.array(img))
        plt.show()

    return img


def find_svg_in_image(svg_code, pil_image):
    png_image = cairosvg.svg2png(bytestring=svg_code)
    svg_image = Image.open(io.BytesIO(png_image))
    opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2GRAY)
    
    svg_image_array = np.array(svg_image)
    if np.any(svg_image_array[:, :, 3] < 255):
        non_transparent_pixels = svg_image_array[svg_image_array[:, :, 3] > 0]
        avg_color = np.mean(non_transparent_pixels, axis=0)

        dist_black = 1 - np.linalg.norm(avg_color[:3] - [0, 0, 0])
        dist_white = 1 - np.linalg.norm(avg_color[:3] - [255, 255, 255])

        background_color = (0, 0, 0) if dist_white > dist_black else (255, 255, 255)
        background = Image.new("RGB", svg_image.size, background_color)
        background.paste(svg_image, mask=svg_image.split()[3])
        opencv_template = cv2.cvtColor(np.array(background), cv2.COLOR_RGB2GRAY)
    else:
        opencv_template = cv2.cvtColor(np.array(svg_image), cv2.COLOR_RGB2GRAY)

    # Open the images
    # cv2.imshow('Image', opencv_image)
    # cv2.imshow('Template', opencv_template)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Initialize ORB detector
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(opencv_image, None)
    kp2, des2 = orb.detectAndCompute(opencv_template, None)

    # Ensure descriptors are valid
    if des1 is None or des2 is None or len(des1) == 0 or len(des2) == 0:
        return None

    # Make sure both descriptors have the same size
    des1_len = len(des1)
    des2_len = len(des2)
    if des1_len < des2_len:
        des1 = np.pad(des1, ((0, des2_len - des1_len), (0, 0)), 'constant')
    elif des2_len < des1_len:
        des2 = np.pad(des2, ((0, des1_len - des2_len), (0, 0)), 'constant')

    # Convert descriptors to the same type
    des1 = des1.astype(np.float32)
    des2 = des2.astype(np.float32)

    # Matcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    print("Matching...")
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)

    # Open all images used, using the systems image viewer (not plt)
    print(pil_image.filename)
    print(svg_image.filename)
    os.system('open ' + pil_image.filename)
    os.system('open ' + svg_image.filename)
    try:
        os.startfile(pil_image.filename)
        os.startfile(svg_image.filename)
    except AttributeError:
        import subprocess
        subprocess.call(['open', pil_image.filename])
        subprocess.call(['open', svg_image.filename])

    # Assuming the best match is the correct match (can be improved)
    if len(matches) > 0:
        best_match = matches[0]
        img_idx = best_match.trainIdx
        (x, y) = kp1[img_idx].pt
        return (int(x), int(y))
    else:
        return None


def find_text_in_image(img, text):
    # Convert PIL Image to NumPy array
    img_array = np.array(img)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)

    # Use pytesseract to get the data from the image
    d = pytesseract.image_to_data(gray, output_type=Output.DICT)

    # Initialize an empty list to store the centers of the bounding boxes
    centers = []

    # Get the number of detected boxes
    n_boxes = len(d['level'])

    # Create a copy of the grayscale image to draw on
    img_draw = np.array(gray.copy())

    # Convert the img_draw grayscale image to RGB
    img_draw = cv2.cvtColor(img_draw, cv2.COLOR_GRAY2RGB)

    id = 0

    # Loop through each box
    for i in range(n_boxes):
        # Print the text of the box
        # If the text in the box matches the given text
        if text.lower() in d['text'][i].lower():
            # Find the start index of the matching text in the box
            start_index = d['text'][i].lower().find(text.lower())
            # Calculate the percentage of the box width that the start of the matching text represents
            start_percentage = start_index / len(d['text'][i])
            # Move the left edge of the box to the right by this percentage of the box width
            d['left'][i] = d['left'][i] + int(d['width'][i] * start_percentage)

            # Calculate the width of the matching text relative to the entire text in the box
            text_width_percentage = len(text) / len(d['text'][i])
            # Adjust the width of the box to match the width of the matching text
            d['width'][i] = int(d['width'][i] * text_width_percentage)

            # Calculate the center of the bounding box
            center = (d['left'][i] + d['width'][i] / 2, d['top'][i] + d['height'][i] / 2)

            """bounding

            bounding

            bounding

            bounding

            bounding    bounding   bounding"""

            # Half both coordinates
            center = (center[0] / 2, center[1] / 2)
                        
            # Add the center to the list
            centers.append(center)

            # Draw the bounding box on the image in red and make it slightly larger
            larger = 10
            cv2.rectangle(img_draw, (d['left'][i] - larger, d['top'][i] - larger), (d['left'][i] + d['width'][i] + larger, d['top'][i] + d['height'][i] + larger), (255, 0, 0), 7)

            # Create a small black square background for the ID
            cv2.rectangle(img_draw, (d['left'][i] + d['width'][i] // 2 - larger*2, d['top'][i] + d['height'][i] // 2 - larger*2), (d['left'][i] + d['width'][i] // 2 + larger*2, d['top'][i] + d['height'][i] // 2 + larger*2), (0, 0, 0), -1)

            # Put the ID in the center of the bounding box in red
            cv2.putText(img_draw, str(id), (d['left'][i] + d['width'][i] // 2 - larger, d['top'][i] + d['height'][i] // 2 + larger), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 155, 155), 4)

            # Increment id
            id += 1

    if not centers:
        word_centers = []
        for word in text.split():
            for i in range(n_boxes):
                if word.lower() in d['text'][i].lower():
                    center = (d['left'][i] + d['width'][i] / 2, d['top'][i] + d['height'][i] / 2)
                    center = (center[0] / 2, center[1] / 2)
                    word_centers.append(center)

        for center1 in word_centers:
            for center2 in word_centers:
                if center1 != center2 and ((center1[0]-center2[0])**2 + (center1[1]-center2[1])**2)**0.5 <= 400:
                    centers.append(((center1[0]+center2[0])/2, (center1[1]+center2[1])/2))
                    break
            if centers:
                break

    bounding_box_image = Image.fromarray(img_draw)
    bounding_box_image.format = img.format

    # Debug by showing bounding boxes:
    # bounding_box_image.show()

    return centers, bounding_box_image

def click(*args, x=None, y=None, show=True, index=None, svg=None):
    if len(args) > 1:
        raise ValueError("Too many positional arguments provided: click(*args, x=None, y=None, show=True, index=None)")
    elif len(args) == 1:
        text = args[0]
        # Take a screenshot
        img = screenshot(show=False)

        # Find the text in the screenshot
        centers, bounding_box_image = find_text_in_image(img, text)

        # If the text was found
        if centers:

            # This could be refactored to be more readable
            if len(centers) > 1:
                if index == None:
                    print(f"This text ('{text}') was found multiple times on screen. Please try 'click()' again, but pass in an `index` int to identify which one you want to click. The indices have been drawn on the attached image.")
                    # Show the image using matplotlib
                    plt.imshow(np.array(bounding_box_image))
                    plt.show()
                    return
                else:
                    center = centers[index]
            else:
                center = centers[0]

            # Slowly move the mouse from its current position to the click position
            pyautogui.moveTo(center[0], center[1], duration=0.5)
            pyautogui.click(center[0], center[1])

        else:
            plt.imshow(np.array(bounding_box_image))
            plt.show()
            print("Your text was not found on the screen. Please try again.")
    elif x is not None and y is not None:
        # Move to the specified coordinates and click
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.click(x, y)
    elif svg is not None:
        # Take a screenshot
        img = screenshot(show=False)
        # Move to the specified coordinates and click
        coordinates = find_svg_in_image(svg, img)
        if coordinates == None:
            print("Not found.")
            return
        pyautogui.moveTo(coordinates[0], coordinates[1], duration=0.5)
        pyautogui.click(coordinates[0], coordinates[1])
    else:
        raise ValueError("Either text or both x and y must be provided")
    
    time.sleep(0.5)
    img = screenshot(show=show)
    return img

def keyboard(text, show=True, modifiers=None):

    if modifiers:
        pyautogui.hotkey(*modifiers, text)
    else:
        # Split the text into words
        words = text.split(' ')

        # Type each word
        for word in words:
            # Type the word
            pyautogui.typewrite(word)
            # Add a delay after each word
            time.sleep(random.uniform(0.1, 0.3))

    time.sleep(0.5)

    img = screenshot(show=show)
    return img