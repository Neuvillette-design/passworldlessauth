import streamlit as st
import requests

API_URL = "https://805kgd8btk.execute-api.ap-south-1.amazonaws.com/prod"

st.set_page_config(page_title="Secure Login")
st.title("LogIn")

if 'otp_sent' not in st.session_state:
    st.session_state.otp_sent = False

email = st.text_input("Enter your registered work email", placeholder="name@example.com")

if not st.session_state.otp_sent:
    if st.button("Verify & Send OTP"):
        with st.spinner("Checking"):
            response = requests.post(f"{API_URL}/request", json={"email": email})
            
            if response.status_code == 200:
                st.session_state.otp_sent = True
                st.success("User found in Cognito! OTP sent to your email.")
                st.rerun() 
            elif response.status_code == 404:
                st.error("Access Denied: You are not in our Cognito User Pool.")
            elif response.status_code == 400:
                st.error("Your Account has been blocked.")
            else:
                st.error("Something went wrong.")

else:
    st.info(f"OTP sent to {email}")
    otp_code = st.text_input("Enter the 6-digit code", max_chars=6)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Login"):
            with st.spinner("Verifying"):
                res = requests.post(f"{API_URL}/verify", json={"email": email, "otp": otp_code})
                
                if res.status_code == 200:
                    st.session_state.logged_in = True
                    st.success("Welcome! You are logged in.")
                else:
                    st.error("Invalid or expired OTP code.")
                
        if st.session_state.get('logged_in'):
            st.subheader("You have been rick rolled.")
    
            video_url = "https://youtu.be/dQw4w9WgXcQ?si=F8lTZ7NKGtvyaFfb"
    
            st.video(
                video_url, 
                autoplay=True,
                muted=True,     
                loop=False      
            )
    
    with col2:
        if st.button("Back / Reset"):
            st.session_state.otp_sent = False

            st.rerun()
