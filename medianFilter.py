#Busra_Unlu_211711008_HW3

from pickletools import uint8
import numpy as np
import cv2 as cv
import math


img_filename = 'C:/Users/Busra/Desktop/BIL561_Odev/hw3/noisyImage.jpg'
img = cv.imread(img_filename, 0)
(h, w) = img.shape[:2]

#QUESTION 1
#Median Filter
def medianFilter(image,kernelSize):
    #padding
    top  = bottom = int((kernelSize-1)/2)        #rows
    left = right  = int((kernelSize-1)/2)        #cols
    padImg = cv.copyMakeBorder( image, top, bottom, left, right, cv.BORDER_REPLICATE)
       
    imageW, imageH = image.shape           # get image dimensions
    filter_out = np.zeros((imageW, imageH))    # intialize output image
    #convolution
    for i in range(w):
        for j in range(h):
            temp = padImg[i:i + kernelSize, j:j + kernelSize]
            filter_out[i,j] = np.median(temp)

    filter_out=filter_out.astype(np.uint8)
    return filter_out
    

output_1=medianFilter(img,5)

#Opencv median filter
output_2=cv.medianBlur(img,5)

#difference
difference_1=np.abs(output_1 - output_2)

#QUESTION 2 
#PNSR -measure the performance of restoration algorithms. (higher is better)
img_filename2 = 'C:/Users/Busra/Desktop/BIL561_Odev/hw3/lena_grayscale_hq.jpg'
groundTruth = cv.imread(img_filename2, 0)

#5x5 box filter
boxOutput = cv.boxFilter(img, 0, (5,5)  , False, borderType=cv.BORDER_CONSTANT)
#zero mean, 7x7 Gaussian function,
gaussOutput = cv.GaussianBlur(img, (7,7),0, borderType = cv.BORDER_CONSTANT)
#5x5 median
medianOutput=cv.medianBlur(img,5)

psnr_0=cv.PSNR(groundTruth,output_1)
psnr_1=cv.PSNR(groundTruth,boxOutput)
psnr_2=cv.PSNR(groundTruth,gaussOutput)
psnr_3=cv.PSNR(groundTruth,medianOutput)

