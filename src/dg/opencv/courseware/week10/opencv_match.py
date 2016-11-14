# -*- coding: utf-8 -*- 

import os
import sys
import argparse

import numpy
from numpy import linalg as la  

import cv2

folder = "/Users/luoyun/Downloads/101_ObjectCategories/accordion/"

"""计算相似度"""
#1.欧式距离
def euclidSimilar(inA,inB):
	print "euclidSimilar"
	inB = cv2.resize(inB,inA.shape)
	return 1.00/(1.00+la.norm(inA-inB))  

#2.皮尔逊相关系数
def pearsonSimilar(inA,inB):
	print "pearsonSimilar"
	if len(inA)<3:
		return 1.00
	return 0.55+0.55*numpy.corrcoef(inA,inB,rowvar=0)[0][1]  

#3.余弦相似度
def cosSimilar(inA,inB):  
	print "cosSimilar"
	inA=numpy.mat(inA)  
	inB=numpy.mat(inB)  
	num=float(inA*inB.T)  
	denom=la.norm(inA)*la.norm(inB)  
	return 0.55+0.55*(num/denom)  

#4.汉明距离
def hammingSimilar(inA,inB):
	print "hammingSimilar"
	inB = cv2.resize(inB.copy(),inA.T.shape)
	match_num = (inA&inB).sum()
	return match_num

"""求取特征"""
def hashFeature(pic_name):
	print "phashFeature"
	image = cv2.imread(pic_name)
	res_image = cv2.resize(image,(8,8))
	gray = cv2.cvtColor(res_image,cv2.COLOR_RGB2GRAY)
	gray = gray / 4
	threshold = gray.sum()/64
	ret,binary = cv2.threshold(gray,threshold,1,cv2.THRESH_BINARY)
	return binary

def rgbFeature(pic_name):
	print "rgbFeature"
	image = cv2.imread(pic_name)
	res_image = cv2.resize(image,(50,50))
	res_image = res_image/64
	r,g,b = cv2.split(res_image)
	norm = r*16 + g*4 + b
	stat = numpy.zeros(64)
	for i in range(res_image.shape[0]):
		for j in range(res_image.shape[1]):
			index = norm[i,j]
			stat[index] += 1
	return stat

def otsuFeature(pic_name):
	print "otsuFeature"
	image = cv2.imread(pic_name)
	gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
	ret,threshold = cv2.threshold(gray,0,1,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	return threshold


#show result
def show_result(image_list):
	for index,image in enumerate(image_list):
		img = cv2.imread(image)
		cv2.imshow(str(index),img)
	cv2.waitKey()

if __name__ == '__main__':

	#解析命令行
	parser = argparse.ArgumentParser(description="Information Here")
	parser.add_argument('-f','--feature',type=str,choices=['hash','rgb','otsu'],help="feature extraction func")
	parser.add_argument('-s','--similar',type=str,choices=['euclid','pearson','cos','hamming'],help="similar match func")
	args = parser.parse_args()

	print vars(args)
	
	#specific a test image
	test_image = folder+"image_0001.jpg"
	if args.feature=="otsu" :
		feature_org = otsuFeature(test_image)
	elif args.feature=="rgb" :
		feature_org = rgbFeature(test_image)
	else:
        	feature_org = hashFeature(test_image)

        #top 10 images
	image_list = []
	result_list = []

	#process
	for pic_name in os.listdir(folder):
		if (folder+pic_name==test_image):
			continue

		if args.feature=="otsu" :
			feature_img = otsuFeature(folder+pic_name)
		elif args.feature=="rgb" :
			feature_img = rgbFeature(folder+pic_name)
		else :
			feature_img = hashFeature(folder+pic_name)

		if args.similar=="euclid":
			match = euclidSimilar(feature_org,feature_img)
		elif args.similar=="pearson":
			match = pearsonSimilar(feature_org,feature_img)
		elif args.similar=="cos":
			match = cosSimilar(feature_org,feature_img)
		else:
			match = hammingSimilar(feature_org,feature_img)

		if len(image_list)==0:
			image_list.append(folder+pic_name)
			result_list.append(match)
			continue

		for index,result in enumerate(result_list):
			if result < match :
				image_list.insert(index,folder+pic_name)
				result_list.insert(index,result)
				if (len(image_list) > 10):
					image_list.pop()
					result_list.pop()
				break

	show_result(image_list)



