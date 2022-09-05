from flask import Flask, render_template, url_for, request
import GeneratePicture
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    im = Image.open("static/images/out.png")
    data = BytesIO()
    im.save(data, "JPEG")
    encoded_img_data = base64.b64encode(data.getvalue())
    return render_template("new_index.html", img_data=encoded_img_data.decode('utf-8'))

@app.route('/result',methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    print(output) # check if key not present. generate random.
    name = output["name"]
    theme = int(output["theme"])
    print(name, theme)
    encoded_img_data = GeneratePicture.generate_picture(name, theme)
    return render_template('new_index.html', img_data=encoded_img_data.decode('utf-8'))