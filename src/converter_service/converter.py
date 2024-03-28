import json, tempfile, os
from bson.objectid import ObjectId
from mongodb import video_fs,mp3_fs,updatstatus
import moviepy.editor

def mp3converter(message):
    message = json.loads(message)
    updatstatus(message,{"video_status":"Running"})

    # empty temp file
    tf = tempfile.NamedTemporaryFile()
    # video content
    out = video_fs.get(ObjectId(message["video_id"]))
    # add video content to temp file
    tf.write(out.read())
    # create audio from temp video file
    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()

    # write audio to the file
    tf_path = tempfile.gettempdir() + f"/{message['video_name']}.mp3"
    audio.write_audiofile(tf_path)

    # save the file to the mongodb database
    f = open(tf_path, "rb")
    data = f.read()
    audio_id = mp3_fs.put(data)
    f.close()
    os.remove(tf_path)

    updatstatus(message,{"audio_id": str(audio_id),"video_status":"Finished"})
