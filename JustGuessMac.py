##This code doesnt read the answer or question, it just waits and guess clicks every time. Less efficient but simple

import os
import AppKit
from Cocoa import NSRunningApplication, NSApplicationActivateIgnoringOtherApps
from AppKit import NSWorkspace
import pyautogui #for screenshots and clicking
import time #for delays
import numpy as np #for pixel colors

#Clear terminal and set read position
os.system('clear')
Check_x = 1200
Check_y = 1100

# Brings desired window to front before screenshot
def bring_app_to_front(app_name):
    workspace = NSWorkspace.sharedWorkspace()
    apps = workspace.runningApplications()
    
    for app in apps:
        if app.localizedName() == app_name:
            app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
            break

#Clicks screen based on GPT response
def Click(response: str):
    # bring_app_to_front("Android Studio")
    x = 670
    y = 0 #-40
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

#Gets pixel color of specific spot to see if question is open
def get_pixel_color(x,y,R,G,B):
    target_color = (R, G, B) 
    
    # Capture the screenshot
    screenshot = pyautogui.screenshot()
    
    # Get the color of the pixel at (x, y)
    pixel_color = screenshot.getpixel((x, y))
    
    # If the pixel color is RGBA (i.e., contains alpha), remove the alpha channel
    if len(pixel_color) == 4:
        pixel_color = pixel_color[:3]  # Only keep the RGB values
    
    # Calculate the Euclidean distance between two RGB colors
    pixel_color = np.array(pixel_color)
    target_color = np.array(target_color)
    #print("Current Color: " + str(pixel_color))
    
    # Compute the Euclidean distance
    distance = np.linalg.norm(pixel_color - target_color)
    return distance

try:
    #initial bit that lets phone remain off til game begins
    gameDelay = input("Enter minutes til next game: ")
    Click("PhonePower")
    print("Waiting for game to begin...")
    time.sleep(int(gameDelay)*60)
    Click("PhonePower")
    
    #Runs until commanded to end "^c"
    while True:

        #Read once every 9 seconds to see if first question is open
        if get_pixel_color(Check_x,Check_y,50,45,45)<10:
            print("Let the games begin!!")
            QuestionsLeft = 8
            
            #Runs eight times, once per question in a game
            while QuestionsLeft>0:
                difference = get_pixel_color(Check_x,Check_y,255,255,255)
                time.sleep(.05)
                diff = get_pixel_color(Check_x,Check_y,255,255,255)
                
                #Waits til question is open then autoclicks random ans
                if difference == diff and difference < 20:
                    Click("1")
                    print("Clicked Q" + str(9-QuestionsLeft) + " and ", end="")
                    QuestionsLeft-=1
                    
                    # Waits for next question
                    if QuestionsLeft>0:
                        print("waiting for Q" + str(9-QuestionsLeft) + "\n")
                        time.sleep(38)
                    
                    #if last question turns off phone for 3 min
                    else:
                        time.sleep(25)
                        print("waiting 3m \n")
                        Click("PhonePower")  
                        time.sleep(60*3)  
                        Click("PhonePower")
                        FifteenCheck = 9
                        Fifteen = True
                        
                        #checks to see if there is a game 3 or 15min later
                        while FifteenCheck>0:
                            if get_pixel_color(Check_x,Check_y,50,45,45)<10:
                                FifteenCheck = -1
                                Fifteen = False
                            FifteenCheck-=1
                            print("Checked " + str(9-FifteenCheck) + " times of 9")
                            if FifteenCheck>-1:
                                time.sleep(9)
                        
                        #if 15 min turns off phone for additional 10.5 min
                        if Fifteen == True:
                            print("waiting 10.5m \n")
                            Click("PhonePower")  
                            time.sleep(60*10.5)  
                            Click("PhonePower")

        print("Currently Between Games")
        time.sleep(9)

        
                          

except KeyboardInterrupt:
    print("\nScript Stopped***********************************************************")
 
