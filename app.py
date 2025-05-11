import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import pickle

st.set_page_config(page_title="Login Gmail", layout="centered")

st.title("📧 Login Gmail dengan OAuth 2.0")

CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def save_token(creds):
    with open('token.pkl', 'wb') as token_file:
        pickle.dump(creds, token_file)

def load_token():
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token_file:
            return pickle.load(token_file)
    return None

creds = load_token()

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        save_token(creds)
    else:
        if st.button("🔐 Login via Gmail"):
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=8501)
            save_token(creds)
            st.experimental_rerun()
else:
    st.success("✅ Login berhasil!")
    service = build('gmail', 'v1', credentials=creds)
    profile = service.users().getProfile(userId='me').execute()
    st.write("📬 Email Anda:", profile['emailAddress'])
