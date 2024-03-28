from flask import Flask,request,jsonify
from schema_check import parameterCheck
from flask_cors import CORS
from aes import decrypt,encrypt
from mongodb import queryUserData
from config import config
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz 
IST = pytz.timezone('Asia/Kolkata')
import jwt

app = Flask(__name__)
cors = CORS(app,supports_credentials=True, origins = ['http://localhost:5555'], methods = ['GET', 'POST'])


@app.route("/login", methods=['POST'])
@parameterCheck
def user_login():
    user_email = request.form.get("email")
    try:
        user_password = decrypt(request.form.get("password")).decode("utf-8", "ignore").replace('"', '')
    except Exception as e:
        user_password = request.form.get("password")

    query = queryUserData(user_email,user_password)

    if query:
        payload = {
            "email":encrypt(user_email),
            "exp":datetime.now(IST)+relativedelta(minutes=30)
        }
        key = config.SECRET.APP_JWT_SECRET_KEY
        encoded = jwt.encode(payload, key, algorithm="HS256") 
        return jsonify({"api_token":encoded , "expiry":str(datetime.now(IST)+relativedelta(minutes=30)),"success":True}) 
    else:
        return jsonify({"message":"incorrect credential", "success":False}), 401
    
if __name__ == '__main__': 
   app.run(host= '0.0.0.0',port=5555,debug=True) 