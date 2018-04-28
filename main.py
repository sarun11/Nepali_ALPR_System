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

    print("Width & Height Of Selected Image is: ", Width, Height)

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

#Function to Display HSV Converted image into the GUI
def display_hsv_image(Image_Path):

    img_maxSize = 427
    image_display = wx.Image(Image_Path, wx.BITMAP_TYPE_ANY)

    # Scale the input image, while preserving the aspect ratio
    Width = image_display.GetWidth()
    Height = image_display.GetHeight()

    if Width > Height:
        NewWidth = img_maxSize
        NewHeight = img_maxSize * Height / Width

    else:
        NewHeight = img_maxSize
        NewWidth = img_maxSize * Width / Height

        image_display = image_display.Scale(NewWidth, NewHeight)

    HSV_imageCtrl.SetBitmap(wx.Bitmap(image_display))

#Function to Display Thresholded image into the GUI
def display_thresholded_image(Image_Path):

    img_maxSize = 427
    image_display = wx.Image(Image_Path, wx.BITMAP_TYPE_ANY)

    # Scale the input image, while preserving the aspect ratio
    Width = image_display.GetWidth()
    Height = image_display.GetHeight()

    if Width > Height:
        NewWidth = img_maxSize
        NewHeight = img_maxSize * Height / Width
    else:
        NewHeight = img_maxSize
        NewWidth = img_maxSize * Width / Height
        image_display = image_display.Scale(NewWidth, NewHeight)

    thresholded_imageCtrl.SetBitmap(wx.Bitmap(image_display))

#Function to Display Total Contours Found into the GUI
def display_total_contours(Image_Path):

    img_maxSize = 427
    image_display = wx.Image(Image_Path, wx.BITMAP_TYPE_ANY)

    # Scale the input image, while preserving the aspect ratio
    Width = image_display.GetWidth()
    Height = image_display.GetHeight()

    if Width > Height:
        NewWidth = img_maxSize
        NewHeight = img_maxSize * Height / Width
    else:
        NewHeight = img_maxSize
        NewWidth = img_maxSize * Width / Height
        image_display = image_display.Scale(NewWidth, NewHeight)

    total_contours_imageCtrl.SetBitmap(wx.Bitmap(image_display))

#Function to Display Top 10 Contours Found into the GUI
def display_contours(Image_Path):

    img_maxSize = 427
    image_display = wx.Image(Image_Path, wx.BITMAP_TYPE_ANY)

    # Scale the input image, while preserving the aspect ratio
    Width = image_display.GetWidth()
    Height = image_display.GetHeight()

    if Width > Height:
        NewWidth = img_maxSize
        NewHeight = img_maxSize * Height / Width
    else:
        NewHeight = img_maxSize
        NewWidth = img_maxSize * Width / Height
        image_display = image_display.Scale(NewWidth, NewHeight)

    contours_imageCtrl.SetBitmap(wx.Bitmap(image_display))

#Function to Display Masked License plate into the GUI
def display_lp_masked(Image_Path):

    img_maxSize = 427
    image_display = wx.Image(Image_Path, wx.BITMAP_TYPE_ANY)

    # Scale the input image, while preserving the aspect ratio
    Width = image_display.GetWidth()
    Height = image_display.GetHeight()

    if Width > Height:
        NewWidth = img_maxSize
        NewHeight = img_maxSize * Height / Width
    else:
        NewHeight = img_maxSize
        NewWidth = img_maxSize * Width / Height
        image_display = image_display.Scale(NewWidth, NewHeight)

    lp_masked_imageCtrl.SetBitmap(wx.Bitmap(image_display))

#Function to Display Skewed License plate into the GUI
def display_lp_skewed(Image_Path):
    Lp_maxSize = 300
    lp_display = wx.Image(Image_Path, wx.BITMAP_TYPE_ANY)

    # Scale the input image, while preserving the aspect ratio
    Width = lp_display.GetWidth()
    Height = lp_display.GetHeight()

    if Width > Height:
        NewWidth = Lp_maxSize
        NewHeight = Lp_maxSize * Height / Width

    else:
        NewHeight = Lp_maxSize
        NewWidth = Lp_maxSize * Width / Height

    lp_display = lp_display.Scale(NewWidth, NewHeight)

    lp_skewed_imageCtrl.SetBitmap(wx.Bitmap(lp_display))

