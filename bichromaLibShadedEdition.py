from PIL import Image
import threading
import time as t
import os
import subprocess
from playsound import playsound

def readBitmapBrightness(path,resolution): # returns an array of true/false correlating to the pixel's brightness
    imageFile = Image.open(path)
    imageFileWidth,imageFileHeight = imageFile.size 
    allPixels = imageFile.load() # generates an object with every pixel's data where we can call on a specific pixel's properties using allPixels[x,y]
    rows = []
    for i in range(imageFileHeight):
        row = []
        if i % resolution == 0: # makes the image 1/resolution in height
            for j in range(imageFileWidth):
                pixelBrightness = 0
                if j % resolution == 0: # makes the image 1/resolution in width
                    for l in range(3): # this is for getting the RGB values of each pixel
                        pixelBrightness += allPixels[j,i][l]
                    row.append(pixelBrightness) # appends if the pixel is closer to being white or black
            rows.append(row)
    return rows 
        
def convertImageToShades(pixels,dark): # does exactly as it says
    rows = []
    for i in range(len(pixels)): # for the height of the image
        row = []
        for j in range(len(pixels[i])): # for the width of the image
            
            if dark: # if the background is dark, the characters will be light, so "██" will represent white. Otherwise "  " will represent white
                if pixels[i][j] > (4/5)*765:row.append("██")
                elif pixels[i][j] > (3/5)*765:row.append("▓▓")
                elif pixels[i][j] > (2/5)*765:row.append("▒▒")
                elif pixels[i][j] > (1/5)*765:row.append("░░")
                else: row.append("  ")
            else:
                if pixels[i][j] > (4/5)*765:row.append("  ")
                elif pixels[i][j] > (3/5)*765:row.append("░░")
                elif pixels[i][j] > (2/5)*765:row.append("▒▒")
                elif pixels[i][j] > (1/5)*765:row.append("▓▓")
                else: row.append("██")
                
        rows.append(''.join(row))
    return '\n'.join(rows)




def renderVideoInTerminal(frameCount,frameRate,path,res=6,audio=False):
    
    frames = [] # we want to prerender the frames so the timing between them can be better controlled; this is the list of all frames so we can call upon each one we wish to play
    print(("\n"*200)+"Pre-rendering frames...\n")

    dones = 1 # only exists for percentage of prerender complete messages
    for i in range(frameCount): # loop for the number of frames
        iNum = list(str(i+1)) # the file names follow a pattern of a number increasing, so this just finds the frame we should be calling
        if len(list(str(i+1))) < 5: # the number is always 5 digits long, so 
            for l in range(5-len(list(str(i+1)))): # we need to add zero's to the start of it in case i < 5 digits long
                iNum.insert(0,'0') 

        fPath = path+str(''.join(iNum))+".png" # file path/frame we want; the "+str(''.join(iNum))+" in the middle is because that part of the filename counts upwards, as mentioned previously.
        frames.append(convertImageToShades(readBitmapBrightness(fPath,res),True)) # appends the text version of the frame to the list of frames with 1/6th resolution
        
        if i == (round(frameCount/10))*dones: # if the number of frames has passed a multiple of 5% of all the frames to render;
            print(("\n"*200)+"Pre-rendering frames...\n\n"+str(round(i/frameCount*100))+"% complete...") # print out the percentage complete
            dones += 1 # increase the multiplier for the next time
    input("\n\nRendering complete; press enter to begin:\n")
    start = t.time()
    
    def videoThread():
        for i in range(len(frames)): # for every frame
            t.sleep(1/frameRate) # time the frames
            
            timePassed = t.time()-start
            if abs((timePassed*frameRate)-i)>5:i=round(timePassed*frameRate) # correct the frame timings
            
            print(frames[i])  # print the frame
            
            
    def audioThread(): # just so we can play sound simultaniously
        if audio:
            playsound(audio)
        else:
            raise exception("wtf")

    t1 = threading.Thread(target=videoThread)
    t2 = threading.Thread(target=audioThread)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Video Complete!")
    
    

def renderVideoInNotepad(frameCount,frameRate,path,res=6,audio=False): # opens up a notepad window for every frame and then closes it 

    try:os.makedirs('notepadFrames')
    except OSError:pass
    
    print(("\n"*200)+"Pre-rendering frames...\n")

    dones = 1 # only exists for percentage of prerender complete messages
    for i in range(frameCount): # loop for the number of frames
        iNum = list(str(i+1)) # the file names follow a pattern of a number increasing, so this just finds the frame we should be calling
        if len(list(str(i+1))) < 5: # the number is always 5 digits long, so 
            for l in range(5-len(list(str(i+1)))): # we need to add zero's to the start of it in case i < 5 digits long
                iNum.insert(0,'0') 

        fPath = path+str(''.join(iNum))+".png" # file path/frame we want; the "+str(''.join(iNum))+" in the middle is because that part of the filename counts upwards, as mentioned previously.
        
        with open("notepadFrames/notepadFrame"+str(''.join(iNum))+".txt",'w',encoding="utf-8") as frame: # we're using unicode characters, so specifying the encoding as "utf-8" is necessary
            frame.write(str(convertImageToShades(readBitmapBrightness(fPath,res),False))) # notepad has a light background; so the second arguement for convertImageToShades is False
            frame.close()
        
        if i == (round(frameCount/10))*dones: # if the number of frames has passed a multiple of 5% of all the frames to render;
            print(("\n"*200)+"Pre-rendering frames...\n\n"+str(round(i/frameCount*100))+"% complete...") # print out the percentage complete
            dones += 1 # increase the multiplier for the next time
    input("\n\nRendering complete; press enter to begin:\n")
    
    
    def videoThread(): # thread for rendering video
        prevFrames = []
        delay = 8
        global corrections;corrections=0
        start = t.time()
        for i in range(frameCount): # for every frame
            t.sleep(1/frameRate) # time the frame
            
            timePassed = t.time()-start
            if abs((timePassed*frameRate)-i)>5:i=round(timePassed*frameRate);corrections+=1 # correct the frame timings
            
            for j in range(frameCount): # loop for the number of frames
                iNum = list(str(i+1)) # the file names follow a pattern of a number increasing, so this just finds the frame we should be calling
                iNumL = list(str(i-delay))
                
                if len(list(str(i+1))) < 5: # the number is always 5 digits long, so 
                    for l in range(5-len(list(str(i+1)))): # we need to add zero's to the start of it in case i < 5 digits long
                        iNum.insert(0,'0')
                        iNumL.insert(0,'0')
               
            current = subprocess.Popen(["notepad","notepadFrames/notepadFrame"+str(''.join(iNum))+".txt"])# display the frame
            
            if len(prevFrames) > delay: # keep the frames open for a little bit so that they are actually displayed
                prevFrames[0].terminate() # close the oldest frame's window
                prevFrames.pop(0) # delete the oldest frame
                print("Terminated frame #"+str(''.join(iNumL)))
                
            prevFrames.append(current)
            
            if i>=frameCount-1:
                for j in range(len(prevFrames)):prevFrames[0].terminate();prevFrames.pop(0)
                print("Terminated final",delay,"frames.")
                break
            
    def audioThread():
        try:playsound(audio)
        except:pass
        
    # start the video and audio threads and then wait for them to finish
    t1 = threading.Thread(target=videoThread)
    t2 = threading.Thread(target=audioThread)

    t1.start()
    t2.start()
    t1.join()

    print("\nVideo Complete!")
    print("Corrections made:",corrections)