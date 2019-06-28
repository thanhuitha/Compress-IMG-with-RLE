import cv2
import numpy as np 
import os
import pickle

class Compress_RLE():
	def __init__(self):
		self.img = None
		self.size_original_file = None
		self.size_compressed_file = None
		self.ratio = 1
	def Load_img(self,path_root,path_uncompess):
		img = cv2.imread(path_root)
		self.img = img
		with open(path_uncompess,'wb') as f:
			pickle.dump(img,f)
		self.size_original_file = os.path.getsize(path_uncompess)
		return img
	def cvt_YCC(self,img):
		arr = cv2.cvtColor(img,cv2.COLOR_BGR2YCrCb)
		y,cr,cb = arr[:,:,0] , arr[:,:,1] , arr[:,:,2]
		y,cb,cr = y.ravel(),cb.ravel(),cr.ravel()
		return y,cr,cb
	def encode_RLE(self,arr):
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
	def compress_img(self,path_root,path_uncompess,path_compessed):
		img = self.Load_img(path_root,path_uncompess)
		w,h,c = img.shape
		Y,CR,CB = self.cvt_YCC(img)
		y,runy = self.encode_RLE(Y)
		cr,runcr = self.encode_RLE(CR)
		cb,runcb = self.encode_RLE(CB)
		data = (bytes(y),bytes(runy),
			bytes(cb),bytes(runcb),
			bytes(cr),bytes(runcr),
			w,h)
		with open(path_compessed,'wb') as f:
			pickle.dump(data,f)
		self.size_compressed_file = os.path.getsize(path_compessed)
		self.ratio = self.size_original_file / self.size_compressed_file



