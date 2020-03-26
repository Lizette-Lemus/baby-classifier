import os

from flask import Flask, request, render_template, send_from_directory
from fastai.vision import *

from werkzeug.utils import secure_filename

PORT = 5000	
app = Flask(__name__)

def model_predict(filepath):
    img = open_image(filepath)
    path = Path('data/')
    learn = load_learner(path)
    pred_class,pred_idx,outputs = learn.predict(img)
    return pred_class

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/", methods = ["GET", "POST"])
def upload():
    if request.method == "POST":
        f = request.files["image_file"]
        filename = secure_filename(f.filename)
        if not filename:
            return "No file selected"
        filepath = os.path.join("./images/", filename)
        f.save(filepath)
        prediction = model_predict(filepath)
        prediction_message = "That looks like a " + str(prediction) + " baby"
        return render_template("index.html", image_name = filename, 
            pred_message = prediction_message)
    return None

@app.route("/upload/<filename>")
def send_image(filename	):
    return send_from_directory("images", filename)

if __name__ == '__main__':
    app.run(port = PORT, debug = False)

