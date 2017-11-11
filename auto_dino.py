import numpy as np
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import base64
import io
from PIL import Image

from tqdm import tqdm

def get_cactus_height(x,y, img):
    while np.any(img[x,y-7:y+7]):
        x -= 1
    return x

def find_cacti(img):
    height,width = np.shape(img)
    dino = img[height//2:,:height//2]
    vision = round(height*.8)
    bird_vision = round(height*0.6)
    field = img[vision,height//2 - width//30 - 5:] + img[bird_vision,height//2 - width//30 - 5:]
    distance = []
    cacti_height = []
    prev_pixel = field[0]
    cur_dist = 0
    for i,pixel in enumerate(field):
        if prev_pixel == 0 and pixel != 0:
            distance.append(cur_dist)
            cacti_height.append(get_cactus_height(vision, height//2 - width//30 - 5 + i, img))
        if pixel == 0:
            cur_dist += 1
        prev_pixel = pixel
    return distance, cacti_height


def run():
    js_call = "return document.getElementsByClassName('runner-canvas')[0].toDataURL('image/png').substring(21);"
    second_js = "Runner.instance_.tRex.startJump({})"
    cur_speed_js = "return Runner.instance_.currentSpeed"
    cur_dist_js = "return Runner.instance_.distanceRan"
    digits_js = "return Runner.instance_.distanceMeter.digits"
    url = "https://chromedino.com/"
    browser = webdriver.Chrome()
    try:
        browser.get(url)
        s = 0

        # start the first game of dino run
        body = browser.find_element_by_id('t')
        body.send_keys(Keys.ARROW_UP)
        
        prev_dist = 0

        speed_factor = 0.999
        counter = 0
        while True:
            s += 1
            print("{}".format("".join(browser.execute_script(digits_js))))
            time.sleep(.0015)
            speed_factor += .0001
            if speed_factor > 2.5:
                speed_factor = 2.5
            b64_image = browser.execute_script(js_call)
            image = base64.b64decode(b64_image)
            buf = io.BytesIO(image)
            img = Image.open(buf).convert('LA')
            np_img = np.array(img)[:,:,0]
            distances, heights = find_cacti(np_img)
            
            counter += 1
            if counter % 60 == 0:
                cur_dista = browser.execute_script(cur_dist_js)
                if prev_dist == cur_dista and cur_dista > 20:
                    speed_factor = 0.999
                    command = input("Type Q to quit")
                    if command == 'Q':
                        break
                    else:
                        body.send_keys(Keys.ARROW_UP)
                    # This is a game over
                else:
                    prev_dist = cur_dista

            if len(distances) != 0:
                distances_copy = distances.copy()
                for i,v in enumerate(distances_copy):
                    try:
                        if abs(distances_copy[i+1] - v) < 10:
                            distances.remove(v)
                        else:
                            break
                    except:
                        pass
                # We know we need to jump over something, how tall is it?
                if 85 <= heights[0] <= 95:
                    
                    if distances[0] < (102 * speed_factor):
                        print("Obstacle Located...")
                        print("Jumping...")
                        cur_speed = float(browser.execute_script(cur_speed_js))
                        browser.execute_script(second_js.format(cur_speed))
                if 95 <= heights[0] <= 103:
                    
                    if distances[0] < (113 * speed_factor):
                        print("Obstacle Located...")
                        print("Jumping...")
                        cur_speed = float(browser.execute_script(cur_speed_js))
                        browser.execute_script(second_js.format(cur_speed))
                if 104 <= heights[0]:

                    if distances[0] < (116 * speed_factor):
                        print("Obstacle Located...")
                        print("Jumping...")
                        cur_speed = float(browser.execute_script(cur_speed_js))
                        browser.execute_script(second_js.format(cur_speed))
            
    except Exception as e:
        print("Errored out at step 1", e)
        time.sleep(10)
    finally:
        browser.close() #make sure we close it when we are finished.

if __name__ == "__main__":
    run()