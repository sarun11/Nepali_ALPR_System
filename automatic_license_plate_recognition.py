import cv2
import numpy as np
from decimal import Decimal
import os, sys
import shutil

class Alpr:


    def __init__(self, image_name):

        self.image_name = image_name

        # Loading Image from drive
        self.image = cv2.imread(self.image_name)

        #Define images to be shown in the GUI Interface
        self.img_path_lp_with_segmented_characters= None
        self.img_path_HSV_Masked_image = None

    #A Method That Creates a Folder Into the Current Working Directory to save images
    def CreateFolder(self):

        foldername = 'bike'
        current_path = sys.path[0]
        os.chdir(current_path)

        if (os.path.isdir(foldername)):
            shutil.rmtree(foldername)
        else:
            os.makedirs(os.path.join(current_path, foldername))


    # Loading input image
    def image_load(self):
        # Loading Image from drive
        image = self.image
        return image

    '''
    Converting the Input image from BGR to HSV values and 
    Since the project is performed on Private Number plate of  2 Wheelers, 
    Masking is perormed to mask off all colors except the color red from the image
    This process helps reduce computing complexity and also aids in accuracy, 
    since unwanted parts are not processed at all!!
    '''

    def BGR_to_HSV_conversion(self, bgr_image):
        # Converting BGR to HSV values so that only red Color is segmented from the image
        image_hsv = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

        # defining range of red values
        # In HSV Format, Color Red is taken as values equivalent to 0-10 and 170-180, and the rest is masked off

        # Lower Mask (0-10)
        lower_red = np.array([0, 50, 50])
        upper_red = np.array([10, 255, 255])
        mask0 = cv2.inRange(image_hsv, lower_red, upper_red)

        # Upper Mask (170-180)
        lower_red = np.array([170, 50, 50])
        upper_red = np.array([180, 255, 255])
        mask1 = cv2.inRange(image_hsv, lower_red, upper_red)

        # join  The two Masks
        mask = mask0 + mask1

        # Output After Masking
        output_hsv = image_hsv.copy()
        output_hsv[np.where(mask == 0)] = 0

        # Saving the image that shows HSV Masked Image (to be shown to the GUI
        path= os.path.join(os.getcwd(), 'HSV_masked_image' + '.png')
        print("Path IS: ", path)
        cv2.imwrite(path, output_hsv)
        hsv_path= os.path.join(os.getcwd(),'bike','HSV_masked_image' + '.png')
        self.img_path_HSV_Masked_image = hsv_path
        print("HSV PATH IS: ", hsv_path)

        return output_hsv


    '''
    After color masking, the image is preprocessed to remove unnecessary noises
    1. The image is converted to Grayscale (to reduce computing complexity)
    2. The contrast of the image is normalized using Histogram Equalization process
    3. A Gaussian Blur of (5,5) Kernel is used to remove unnecessary noises
    4. Morpological Dilation and Erosion is also used thereafter to remove any noises if left 
    5. Finally, the image is thresholded to convert to Binary using Ostu's Binarization. 
    '''

    def preprocessing(self, image):
        # Conversion To grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Histogram Equalization
        equal_histogram = cv2.equalizeHist(gray)

        # Apllying Gaussian Blur with 5*5 Filter
        blur = cv2.GaussianBlur(equal_histogram, (5, 5), 0)

        # perform a series of erosions and dilations on the image
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(blur, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

        thresh3 = cv2.erode(closing, kernel, iterations=1)

        thresh4 = cv2.dilate(thresh3, kernel, iterations=1)

        # Conversion to Binary (Thresholding using Ostu's Binarization)
        ret, thresholded = cv2.threshold(thresh4, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        return thresholded

    '''
    Finding The total Contours in an image
    Thereafter, only top 10 contours are selected for further processing based on the total area,
    since the licence plate falls under the top 10 contours in an image
    '''

    def find_contours(self, image):

        # Finding the total Contours in the image
        _, contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Testing
        print("No. of contours detected -> %d " % len(contours))

        # Sorting contours as per area, Only the biggest 10 selected for further processing
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        return contours

    '''
    Localization of the License plate.
    Firstly, a polygonal contour is approximated to be a rectangle if it has 4 sides (7% error rate accepted)
    Aspect ratio profiling is performed after the process of approximation
    Aspect ratio numbers are calculated as per dataset of 300 licesnse plates

    Masking off the license plate contour into a new image. 
    Also, The license plate is deskewed to correct any skew errors.
    '''

    def lp_localization(self, contours, thresholded_image, image):
        # For each Contour, further Processing
        screen_contours = None
        for c in contours:

            # approximating a poligonal structure to be a rectangle. 7% error rate accepted as a rectangle
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.07 * peri, True)

            x, y, w, h = cv2.boundingRect(approx)
            a_ratio = float(w) / h
            aspect_ratio_string = str(a_ratio)
            aspect_ratio = Decimal(aspect_ratio_string)

            if (1.20 < aspect_ratio < 1.99):

                if len(approx) == 4:
                    rect = cv2.minAreaRect(c)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)

                    print("asp ratio ->", aspect_ratio)
                    screen_contours = approx
                    break

        # If Found draw Contours on image, else display Error Message
        if (screen_contours is not None):

            # Drawing Contours on Image
            # cv2.drawContours(image,[screen_contours],-1,(255,255,255), 3)
            cv2.drawContours(image, [box], -1, (0, 255, 0), 3)

            # Masking the other parts of the picture other than the number plate
            img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image_masking = np.zeros(img.shape, np.uint8)

            new_image = cv2.drawContours(image_masking, [box], 0, 255, -1, )
            new_image = cv2.bitwise_and(thresholded_image, thresholded_image, mask=image_masking)

            # Displaying the Masked image (For Testing purposes)

            # cv2.namedWindow('Plate', cv2.WINDOW_KEEPRATIO)
            # cv2.resizeWindow('Plate', 960, 960)
            # cv2.imshow('Plate', new_image)

            '''
            Cropping License Plates region as per the co-ordinates of the Bounding Box rectangle so calculated
            During Aspect Ratio Profiling
            '''
            x, y, w, h = cv2.boundingRect(box)
            roi = new_image[y:y + h, x:x + w]

            # Deskewing the image
            # roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            coords = np.column_stack(np.where(roi > 0))
            angle = cv2.minAreaRect(coords)[-1]

            if angle < -45:
                angle = -(90 + angle)
            else:
                angle = -angle

            # rotate the image to deskew it
            (h, w) = roi.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(roi, M, (w, h),
                                     flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


            return rotated



    '''
    Segmentation of characters from the Localized license plate.
    The so segmented license plate is again converted to Binary in Inverse so that the characters become
    the foreground pixels (in black) and the background is converted to white.
    Thenafter, All the connected components are searched for in the image. 
    The next step is to find out the median Aspect ratio of each Connected Components 
    (Since the because the majority of connected components are numbers)
    Thenafter, Characters are segmented by the way of aspect ratio profiling, 
    as per the aspect ratio so calculated above, and written to a new image.
    '''

    def character_segmentation(self, img, serial_no):
        # Parameterss
        EPSSILON = 1
        MIN_AREA = 500
        BIG_AREA = 25000

        # Converting the Segmented License plate to Grayscale because an RGB image cannot be converted to Binary

        # image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Thresholding in Inverse using Ostu's Method
        a, thI = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Performing Morpholgical operations (Thinnng the characters)
        se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
        thIMor = cv2.morphologyEx(thI, cv2.MORPH_CLOSE, se)

        # Connected component labeling
        stats = cv2.connectedComponentsWithStats(thIMor, connectivity=8)

        num_labels = stats[0]
        labels = stats[1]
        labelStats = stats[2]

        print("No of connected components found =", num_labels)

        # We expect the connected component of the numbers to be more or less with a constant ratio
        # So we find the median ratio of all the components because the majority of connected components are numbers
        # Find Total Height and Width of the image
        image_height, image_width = img.shape[:2]

        ratios = []
        for label in range(num_labels):
            connectedComponentWidth = labelStats[label, cv2.CC_STAT_WIDTH]
            connectedComponentHeight = labelStats[label, cv2.CC_STAT_HEIGHT]

            ratios.append(float(connectedComponentWidth) / float(connectedComponentHeight))

        # Find median ratio
        medianRatio = np.median(np.asarray(ratios))

        # Go over all the connected component again and filter out component that are far from the ratio.

        a = 0
        count = 1
        #Declare lists required for seperating digits based on their location, i.e. if they fall on first line or second line of the plate
        y_list = []
        list_of_labels = []

        for label in range(num_labels):
            #print("a=", a)
            a += 1

            connectedComponentWidth = labelStats[label, cv2.CC_STAT_WIDTH]
            connectedComponentHeight = labelStats[label, cv2.CC_STAT_HEIGHT]

            ratio = float(connectedComponentWidth) / float(connectedComponentHeight)

            # Ignore biggest label
            if (label == 1):
                continue

            # Exclude connected components which do not satisfy ratio profiling
            elif ratio > medianRatio + EPSSILON or ratio < medianRatio - EPSSILON:
                 continue


            # Filter small or large component
            elif labelStats[label, cv2.CC_STAT_AREA] < MIN_AREA or labelStats[label, cv2.CC_STAT_AREA] > BIG_AREA:
                continue

            #Filter based on Height and width of the total Image (if the label doesnot fall under some predetermined criteria, continue)
            elif connectedComponentHeight < (image_height * 0.07) or connectedComponentWidth < (image_width * 0.07):
                continue

            # For Testing Purposes
            #print("label no:", label)
            #print("label stats:", labelStats[label])
            #print("count:", count)

            x, y, w, h, size = labelStats[label]
            
            #Drawing Bounding Box around Contours
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

            # Appending items to list for calculation of position of digits
            y_list.append(y)
            list_of_labels.append(labelStats[label])

            # Testing
            count += 1
            #digit = img[y:y + h, x:x + w]
            # cv2.imshow('Digit', digit)


        #Edit From here
        # Find mean Y for segregation of Digits into 2 columns of Y
        #median_Y = np.median(np.asarray(y_list))
        mean_Y= sum(y_list)/ len(y_list)
        #print("Y list is: ", y_list)
        #print("Mean y is", mean_Y)

        #Declare Lists to store Stats baed on whether the digit lies in the upper line or lower line
        upperLineDigits = []
        lowerLineDigits = []

        # Segregate each digit into UpperLine Digit or LowerLine digit based on comparision with median Y value.
        for item in list_of_labels:
            if (item[1]) < mean_Y:
                upperLineDigits.append(item)
            else:
                lowerLineDigits.append(item)
        
        #Now After segregating the digits as Digit in upper line or lower line, sorting each line based on x
        upperLineDigits.sort(key=lambda x: x[0])
        #print("Sorted: ", upperLineDigits)

        lowerLineDigits.sort(key=lambda x: x[0])
        #print("Sorted lower: ", lowerLineDigits)

        #Now, define Path to store each digit into a new File

        foldername = 'bike'
        folder_path = sys.path[0]
        os.chdir(os.path.join(folder_path, foldername))
        file_path = os.path.join(folder_path, foldername)
        print("Content Folder path is: ", file_path)

        # Sometimes the Pins are also categoried as digits, in such a case we filter by height again
        heights=[]
        for eachDigit in upperLineDigits:
            x, y, w, h, size = eachDigit
            heights.append(h)

        #print("total heights", heights)
        avg_height= sum(heights)/len(heights)
        #print("avg height: ", avg_height)

        correctedUpperLineDigits= []
        for eachDigit in upperLineDigits:
            x, y, w, h, size = eachDigit
            # 85% is an arbitraty number, just in case in some real digit has smaller height than avg_height
            if h>(0.85*avg_height):
                correctedUpperLineDigits.append(eachDigit)

        serialNo_upperDigits = 1

        digits_found=0
        for eachDigit in correctedUpperLineDigits:
            x, y, w, h, size = eachDigit
            digit = img[y:y + h, x:x + w]

            # Thinning the digit for further Processing
            ret, thresholding = cv2.threshold(digit, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            kernel = np.ones((3, 3), np.uint8)
            erosion = cv2.erode(thresholding, kernel, iterations=2)

            ret, final = cv2.threshold(erosion, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            smallsize = (28, 28)
            smallimage = cv2.resize(final, smallsize)


            filename = "upper_"+ str(serialNo_upperDigits) + ".png"
            file_name= os.path.join(file_path,filename)
            #print("filename is ! ", filename)
            cv2.imwrite(file_name, smallimage)
            digits_found+=1
            serialNo_upperDigits += 1


            #Creating Dataset of the character to be fed to the Neural Network
            pixels = np.asarray(smallimage)
            fileName= str(digits_found)+ ".csv"
            dataset_filename= os.path.join(file_path, fileName)
            np.savetxt(dataset_filename, pixels, fmt='%d', newline=',', delimiter=",")


        # Now, compare based on x co-ordinate to find correct sequence of digits in each row (Lower)
        serialNo_LowerDigits = 1
        for eachDigit in lowerLineDigits:
            x, y, w, h, size = eachDigit
            digit = img[y:y + h, x:x + w]

            # Thinning the digit for further Processing
            ret, thresholding = cv2.threshold(digit, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            kernel = np.ones((3, 3), np.uint8)
            erosion = cv2.erode(thresholding, kernel, iterations=2)

            ret, final = cv2.threshold(erosion, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            #Converted The characters into 28*28 uniform pixels, to feed into the neural Network
            smallsize = (28, 28)
            smallimage = cv2.resize(final, smallsize)

            filename = "lower_" + str(serialNo_LowerDigits)+ ".png"
            file_name = os.path.join(file_path, filename)
            #print(file_name)
            cv2.imwrite(filename, smallimage)
            serialNo_LowerDigits += 1
            digits_found += 1

            # Creating Dataset of the character to be fed to the Neural Network
            pixels = np.asarray(smallimage)
            fileName = str(digits_found) + ".csv"
            dataset_filename = os.path.join(file_path, fileName)
            np.savetxt(dataset_filename, pixels, fmt='%d', newline=',', delimiter=",")



        #Saving the image that shows segregation of characters (to be shown to the GUI)
        folderPath= os.path.join(folder_path,foldername)
        imageName= "lp_with_segmented_characters" + ".png"
        lp_with_segmented_characters_image_path = os.path.join(folderPath, imageName)
        #print("Image to Display path is: ", image_path)
        cv2.imwrite(lp_with_segmented_characters_image_path, img)
        self.img_path_lp_with_segmented_characters= lp_with_segmented_characters_image_path



    # Create Individual Directory for each Picture and write the image into it
    def writeImage(self, image, imgName):

        foldername = 'bike'
        path = sys.path[0]
        os.chdir(path)

        if (os.path.isdir(foldername)):
            shutil.rmtree(foldername)

        os.mkdir(foldername)

        # Writing the Image into a File
        os.chdir(os.path.join(path, foldername))
        #imgName = 'localized_plate' + ".png"
        folderPath= os.path.join(path,foldername)
        file_name = os.path.join(folderPath,imgName)
        print("Filename IS: ", file_name)
        cv2.imwrite(file_name, image)