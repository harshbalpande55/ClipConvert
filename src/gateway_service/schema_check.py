from flask import jsonify, request
from functools import wraps
import re

ALLOWED_EXTENSIONS = set(['mp4'])
def allowed_file(filename):
	return ('.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS) and (filename.count(".")==1)

def parameterCheck(f):
    @wraps(f)
    def wrapped_parameterCheck(*args, **kwargs):
        if request.method in ['GET','POST']:
            if "upload-video" in request.path:
                if 'video' not in request.files:
                    return jsonify({'message' : 'No file part in the request', "success":False}), 400
                file = request.files['video']
                if file.filename == '':
                    return jsonify({'message' : 'No file selected for uploading', "success":False}), 400
                if not allowed_file(file.filename):
                    return jsonify({'message' : 'Allowed file types are mp4 only', "success":False}), 400
            if "download-video" in request.path:
                video_id = request.form.get("video_id")
                if not video_id:
                    return jsonify({'message' : 'Video id Missing', "success":False}), 400
            if "poll-video-status" in request.path:
                video_id = request.form.get("video_id")
                if not video_id:
                    return jsonify({'message' : 'Video id Missing', "success":False}), 400
            else:
                pass

        return f(*args, **kwargs)
    return wrapped_parameterCheck