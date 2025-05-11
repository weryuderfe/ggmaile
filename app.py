import streamlit as st
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os
import pickle

st.set_page_config(page_title="Login Gmail OAuth", layout="centered")

st.title("📧 Login Gmail (OAuth 2.0) via Streamlit Cloud")

CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TOKEN_FILE = 'token.pkl'

def save_token(creds):
    with open(TOKEN_FILE, 'wb') as token:
        pickle.dump(creds, token)

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            return pickle.load(token)
    return None

creds = load_token()

if not creds or not creds.valid:
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob'  # Khusus untuk command-line atau manual input
    )

    auth_url, _ = flow.authorization_url(prompt='consent')

    st.warning("🔐 Anda belum login. Silakan login dengan langkah berikut:")
    st.markdown(f"[Klik di sini untuk login Google]({auth_url})")

    code = st.text_input("📥 Masukkan kode auth dari Google di sini:")
    if code:
        try:
            flow.fetch_token(code=code)
            creds = flow.credentials
            save_token(creds)
            st.success("✅ Login berhasil! Jalankan ulang aplikasi.")
        except Exception as e:
            st.error(f"❌ Gagal login: {e}")
else:
    st.success("✅ Anda sudah login.")
    service = build('gmail', 'v1', credentials=creds)
    profile = service.users().getProfile(userId='me').execute()
    st.write("📬 Email Anda:", profile['emailAddress'])
