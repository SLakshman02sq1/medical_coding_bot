import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = None

user_input = st.text_input("Ask questions related to medical coding")

if st.button("Send") and user_input:
    payload = {
        "message": user_input,
        "session_id": st.session_state.session_id
    }

    try:
        resp = requests.post(API_URL, json=payload)
        resp.raise_for_status()
        response = resp.json()

        # Update session_id safely
        st.session_state.session_id = response.get("session_id", None)

        # Display bot reply
        st.write("Bot:", response.get("message", "[No message returned]"))

    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
