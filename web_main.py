from flask import Flask,send_file
from flask import request, jsonify
import base64
import numpy as np
import cv2
from io import StringIO
from flask_cors import CORS
from flask_ngrok import run_with_ngrok
count=0
main_source=0
app=Flask(__name__)
CORS(app)
#run_with_ngrok(app)

@app.route("/", methods=['POST','GET'])
def index():
	if request.method == 'POST':
		data=request.stream.read()
		data=str(data).split(',')[1] #.encode()
		global count
		count+=1
		img = base64.b64decode(data)
		npimg = np.frombuffer(img, dtype=np.uint8)
		source = cv2.imdecode(npimg, 1)
		
		face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		face_img = source.copy()
		face_rects = face_cascade.detectMultiScale(face_img,scaleFactor=1.2)
		for (x,y,w,h) in face_rects: 
        		cv2.rectangle(face_img, (x,y), (x+w,y+h), (255,255,255), 10) 



		global main_source
		cv2.imwrite('images\\hello'+str(count)+'.jpg', face_img)
		with open('images\\hello'+str(count)+'.jpg', 'rb') as image_file:
			encoded_string = base64.b64encode(image_file.read())
		main_source=encoded_string
		return ""
	else:	
		return main_source
if __name__ == "__main__":
	app.run()