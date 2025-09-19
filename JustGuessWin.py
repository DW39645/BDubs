# This is just a WINDOWS OS version of "5.0JustGuess.py"


# # Before running must do following installs:
# pip install pywin32

# # Make sure pip is up to date
# python -m pip install --upgrade pip

# # Install required libraries
# pip install pyautogui
# pip install pygetwindow
# pip install numpy
# pip install pillow

import os
import pygetwindow as gw
import pyautogui  # for screenshots and clicking
import time       # for delays
import numpy as np  # for pixel colors

# Clear terminal and set read position
os.system('cls')  # use 'clear' on Mac/Linux
Check_x = 1200
Check_y = 1100

# Brings desired window to front before screenshot
def bring_app_to_front(app_name):
    try:
        win = gw.getWindowsWithTitle(app_name)[0]
        if win:
            win.activate()
    except IndexError:
        print(f"App '{app_name}' not found.")

# Clicks screen based on GPT response
def Click(response: str):
    # bring_app_to_front("Android Studio")  # Uncomment if needed
    x = 670
    y = 0
    if "1" in response:
        pyautogui.click(x, 620+y)
    elif "2" in response:
        pyautogui.click(x, 665+y)  
    elif "3" in response:
        pyautogui.click(x, 710+y) 
    elif "4" in response:
        pyautogui.click(x, 755+y) 
    elif "PhonePower" in response:
        pyautogui.click(29,138)
    else:
        pyautogui.click(x, 755+y)
    bring_app_to_front("Code")

# Gets pixel color of specific spot to see if question is open
def get_pixel_color(x,y,R,G,B):
    target_color = (R, G, B) 
    
    screenshot = pyautogui.screenshot()
    pixel_color = screenshot.getpixel((x, y))
    
    if len(pixel_color) == 4:
        pixel_color = pixel_color[:3]
    
    pixel_color = np.array(pixel_color)
    target_color = np.array(target_color)
    
    distance = np.linalg.norm(pixel_color - target_color)
    return distance

try:
    gameDelay = input("Enter minutes til next game: ")
    Click("PhonePower")
    print("Waiting for game to begin...")
    time.sleep(int(gameDelay)*60)
    Click("PhonePower")
    
    while True:
        if get_pixel_color(Check_x,Check_y,50,45,45) < 10:
            print("Let the games begin!!")
            QuestionsLeft = 8
            
            while QuestionsLeft > 0:
                difference = get_pixel_color(Check_x,Check_y,255,255,255)
                time.sleep(.05)
                diff = get_pixel_color(Check_x,Check_y,255,255,255)
                
                if difference == diff and difference < 20:
                    Click("1")
                    print("Clicked Q" + str(9-QuestionsLeft) + " and ", end="")
                    QuestionsLeft -= 1
                    
                    if QuestionsLeft > 0:
                        print("waiting for Q" + str(9-QuestionsLeft) + "\n")
                        time.sleep(38)
                    else:
                        time.sleep(25)
                        print("waiting 3m \n")
                        Click("PhonePower")  
                        time.sleep(60*3)  
                        Click("PhonePower")
                        FifteenCheck = 9
                        Fifteen = True
                        
                        while FifteenCheck > 0:
                            if get_pixel_color(Check_x,Check_y,50,45,45) < 10:
                                FifteenCheck = -1
                                Fifteen = False
                            FifteenCheck -= 1
                            print("Checked " + str(9-FifteenCheck) + " times of 9")
                            if FifteenCheck > -1:
                                time.sleep(9)
                        
                        if Fifteen:
                            print("waiting 10.5m \n")
                            Click("PhonePower")  
                            time.sleep(60*10.5)  
                            Click("PhonePower")

        print("Currently Between Games")
        time.sleep(9)

except KeyboardInterrupt:
    print("\nScript Stopped***********************************************************")