#Function to Display deSkewed License plate into the GUI
def display_lp_deSkewed(Image_Path):

    Lp_maxSize = 300
    lp_display = wx.Image(Image_Path, wx.BITMAP_TYPE_ANY)

    # Scale the input image, while preserving the aspect ratio
    Width = lp_display.GetWidth()
    Height = lp_display.GetHeight()

    if Width > Height:
        NewWidth = Lp_maxSize
        NewHeight = Lp_maxSize * Height / Width

    else:
        NewHeight = Lp_maxSize
        NewWidth = Lp_maxSize * Width / Height

    lp_display = lp_display.Scale(NewWidth, NewHeight)

    lp_deSkewed_imageCtrl.SetBitmap(wx.Bitmap(lp_display))

#Function to Display First Character into the GUI
def display_char1(Image_Path):

    Lp_maxSize = 100
    lp_display = wx.Image(Image_Path, wx.BITMAP_TYPE_ANY)

    # Scale the input image, while preserving the aspect ratio
    Width = lp_display.GetWidth()
    Height = lp_display.GetHeight()

    if Width > Height:
        NewWidth = Lp_maxSize
        NewHeight = Lp_maxSize * Height / Width

    else:
        NewHeight = Lp_maxSize
        NewWidth = Lp_maxSize * Width / Height

    lp_display = lp_display.Scale(NewWidth, NewHeight)

    char1_imageCtrl.SetBitmap(wx.Bitmap(lp_display))

#Function to Display Second Character into the GUI
def display_char2(Image_Path):

    Lp_maxSize = 100
    lp_display = wx.Image(Image_Path, wx.BITMAP_TYPE_ANY)

    # Scale the input image, while preserving the aspect ratio
    Width = lp_display.GetWidth()
    Height = lp_display.GetHeight()

    if Width > Height:
        NewWidth = Lp_maxSize
        NewHeight = Lp_maxSize * Height / Width

    else:
        NewHeight = Lp_maxSize
        NewWidth = Lp_maxSize * Width / Height

    lp_display = lp_display.Scale(NewWidth, NewHeight)

    char2_imageCtrl.SetBitmap(wx.Bitmap(lp_display))

#Function to Display Third Character into the GUI
def display_char3(Image_Path):

    Lp_maxSize = 100
    lp_display = wx.Image(Image_Path, wx.BITMAP_TYPE_ANY)

    # Scale the input image, while preserving the aspect ratio
    Width = lp_display.GetWidth()
    Height = lp_display.GetHeight()

    if Width > Height:
        NewWidth = Lp_maxSize
        NewHeight = Lp_maxSize * Height / Width

    else:
        NewHeight = Lp_maxSize
        NewWidth = Lp_maxSize * Width / Height

    lp_display = lp_display.Scale(NewWidth, NewHeight)

    char3_imageCtrl.SetBitmap(wx.Bitmap(lp_display))

#Function to Display Fourth Character into the GUI
def display_char4(Image_Path):

    Lp_maxSize = 100
    lp_display = wx.Image(Image_Path, wx.BITMAP_TYPE_ANY)

    # Scale the input image, while preserving the aspect ratio
    Width = lp_display.GetWidth()
    Height = lp_display.GetHeight()

    if Width > Height:
        NewWidth = Lp_maxSize
        NewHeight = Lp_maxSize * Height / Width

    else:
        NewHeight = Lp_maxSize
        NewWidth = Lp_maxSize * Width / Height

    lp_display = lp_display.Scale(NewWidth, NewHeight)

    char4_imageCtrl.SetBitmap(wx.Bitmap(lp_display))

