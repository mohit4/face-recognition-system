#!/usr/bin/python

import os,cv2
import sys
import numpy as np
from PIL import Image

from database_work import *

# For face detection we will use the Haar Cascade provided by OpenCV.
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

# For face recognition we will the the LBPH Face Recognizer 
recognizer = cv2.createLBPHFaceRecognizer()

# it reads and returns the image in numpy format
# also returns the coordinates of the faces
def get_face_coordinates(imagePath):
	#read the image and convert it into grayscale
	image_grayscale = Image.open(imagePath).convert('L')
	#convert it to numpy array
	image_numpy = np.array(image_grayscale,'uint8')
	#fetch the face out of it
	faces = faceCascade.detectMultiScale(image_numpy)
	#return the numpy image with face coordinates
	return image_numpy,faces

#now we need to fetch faces from database
def get_faces_and_names():
	faces = []
	names = []
	# get all the user directories
	user_dirs = os.listdir("database")
	# listing the images in a user directory
	for one_user_dir in user_dirs:
		# listed all the pictures of a particular user
		all_pics = os.listdir("database/"+one_user_dir)
		for a_pic in all_pics:
			# a_pic is one picture
			# fetched the numpy_image and all the faces in it
			image_numpy,faces_cord = get_face_coordinates("database/"+one_user_dir+"/"+a_pic)
			for (x,y,w,h) in faces_cord:
				# cropping one face from image
				a_face = image_numpy[y:y+h,x:x+w]
				# finally adding face and name
				faces.append(a_face)
				names.append(int(one_user_dir))
				#for debugging purposes only
				#cv2.imshow("Reloading images...",a_face)
				#cv2.waitKey(10)
	return faces,names

def create_new_account(data):
	#the data from form
	name = data[0]
	age = data[1]
	desc = data[2]
	img_loc = data[3]

	#first of all we check if the img_loc exists or not
	if not os.path.exists(img_loc):
		return False

	#add the data into table
	#id will be used for naming the database
	ID=sqlite_new_user(name,age,desc)
	#created a new entry in database
	destination = "database/"+str(ID)
	os.mkdir(destination)
	#list all the images
	imageslist = os.listdir(img_loc)
	#move the images from source to destination
	for an_image in imageslist:
		source = img_loc+'/'+an_image
		os.rename(source,destination+'/'+an_image)
	return True

def train_recognizer():
	# faces and names are lists of equal length
	# so faces[i] is face of names[i]
	print "Initializing Face database for recognition ..."
	faces,names = get_faces_and_names()
	# finally we train our recognizer
	recognizer.train(faces,np.array(names))

def face_recognition(uploaded_img_name):
	# reading the image
	image_numpy,faces=get_face_coordinates(uploaded_img_name)
	# for each face in image call recognizer
	for(x,y,w,h) in faces:
		print "Working on",uploaded_img_name
		predicted_no, surity = recognizer.predict(image_numpy[y:y+h,x:x+w])
		if (100-int(surity) < 30):
			print "Unrecognized!"
			cv2.rectangle(image_numpy, (x, y), (x+w, y+h), (0, 0, 0), 2)
			cv2.imshow('Unrecognized '+uploaded_img_name, image_numpy)
			cv2.waitKey(50)
		else:
			name,age,desc = sqlite_get_info(predicted_no)
			
			print "Match Found!!!"
			print " "
			print "Name :",name
			print "Age  :",age
			print "Desc :",desc
			print "--------------------------------"
			print "Recognized with",100-surity,"%","surity"
			cv2.rectangle(image_numpy, (x, y), (x+w, y+h), (0, 0, 0), 2)
			cv2.imshow("Recognized "+name, image_numpy)
			cv2.waitKey(50)
		print "--------------------------------"

def create_some():
	data = ['Ben',34,'','/home/mohit/Desktop/Face Recognition Project/FINAL PROJECT/1']
	create_new_account(data)
	data = ['Glenn',28,'','/home/mohit/Desktop/Face Recognition Project/FINAL PROJECT/2']
	create_new_account(data)
	data = ['Kylo',26,'','/home/mohit/Desktop/Face Recognition Project/FINAL PROJECT/3']
	create_new_account(data)
	data = ['Richard',35,'','/home/mohit/Desktop/Face Recognition Project/FINAL PROJECT/4']
	create_new_account(data)

def all_documentation():
	print """
-----------------------------------
Face Recognition System 
-----------------------------------
Face recognition system accepts following command line arguments
	
	1. specifying a file name :
		face_recognizer -f <filename.ext>
	
	2. specifying a complete directory as input :
		face_recognizer -d <dirname/>
	
	3. Adding a new user details :
		face_recognizer -a <dirname/>

	4. View help
		face_recognizer -h help

		Note : 1. The directory must contains at least 4 images of the person for better results.

------------------------------------
	"""

def main():
	if len(sys.argv) < 3:
		print "Please specify a proper file or directory name with option."
		print "type face_recognizer.py -h help for more info"
		sys.exit(1)

	if(sys.argv[1]=='-h'):
		all_documentation()
		sys.exit(10)

	train_recognizer()

	if(sys.argv[1]=='-d'):
		dirname = sys.argv[2]
		if not os.path.isdir(dirname):
			print "Error :",sys.argv[2],"is not a directory."
			sys.exit(2)
		files = os.listdir(dirname)
		for a_file in files:
			face_recognition(dirname+a_file)
		cv2.waitKey(0)

	elif(sys.argv[1]=='-f'):
		filename = sys.argv[2]
		if not os.path.exists(filename):
			print "Error : Couldn't find the file",sys.argv[2]
			sys.exit(3)
		face_recognition(filename)
		cv2.waitKey(0)

	elif(sys.argv[1]=='-a'):
		dirname = sys.argv[2]
		if not os.path.isdir(dirname):
			print "Error :",sys.argv[2],"is not a directory."
			sys.exit(4)
		print "Please enter the following details :"
		name = raw_input('Name : ')
		if(not len(name)>1):
			print "Error : Name is too small."
			sys.exit(5)
		age = int(raw_input('Age : '))
		if(age<10):
			print "Error : Unaccepted Age."
			sys.exit(6)
		desc = raw_input('Desc (can be empty) : ')
		data=[name,age,desc,dirname]
		t=create_new_account(data)
		if(t):
			print "New account successfully created."
		else:
			print "Unable to create new account."

	else:
		print "Error : Unrecognized option."
		print "type face_recognizer.py -h help for more info"
		sys.exit(1)

if __name__ == "__main__":
	main()
