import streamlit as st
import hashlib
from cryptography.fernet import Fernet 


KEY = Fernet.generate_key()
cipher = Fernet(KEY)


stored_data = {} 
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0


def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()


def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()


def decrypt_data(encrypted_text):
    return cipher.decrypt(encrypted_text.encode()).decode()


st.title("🔒 Secure Data Encryption System")


menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Home":
    st.subheader("🏠 Welcome to Secure Data System")
    st.write("Use this app to **securely store and retrieve data** using unique passkeys.")

elif choice == "Store Data":
    st.subheader("📂 Store Data Securely")
    user_data = st.text_area("Enter Data:")
    passkey = st.text_input("Enter Passkey:", type="password")

    if st.button("Encrypt & Save"):
        if user_data and passkey:
            hashed_passkey = hash_passkey(passkey)
            encrypted_text = encrypt_data(user_data)
            stored_data[encrypted_text] = {"encrypted_text": encrypted_text, "passkey": hashed_passkey}
            st.success("✅ Data stored securely!")
            st.code(f"Your Encrypted Text:\n{encrypted_text}", language="plaintext")
        else:
            st.error("⚠️ Both fields are required!")

elif choice == "Retrieve Data":
    st.subheader("🔍 Retrieve Your Data")
    encrypted_text = st.text_area("Enter Encrypted Data:")
    passkey = st.text_input("Enter Passkey:", type="password")

    if st.button("Decrypt"):
        if encrypted_text and passkey:
            hashed_passkey = hash_passkey(passkey)
            stored_entry = stored_data.get(encrypted_text)

            if stored_entry and stored_entry["passkey"] == hashed_passkey:
                
                decrypted_text = decrypt_data(encrypted_text)
                st.success(f"✅ Decrypted Data: {decrypted_text}")
                st.session_state.failed_attempts = 0
            else:
                st.session_state.failed_attempts += 1
                attempts_left = 3 - st.session_state.failed_attempts
                st.error(f"❌ Incorrect passkey! Attempts remaining: {attempts_left}")

                if st.session_state.failed_attempts >= 3:
                    st.warning("🔒 Too many failed attempts! Redirecting to Login Page...")
                    st.experimental_rerun()
        else:
            st.error("⚠️ Both fields are required!")

elif choice == "Login":
    st.subheader("🔑 Reauthorization Required")
    login_pass = st.text_input("Enter Master Password:", type="password")

    if st.button("Login"):
        if login_pass == "admin123": 
            st.session_state.failed_attempts = 0
            st.success("✅ Reauthorized successfully! Redirecting...")
            st.experimental_rerun()
        else:
            st.error("❌ Incorrect password!")
