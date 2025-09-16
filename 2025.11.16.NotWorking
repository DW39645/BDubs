import os
import AppKit
from Cocoa import NSRunningApplication, NSApplicationActivateIgnoringOtherApps
from AppKit import NSWorkspace
from Quartz.CoreGraphics import CGEventSourceCreate, kCGEventLeftMouseDown, kCGEventLeftMouseUp
from Quartz import Quartz
from PIL import ImageGrab
import pytesseract
from PIL import Image
from huggingface_hub import InferenceClient
import json
import requests
import pyautogui
import time
import numpy as np
import csv
from fuzzywuzzy import fuzz
from openai import OpenAI
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'



os.system('clear')

# Function to get window bounds (left, top, width, height)
def get_window_bounds(window_title, sideVal,heightVal,height):
    # Get all the windows in the current system
    windows = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID)
    
    for window in windows:
        if window.get('kCGWindowName', '') == window_title:
            window_id = window.get('kCGWindowNumber')
            
            window_frame = Quartz.CGWindowListCreateDescriptionFromArray([window_id])[0]
            window_bounds = window_frame.get('kCGWindowBounds', {})
            
            left = int(window_bounds.get('X', 0)) + sideVal
            top = int(window_bounds.get('Y', 0)) + heightVal
            width = int(window_bounds.get('Width', 0)) - 2 * sideVal
            height = height #Fixed height of window
            
            return left, top, width, height
    
    return None  

# Function to capture a screenshot of a specific window
def capture_window_screenshot(left, top, width, height):
    screenshot = ImageGrab.grab(bbox=(left, top, left + width, top + height))
    screenshot.save('window_screenshot.png')
    #screenshot.show()

# Brings desired window to front before screenshot
def bring_app_to_front(app_name):
    workspace = NSWorkspace.sharedWorkspace()
    apps = workspace.runningApplications()
    
    for app in apps:
        if app.localizedName() == app_name:
            app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
            break

#Runs OCR on the screenshot then calls csv function
def run_OCR():

    image_path = ""  # Replace with the path to your image
    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)
    text = text.replace('\n', ' ').strip()

    # print("OCR Result:")
    # print(text)
    return text
    # will use this later
    # #saves the question to csv file if it isn't already in there
    # save_unique_string_to_csv(text, "")# Replace with the path to your image

# Captures screenshot of specific window 
def capture_window_by_title(window_title,sideVal,heightVal,height):
    bring_app_to_front("Android Studio")

    window_info = get_window_bounds(window_title, sideVal,heightVal,height)
    
    if window_info is None:
        print("Window not found!")
    else:
        left, top, width, height = window_info
        capture_window_screenshot(left, top, width, height)

    text = run_OCR()
    return text
    
# Calls all the above functions to take the screenshots based on manual windowing calibration
def ScreenCaptureCalls():
    #SS and OCR of Q. 2nd crops horizontal. 3rd crops vertical. 4th window height
    Q = capture_window_by_title('Running Devices - Test1', 600,360,100) #Good 9/12/25
    prompt = Q
    #SS and OCR of A1. 2nd crops horizontal. 3rd crops vertical. 4th window height
    A1 = capture_window_by_title('Running Devices - Test1', 645,530,50) #Good 9/12/25
    prompt = prompt + " 1: " + A1
    #SS and OCR of A2. 2nd crops horizontal. 3rd crops vertical. 4th window height
    A2 = capture_window_by_title('Running Devices - Test1', 645,575,50)#Good 9/12/25
    prompt = prompt + " 2: " + A2
    #SS and OCR of A2. 2nd crops horizontal. 3rd crops vertical. 4th window height
    A3 = capture_window_by_title('Running Devices - Test1', 645,620,50)#Good 9/12/25
    prompt = prompt + " 3: " + A3
    #SS and OCR of A2. 2nd crops horizontal. 3rd crops vertical. 4th window height
    A4 = capture_window_by_title('Running Devices - Test1', 645,665,40)#Good 9/12/25
    prompt = prompt + " 4: " + A4 #+ "/Other"

    bring_app_to_front("Code")
    print(prompt)

def call_llm( prompt: str):

    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="",
    )

    completion = client.chat.completions.create(
        model="openrouter/auto",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10,
        extra_body={"reasoning": {"exclude": True}}
    )
    print(completion.choices[0].message.content.strip())
    x = completion.choices[0].message.content.strip()
    prompt = x[:2] #takes first 2 characters of response only
    return prompt

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
    else:
        pyautogui.click(x, 755+y)
    bring_app_to_front("Code")

#Gets pixel color of specific spot to see if question is open
def get_pixel_color(x,y,R,G,B):
    #x, y = 1200, 1200  # Coordinates of the pixel you want to check
    target_color = (R, G, B)
    
    screenshot = pyautogui.screenshot()
    
    pixel_color = screenshot.getpixel((x, y))
    
    if len(pixel_color) == 4:
        pixel_color = pixel_color[:3]  # Only keep the RGB values
    
    # Calculate the Euclidean distance between two RGB colors
    pixel_color = np.array(pixel_color)
    target_color = np.array(target_color)
    print("Current Color: " + str(pixel_color))
    # Compute the Euclidean distance
    distance = np.linalg.norm(pixel_color - target_color)
    return distance

#Saves Prompt to CSV if new or returns old answer if old
def save_unique_string_to_csv(new_string):
    file_path = "/Users/dominicwilson/Documents/VS_Code/Questions.csv"
    similarity_threshold=91
    counter = 0
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            lines = [row for row in reader]  # Extract all rows as lists
    except FileNotFoundError:
        lines = []

    for row in lines:
        counter+=1
        if len(row) >= 2:  
            similarity = fuzz.ratio(new_string, row[0])
            if similarity >= similarity_threshold:
                #os.system('clear')
                print(f"Skipped: Found a similar string in row {counter} with {similarity}% similarity.************************************************************")
                return row[1] 

    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([new_string])
        print("Added new string to CSV.")
        return 100

def save_new_GPT_Answer(response):
    file_path = "" #your file path
    
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        lines = [row for row in reader]

    if lines and len(lines[-1]) >= 1:
        if len(lines[-1]) == 1:
            lines[-1].append(response)

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(lines)
        print("Added response to the second column.")

try:
    while True:
        difference = get_pixel_color(1200,1200,255,255,255)
        time.sleep(.05)
        diff = get_pixel_color(1200,1200,255,255,255)
        if difference == diff and difference < 20:
            #Click("2")#preclick for points
            prompt = ScreenCaptureCalls()
            SeenBefore = save_unique_string_to_csv(prompt)
            if SeenBefore == 100:
                response = call_llm(prompt)
                while SeenBefore == 100:     
                    if any(char.isdigit() for char in response):
                        Click(response)
                        save_new_GPT_Answer(response)
                        SeenBefore = 99
                    else:
                        print("No numbers in response.")
                        response = call_llm(prompt)
                time.sleep(33)              
            else:
                Click(SeenBefore)
                time.sleep(33)
        #time.sleep(.05)

except KeyboardInterrupt:
    print("\nScript Stopped***********************************************************")