#Function to Display Fifth Character into the GUI
def display_char5(Image_Path):

    Lp_maxSize = 100
    lp_display = wx.Image(Image_Path, wx.BITMAP_TYPE_ANY)

    # Scale the input image, while preserving the aspect ratio
    Width = lp_display.GetWidth()
    Height = lp_display.GetHeight()

    if Width > Height:
        NewWidth = Lp_maxSize
        NewHeight = Lp_maxSize * Height / Width

    else:
        NewHeight = Lp_maxSize
        NewWidth = Lp_maxSize * Width / Height

    lp_display = lp_display.Scale(NewWidth, NewHeight)

    char5_imageCtrl.SetBitmap(wx.Bitmap(lp_display))

#Function to Display Sixth Character into the GUI
def display_char6(Image_Path):

    Lp_maxSize = 100
    lp_display = wx.Image(Image_Path, wx.BITMAP_TYPE_ANY)

    # Scale the input image, while preserving the aspect ratio
    Width = lp_display.GetWidth()
    Height = lp_display.GetHeight()

    if Width > Height:
        NewWidth = Lp_maxSize
        NewHeight = Lp_maxSize * Height / Width

    else:
        NewHeight = Lp_maxSize
        NewWidth = Lp_maxSize * Width / Height

    lp_display = lp_display.Scale(NewWidth, NewHeight)

    char6_imageCtrl.SetBitmap(wx.Bitmap(lp_display))

#Function to Display Seventh Character into the GUI
def display_char7(Image_Path):

    Lp_maxSize = 100
    lp_display = wx.Image(Image_Path, wx.BITMAP_TYPE_ANY)

    # Scale the input image, while preserving the aspect ratio
    Width = lp_display.GetWidth()
    Height = lp_display.GetHeight()

    if Width > Height:
        NewWidth = Lp_maxSize
        NewHeight = Lp_maxSize * Height / Width

    else:
        NewHeight = Lp_maxSize
        NewWidth = Lp_maxSize * Width / Height

    lp_display = lp_display.Scale(NewWidth, NewHeight)

    char7_imageCtrl.SetBitmap(wx.Bitmap(lp_display))

