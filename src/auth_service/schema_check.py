from flask import jsonify, request
from functools import wraps
import re

def validate_email(email):
    # Regular expression pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Using re.match() to match the pattern against the email address
    if re.match(pattern, email):
        return True
    else:
        return False

ALLOWED_EXTENSIONS = set(['mp4'])
def allowed_file(filename):
	return ('.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS) and (filename.count(".")==1)

def parameterCheck(f):
    @wraps(f)
    def wrapped_parameterCheck(*args, **kwargs):
        if request.method in ['GET','POST']:
            if "login" in request.path:
                email = request.form.get("email")
                password = request.form.get("password")
                if not email or not password:
                    if not email and not password:
                        return jsonify({"message":"email and password is missing", "success":False}), 400
                    if not email:
                        return jsonify({"message":"email is missing", "success":False}), 400 
                    if not password:
                        return jsonify({"message":"password is missing", "success":False}), 400
                if not validate_email(email):
                   return  jsonify({"message":"invalid email", "success":False}), 400
            elif "upload-video" in request.path:
                if 'video' not in request.files:
                    return jsonify({'message' : 'No file part in the request', "success":False}), 400
                file = request.files['video']
                if file.filename == '':
                    return jsonify({'message' : 'No file selected for uploading', "success":False}), 400
                if not allowed_file(file.filename):
                    return jsonify({'message' : 'Allowed file types are mp4 only', "success":False}), 400
            else:
                pass

        return f(*args, **kwargs)
    return wrapped_parameterCheck