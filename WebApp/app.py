# from flask import Flask, render_template, url_for, request
# import GeneratePicture
# from PIL import Image
# from io import BytesIO
# import base64

# app = Flask(__name__)

# @app.route('/')
# @app.route('/home')
# def home():
#     im = Image.open("static/images/out.png")
#     data = BytesIO()
#     im.save(data, "JPEG")
#     encoded_img_data = base64.b64encode(data.getvalue())
#     return render_template("new_index.html", img_data=encoded_img_data.decode('utf-8'))

# @app.route('/result',methods=['POST'])
# def result():
#     output = request.form.to_dict()
#     print(output) # check if key not present. generate random.
#     name = "DNA Tornado"
#     theme = 1
#     if "name" in output:
#         name = output["name"]
#     if "theme" in output:
#         theme = int(output["theme"])
#     print(name, theme)
#     encoded_img_data = GeneratePicture.generate_picture(name, theme)
#     return render_template('new_index.html', img_data=encoded_img_data.decode('utf-8'))

import imghdr
import pymongo
from pymongo import *
import ssl
from bson.json_util import dumps, loads
from flask import Flask, render_template, url_for, request
import datetime
import json
import GeneratePicture
from PIL import Image
import uuid
from io import BytesIO
import os
import base64

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'

    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
mongodb_host="mongodb+srv://njshah301:*NILAy4564*@cluster0.lyugc.mongodb.net/test"
(f"{bcolors.HEADER}Initializing database connections...{bcolors.ENDC}")

#MongoDB connection
print(f"{bcolors.HEADER}Connecting to MongoDB server...{bcolors.ENDC}")
myClient = pymongo.MongoClient(mongodb_host,tls=True, tlsAllowInvalidCertificates=True)
print(f"{bcolors.HEADER}Connection to MongoDB Server succeeded.{bcolors.ENDC}")
print(f"{bcolors.HEADER}Database connections initialized successfully.{bcolors.ENDC}")  
mydb=myClient["Aviato"]
mycol=mydb["register"]
app = Flask(__name__)
@app.route('/')
def student():
   return render_template('register.html')

def gethome():
      im = Image.open("static/images/out.png")
      data = BytesIO()
      im.save(data, "JPEG")
      encoded_img_data = base64.b64encode(data.getvalue())
      return render_template("new_index.html",img_data=encoded_img_data.decode('utf-8'))

@app.route('/register', methods = ['POST','GET'])
def register():
   if request.method == 'POST':
      userName = request.form.get("name")
      email_add=request.form.get("email")
      pwd=request.form.get("password")
      cpwd=request.form.get("c_password")
      mylist={"Name":userName,"Email":email_add,"Password":pwd}
      print(mylist)
      mycol.insert_one(mylist)
   return gethome()

@app.route('/login', methods = ['POST','GET'])
def login():
   if request.method == 'POST':
      email_id=request.form.get("email")
      pwd=request.form.get("password")
      csr=mycol.find({"$and":[{'Email':email_id},{'Password':pwd}]})
      check=list(csr)
      print(check)
      if(len(check)):
        return gethome()

@app.route('/result',methods=['POST'])
def result():
    output = request.form.to_dict()
    print(output) # check if key not present. generate random.
    name = "DNA Tornado"
    theme = 1
    if "name" in output:
        name = output["name"]
    if "theme" in output:
        theme = int(output["theme"])
    print(name, theme)
    encoded_img_data = GeneratePicture.generate_picture(name, theme)
    return render_template('new_index.html', img_data=encoded_img_data.decode('utf-8'))



if __name__ == '__main__':
   app.run(debug = True)