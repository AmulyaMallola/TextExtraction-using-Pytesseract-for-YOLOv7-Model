import os
import cv2
import shutil
from pathlib import Path
import pytesseract
from PIL import Image
import json
from tqdm import tqdm   
from time import time, sleep
import datetime


start = time()
def DriveFiles(source):
    
    list1=[]

    allfiles = os.listdir(source) # Gather all files
    count=0
    for path in allfiles:
        list1.append(path)
    source1 = source+"\\"+list1[len(list1)-1]
    print("\n\nThe total directories in the given Path:   ",list1)

    print("\n\nPath of the last directory in the above list:    ",source1)

    if "." not in source1:
        # Iterate on all files to upload
        source1=str(Path(source1))
        allfiles = os.listdir(source1) 
        list2 = []
        for path in allfiles:
            if os.path.isfile(os.path.join(source1, path)):
                count += 1
            list2.append(path)

        print("\n\nThe list of files in the above folder(last folder): ",list2,"\n\n")
        
        input = list2[len(list2)-1]
        print("The required input file is:  ",input)
        print("\nTotal no of files in the given directory: ",count)


        #change the current working directory to specified path
        os.chdir(source1)
        print("\nDirectory is Changed according to our requirement....\n")

        # verify the path using getcwd()
        cwd = os.getcwd()

        print("\nCurrent working directory is:    ", cwd,"\n\n")
        
        
        list3 = []
        source1 = source1+"\\"+input
        list3.append(source1)
        list3.append(input)
        
        
        #os.system("dir")
        #print()
        #print("\n\nCommand prompt is opened in above mentioned directory as Current working directory you can do required operations at this directory ....\n")
        #os.system("start cmd /K cd {}".format(cwd))
        
        
        return list3
    
    print("\nThere are no further folder at last index in this directory, It only has a file at last in this directory......\n")
    print("\nAnd the last indexed file in this directory is returned below....\n ")
    return source1
    


print("\n\n......................ACCESSING DRIVE OUTPUT FILE..........................\n")

#Path of the Drive directory we want to work with
source = input("Enter your Drive detect folder path of your model: ")

a = DriveFiles(source)
if type(a) is list:
    if ".mp4"in str(a) or ".avi" in str(a):
        print("\nThe required return values are (Path and video file names):   ",a)
        print("\nThe Path is:   ",a[0])
        print("\nThe Video file is:   ",a[1])
    else:
        print("\nThe folder doesn't contains required video files at its last index.....")
elif ".mp4" in a or ".avi"in a:
    print("\nThe required return value is path of video file:   ",a)
else:
    print("\nThe file is not a video file.... It is other than video file.....")





    
#..............FRAMES CONVERSION.................

print("\n\n.........................FRAMES CONVERSION.............................\n")


if not os.path.exists('image_frames'):
    os.makedirs('image_frames')

#video_path = input("Enter video path: ")
video_handle = cv2.VideoCapture(r"H:\My Drive\TheCoding\yolov7\runs\detect\exp6\1.mp4", cv2.CAP_FFMPEG)
frame_no = 0
frameRate = 24
print("\nCreating Frames.....\n")
time_stamps = {}
while True:
    eof, frame = video_handle.read()
    if not eof:
        break
    if frame_no % frameRate == 0:
        '''# assigning name for our files
        name = './image_frames/frame'+str(int(frame_no/frameRate))+'.png'
        print("Extracting frames .."+name)'''
        # Saving frame to .png file  
        name = './image_frames/frame%d.jpg' % frame_no
        #print("Extracting frames .."+name)
        #print("Extracting frames....for frame : " + str(frame_no) + "   timestamp is: ", str(video_handle.get(cv2.CAP_PROP_POS_MSEC)))
        frameTime = "frame"+str(frame_no)
        time_stamps[frameTime] = str((video_handle.get(cv2.CAP_PROP_POS_MSEC))/(1000))
        cv2.imwrite(name, frame)
    frame_no += 1
    
video_handle.release()
cv2.destroyAllWindows()

print("\n\nFrames Created.....\n")



#.........................TEXT EXTRATION.............................



print("\n\n.........................TEXT EXTRATION.............................\n")

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

my_dict = {}

# Loading frames from directory 
frames = os.listdir('./image_frames')

# Sorting frames according to their numbers
frames.sort(key=lambda x: int(x[5:-4]))

# printing total number of frames loaded
print("Number of frames :- " + str(len(frames)))

for frame in tqdm(frames):

    # extracting text from image frame
    text_in_image = pytesseract.image_to_string('./image_frames/'+frame, lang='eng' )

    # replacing \n and \f character
    text_in_image = text_in_image.replace('\n', '')
    text_in_image = text_in_image.replace('\f', '')

    # Removing unwanted spaces
    text_in_image = text_in_image.strip()

    # removing unicode characters
    text_in_image = text_in_image.encode('ascii', 'ignore').decode()

    # appending output to dictionary (only those frames which contain text)
    if(len(text_in_image) != 0):        
        my_dict[str(frame)] = text_in_image


ts = []
for key in my_dict:
    if "Chain _Snatching" in my_dict[key] or "Chain_Snatching" in my_dict[key] or "Choin_Snatching" in my_dict[key] or "Choin_Snotching" in my_dict[key] or "Choin _Snotching" in my_dict[key] or "Choin _Snatching" in my_dict[key]:
        print("\n\n",key,"  ==>  ",my_dict[key])
        print(" Chain Snacting detected........\n\n")
        key = key[:-4]
        ts.append(key)

for i in range(len(ts)):
    for key in time_stamps:
        if key == ts[i]:
            ct = datetime.datetime.now()
            print("\n\n Detected At time stamp of ",key," ==> ",time_stamps[key],"seconds")
            print("\n And Current Time is: ",ct,"\n\n")


'''
# Saving output of dictionary to json file
with open('image_to_text.json', 'w') as outputFile:
    json.dump(my_dict, outputFile)
    

with open('outputFile.txt',mode ='w') as file:
    file.write(str(my_dict))
    print("Finally ready!....")'''



print("\n\n............Deleting image_frames directory for or convinence........\n")
cwd = os.getcwd()
#print(cwd)
shutil.rmtree(cwd+"\\image_frames", ignore_errors=True)
print("\nAlready presented image_frames  directory deleted......\n")

print(f"finished after {round(time() - start,2)} seconds")  