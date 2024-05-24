from PIL import Image, ImageOps
import math
import cv2
import os
import tkinter as tk

# to convert an image to ascii, call asciify with image path and name of desired output file. ex:
# asciify("tomka.jpeg", "tomka")

# to convert a video to ascii, call extract_frames with video path and folder_to_ascii with directory name where the frames will go. ex:
# extract_frames("dog.mov")
# folder_to_ascii("frames")
# first, the specified video has frames extracted and placed into the frames directory. Then, each frame is converted into ascii
# and placed into the asciiframes directory. Last, 

# extract frames from a video
def extract_frames(video):
    print("Extracting frames")
    os.makedirs("frames", exist_ok=True)
    os.makedirs("asciiframes", exist_ok=True)
    # clear the frames and asciiframes folder if there's stuff in it
    directory_paths = ['./frames','./asciiframes']
    for directory in directory_paths:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Removes the file or symbolic link

    cam = cv2.VideoCapture(video)
    current_frame = 0
    while(True):
        ret, frame = cam.read()
        if ret:
            name = "./frames/frame" + str(current_frame) + ".jpg"
            cv2.imwrite(name, frame)
            current_frame += 1
        else:
            break
    
    cam.release()
    cv2.destroyAllWindows()
    print("Finished extracting")

# given a path to an image, print ascii text conversion to a .txt file
def asciify(path, out_file):
    im1 = Image.open(path)

    # grayscale
    im2 = ImageOps.grayscale(im1)

    # resize
    width, height = im2.size
    current_res = width * height
    # This is the number of pixels. change it to increase/decrease resolution.
    desired_res = 20000
    scale_factor = (desired_res/current_res) ** 0.5
    im = im2.resize((math.ceil(width*scale_factor), math.ceil(height*scale_factor)))

    # get pixel vals
    pixel_vals = list(im.getdata())

    # categorizing pixels into ascii characters. uncomment for a more expansive set of characters.
    ascii_chars = ["@","%","#","*","+","=","-",":","."," "]
    # ascii_chars = ['$', '@', 'B', '%', '8', '&', 'W', 'M', '#', '*', 'o', 'a', 'h', 'k', 'b', 'd', 'p', 'q', 'w', 'm', 'Z', 'O', '0', 'Q', 'L', 'C', 'J', 'U', 'Y', 'X', 'z', 'c', 'v', 'u', 'n', 'x', 'r', 'j', 'f', 't', '/', '\\', '|', '(', ')', '1', '{', '}', '[', ']', '?', '-', '_', '+', '~', 'i', '!', 'l', 'I', ';', ':', ',', '"', '^', '`', "'", '.', ' ']

    min_val = min(pixel_vals)
    max_val = max(pixel_vals)
    # step = (max_val-min_val) // 5
    step = (max_val-min_val) // len(ascii_chars)

    # 0 - 500 (min and max values)
    # step is 50
    print(step)
    print(max_val)

    # for each pixel assign it an ascii based on grayscale value
    ascii = ""
    row_counter = 0
    # this was my original implementation. it just converts each pixel to an ascii character based on it's value.
    # for pixel in pixel_vals:
    #     if pixel < step + min_val:
    #         ascii += ("@")
    #     elif pixel < step*2 + min_val:
    #         ascii += ("%")
    #     elif pixel < step*3 + min_val:
    #         ascii += ("*")
    #     elif pixel < step*4 + min_val:
    #         ascii += (".")
    #     elif pixel <= max_val:
    #         ascii += (" ")
    for pixel in pixel_vals:
        # calculate the index in the ascii list corresponding to the pixel
        index = pixel//step 
        # set overflow pixels to be the darkest value
        if index >= len(ascii_chars):
            index = len(ascii_chars) - 1
        character = ascii_chars[index]
        ascii += character

        # restore dimensions by adding a space. Otherwise the image is too squished.
        ascii += " "
        row_counter += 1
        # add a newline when you get to the end of a row
        if row_counter >= width*scale_factor:
            ascii += ("\n")
            row_counter = 0

    out_file_path = "./asciiframes/" + out_file + ".txt" 
    with open(out_file_path, 'w') as f:
        print(ascii, file=f)

# convert frames to ascii and put into new directory
def folder_to_ascii(directory):
    print("Converting frames to ascii")
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        asciify(f, filename)
    print("Finished converting")

# display the ascii video
def update_display(index=0):
    with open(sorted_file_paths[index], 'r') as file:
        content = file.read()

    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, content)

    next_index = (index+1) % len(sorted_file_paths)
    # update this integer to change the speed. higher value = faster.
    root.after(15, update_display, next_index)


# uncomment the two lines below to extract frames from a new video path
extract_frames("horse.mov")
folder_to_ascii("frames")

# comment out below code if you don't want to run the tkinter display for a video

file_paths = []
# change this if your directory is different
directory = "asciiframes"
for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        file_paths.append(f)
sorted_file_paths = sorted(file_paths, key=lambda x: int(x.split('/')[-1].split('frame')[-1].split('.jpg')[0]))

# configure tk window
root = tk.Tk()
root.title("Text Display Window")
root.geometry("1000x2000")

# change the font and font size for a different look. It must be a monospaced font. 
# Use height and width to resize the window if it doesn't fit.
text_widget = tk.Text(root, height=300, width=300, font=("Monaco", 4))
text_widget.pack()

update_display(0)
root.mainloop()
