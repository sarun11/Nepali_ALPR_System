import os
import shutil
import wx
import sys
from automatic_license_plate_recognition import Alpr
from Recognise_characters import recognition
from Recognise_characters import answers

#A variable to store Path of an Image to be displayed into the GUI
Image_Path = ""
noOfCharactersFound = 0

'''Gui WxPython Part Here'''

def onBrowse(event):

    # Browsing For Image File
    wildcard = "JPEG files (*.jpg)|*.jpg"
    dialog = wx.FileDialog(None, "Choose a file",
                           wildcard=wildcard,
                           style=wx.DD_DEFAULT_STYLE)
    if dialog.ShowModal() == wx.ID_OK:
        picturePath.SetValue(dialog.GetPath())
    dialog.Destroy()
    onView()

def onView():

    #Extracting the Input image path so selected from FileDialog
    imagePath = picturePath.GetValue()
    img = wx.Image(imagePath, wx.BITMAP_TYPE_ANY).Rotate90(clockwise=True)

    # Scale the input image, while preserving the aspect ratio
    Width = img.GetWidth()
    Height = img.GetHeight()

    print(Width, Height)

    if Width > Height:
        NewWidth = PhotoMaxSize
        NewHeight = PhotoMaxSize * Height / Width

    else:
        NewHeight = PhotoMaxSize
        NewWidth = PhotoMaxSize * Width / Height

    img = img.Scale(NewWidth, NewHeight)

    imageCtrl.SetBitmap(wx.Bitmap(img))

    return imagePath

#Function to display Character Segregated image into Gui
def display_segmented_characters(Image_Path):


    Lp_maxSize = 300
    lp_display = wx.Image(Image_Path, wx.BITMAP_TYPE_ANY)

    # Scale the input image, while preserving the aspect ratio
    Width = lp_display.GetWidth()
    Height = lp_display.GetHeight()

    # Testing
    # print(Width, Height)

    if Width > Height:
        NewWidth = Lp_maxSize
        NewHeight = Lp_maxSize * Height / Width

    else:
        NewHeight = Lp_maxSize
        NewWidth = Lp_maxSize * Width / Height

    lp_display = lp_display.Scale(NewWidth, NewHeight)

    License_plateImgCtrl.SetBitmap(wx.Bitmap(lp_display))


