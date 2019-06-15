from flask import Flask,send_file
from flask import request, jsonify
import base64
import os
import numpy as np
import cv2
from io import StringIO
from flask_cors import CORS
import shutil
count=0                              #global count value to save and retreive frames
main_source=0			     #global value of detected face value to return
app=Flask(__name__)
CORS(app)				#adding cors policy to flask

@app.route("/", methods=['POST','GET'])			#taking both method 'POST' for receiving images and 'GET' for receiving request to send classified images.
def index():

	#if 'post' request and frames are being received

	if request.method == 'POST':		
		global count
		global main_source			
		data=request.stream.read()		#encoded frame received
		data=str(data).split(',')[1] #.encode()
		count+=1
		img = base64.b64decode(data)
		npimg = np.frombuffer(img, dtype=np.uint8)
		source = cv2.imdecode(npimg, 1)			#source contains nd array of image
		if count <4:				#for black frames which generate at starting of stream 
			return ""
		cv2.imwrite('images\\hello1'+str(count)+'.jpg', source) #saving the received frame
		face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')  #for classification of face
		face_img = source.copy()
		face_rects = face_cascade.detectMultiScale(face_img,scaleFactor=1.2)
		for (x,y,w,h) in face_rects: 
        		cv2.rectangle(face_img, (x,y), (x+w,y+h), (255,255,255), 10) 
		
		cv2.imwrite('images\\hello'+str(count)+'.jpg', face_img) 	#saving the classified frame
		
		
		#sending the latest classified frame and encoding it but if there is no image then previous recevied frame will be choosen and sent by using try catch.
		try:
			with open('images\\hello'+str(count)+'.jpg', 'rb') as image_file:	
				encoded_string = base64.b64encode(image_file.read())					
			main_source=encoded_string
		
		except:
			try:
				with open('images\\hello1'+str(count-1)+'.jpg', 'rb') as image_file:
					encoded_string = base64.b64encode(image_file.read())
				main_source=encoded_string
			except:
				with open('images\\hello1'+str(count-2)+'.jpg', 'rb') as image_file:
					encoded_string = base64.b64encode(image_file.read())
				main_source=encoded_string
		return ""			# it is a post request so empty string is sent. 
	
	
	#if 'get' request for sending frames is received.
	else:	
		if type(main_source)==int:		 
			return ""
		return main_source
if __name__ == "__main__":
	app.run()