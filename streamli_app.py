import streamlit as st
import requests

st.title("AskDB 💬")

user_input = st.text_input("Ask a question:")
if st.button("Submit") and user_input:
    response = requests.post("http://localhost:8000/ask", json={"question": user_input})
    result = response.json()
    st.write(result)

