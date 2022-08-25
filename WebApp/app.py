from flask import Flask, render_template, url_for, request
import GeneratePicture

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/result',methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    print(output)
    name = output["name"]
    GeneratePicture.generate_picture(name)
    return render_template('photo.html')