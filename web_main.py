from flask import request, Flask
from flask_ngrok import run_with_ngrok
import base64
import cv2
import numpy as np

app=Flask(__name__)
# ngrok used for tunneling the network
# run_with_ngrok(app)
count=0
# index function execute when traffic occur at '/'
@app.route("/", methods=['POST','GET'])
def index():
	if request.method == 'POST':
		# reading the image (byte stream)
		data=request.stream.read()
		# seperating data from the header {data:image/png;....}
		data=str(data).split(',')[1]
		# print to be sure we are receiving the data correctly
		# print(data)

		global count
		count+=1
		
		''' starting conversion of html-base64 data to cv-numpy array '''
		# decoding base64 data
		img = base64.b64decode(data)
		# generating numpy array from decoded data
		npimg = np.frombuffer(img, dtype=np.uint8)
		# generating 3d array from 1d
		source = cv2.imdecode(npimg, 1)
		''' conversion finished '''

		''' saving the image to the local images folder
		to see that conversion is successful '''
		cv2.imwrite('images\\hello'+str(count)+'.jpg', source)
		
		return ""


if __name__ == "__main__":
	app.run()
