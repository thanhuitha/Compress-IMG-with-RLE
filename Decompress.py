import cv2
import numpy as np 
import os
import pickle

class Decompress_RLE():
	def __init__(self):
		self.img = None
	def Load_img(self,path):
		data = None
		with open(path,'rb') as f:
			data = pickle.load(f)
		self.img_uncompress = data
	def cvt_RGB(self,Y,CB,CR,w,h):
		Y = np.reshape(Y,(w,h))
		CB = np.reshape(CB,(w,h))
		CR = np.reshape(CR,(w,h))
		img = np.zeros((w,h,3),'uint8')
		img[:,:,0] = Y
		img[:,:,1] = CR
		img[:,:,2] = CB
		self.img = cv2.cvtColor(img,cv2.COLOR_YCrCb2BGR)
	def decode_RLE(self,arr,run):
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
	def decompress_img(self,path_compess,path_decompressed = 'Decompress_img'):
		self.Load_img(path_compess)
		y,runy,cb,runcb,cr,runcr,w,h = self.img_uncompress
		Y = self.decode_RLE(y,runy)
		CB = self.decode_RLE(cb,runcb)
		CR = self.decode_RLE(cr,runcr)
		self.cvt_RGB(Y,CB,CR,w,h)
		with open('Decompress_img','wb') as f:
			pickle.dump(self.img,f)