#Function to Display Eighth Character into the GUI
def display_char8(Image_Path):

    Lp_maxSize = 100
    lp_display = wx.Image(Image_Path, wx.BITMAP_TYPE_ANY)

    # Scale the input image, while preserving the aspect ratio
    Width = lp_display.GetWidth()
    Height = lp_display.GetHeight()

    if Width > Height:
        NewWidth = Lp_maxSize
        NewHeight = Lp_maxSize * Height / Width

    else:
        NewHeight = Lp_maxSize
        NewWidth = Lp_maxSize * Width / Height

    lp_display = lp_display.Scale(NewWidth, NewHeight)

    char8_imageCtrl.SetBitmap(wx.Bitmap(lp_display))


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
    print("Selected Image's path is: ", imgPath)
    serial_no=1

    # Instantiating the class
    process = Alpr(imgPath)

    #A Function to clear label values that displays Network's prediction
    clear_label_values()

    #Calling A method to Create Folder into the Working directory
    try:
        process.CreateFolder()
    except Exception as ex:
        print(ex)
        print("ERROR!! Folder Could Not Be created!!")
        print("")

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
        imageName= 'localized_plate' + ".png"
        process.writeImage(lp, imageName)
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


    # Calling a Method to Copy Image files to Utitity Folder
    try:
        copyImages()
    except Exception as ex:
        print("Cannot Copy Images to the Utility Folder")
        print(ex)

    #Call a Function to Display HSV COnverted Image into the GUI
    try:
        HSV_image_Path = process.img_path_HSV_Masked_image
        display_hsv_image(HSV_image_Path)

    except Exception as ex:
        print(ex)
        print("Cannot Load HSV Masked image into the GUI")

    # Call a Function to Display Thresholded Image into the GUI
    try:
        thresholded_image_Path = process.img_path_thresholded_image
        display_thresholded_image(thresholded_image_Path)

    except Exception as ex:
        print(ex)
        print("Cannot Load Thresholded image into the GUI")

    # Call a Function to Display Total Contours Found into the GUI
    try:
        total_contours_image_Path = process.img_path_total_contours
        display_total_contours(total_contours_image_Path)

    except Exception as ex:
        print(ex)
        print("Cannot Load Total Contours image into the GUI")

    # Call a Function to Display Top 10 Contours Found into the GUI
    try:
        contours_image_Path = process.img_path_contours
        display_contours(contours_image_Path)

    except Exception as ex:
        print(ex)
        print("Cannot Load Total Contours image into the GUI")

    # Call a Function to Display Masked License plate into the GUI
    try:
        masked_lp_image_Path = process.img_path_lp_masked
        display_lp_masked(masked_lp_image_Path)

    except Exception as ex:
        print(ex)
        print("Cannot Load Masked License Plate image into the GUI")

    # Call a Function to Display skewed License plate into the GUI
    try:
        skewed_lp_image_Path = process.img_path_skewed_lp
        display_lp_skewed(skewed_lp_image_Path)

    except Exception as ex:
        print(ex)
        print("Cannot Load skewed License Plate image into the GUI")

    # Call a Function to Display deSkewed License plate into the GUI
    try:
        deSkewed_lp_image_Path = process.img_path_deSkewed_lp
        display_lp_deSkewed(deSkewed_lp_image_Path)

    except Exception as ex:
        print(ex)
        print("Cannot Load deSkewed License Plate image into the GUI")

    #Call Function to Display LP with Segmented Characters into the GUI
    try:
        Image_Path = process.img_path_lp_with_segmented_characters
        display_segmented_characters(Image_Path)

    except Exception as ex:
        print("Cannot Display Image to GUI")
        print(ex)

    # Call Function to Display Segmented Characters into the GUI
    try:
        char1_Path = os.path.join(os.getcwd(), "upper_1.png")
        display_char1(char1_Path)

        char2_Path = os.path.join(os.getcwd(), "upper_2.png")
        display_char2(char2_Path)

        char3_Path = os.path.join(os.getcwd(), "upper_3.png")
        display_char3(char3_Path)

        char4_Path = os.path.join(os.getcwd(), "upper_4.png")
        display_char4(char4_Path)

        char5_Path = os.path.join(os.getcwd(), "lower_1.png")
        display_char5(char5_Path)

        char6_Path = os.path.join(os.getcwd(), "lower_2.png")
        display_char6(char6_Path)

        char7_Path = os.path.join(os.getcwd(), "lower_3.png")
        display_char7(char7_Path)

        char8_Path = os.path.join(os.getcwd(), "lower_4.png")
        display_char8(char8_Path)

    except Exception as ex:
        print("Cannot Display Characters to GUI")
        print(ex)

    #Call Function to recognise so segmented characters (The method is present in Script Recognise_Characters.py)
    recognition()

    #print Network's Answers
    display_prediction()


#Function to show Network's predicted answers into the GUI
def display_prediction():

    #To Display Label in GUI
    # Text Label
    instructions = 'NETWORK PREDICTION:'
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

#A Utility method to copy files into the Bike folder
def copyImages():

    shutil.move( os.path.join(sys.path[0],"HSV_masked_image.png"), os.path.join(os.getcwd(),"HSV_masked_image.png"))
    shutil.move(os.path.join(sys.path[0], "thresholded_image.png"), os.path.join(os.getcwd(), "thresholded_image.png"))
    shutil.move(os.path.join(sys.path[0], "total_contours_image.png"), os.path.join(os.getcwd(), "total_contours_image.png"))
    shutil.move(os.path.join(sys.path[0], "contours_image.png"),os.path.join(os.getcwd(), "contours_image.png"))
    shutil.move(os.path.join(sys.path[0], "lp_masked_image.png"), os.path.join(os.getcwd(), "lp_masked_image.png"))
    shutil.move(os.path.join(sys.path[0], "lp_skewed.png"), os.path.join(os.getcwd(), "lp_skewed.png"))
    shutil.move(os.path.join(sys.path[0], "lp_deSkewed.png"), os.path.join(os.getcwd(), "lp_deSkewed.png"))

