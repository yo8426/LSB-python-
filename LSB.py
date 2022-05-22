import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

im1=cv2.imread('lena.png',0)
[m,n]=im1.shape
im2=np.zeros([int(m/4),int(n/4)])
im2=im2.astype(np.uint8)
im3=im1.copy()
im4=np.zeros([int(m/4),int(n/4)])

# write text on secret-image
im2 = cv2.putText(im2, 'secret data', (0, 8), cv2.FONT_HERSHEY_SIMPLEX, 0.3, 255, 1, cv2.LINE_AA)
im2 = cv2.putText(im2, 'careful', (0, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.3, 255, 1, cv2.LINE_AA)
im2 = cv2.putText(im2, 'please', (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.3, 255, 1, cv2.LINE_AA)
im2 = cv2.putText(im2, 'thank you', (0, 56), cv2.FONT_HERSHEY_SIMPLEX, 0.3, 255, 1, cv2.LINE_AA)
# secret image transfer to secret data
secret_pixel=[]
for i in range(int(m/4)):
    for j in range(int(n/4)):
        secret_pixel.append(format(im2[i,j],'08b'))
secret_pixel='%s'*len(secret_pixel) % tuple(secret_pixel)
secret_pixel=np.array(list(secret_pixel), dtype=int)
# host-image + secret-data transfer to stego-image
k=0
for i in range(m):
    for j in range(n):
        if k<len(secret_pixel):
            pixel_binary=np.unpackbits(im1[i,j],axis=0)
            pixel_binary[4:]=secret_pixel[k:k+4]
            im3[i,j]=int(np.packbits(pixel_binary))
            k=k+4
# from stego-image get 4bits secret-data
x=[]
for i in range(m):
    for j in range(n):
        value_binary=np.unpackbits(im3[i,j],axis=0)
        value_binary[4:]
        x.append(value_binary[4:])
# secret-data transfer to secret-image
k=0        
for i in range(int(m/4)):
    for j in range(int(n/4)):
        if k+1<len(x):
            im4[i,j]=x[k][0]*1+x[k][1]*2+x[k][2]*4+x[k][3]*8+x[k+1][0]*16+x[k+1][1]*32+x[k+1][2]*264+x[k+1][3]*128
        k=k+2

plt.figure()
# all title
plt.suptitle('compare') 
# one row two column 1th
plt.subplot(2,2,1)
plt.title('host-image')
plt.imshow(im1)
plt.subplot(2,2,2)
plt.title('embedding_data')
plt.imshow(im2)
plt.subplot(2,2,3)
plt.title('stego_data')
plt.imshow(im3)
plt.subplot(2,2,4)
plt.title('extration_data')
plt.imshow(im4)
plt.show()