"""
Testing for automatic nuclei segmentation of PWS image
Patches of 512x512 from images and labels
The labels are created using manual segmentation from PWS software

data muist be input of 8 bit tif files of rms 

turn this into a function where it loads the rms in each folder it is iterating through 
at the end it will save teh resultant tif cube for each roi in the cell folder! 
then the conversion to hdf5 script can save it as a roi in the pwspy software.
"""

from pwsAI.regular_unet import unet_model   #Use regular unet model
import os
import numpy as np 
from matplotlib import pyplot as plt
from patchify import patchify, unpatchify
from tifffile import imsave
from sklearn import preprocessing
from skimage.color import label2rgb
from skimage import morphology
import cv2 as cv
import tifffile as tif 
import pathlib as pl
import sys
print("User Current Version:-", sys.version) 

pwsAIResourceDir = pl.Path(__file__).parent / '_resources'

###############################################################
# Function definitions for reading images as cv.imread gives issues sometimes
def readImages(imgPath):
    ''' 
    read image file and return array, dtype and the  shape 
    '''
    img = cv.imread(imgPath,0) # read image as grayscale
    try: 
        imgShape = img.shape
    except AttributeError:
        print("Initial attempt with opencv failed, will try again with tifffile package...")

    if img is None:
        img2 = tif.imread(imgPath)
        img = img2 
        imgShape = img2.shape
        
    ## create return obj 
    outList= [img,type(img), imgShape]
    return outList

# defined as a function so it can be iteratively called 