if __name__ == '__main__':

    '''Since a part of the process is such that
    the Segregated License Plate and Characters are to be stored in a dedicated seperate folder,
    we need to Delete the folder that stores images and digits in the first place IN CASES where this 
    script is already run before, and thus a folder is already created'''


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
    imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(img), pos=(40, 260), style = wx.SUNKEN_BORDER)

    # Text Label
    instructions = 'Input Raw Image for Recognition Here!'
    instructLbl = wx.StaticText(panel, label=instructions, pos=(70, 720))
    font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
    instructLbl.SetFont(font)

    #Browse Button Defined Here
    browseBtn = wx.Button(panel, label='Browse', pos=(40, 760), style = wx.SUNKEN_BORDER)
    browseBtn.Bind(wx.EVT_BUTTON, onBrowse)

    #Path of Input picture is shown through this Textctrl
    picturePath = wx.TextCtrl(panel, size=(320, 30), pos=(40, 800), style = wx.SUNKEN_BORDER)

    #Process Button Defined here
    processBtn = wx.Button(panel, label='Process', pos=(40, 870), size = ((320, 100)), style = wx.SUNKEN_BORDER)
    processBtn.Bind(wx.EVT_BUTTON, onProcess)

    # Creating a Bitmap to hold Pre-processed image 2 inside
    img_hsv = wx.Image(320, 427)
    HSV_imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(img_hsv), pos=(450, 70), style = wx.SUNKEN_BORDER)

    # Creating a Bitmap to hold Pre-processed image 3 inside
    img_thresholded = wx.Image(320, 427)
    thresholded_imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(img_thresholded), pos=(820, 70), style = wx.SUNKEN_BORDER)

    # Creating a Bitmap to hold Total Contours Found inside
    img_total_contours = wx.Image(320, 427)
    total_contours_imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(img_total_contours), pos=(1190, 70), style = wx.SUNKEN_BORDER)

    # Creating a Bitmap to hold Top 10 Contours found inside
    img_contours = wx.Image(320, 427)
    contours_imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(img_contours), pos=(1560, 70), style = wx.SUNKEN_BORDER)

    # Creating a Bitmap to hold Masked License Plate inside
    img_lp_masked = wx.Image(320, 427)
    lp_masked_imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(img_lp_masked), pos=(450, 550), style = wx.SUNKEN_BORDER)

    # Creating a Bitmap to hold Segmented and skewed License Plate
    img_lp_skewed = wx.Image(300, 200)
    lp_skewed_imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(img_lp_skewed), pos=(827, 550), style = wx.SUNKEN_BORDER)

    # Creating a Bitmap to hold Segmented and de-skewed License Plate
    img_lp_deskewed = wx.Image(300, 200)
    lp_deSkewed_imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(img_lp_deskewed), pos=(1197, 550), style = wx.SUNKEN_BORDER)

    # Creating a Bitmap to hold Segmented License Plate with Segmented Characters
    img_license_plate = wx.Image(300, 200)
    License_plateImgCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(img_license_plate), pos=(1567, 550), style = wx.SUNKEN_BORDER)

    # Label => Display Segmented Characters
    instructLbl = wx.StaticText(panel, label='SEGMENTED CHARACTERS:', pos=(1180, 800))
    font = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
    instructLbl.SetFont(font)

    # Creating a Bitmap to hold Segmented Characters
    char1 = wx.Image(100, 100)
    char1_imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(char1), pos=(820, 850), style = wx.SUNKEN_BORDER)

    char2 = wx.Image(100, 100)
    char2_imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(char2), pos=(955, 850), style = wx.SUNKEN_BORDER)

    char3 = wx.Image(100, 100)
    char3_imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(char3), pos=(1085, 850), style = wx.SUNKEN_BORDER)

    char4 = wx.Image(100, 100)
    char4_imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(char4), pos=(1215, 850), style = wx.SUNKEN_BORDER)

    char5 = wx.Image(100, 100)
    char5_imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(char5), pos=(1345, 850), style = wx.SUNKEN_BORDER)

    char6 = wx.Image(100, 100)
    char6_imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(char6), pos=(1475, 850), style = wx.SUNKEN_BORDER)

    char7 = wx.Image(100, 100)
    char7_imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(char7), pos=(1605, 850), style = wx.SUNKEN_BORDER)

    char8 = wx.Image(100, 100)
    char8_imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(char8), pos=(1735, 850), style = wx.SUNKEN_BORDER)

    # To make GUI visible
    frame.Show()
    app.MainLoop()





