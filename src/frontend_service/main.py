import streamlit as st
import requests
import pytz 
IST = pytz.timezone('Asia/Kolkata')
from datetime import datetime
from dateutil.relativedelta import relativedelta
from config import config

# Define base URL for your Flask backend
LOGIN_BASE_URL = config.SECRET.LOGIN_BASE_URL
GATEWAY_BASE_URL = config.SECRET.GATEWAY_BASE_URL

# Function to login
def login(email,password):
    payload = {'email': email,'password': password}
    response = requests.request("POST", LOGIN_BASE_URL + "/login", headers={}, data=payload, files=[])
    data = response.json()
    if response.ok and "api_token" in data:
        st.success("Login successful!")
        st.session_state.logged_in = True
        st.session_state.token = data["api_token"]
        st.session_state.token_expiry = datetime.now(IST)+relativedelta(minutes=30)
    else:
        st.error("Login failed. Please try again.")

# Function to check if token is expired
def is_token_expired():
    if "token_expiry" in st.session_state:
        return st.session_state.token_expiry < datetime.now(IST)
    return True

# Function to logout
def logout():
    st.session_state.logged_in = False
    st.session_state.token = None
    st.session_state.token_expiry = None

# Function to upload video
def upload_video(file):
    headers = {'auth': st.session_state.token}
    files = {'video': file}
    response = requests.request("POST", url=GATEWAY_BASE_URL+"/upload-video", headers=headers, data={}, files=files)
    if response.ok:
        st.success("Video uploaded successfully!")
    else:
        st.error("Failed to upload video.")

def get_mp3_files():
    headers = {'auth': st.session_state.token}
    response = requests.request("GET", url=GATEWAY_BASE_URL+"/get-user-history", headers=headers, data={}, files={})
    if response.ok:
        return response.json()['data']
    else:
        return []

def donwload_file(video_id):
    payload = {'video_id': video_id}
    headers = {'auth': st.session_state.token}
    response = requests.request("POST", url=GATEWAY_BASE_URL+"/download-audio", headers=headers, data=payload, files={})
    
    if response.ok:
        return response.content
    
# Main Function
def main():
    # Check if user is logged in
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "token" not in st.session_state:
        st.session_state.token = None
    if "token_expiry" not in st.session_state:
        st.session_state.token_expiry = None
    

    # If not logged in, show login form
    if not st.session_state.logged_in or is_token_expired():
        st.title("Video to Audio Converter")
        st.subheader("Login")
        email = st.text_input("email")
        password = st.text_input("Password", type="password")
        st.button("Login", on_click=lambda: login(email, password))

    else:
        # Logged in, show upload and download options
        st.title("Video to Audio Converter")
        menu = st.sidebar.radio("Navigation", ["Upload Video", "Download Audio"])
        st.sidebar.button("Logout", on_click=logout)
        if menu == "Upload Video":
            st.subheader("Upload Video")
            uploaded_file = st.file_uploader("Choose a video file")
            
            if uploaded_file is not None:
                if st.button("Upload"):
                    if st.session_state.logged_in:
                        upload_video(uploaded_file)

        elif menu == "Download Audio":
            st.subheader("Download Audio")
            # Retrieve MP3 files
            # Remove unwanted keys and add download button or disabled button
            all_data = get_mp3_files()
            col1, col2 = st.columns(2)
            for index,row in enumerate(all_data):
                with st.container():
                    with col1:
                        st.button(row["video_name"],"1"+str(index),use_container_width=True,disabled=True)
                    with col2:
                        label = "Download" if row["video_status"]=="Finished" else row["video_status"]
                        st.download_button(
                            label=label,
                            data = donwload_file(row['video_id']),
                            file_name=row['video_name']+".mp3",
                            key = "2"+str(index),
                            use_container_width=True,
                            mime='audio/mp3',
                            disabled= False if row["video_status"]=="Finished" else True
                        )
                        
            if len(all_data) == 0:
                st.error("Sorry no audio to show")
            

if __name__ == "__main__":
    main()