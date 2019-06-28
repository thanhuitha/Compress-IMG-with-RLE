from Compress import Compress_RLE
from Decompress import Decompress_RLE
import cv2
import numpy as np

path_original_img = 'Original.jpeg'
path_Uncompress_img = 'Uncompress_img'
path_compessed_img = 'Compressed_img'

encode = Compress_RLE()
print('Compressing ...')
encode.compress_img(path_original_img,path_Uncompress_img,path_compessed_img)
print('Compress completed ! Ratio :%f' %encode.ratio)
decode = Decompress_RLE()
print('Decompressing ...')
decode.decompress_img(path_compessed_img)
cv2.imshow('Original_img',encode.img)
cv2.imshow('Decompressed_img',decode.img)
print('Decompress completed !')

#Compare 2 img to check algorithm 
before = encode.img.ravel()
after = encode.img.ravel()
if np.array_equal(before,after):
	print('correct')
else:
	print('wrong')

cv2.waitKey(0)
cv2.destroyAllWindows()


