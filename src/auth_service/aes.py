import base64 
from config import config
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

#CBC with Fix IV
def decrypt(enc):
    key = config.SECRET.APP_AES_KEY #16 char for AES128

    #FIX IV
    iv =  'globalaesvectors'.encode('utf-8') #16 char for AES128
    
    enc = base64.b64decode(enc)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc),16)

def encrypt(data):
    key = config.SECRET.APP_AES_KEY # 16 char for AES128

    # FIX IV
    iv = 'globalaesvectors'.encode('utf-8')  # 16 char for AES128

    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    padded_data = pad(data.encode('utf-8'), 16)
    encrypted_data = cipher.encrypt(padded_data)

    return base64.b64encode(encrypted_data).decode('utf-8')