def autoSeg(fpath,num,t):
    #import os
    #os.environ["CUDA_VISIBLE_DEVICES"] = "-1" # Enable CPU

    ###############################################################
    # Provide the patch size of the images. 512x512
    IMG_HEIGHT = 512
    IMG_WIDTH  = 512
    IMG_CHANNELS = 1

    # Threshold for the predicted mask
    # Need to change this value for better output threshold value from 0.1 to 0.6 works
    thresh = t

    #####################################################################
    # Read test image. Sample test data can be found in Test_data folder
    ## bf
    #large_image = cv.imread('Test/Culture6_image_bd_cell15.tif', 0)

    ## rms test image
    large_image = readImages(os.path.join(fpath,f'rms_Cell{num}.tif'))[0]

    ## Single_wave
    #large_image = cv.imread('Test/Single_wavelength_600nm_image_stack_3_18_2021_48h_Mock3_cell_4.tif',0)

    # SW/Edge images
    #large_image = cv.imread('Test/Single_wavelength_600nm_image_stack_3_18_2021_48h_Mock3_Cell_5.tif',0)

    def get_model():
        return unet_model(IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS)

    model = get_model()

    #######################################################################
    # Select the training weights
    # only the weights for live_cell data available now.
    # other will be available after the training is complete
    Weights = "live_cell"

    if Weights == "HCT116_Oxa_treated":
        weights_path = pwsAIResourceDir / 'PWS_with_augmentation_weights_45_images_updated_minmax_norm.hdf5'
        #weights_path = 'Weight/PWS_with_augmentation_weights_88_images_minmax_norm.hdf5'
    elif Weights == "untreated":
        weights_path = pwsAIResourceDir / 'PWS_with_augmentation_weights_45_images_updated_minmax_norm1.hdf5' # this path will be updated later
    elif Weights == "live_cell":
        #bf
        #weights_path = 'Weight/PWS_with_augmentation_weights_minmax_norm_ali_roi_updated_174_images_bf_patch512.hdf5'

        # mean ref
        #weights_path = 'Weight/PWS_with_augmentation_weights_minmax_norm_ali_roi_updated_174_images_mean_ref_patch512.hdf5'

        # rms
        #weights_path = 'Weight/PWS_with_augmentation_weights_minmax_norm_ali_roi_updated_174_images_rms_patch512.hdf5'

        # Single_Wavelength
        #weights_path = 'Weight/PWS_with_augmentation_weights_minmax_norm_ali_roi_updated_174_images_sw_patch512.hdf5'

        # RMS+Single_Wavelength
        #weights_path = 'Weight/PWS_with_augmentation_weights_minmax_norm_ali_roi_updated_348_images_sw_n_rms_patch512_100_epoches.hdf5'

        # Edge images
        #weights_path = 'Weight/PWS_with_augmentation_weights_minmax_norm_ali_roi_updated_84_images_sw_edges_patch512_100_epoches.hdf5'

        # BF+RMS+SW images
        # 174 images each for BF, RMS, SW with total of 522 images used for training
        # Work for testing of BF/RMS/SW images separately
        weights_path = pwsAIResourceDir / 'PWS_with_augmentation_weights_minmax_norm_ali_roi_updated_522_images_bf_rms_sw_patch512_100_epoches.hdf5'

    elif Weights == "None":
        pass

    #Predict on a test images
    model.load_weights(weights_path)

    #This will split the image into small image patches. The training was on 512x512 image patches so we need to have same patch size
    # Instead of training on full size images 1024x1024 patches are created to minimize the computation during training.
    patches = patchify(large_image, (512, 512), step=512)  # Step=512 for 512 patches means no overlap
    min_max_scaler = preprocessing.MinMaxScaler() # Normalization

    predicted_patches = []
    for i in range(patches.shape[0]):
        for j in range(patches.shape[1]):
            print(i, j)
            single_patch = patches[i, j, :, :]
            single_patch_norm = np.expand_dims(min_max_scaler.fit_transform(single_patch),2) # normalization
            single_patch_norm = single_patch_norm[:, :, 0][:, :, None]
            single_patch_input = np.expand_dims(single_patch_norm, 0)

            # Predict and threshold for values above certain probability. This need to be set by the user and will affect the segmentaion result.
            #single_patch_prediction = (model.predict(single_patch_input)[0, :, :, 0] > 0.51).astype(np.uint8)

            # test time augmentation
            # Basically test data are augmented to obtain better results
            single_patch_prediction = (model.predict(single_patch_input)[0, :, :, 0])

            pred_lr0 = model.predict(np.expand_dims(np.fliplr(single_patch_norm), 0))[0][:, :, 0]
            pred_lr = np.fliplr(pred_lr0)

            pred_ud0 = model.predict(np.expand_dims(np.flipud(single_patch_norm), 0))[0][:, :, 0]
            pred_ud = np.flipud(pred_ud0)

            pred_lr_ud0 = model.predict(np.expand_dims(np.fliplr(np.flipud(single_patch_norm)), 0))[0][:, :, 0]
            pred_lr_ud = np.fliplr(np.flipud(pred_lr_ud0))

            predicted_patches_combined = (((single_patch_prediction + pred_lr + pred_ud + pred_lr_ud) / 4) > thresh).astype(np.uint8)
            #single_patch_prediction = (single_patch_prediction>thresh).astype(np.uint8)

            #predicted_patches.append(single_patch_prediction)
            predicted_patches.append(predicted_patches_combined)

    ## combine the patched to make a single large image
    predicted_patches = np.array(predicted_patches)
    predicted_patches_reshaped = np.reshape(predicted_patches, (patches.shape[0], patches.shape[1], 512,512) )
    reconstructed_image0 = unpatchify(predicted_patches_reshaped, large_image.shape)

    ## Threshold the small objects
    dtype = reconstructed_image0.dtype
    obj_thresh = 512 # Change this based on your requirements e.g. 512
    Th_img = (reconstructed_image0 > 0) # convert to binary image
    rec_image = morphology.remove_small_objects(Th_img, min_size=obj_thresh, connectivity=1)
    reconstructed_image = morphology.area_closing(rec_image, area_threshold=300, connectivity=1, parent=None, tree_traverser=None).astype(dtype) # fill the hole if there are any

    # Display various results
    brightest = large_image.max()
    darkest = large_image.min()
    # create a CLAHE object (Arguments are optional). # histogram equalization
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    large_image1 = clahe.apply(large_image)

    ## Check the area thresholding
    ### change it to one figure so not many popups 
    # set combined
    combined = label2rgb(reconstructed_image, large_image1, bg_label=0, bg_color=(0, 0, 0), kind='overlay')

    ## getting the boundary
    ret,thrs = cv.threshold(reconstructed_image,0,1,0)
    contours, hierarchy = cv.findContours(thrs,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    tmp = np.zeros_like(reconstructed_image)
    boundary = cv.drawContours(tmp, contours, -1, (1,1,1), 2)# 2 is the width of contours
    fig,axs = plt.subplots(nrows=1,ncols=4,figsize=(16,8))
    # overlay the boundary image
    combined_bou = label2rgb(boundary, large_image1, bg_label=0, bg_color=(0, 0, 0), kind='overlay')
    # display in one figure
    data = [large_image1,reconstructed_image,combined,combined_bou]
    titles = [f'Cell{num} RMS Image','Predicted RMS mask ','Auto ROI Overlay','Auto ROI Boundary']
    # ignore plotting
    if False:
        for i,ax in enumerate(axs.flatten()):
            print(i,'HERE')
            if i < 2: 
                ax.imshow(data[i],cmap = 'gray')
                ax.set_title(titles[i])
            else:
                ax.imshow(data[i])
                ax.set_title(titles[i])
        plt.show()

    if False:
        plt.figure(figsize=(16, 8))
        plt.subplot(121)
        plt.title('object_threshold_img')
        plt.imshow(rec_image, cmap='gray')
        plt.subplot(122)
        plt.title('Combined Rec_Image')
        plt.imshow(reconstructed_image, cmap='gray')
        plt.show()

        ###### ******* Quantitative evaluation of test results (IOU) *********

        # Plot the figure
        plt.figure(figsize=(16, 8))
        plt.subplot(121)
        plt.title('Test Image')
        plt.imshow(large_image1, cmap='gray')
        plt.subplot(122)
        plt.title('Prediction of Test Image')
        plt.imshow(reconstructed_image, cmap='gray')
        plt.show()

        #### Overlay the segmented image

        combined = label2rgb(reconstructed_image, large_image1, bg_label=0, bg_color=(0, 0, 0), kind='overlay')
        plt.figure(figsize=(16, 8))
        plt.subplot(121)
        plt.title('Test Image')
        plt.imshow(large_image1, cmap='gray')
        plt.subplot(122)
        plt.title('Combined Image')
        plt.imshow(combined)
        plt.show()


    # display
    if False:
        plt.figure(figsize=(16, 8))
        plt.subplot(121)
        plt.title('Test Image')
        plt.imshow(large_image1, cmap='gray')
        plt.subplot(122)
        plt.title('boundary mask combined image')
        plt.imshow(combined_bou)
        plt.show()

    print("The number of nucleus:", len(contours))

    # ****************** Save the segmented image as tif ****************
    #reconstructed_image1 = reconstructed_image.astype('uint16')
    #plt.imsave('results/reconstructed_mask6.tiff', reconstructed_image1, cmap='gray')

    ## ****************** isolate nuclei from the segmented image and create a image cube ****************

    def findBiggestBlob(inputImage):
        biggestBlob = inputImage.copy()
        largestArea = 0
        largestContourIndex = 0

        contours, hierarchy = cv.findContours(inputImage, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)

        for i, cc in enumerate(contours):
            area = cv.contourArea(cc)
            if area > largestArea:
                largestArea = area
                largestContourIndex = i

        tempMat = inputImage.copy()
        cv.drawContours(tempMat, contours, largestContourIndex, (0, 0, 0), -1, 8, hierarchy)
        biggestBlob = biggestBlob - tempMat
        return biggestBlob

    imageCounter = 0

    # Segmentation flag to stop the processing loop
    segmentObjects = True
    colorCopy = reconstructed_image.copy()

    # Resize at a fixed scale:
    resizePercent = 30
    resizedWidth = int(1024 * resizePercent / 100)
    resizedHeight = int(1024 * resizePercent / 100)

    # initialize cube to store the separated nuclei
    nucleus_cube= []

    for m in range(len(contours)):
        currentBiggest = findBiggestBlob(reconstructed_image)
        # check the isolated nucleus ROI
        #plt.imshow(currentBiggest, cmap='gray')
        #plt.show()

        # Use a little bit of morphology to "widen" the mask:
        kernelSize = 3
        opIterations = 2
        morphKernel = cv.getStructuringElement(cv.MORPH_RECT, (kernelSize, kernelSize))
        binaryMask = cv.morphologyEx(currentBiggest, cv.MORPH_DILATE, morphKernel, None, None, opIterations,cv.BORDER_REFLECT101)
        blobMask = cv.bitwise_and(colorCopy, colorCopy, mask=binaryMask)
        binaryImage = reconstructed_image - blobMask
        reconstructed_image= binaryImage
        blobMask = blobMask.astype('uint16')
        nucleus_cube.append(blobMask) # create the image cube. This cube can be used to integrate it with PWS software

    # ****************** Save the segmented nuclei as tif cube ****************
    imsave(os.path.join(fpath,f'reconstructed_nuclie_cube_Cell{num}.tif'), nucleus_cube)


    return data,titles


if __name__ =='__main__':
    # run the code here by giving it the number, the fpath and the thresh
    fpath= r'''C:\Users\nai5790\OneDrive - Northwestern University\Sunil - PWS Project\PWS Nuclei segmentation AI code\Test\guiTestData\Cell3'''
    num = 3 
    thresh = 0.6
    autoSeg(fpath,num,thresh)