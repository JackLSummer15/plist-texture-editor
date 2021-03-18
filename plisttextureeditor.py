from PIL import Image
import time,os,os.path
 
keys = []
data = ''
 
# functions
 
def GetArray(key):
    'Get plist array from key'
    global data # grabbing sprite file data
    try:
        array = data.split('<key>'+key+'</key>')[1].split('<dict>')[1].split('</dict')[0].replace('    ','') # getting array from spitename
    except IndexError: # catching IndexError if raised
        return None # exiting function
    return array # returning array
 
def GetSizeFromArray(array):
    'Get sprite size from plist array'
    size = array.split('<key>spriteSize</key>')[1].split('<string>')[1].split('</string')[0].replace('{','').replace('}','') # getting spriteSize from sprite array
    x,y = int(size.split(',')[0]),int(size.split(',')[1]) # splitting data and getting x&y
    return x,y # returning spriteSize
 
def GetPosFromArray(array):
    'Get sprite pos from plist array'
    size = array.split('<key>textureRect</key>')[1].split('<string>')[1].split('</string')[0].replace('{','').replace('}','') # getting sprite position from sprite array
    x,y = int(size.split(',')[0]),int(size.split(',')[1]) # splitting data and getting x&y
    return x,y # returning spriteSize
 
def IsSpriteRotated(array):
    'Check if sprite is rotated on gamesheet'
    string = array.split('<key>textureRotated</key>')[1] # getting bool from file
    if ('false' in string): # checking if false
        return False
    return True
 
def GetGamesheetSize():
    'Get size of Gamesheet'
    strsize = GetArray('metadata').split('<key>size</key>\n<string>{')[1].split('}')[0].split(',')
    return int(strsize[0]),int(strsize[1])
 
def SaveSprite(key):
    global f
    'Created image file form sprite in gamesheet'
    array = GetArray(key) # getting data of the sprite
    size = GetSizeFromArray(array) # getting sprite size
    position = GetPosFromArray(array) # getting sprite position
    rotated = IsSpriteRotated(array) # getting sprite rotation
    gamesheet = Image.open(f+'.png','r') # opening gamesheet
    if (rotated):
        size = size[::-1]
    img = Image.new('RGBA',size) # creating new image with size of target sprite
    for x in range(size[0]):
        for y in range(size[1]):
            img.putpixel((x,y),
                         gamesheet.getpixel((x+position[0],y+position[1])))
            # creating image of the target sprite, pixel by pixel
    img.save(f+'\\'+key) # saving file :D
    img.close() # closing file
    gamesheet.close() # closing gamesheet
    return None
 
# main code:
 
print('Texture Editor by Absolute Gamer (2017)')
print('Make sure to copy the gamesheets, both png & plist into the directory of the program!')
 
loaded = False
 
while 1:
    print('\nOptions:')
    print('1) Load texture')
    if (loaded):
        print('2) Split texture')
        print('3) Merge texture')
    ui = input('Enter valid number: ')
 
    if (ui == '1'): # load textures
        loaded = True
        f = input('Texture name (without the extention): ') # get texture name
 
        if not('-hd' in f) and not('-uhd' in f):
            print('NOTE: You have chosen a low quality file') # warn user if non-hd file used
 
        print('Getting keys...')
        fr = open(f+'.plist','r') # opening file with read permissions
        data = fr.read() # reading file
        fr.close() # closing file
 
        for i in data.split('<key>')[1:]:
            if not(i.split('</key>')[0] in ['aliases','spriteOffset','spriteSize','spriteSourceSize','textureRect','textureRotated','frames']):
                if (i.split('</key>')[0] == 'metadata'):
                    break # break loop if key = 'metadata'
                keys.append(i.split('</key>')[0]) # append key to array if not blacklisted
        print('Done!')
 
        try:
            if not os.path.isdir('merged'):
                os.makedirs('merged') # create folder if not exist
                print('Merged folder created')
            if not os.path.isdir(f):
                os.makedirs(os.makedirs(f)) # create folder if not exist
                print('Gamesheet folder created')
        except:
            pass
    if (ui == '2'): # split texture
        print('Saving images...')
        for i in keys:
            SaveSprite(i) # for all keys, save sprite 
            print('Completed: '+i)
        print('Rotating images...')
        for i in keys: # rotate images needed
            if IsSpriteRotated(GetArray(i)):
                img = Image.open(f+'\\'+i) # opening target image
                img.rotate(90, expand=True).save(f+'\\'+i) # rotating image
                img.close() # closing image
                print('Rotated: '+i)
    if (ui == '3'):
        print('Rotating images...')
        for i in keys: # rotating images back if needed
            if IsSpriteRotated(GetArray(i)):
                img = Image.open(f+'\\'+i) # opening target image
                img.rotate(-90, expand=True).save(f+'\\'+i) # rotating image by -90
                img.close() # closing image
                print('Rotated: '+i)
 
        new = Image.new('RGBA',GetGamesheetSize())
 
        for key in keys: # for all textures
            targ = GetArray(key) # getting plist array from plist file
            pos = GetPosFromArray(targ) # getting position of key on gamesheet
            size = GetSizeFromArray(targ) # getting size of key on gamesheet
            print('Completed: '+key)
            rd = Image.open(f+'\\'+key) # opening image (made a stupid mistake earlier by opening the image per pixel, oops)
            if (IsSpriteRotated(targ)): # if rotated, spaw x and y in the size variable
                size = size[::-1] # reverse tuple
            for x in range(size[0]):
                for y in range(size[1]):
                    new.putpixel((x+pos[0],y+pos[1]),rd.getpixel((x,y))) # add target image, pixel by pixel, to gamesheet by size and position
            rd.close() # close target image
        new.save('merged\\'+f+'.png') # save gamesheet in 'merged' folder
        new.close() # close gamesheet
 
        print('Rotating images...')
        for i in keys:
            if IsSpriteRotated(GetArray(i)):
                img = Image.open(f+'\\'+i) # opening target image
                img.rotate(90, expand=True).save(f+'\\'+i) # rotating image by 90
                img.close() # closing image
                print('Rotated: '+i)