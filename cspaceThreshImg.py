import cv2
import numpy as np



__author__ = "Alexander Reynolds"
__email__ = "ar@reynoldsalexander.com"



"""Private helper functions"""



def __cspaceSwitch(img, cspace):
    """Coverts the colorspace of img from BGR to cspace

    Keyword arguments: 
        img -- the image to convert
        cspace -- the colorspace to convert to; see keys below

    Colorspace keys:
        0 -- BGR        1 -- HSV        2 -- HLS        3 -- Lab        
        4 -- Luv        5 -- YCrCb      6 -- XYZ        7 -- Grayscale

    Returns:
        img -- img with the converted colorspace
    """
    if cspace is 0:
        return img
    convert_code = {
        1: cv2.COLOR_BGR2HSV,
        2: cv2.COLOR_BGR2HLS,
        3: cv2.COLOR_BGR2Lab,
        4: cv2.COLOR_BGR2Luv,
        5: cv2.COLOR_BGR2YCrCb,
        6: cv2.COLOR_BGR2XYZ,
        7: cv2.COLOR_BGR2GRAY
    }[cspace]
    img = cv2.cvtColor(img, convert_code)

    return img


def __cspaceBounds(cspace, sliderPos):
    """Calculates the lower and upper bounds for thresholding a 
    colorspace based on the thresholding slider positions.

    Keyword arguments:
        cspace -- the colorspace to find bounds of; see keys in __cspaceSwitch()
        sliderPos -- the positions of the thresholding trackbars; length 6 list

    Returns:
        lowerb -- np.array containing the lower bounds for each channel threshold
        upperb -- np.array containing the upper bounds for each channel threshold
    """
    min_dict = {3: np.array([0,1,1])}
    max_dict = {1: np.array([180,255,255]), 2: np.array([180,255,255])}

    mins = min_dict.get(cspace, np.array([0,0,0]))
    maxs = max_dict.get(cspace, np.array([255,255,255]))

    lowerb = np.array([sliderPos[0], sliderPos[2], sliderPos[4]])
    upperb = np.array([sliderPos[1], sliderPos[3], sliderPos[5]])
    lowerb = lowerb * (maxs-mins) / 100 + mins # put in the correct range
    upperb = upperb * (maxs-mins) / 100 + mins

    if cspace is 7: lowerb, upperb = lowerb[0], upperb[0]

    return lowerb, upperb


def __cspaceRange(img, cspace, lowerb, upperb):
    """Thresholds img in cspace with lowerb and upperb

    Keyword arguments:
        img -- the image to be thresholded
        cspace -- the colorspace to threshold in; see keys in __cspaceSwitch()

    Returns:
        bin_img -- a binary image that has been thresholded
    """
    img = __cspaceSwitch(img, cspace)
    bin_img = cv2.inRange(img, lowerb, upperb)

    return bin_img



"""Main public function"""



def main(imgPath, cspaceLabel, sliderPos):
    """Computes the colorspace thresholded image based on 
    slider positions and selected colorspace.

    Inputs:
        imgPath -- path to the input image (string)
        cspaceLabel -- see colorspace labels (string)
        sliderPos -- positions of the six sliders (6-long int list)

    Available colorspace labels:
        BGR        HSV        HLS        Lab        
        Luv        YCrCb      XYZ        Grayscale

    returns
        outPath -- path of saved processed image file (string)
        colorspaceLabel -- colorspace of the image (string)
        lowerBound -- threshold lower bound (list[])
        upperBound -- threshold upper bound (list[])
    """
    img = cv2.imread(imgPath)

    # create colorspace labels to be displayed
    cspace_dict = {'BGR':0,'HSV':1,'HLS':2,'Lab':3,'Luv':4,'YCrCb':5,'XYZ':6,'Gray':7}
    cspace = cspace_dict[cspaceLabel]

    # create thresholded image
    lowerb, upperb = __cspaceBounds(cspace, sliderPos)
    bin_img = __cspaceRange(img, cspace, lowerb, upperb)

    # output processing
    lowerb = lowerb.tolist()
    upperb = upperb.tolist()
    out_path = 'output.png'
    cv2.imwrite(out_path, bin_img)

    return_dict = {
        'outPath' : out_path,
        'cspaceLabel' : cspaceLabel,
        'lowerBound': lowerb,
        'upperBound': upperb}
    
    return return_dict