#A Function to clear label values that displays Network's prediction
def clear_label_values():
    x = 40
    y = 180
    for i in range(9):

        label_value = "      "
        instructLbl = wx.StaticText(panel, label=label_value, pos=(x, y))
        font = wx.Font(22, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        instructLbl.SetFont(font)
        x += 45

    # Creating a label to show Message/ one popUp here
    instructions = '                '
    instructLbl = wx.StaticText(panel, label=instructions, pos=(40, 50))
    font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
    instructLbl.SetFont(font)

    instructions_toRemove = "                                                                                   "
    instructLbl = wx.StaticText(panel, label=instructions_toRemove, pos=(40, 80))
    font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
    instructLbl.SetFont(font)


def onProcess(event):

    '''Functionality Code here'''

    imgPath= onView()
    print(imgPath)
    serial_no=1

    # Instantiating the class
    process = Alpr(imgPath)

    #A Function to clear label values that displays Network's prediction
    clear_label_values()

    # Reading the input image for further processing
    try:
        input_image = process.image_load()

        #Creating a label to show Message/ one popUp here
        instructions = 'Image Load Success!!'
        instructLbl = wx.StaticText(panel, label=instructions, pos=(40, 50))
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        instructLbl.SetFont(font)

    except:
        print("Image Couldnot Be loaded!!")

        # Creating a label to show Message/ One PopUP here
        instructions = 'The Image CouldNot be Loaded!!'
        instructLbl = wx.StaticText(panel, label=instructions, pos=(600, 400))
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        instructLbl.SetFont(font)

    # Converting to HSV format and masking off colors other than the Color Red
    hsv_image = process.BGR_to_HSV_conversion(input_image)

    # Pre-processing the HSV image to reduce noise
    preprocessed_image = process.preprocessing(hsv_image)

    # Finding Contours in a pre-processed image
    contours = process.find_contours(preprocessed_image)

    # Finding the Region of Intrest and Localizing the License Plate
    try:
        lp = process.lp_localization(contours, preprocessed_image, image=input_image)

    except Exception as ex:
        print(ex)
        print("Licence Plate Not Found!!")
        # Creating a label to show Message

        instructions = "Licence Plate Not Found!!"
        instructLbl = wx.StaticText(panel, label=instructions, pos=(600, 410))
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        instructLbl.SetFont(font)


    try:
        # Writing such localized license plate into a New Image file
        process.writeImage(lp, serial_no)
        #serial_no+=1

    except Exception as ex:#one pop up here
        print("Error Making Directory/ Writing Number plate into new File!!!")
        print(ex)

    try:
        # Segmenting Individual Characters in the license plate and writing each character into a new Image
        process.character_segmentation(lp, serial_no)

    except Exception as ex:
        print("Error Writing Individual Digits into a new File")
        print(ex)
        instructions = "Licence Plate Could Not be detected!!"
        instructLbl = wx.StaticText(panel, label=instructions, pos=(40, 80))
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        instructLbl.SetFont(font)

    #Call Function to Display Segmented Characters into the GUI
    try:
        Image_Path = process.img_path
        display_segmented_characters(Image_Path)

    except Exception as ex:
        print("Cannot Display Image to GUI")
        print(ex)

    #Call Function to recognise so segmented characters (The method is present in Script Recognise_Characters.py)
    recognition()

    #print Network's Answers
    display_prediction()


#Function to show Network's predicted answers into the GUI
def display_prediction():

    #To Display Label in GUI
    # Text Label
    instructions = 'Network Prediction:'
    instructLbl = wx.StaticText(panel, label=instructions, pos=(40, 140))
    font = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
    instructLbl.SetFont(font)

    #answers refers to an Array, (refer to Script Recognise_characters.py)
    print(answers)
    labels= {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "BA", 11: "PA"}

    # Creating Label to Display Network's Predicted Answers
    x = 40
    y = 180

    for i in range(len(answers)):

        a= answers[i]
        instructions = labels[a]
        print(instructions)

        network_prediction = instructions
        instructLbl = wx.StaticText(panel, label=network_prediction, pos=(x, y))
        font = wx.Font(23, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        instructLbl.SetFont(font)
        x += 45

if __name__ == '__main__':

    '''Since a part of the process is such that
    the Segregated License Plate and Characters are to be stored in a dedicated seperate folder,
    we need to Delete the folder that stores images and digits in the first place IN CASES where this 
    script is already run before, and thus a folder is already created'''

    foldername = 'bike'
    current_path = sys.path[0]
    os.chdir(current_path)


    if (os.path.isdir(foldername)):
        shutil.rmtree(foldername)
    else:
        os.makedirs(os.path.join(current_path,foldername))

    '''GUI part here'''
    imgPath=""
    #GUI using wxpython
    app = wx.App()

    #Create a Frame to Fit all GUI Components inside
    frame = wx.Frame(None, -1, 'Final Year Project Sarun Dahal 15043018', size=(1920, 1080))

    #Creating a panel
    panel = wx.Panel(frame)

    # Define a Label inside a panel
    label = wx.StaticText(panel, label="***Nepali License Plate Recognition System***", pos=(750, 10))
    font = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
    label.SetFont(font)

    #Set Max size for photo
    PhotoMaxSize = 427

    #Creating a Bitmap to hold Raw Input Image inside
    img = wx.Image(320, 427)
    imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(img), pos=(40, 260))

    # Text Label
    instructions = 'Input Raw Image for Recognition Here!'
    instructLbl = wx.StaticText(panel, label=instructions, pos=(70, 720))
    font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
    instructLbl.SetFont(font)

    #Browse Button Defined Here
    browseBtn = wx.Button(panel, label='Browse', pos=(40, 760))
    browseBtn.Bind(wx.EVT_BUTTON, onBrowse)

    #Path of Input picture is shown through this Textctrl
    picturePath = wx.TextCtrl(panel, size=(320, 30), pos=(40, 800))

    #Process Button Defined here
    processBtn = wx.Button(panel, label='Process', pos=(40, 870), size = ((320, 100)))
    processBtn.Bind(wx.EVT_BUTTON, onProcess)


    #Display Segmented Characters
    instructLbl = wx.StaticText(panel, label='Localized License Plate:', pos=(1550, 700))
    font = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
    instructLbl.SetFont(font)

    # Creating a Bitmap to hold Segmented License Plate
    img_license_plate = wx.Image(300, 200)
    License_plateImgCtrl = wx.StaticBitmap(panel, wx.ID_ANY,
                                           wx.Bitmap(img_license_plate), pos=(1550, 750))

    # Creating a Bitmap to hold Pre-processed image 2 inside
    img_hsv = wx.Image(320, 427)
    HSV_imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(img_hsv), pos=(450, 70))

    # Creating a Bitmap to hold Pre-processed image 3 inside
    img2 = wx.Image(320, 427)
    img2_imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(img2), pos=(820, 70))

    # Creating a Bitmap to hold HSV Converted Image inside
    img3 = wx.Image(320, 427)
    img3_imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(img3), pos=(1190, 70))

    # Creating a Bitmap to hold Pre-processed image 4 inside
    img4 = wx.Image(320, 427)
    img4_imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(img4), pos=(1560, 70))

    # Creating a Bitmap to hold Pre-processed image 5 inside
    img5 = wx.Image(320, 427)
    img5_imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(img5), pos=(450, 550))

    # Creating a Bitmap to hold HSV Converted Image inside
    img6 = wx.Image(320, 427)
    img6_imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(img6), pos=(820, 550))

    # Creating a Bitmap to hold Pre-processed image 6 inside
    img_hsv = wx.Image(320, 427)
    HSV_imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(img_hsv), pos=(1190, 550))


    # To make GUI visible
    frame.Show()
    app.MainLoop()





