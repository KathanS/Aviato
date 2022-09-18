import imghdr
import psycopg2
import psycopg2.extras
import pymongo
import ssl
from bson.json_util import dumps, loads
from flask import Flask, render_template, url_for, request
import datetime
import json
import GeneratePicture
from PIL import Image
from io import BytesIO
import base64
import uuid

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
mycol="register"

app = Flask(__name__)
@app.route('/')
def student():
   return render_template('register.html')

@app.route('/home', methods = ['POST','GET'])
def home():
   print("Hello")
   userName = request.form.get("name")
   print(userName)
   email_add=request.form.get("email")
   pwd=request.form.get("password")
   cpwd=request.form.get("c_password")
   uid=uuid.uuid1
   id=uid.int
   mylist=[userName,email_add,pwd]
   it = iter(mylist)
   res_dct = dict(zip(it, it))
   print(res_dct)
   mycol.insert_one(res_dct)
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

def gethome():
      print("From Home")
      im = Image.open("static/images/out.png")
      data = BytesIO()
      im.save(data, "JPEG")
      encoded_img_data = base64.b64encode(data.getvalue())
      return render_template("new_index.html",img_data=encoded_img_data.decode('utf-8'))

if __name__ == '__main__':
   app.run(debug = True)

