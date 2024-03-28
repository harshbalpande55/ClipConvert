from flask import Flask,request,jsonify,g,send_file
from flask_cors import CORS
from aes import encrypt,decrypt
from bson.objectid import ObjectId
from schema_check import parameterCheck
from mongodb import video_fs,mp3_fs,insertstatus,querystatus,getuserhistory
from config import config
import jwt,json,pika

app = Flask(__name__)
cors = CORS(app,supports_credentials=True, origins = ['http://localhost:6666'], methods = ['GET', 'POST'])


@app.before_request
def before_request():
   token = request.headers.get("auth")

   if not token:
      return jsonify({"message": "Missing Authorization header", "success": False}), 401
   else:
      token = token.split()[-1]
      try:
         payload = jwt.decode(token,config.SECRET.APP_JWT_SECRET_KEY, algorithms=["HS256"])
         g.email = decrypt(payload['email']).decode("utf-8", "ignore").replace('"', '')
         
      except jwt.ExpiredSignatureError:
         return jsonify({"message": "Token has expired", "success": False}), 403
      except Exception as e:
         return jsonify({"message": "Invalid Token", "success": False}), 403

@app.route('/upload-video', methods=['POST'])
@parameterCheck
def upload_video():
   video_file = request.files['video']

   ## upload the data to mongodb using GridFS
   video_id = video_fs.put(video_file)

   ##Publish to the video queue
   message = {
        "video_id": str(video_id),
        "audio_id": None,
        "video_name":video_file.filename.split(".mp4")[0],
        "email": g.email,
        "video_status":"Processing"
    }

   try:
      connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
      channel = connection.channel()
      channel.basic_publish(
            exchange="",
            routing_key="video-queue",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
      ##insert the status table
      insertstatus(message)
      
      return jsonify({'video_id':str(video_id) ,'message':"Video uploaded successfully", 'success':True}), 200
   except Exception as err:
      print(err)
      video_fs.delete(video_id)
      return jsonify({'message':"Error Occured", 'success':False}), 500 

@app.route("/get-user-history", methods=['GET'])
@parameterCheck
def get_user_history():
   status_data = getuserhistory({"email": g.email})
   data = []
   for status_dict in status_data:
      status_dict['_id'] = str(status_dict['_id'])
      data.append(status_dict)
   
   return jsonify({'data':data, 'success':True}), 200

@app.route('/download-audio', methods=['POST'])
@parameterCheck
def download_audio():
   status_data = querystatus({"video_id": request.form.get("video_id"), "email": g.email})
   try:
      if status_data['video_status'] =="Finished":
         out = mp3_fs.get(ObjectId(status_data['audio_id']))
         return send_file(out, download_name=f"{status_data['video_name']}.mp3")
      else:
         return jsonify({"message": "Audio file is not generated yet", "success":False}), 202
   except Exception as err:
      print(err)
      return jsonify({'message':"Error Occured", 'success':False}), 500 

@app.route('/poll-video-status', methods=['POST'])
@parameterCheck
def poll_video_status():
   status_data = querystatus({"video_id": request.form.get("video_id"), "email": g.email})
   if status_data:
      video_status = status_data['video_status']
      if video_status == "Processing":
            return jsonify({"message": "Data is ready and waiting in queue for processing", "success":False}), 202
      elif video_status =="Running":
            return jsonify({"message": "Data is getting processed", "success":False}), 202
      elif video_status =="Finished":
            return jsonify({"message": "Data is ready to consume", "success":True}), 200
      elif video_status =="Error":
            return jsonify({"message": "Found error while processing this data", "success":False}), 205
      else:
            return jsonify({"success":False}), 202
   else:
      return jsonify({"message": "Invalid video_id", "success":False}), 404
    

if __name__ == '__main__': 
   app.run(host= '0.0.0.0',port=6666,debug=True) 