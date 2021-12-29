import time
import pyautogui
import cv2
import numpy as np
import random
import sys



startX, startY = 5, 500
THRESHOLD = 0.57
NONMERGECOUNT = 0
rocks = ['rock7.png', 'rock8.png', 'rock9.png', 'rock10.png',
         'rock11.png', 'rock11.png', 'rock12.png', 'rock13.png',
         'rock14.png', 'rock15.png', 'rock16.png', 'rock17.png',
         'rock18.png', 'rock19.png', , 'rock20.png']


def equalize_image_hist(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    eq_hist_image = cv2.equalizeHist(gray_image)
    # cv2.imshow('img', eq_hist_image)
    # cv2.waitKey(0)
    return eq_hist_image

def sharp_process(image):
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    sharp_image = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
    return sharp_image

def blur_process(image):
    blur_3x3_image = cv2.GaussianBlur(image,(3,3), sigmaX=0, sigmaY=0)
    # cv2.imshow('img', blur_3x3_image)
    # cv2.waitKey(0)
    return blur_3x3_image


def check_color_similarity(template, match1, match2):
    '''
        Check if average color of template is similar to match
    '''
    # Check match 1
    if ((match1[0]*0.85 < template[0] < match1[0]*1.15) and (match1[1]*0.85 < template[1] < match1[1]*1.15) and (match1[2]*0.85 < template[2] < match1[2]*1.15)):
        # Check match 2
        if ((match2[0]*0.85 < template[0] < match2[0]*1.15) and (match2[1]*0.85 < template[1] < match2[1]*1.15) and (match2[2]*0.85 < template[2] < match2[2]*1.15)):
            return True

def merge_rocks(screenshot, rock_template, matches_filtered):
    for point in zip(*matches_filtered[::-1]):
        # print(111)
        for point2 in zip(*matches_filtered[::-1]):
            if ((abs(point[0] - point2[0]) > 25) or (abs(point[1] - point2[1]) > 25)):
                # print('Found potential matches', point, point2)
                # print(matches_filtered[::-1])
                width, height, channels = rock_template.shape
                avg_color_per_row = np.average(rock_template, axis=0)
                template_avg_color = np.average(avg_color_per_row, axis=0)
                # print('rock template avg colors:', template_avg_color[0])
                # print(sum(avg_color))
                # cv2.imshow('img', rock_template)
                # cv2.waitKey(0)
                screenshot_rock_match1 = screenshot[point[1]:point[1]+height, point[0]:point[0]+width]
                screenshot_rock_match2 = screenshot[point2[1]:point2[1]+height, point2[0]:point2[0]+width]
                avg_color_per_row = np.average(screenshot_rock_match1, axis=0)
                match1_avg_color = np.average(avg_color_per_row, axis=0)

                avg_color_per_row = np.average(screenshot_rock_match2, axis=0)
                match2_avg_color = np.average(avg_color_per_row, axis=0)
                # cv2.rectangle(screenshot, point, (point[0] + width, point[1] + height), (0, 204, 153), 0)
                # cv2.imshow('img', screenshot)
                # cv2.waitKey(0)
                if(check_color_similarity(template_avg_color, match1_avg_color, match2_avg_color)):
                    print('Found matches')
                    # Click and drag to combine rocks
                    pyautogui.moveTo(startX + point[0]+random.randint(13,21), startY + point[1]+random.randint(13,21))
                    time.sleep(random.uniform(0.08, 0.12))
                    pyautogui.mouseDown(button='left')
                    time.sleep(random.uniform(0.08, 0.12))
                    pyautogui.moveTo(startX + point2[0]+random.randint(13,21), startY + point2[1]+random.randint(13,21), random.uniform(0.15, 0.4))
                    time.sleep(random.uniform(0.08, 0.12))
                    pyautogui.mouseUp()
                    time.sleep(random.uniform(1, 1.35))
                    return True

def iterate_rocks(screenshot):
    for rock in rocks:
        # print(rock)
        rock_template = cv2.imread(f'images/{rock}')
        # rock_template = blur_process(rock_template)

        matches = cv2.matchTemplate(screenshot, rock_template, cv2.TM_CCOEFF_NORMED)
        matches_filtered = np.where(matches >= THRESHOLD)
        if(merge_rocks(screenshot, rock_template, matches_filtered)):
            print('Combined rock')
            # Reset non-merge counter
            global NONMERGECOUNT
            NONMERGECOUNT = 0
            # time.sleep(random.uniform(0.4, 0.6))
            return True
    return None

minutes = int(sys.argv[1])
seconds = 60 * minutes
start_time = time.time()

while True:
    # Take screenshot, save and read it
    print('Taking screenshot')
    screenshot = pyautogui.screenshot(region=(startX, startY, 340, 170))
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    cv2.imwrite("images/screenshot.png", screenshot)
    screenshot = cv2.imread('images/screenshot.png')
    # screenshot = blur_process(screenshot)
    # Iterate through rocks
    if (not iterate_rocks(screenshot)):
        # If checked all rocks and none was merged, wait to gather more rocks
        print('Waiting to gather rocks')
        NONMERGECOUNT += 1
        print('NONMERGECOUNT:', NONMERGECOUNT)
        # If did not merge consecutive times, press 'Esc' (possible ad)
        if (NONMERGECOUNT > 55):
            print('pressing escape')
            pyautogui.press('esc')
        time.sleep(random.uniform(3.5, 4.5))
    print('Re-scanning')

    # End program if elapsed time is over parameter
    current_time = time.time()
    elapsed_time = current_time - start_time
    if elapsed_time > seconds:
        break


# # screenshot = pyautogui.screenshot(region=(5,500, 340, 170))
# screenshot = pyautogui.screenshot()
# screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
# cv2.imwrite("images/screenshot.png", screenshot)
# screenshot = cv2.imread('images/screenshot.png')
# # Iterate through rocks
# rock_template = cv2.imread(f'images/rock1.png')
# width, height, channels = rock_template.shape

# matches = cv2.matchTemplate(screenshot, rock_template, cv2.TM_CCOEFF_NORMED)
# matches_filtered = np.where(matches >= 0.60)
# print(len(matches_filtered))
# print(matches_filtered)
# for point in zip(*matches_filtered[::-1]):
#     for point2 in zip(*matches_filtered[::-1]):
#         print('point1:', point, 'point2:', point2)
#         if ((abs(point[0] - point2[0]) > 25) and (abs(point[1] - point2[1]) > 25)):
#             pyautogui.moveTo(point[0]+8, point[1]+8)
#             time.sleep(1)
#             pyautogui.mouseDown(button='left')
#             pyautogui.moveTo(point2[0]+8, point2[1]+8, 3)
#             pyautogui.mouseUp()
#             break
#         else:
#             continue
#     cv2.rectangle(screenshot, point, (point[0] + width, point[1] + height), (0, 204, 153), 0)

# cv2.imshow('img', screenshot)
# cv2.waitKey(0)