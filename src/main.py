# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Copyright: Dwaipayan Deb @ 2024

import cv2
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import filedialog
import os
from datetime import datetime
import json

n=3 # Default number of profile divisions
shadow_pattern=[]
current_directory=os.getcwd()
file_out=open('shadow_pattern.csv','w')
f2=open("output.txt",'a')

print("------------------------------")
print("*** Shadow2Profile ***")
print("\nVersion: 0.1.0")

print("\nShadow2Profile is a roughness estimation tool from an image of rough surface with known illumination angle.")
print("Surface image should be taken in Normally Viewed condition when parallel light is coming from Right to Left.")
print("This program will first generate a shadow pattern (x coordinate,shadow-length) from threshold image and store in a CSV file.")
print("This data is then read to calculate best fitted roghness parameters (Average-slope,Ra).")
print("The Ra value will be given in terms of unit length. To get the value in desired unit, multiply this by (No. of profile divisions x Actual length in desired unit)")
print("All output data is stored in 'output.txt'")
print("Equivalent roughness profile data (x,y) will be saved at 'profile.csv'")
print("\nFor more information please read the paper doi:....")

print("\nThis project is distributed under Apache License Version 2.0 http://www.apache.org/licenses/")
print("2024 \u00A9 Dwaipayan Deb")
print("------------------------------")
input("Press enter to proceed")

profile_generated=False

# Function to select an image using a file dialog
def select_image():
    global image_file
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")]
    )
    image_file=os.path.basename(file_path)
    return file_path

def get_number_input():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    number = simpledialog.askinteger("Divisions", "Please enter number of profile divisions:")
    if number is not None:
        print(f"Proceeding with {number} profile divisions")
        return number
    else:
        messagebox.showinfo("No Input", "You didn't enter a number!\nProceeding with default 3")
        print(f"Proceeding with {n} profile divisions")
        return None

# Mouse callback function to display pixel value
def show_pixel_value(event, x, y, flags, param):
    if profile_generated==False:
        global img_displayed
        img_displayed = img_resized.copy()  # Reset the displayed image
        if event == cv2.EVENT_MOUSEMOVE:
            # Get the pixel value at (x, y)
            if 0 <= x < img_resized.shape[1] and 0 <= y < img_resized.shape[0]:
                pixel_value = img_resized[y, x]
                # Display coordinates and grayscale value on the image in red color
                text = f"X: {x}, Y: {y}, Gray: {pixel_value}"
                # Text color is red (BGR: 0, 0, 255)
                cv2.putText(img_displayed, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                            0.8, (0, 0, 255), 2, cv2.LINE_AA)  # Red text

# Function to resize the image for zoom
def resize_image(scale_factor):
    global img_resized, width,height
    width = int(img.shape[1] * scale_factor)
    height = int(img.shape[0] * scale_factor)
    img_resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_LINEAR)

# Function to apply threshold based on the slider value
def apply_threshold(value):
    global img_displayed, threshold_value
    threshold_value = value
    _, img_displayed = cv2.threshold(img_resized, threshold_value, 255, cv2.THRESH_BINARY)

def create_pattern(divisions):    
    h=height//(divisions+1)   # height is image height
    shadow_length=0
    for i in range(divisions):
        i=i+1
        start_point = (0, i*h)  # (x, y) starting point
        end_point = (width, i*h)  # (x, y) ending point
        color = (0, 255, 0) 
        thickness = 2  # Thickness in pixels
        #print(height,i*h)
        for x in range(width):
            intensity=img_displayed[i*h,x]
            x_continued=x+(i-1)*width
            if intensity==0:
                shadow_length=shadow_length+1
            else:
                if shadow_length!=0:
                    #shadow_pattern.append([x_continued,shadow_length])
                    file_out.write(str(x_continued/(divisions*width))+","+str(shadow_length/(divisions*width))+'\n')
                shadow_length=0

        # Draw the line on the image
        cv2.line(img_displayed, start_point, end_point, color, thickness)
    file_out.close()
    f2.write(f"\n\nPattern created with {n} profile divisions for: '"+image_file+"'  at: "+str(datetime.now()))
    f2.close()
    print()
    print(f"Pattern succesfully crteated and saved to '{current_directory}\shadow_pattern.csv'")
    print("Close the image window to proceed\n")

