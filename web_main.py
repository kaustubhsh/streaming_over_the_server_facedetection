from flask import request
from flask_ngrok import run_with_ngrok

app=Flask(__name__)
run_with_ngrok(app)

@app.route("/", methods=['POST','GET'])
def index():
		return "Hello world"


if __name__ == "__main__":
	app.run()