#Question 3
#center weighted median filter
def weightedMedianFilter(image,kernelSize):
    #padding
    top  = bottom = int((kernelSize-1)/2)        #rows
    left = right  = int((kernelSize-1)/2)        #cols
    padImg = cv.copyMakeBorder( image, top, bottom, left, right, cv.BORDER_REPLICATE)
       
    imageW, imageH = image.shape           # get image dimensions
    filter_out = np.zeros((imageW, imageH))    # intialize output image
    #convolution
    for i in range(w):
        for j in range(h):
            temp = padImg[i:i + kernelSize, j:j + kernelSize]
            #1.yol
            #meds=np.array([np.median(temp),np.median(temp)])
            #temp=np.append(temp,meds)
            #2.yol
            #temp1=np.append(temp,np.median(temp))
            #temp1=np.append(temp1,np.median(temp))
            #filter_out[i,j] = np.median(temp1)
            #3.yol
            centerValue=temp[kernelSize//2,kernelSize//2]
            flattenedImg=temp.flatten()
            flattenedImg=np.append(flattenedImg,centerValue)
            flattenedImg=np.append(flattenedImg,centerValue)
            median=np.median(flattenedImg)
            filter_out[i,j] = median
    filter_out=filter_out.astype(np.uint8)
    return filter_out


output_3=weightedMedianFilter(img,5)

psnr_5=cv.PSNR(groundTruth,output_3)

#Observation:
"""
What are the PSNR values? 
- PSNR sinyal ve g??r??lt?? oran??d??r. Elde edilmek istenen
temiz g??r??lt??n??n ??zerine binmi?? g??r??lt??ye oran??d??r. 
Y??ksek PSNR de??eri i??ermesi- temiz g??r??nt??n??n 
g??r??lt??den ??ok olmas??/ g??r??lt??n??n az olmas??- tercih edilen durumdur. 
????lem yap??lan g??r??nt?? ve i??lem hakk??nda bilgi sahibi olmam??za
da yarar. 
According to PSNR, which filter performs the best? Can you tell why? 
-weighted median filtrenin PSNR de??eri daha y??ksektir bunun nedeni merkez a????rl??kl?? ger??ekle??tiriliyor
olmas?? ve daha iyi salt and paper g??r??lt??y?? temizlemesidir.
"""

#QUESTION 4
#sharpening and try to cheat PSNR
kernel = np.array([[0, -1, 0],
                   [-1, 5,-1],
                   [0, -1, 0]])
image_sharp = cv.filter2D(src=output_3, ddepth=-1, kernel=kernel)

psnr_6=cv.PSNR(groundTruth,image_sharp)

#change contrast and try to cheat PSNR
alpha = 1.5 # Contrast control (1.0-3.0)
beta = 0    # Brightness control (0-100)
adjusted = cv.convertScaleAbs(output_3, alpha=alpha, beta=beta)
psnr_7=cv.PSNR(groundTruth,adjusted)

"""
PSNR her durumda kalitenin ??l????lmesi i??in en iyi ??l??ek olamayabilir, color enhancement, sharpening i??in g??rsel de??erlendirme
daha do??ru sonu??lar al??nmas??n?? sa??layabilir.Bu durumlarda ??oklu kat??l??mc??lara g??rsel ????kt??lar??n 
g??sterilip metotlar??n kalitesinin ??l????lmesi tercih edilebilmektedir. Bu ??devde de en iyi PSNR 
sonucu weighted median filtre (PSNR=31.40dB) ile al??nsa da g??rsel olarak sharpening (image_sharp) ????kt??s?? (PSNR=25.40dB) 
daha iyi bir ????kt??d??r.Buna ek olarak contrast de??i??tirirsek(adjusted) de d??????k PSNR(PSNR=12.54dB) ile daha iyi g??rsel ????kt?? al??nabilir. 
Bu ba??lamda PSNR her zaman g??rsel kalite ??l????m?? i??in alt??n standart de??ildir. 

"""

#Outputs
cv.imshow("original image", img),
cv.imshow("ground truth", groundTruth )

cv.imshow("my median filter image, PSNR= " + str(psnr_0) , output_1 )
cv.imshow("opencv box filter image, PSNR= "+ str(psnr_1), boxOutput )
cv.imshow("opencv gaussian filter image, PSNR= "+ str(psnr_2), gaussOutput )
cv.imshow("opencv median filter image, PSNR= " + str(psnr_3), medianOutput )
cv.imshow("weighted median filtered image, PSNR= "+ str(psnr_5), output_3 )

cv.imshow("sharpening image, PSNR= "+ str(psnr_6), image_sharp )
cv.imshow("contrast changed image, PSNR= "+ str(psnr_7), adjusted )

cv.imshow("difference my median and opencv median filter",   100 *difference_1)


#TERMINAL OUTPUTS
print("------------------------------------------")
print("Difference (my median and opencv median filter) is : ",    np.sum(np.sum(np.abs(output_1 - output_2))))
print("There is no difference")
print("-------------------PSNRS------------------")
print("PSNR value (ground truth and box filter)",psnr_1)
print("PSNR value (ground truth and gauss filter)",psnr_2)
print("PSNR value (ground truth and median filter)",psnr_3)
print("PSNR value (ground truth and my median filter)",psnr_0)
print("PSNR value (ground truth and my weighted median filter)",psnr_5)
print("-------------------Question4------------------")
print("PSNR value (ground truth and sharpening image)",psnr_6)
print("PSNR value (ground truth and contrast changed image)",psnr_7)

cv.waitKey(0)
cv.destroyAllWindows()