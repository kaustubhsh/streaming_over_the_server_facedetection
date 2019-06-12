from flask import request, Flask
from flask_ngrok import run_with_ngrok

app=Flask(__name__)
# ngrok used for tunneling the network
# run_with_ngrok(app)

# index function execute when traffic occur at '/'
@app.route("/", methods=['POST','GET'])
def index():
	if request.method == 'POST':
		# reading the image (byte stream)
		data=request.stream.read()
		# seperating data from the header {data:image/png;....}
		data=str(data).split(',')[1]
		# print to be sure we are receiving the data correctly
		print(data)
		return ""

if __name__ == "__main__":
	app.run()
