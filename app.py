import streamlit as st
import streamlit_authenticator as stauth
import numpy
import cv2
from PIL import Image
import pandas as pd
from datetime import datetime
file_dict = {'Scanned By': []}
def qrcode(name):
    # Initialize session state
    if "captured_image" not in st.session_state:
        st.session_state["captured_image"] = None

    # Define app layout
    st.subheader("QR Code Scanning Of files")
    col1, col2, col3 = st.columns(3)

    # Capture QR code image using camera input
    with col1:
        capture_qr_code = st.camera_input(
            "Scan Your QR Code Here",
            key="cameraQRCode",
            help="Place the QR Code correctly the camera for better results"
        )
        if capture_qr_code:
            st.session_state["captured_image"] = capture_qr_code

    # Display input QR code image
    with col2:
        st.markdown("The Input QR Code")
        if st.session_state["captured_image"]:
            st.image(st.session_state["captured_image"])

    # Decode QR code and display output
    with col3:
        st.markdown("The Output of QR Code")
        if st.session_state["captured_image"]:
            img = Image.open(st.session_state["captured_image"])
            opencvImage = numpy.array(img)
            qrCodeDetector = cv2.QRCodeDetector()
            data = qrCodeDetector.detectAndDecode(opencvImage)
            output=str(data[0])
            st.write(output)
            def scan_file(name):
                file_dict['Scanned By'].append(st.session_state["name"] )
                st.write((f"{name} has scanned the file at {datetime.now()}."))
                st.success('Successfully Updated Data')
                # Define a function to scan the file and update the dictionary
            st.write(f"{name}, press the button to scan the file.") 
            button=st.button("Click if Scanned")
            if button:  
                scan_file(name)
            s = output.replace("{" ,"")
            finalstring = s.replace("}" , "")
            #Splitting the string based on , we get key value pairs
            list = finalstring.split(",")
            dictionary ={}
            for i in list:
            #Get Key Value pairs separately to store in dictionary
                keyvalue = i.split(":")
            #Replacing the single quotes in the leading.
                m= keyvalue[0].strip('\'')
                m = m.replace("\"", "")
                dictionary[m] = keyvalue[1].strip('"\'')
                dict2={'User':st.session_state["name"], 'Status': "Received",'Date-Time': datetime.now()}
                dictionary |= dict2
                dictionary |= file_dict
                df=pd.read_excel('datasheet.xlsx')
                df= df.append(dictionary,ignore_index=True)
                df.to_excel("datasheet.xlsx", index=False)  


def login():
    names = ['Chairman TL','Dean Feece','Director Finance','Coordinate of Exams','ICPC MUET','MIS MUET','Vice Chancellor']
    usernames = ['chairman_tl','dean_feece','director_finance','coordinator_exams','icpc_muet','mis_muet','vc_muet']
    passwords = ['abcd','efgh','mnop','ijkl','uvwx','qrst','muet']
    hashed_passwords = stauth.Hasher(passwords).generate()
    authenticator = stauth.Authenticate(names,usernames,hashed_passwords,'some_cookie_name','some_signature_key',cookie_expiry_days=30)
    name,authentication_status, username = authenticator.login('Login', 'main')
        
    if st.session_state["authentication_status"]:
        test=authenticator.logout('Logout', 'main')
        st.write(f'Welcome *{st.session_state["name"]}*')
        st.title('FILE TRACKING AND WORKFLOW MANAGEMENT')
        qrcode(name)
    elif st.session_state["authentication_status"] == False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] == None:
        st.warning('Please enter your username and password')

def main():
    st.set_page_config(page_title="CS Project APP",page_icon="🗃️", layout="wide")
    login()

if __name__ == "__main__":
    
    main()
            