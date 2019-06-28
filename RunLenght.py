import numpy as np 
import pickle
import cv2
import sys
import os
def encode_RLE(arr):
	pre_value = arr[0]
	result = []
	lenght = []
	pre_value = arr[0]
	doub = False
	for i,value in enumerate(arr[1:]):
		if value == pre_value:
			if doub is False:
				result += [value] + [value]
				doub = True
				lenght += [2]
			else:
				if lenght[-1] == 255:
					doub = False
					pre_value = value
				else:
					lenght[-1] +=1
		else :
			if doub == False:
				result += [pre_value]
			pre_value = value
			doub = False
	if doub == False:
		result += [pre_value]
	return (result,lenght)

def decode_RLE(arr,run):
	result = []
	pre_value = arr[0]
	doub = False
	count =0
	Max_len = False
	for i,value in enumerate(arr[1:]):
		if value == pre_value:
			if Max_len == True:
				pre_value = value
				Max_len = False
				doub = False
			else:
				result += [value]*run[count]
				if run[count] == 255:
					Max_len = True
				count +=1
				pre_value = value
				doub = True
		else:
			if Max_len == True:
				Max_len = False
			if doub == False:
				result += [pre_value]
			pre_value = value
			doub = False
	if doub == False:
		result += [pre_value]

	return result

if __name__ == '__main__':
	
	
	img = cv2.imread('Original.jpeg')
	root = img
	arr = np.array(img)
	w,h,c = img.shape

	with open('Uncompress_img','wb') as f:
		pickle.dump(img,f)



	print('Compressing...')
	arr = cv2.cvtColor(img,cv2.COLOR_BGR2YCrCb)
	y,cr,cb = arr[:,:,0] , arr[:,:,1] , arr[:,:,2]
	y,cb,cr = y.ravel(),cb.ravel(),cr.ravel()

	y,runy = encode_RLE(y)
	cb,runcb =encode_RLE(cb)
	cr,runcr = encode_RLE(cr)

	data = (bytes(y),bytes(runy),
			bytes(cb),bytes(runcb),
			bytes(cr),bytes(runcr),
			w,h)

	with open('Compress_img','wb') as f:
		pickle.dump(data,f)
	print('Compress completed!')
	data = None
	with open('Compress_img','rb') as f:
		data = pickle.load(f)

	print('Decompressing ...')
	y,runy,cb,runcb,cr,runcr,w,h = data

	Y = decode_RLE(y,runy)

	CB = decode_RLE(cb,runcb)

	CR = decode_RLE(cr,runcr)
	#Y = np.array(Y)
	Y = np.reshape(Y,(w,h))
	CB = np.reshape(CB,(w,h))
	CR = np.reshape(CR,(w,h))
	img = np.zeros((w,h,3),'uint8')
	img[:,:,0] = Y
	img[:,:,1] = CR
	img[:,:,2] = CB
	img = cv2.cvtColor(img,cv2.COLOR_YCrCb2BGR)
	with open('Decompress_img','wb') as f:
		pickle.dump(img,f)
	print('Decompress completedm !')
	cv2.imshow('Uncompress',root)
	cv2.imshow('Compress',img)

	a = root.ravel()
	b = img.ravel()
	if np.array_equal(a,b):
		print('correct')
	else:
		print('wrong')

	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
	

	




	
	

	

	
	