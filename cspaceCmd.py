import argparse
import cspaceThreshImg
import cv2 # for checking the image



__author__ = "Alexander Reynolds"
__email__ = "ar@reynoldsalexander.com"



"""Private validator functions"""



def __sanitize(filename):
    return "".join([c for c in filename 
        if c.isalpha() or c.isdigit() or c in ['.','_','/']]).rstrip()


def __checkimg(imgPath):
    imgPath = __sanitize(imgPath)
    img = cv2.imread(imgPath)
    if img is None or len(img.shape)==2:
         raise argparse.ArgumentTypeError("%s is an invalid image filename, \
            must be a three-channel image." % imgPath)
    return imgPath


def __checkcspace(cspace):
    validspaces = ['BGR', 'HSV', 'HLS', 'Lab', 'Luv', 'YCrCb', 'XYZ', 'Grayscale']
    if cspace not in validspaces:
         raise argparse.ArgumentTypeError("%s is an invalid colorspace, \
            must be one of: BGR, HSV, HLS, Lab, Luv, YCrCb, XYZ, or Grayscale." % cspace)
    return cspace



"""Command line parsing"""



if __name__ == "__main__":
    """To be ran from command line

    Usage: python3 cspaceCmd.py input/lane.jpg HSV 0 16 21 72 78 100
    """
    parser = argparse.ArgumentParser(description='Color threshold an image in any colorspace \
        and save it to a file.')

    parser.add_argument('imgPath', 
        help='Filename of the image to be thresholded (string)', type=__checkimg)
    parser.add_argument('cspaceLabel', 
        help='Colorspace (BGR, HSV, HLS, Lab, Luv, YCrCb, XYZ, or Grayscale (string))', type=__checkcspace)
    parser.add_argument('sliderPos1', 
        help='Channel 1 Min (int)', type=int)
    parser.add_argument('sliderPos2', 
        help='Channel 1 Max (int)', type=int)
    parser.add_argument('sliderPos3', 
        help='Channel 2 Min (int)', type=int)
    parser.add_argument('sliderPos4', 
        help='Channel 2 Max (int)', type=int)
    parser.add_argument('sliderPos5', 
        help='Channel 3 Min (int)', type=int)
    parser.add_argument('sliderPos6', 
        help='Channel 3 Max (int)', type=int)

    args = parser.parse_args()

    # grab arguments
    imgPath = args.imgPath
    cspaceLabel = args.cspaceLabel
    sliderPos = [args.sliderPos1, args.sliderPos2, args.sliderPos3, 
        args.sliderPos4, args.sliderPos5, args.sliderPos6]

    # read input image
    img = cv2.imread(imgPath)

    # run the colorspace thresh script
    outImg, cspaceLabel, lowerb, upperb = cspaceThreshImg.main(
        img, cspaceLabel, sliderPos)

    # write the output image
    outPath = 'output/output.png'
    os.makedirs(outPath, exist_ok=True)
    cv2.imwrite(outPath, outImg)

    # return a dict (eventually JSON dump)
    return_dict = {'outPath' : outPath,
        'cspaceLabel' : cspaceLabel,
        'lowerBound': lowerb,
        'upperBound': upperb}

    print(return_dict)