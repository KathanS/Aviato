from flask import Flask, render_template, url_for, request
import GeneratePicture

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template("new_index.html")

@app.route('/result',methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    name = output["name"]
    theme = int(output["theme"])
    print(name, theme)
    GeneratePicture.generate_picture(name, theme)
    return render_template('index.html')