def save_settings(filename, settings):
    with open(filename, 'w') as json_file:
        json.dump(settings, json_file, indent=4)





print("Select image....")
# Open a dialog box to select an image
image_path = select_image()

# Check if an image was selected
if image_path:
    print("\nSelected image: "+image_path)
    print()
    print("INSTRUCTIONS:")
    print("1) Hover mouse to inspect threshold value manually")
    print("2) Press Enter to view thresold image")
    print("3) Use slider to select new threshold")
    print("4) Press 'Ctrl+s' to save displayed image")
    print("5) Press '+' (or '=') to Zoom In and '-' to Zoom Out")
    print("6) Press 'p' to generate shadow pattern")
    print("7) Press 'Esc' to exit")
    print()
    # Load the selected image in grayscale mode
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    height,width =img.shape
    #print(height,width)
    # Find the minimum and maximum grayscale values in the image
    min_val, max_val, _, _ = cv2.minMaxLoc(img)

    # Set the default threshold to be the midpoint between the min and max grayscale values
    default_threshold = int((min_val + max_val) / 2)

    # Initialize the image to be displayed (start with original image)
    img_resized = img.copy()
    img_displayed = img.copy()

    # Create a window
    cv2.namedWindow('Threshold Image')

    # Set the mouse callback function for the window
    cv2.setMouseCallback('Threshold Image', show_pixel_value)

    # Create a trackbar (slider) for threshold adjustment
    cv2.createTrackbar('Threshold', 'Threshold Image', default_threshold, 255, apply_threshold)

    # Apply the initial threshold
    #apply_threshold(default_threshold)

    # Initialize zoom factor
    zoom_factor = 1.0
    zoom_step = 0.1  # Change in zoom factor
    closed=False
    # Display the image with zoom in/out and threshold functionality
    while True:
        cv2.imshow('Threshold Image', img_displayed)

        key = cv2.waitKey(1) & 0xFF
        #print(key)
        # If ESC key is pressed, exit
        if key == 27:  # ESC key
            break

        if key == 13:  #Enter key
            apply_threshold(threshold_value)

        if profile_generated==True and closed==False:
            tk.messagebox.showinfo("Pattern Created", "Pattern created!\nColse image window to proceed")
            closed=True

        if key == 112:  #P
            if profile_generated==False:
                #n_str=input('Give number of profile divisions \n(Press Enter to go with Default 3):')
                n=get_number_input()
                if n==None:
                    n=3
                apply_threshold(threshold_value)
                create_pattern(n)
                profile_generated=True
                settings = {
                    "divisions": n
                }
                # Save settings to a file
                save_settings('settings.json', settings)
            else:
                tk.messagebox.showinfo("Pattern Created", "Pattern already created!\nColse image window to proceed")
        
        # Check if the window is closed
        if cv2.getWindowProperty('Threshold Image', cv2.WND_PROP_VISIBLE) < 1:
            break

        # Zoom in with '+'
        if key == ord('+') or key == ord('='):
            zoom_factor += zoom_step
            resize_image(zoom_factor)
            apply_threshold(threshold_value)  # Apply the current threshold after resizing
            print(f"Zoomed In: {zoom_factor:.1f}x")

        # Zoom out with '-'
        elif key == ord('-'):
            zoom_factor = max(zoom_factor - zoom_step, 0.1)  # Prevent zooming out too much
            resize_image(zoom_factor)
            apply_threshold(threshold_value)  # Apply the current threshold after resizing
            print(f"Zoomed Out: {zoom_factor:.1f}x")

    # Close the window and clean up
    cv2.destroyAllWindows()
    if profile_generated==False:
        print("No new shadow pattern is generated.")
    answer=input('Would you like to find roughness parameters (Y/N)?')
    if answer=='Y' or answer=='y':
        print("\nStarting fitting program...\n")
        try:
            import  module1
        except:
            print("\nAn error has occurred")
    else:
        print("Terminating process...")

else:
    print("No image selected. Exiting...")

#print(shadow_pattern)









