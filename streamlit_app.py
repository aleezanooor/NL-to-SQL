import streamlit as st
import requests
import pandas as pd

# Set page configuration for centered layout
st.set_page_config(page_title="AskDB 💬", layout="centered")

# Title and subtitle
st.title("AskDB 💬")
st.subheader("Talk to your database like it's a friend. Ask your questions below!")

# User input for the question
user_input = st.text_area("Type your question here:", height=150)

# Submit button to send the query
submit = st.button("Submit")

# Interaction with the API once the question is submitted
if submit and user_input:
    with st.spinner("Thinking... 🤖"):
        try:
            # Send the query to the backend (FastAPI endpoint)
            response = requests.post("http://localhost:8000/ask", json={"question": user_input})
            result = response.json()

            # Check if there's an error in the response
            if "error" in result:
                st.error(f"❌ {result['error']}")
            else:
                # Display summary and data if available
                st.markdown("### 🧠 Summary of your query")
                st.markdown(result.get("summary", "No summary available"))

                # Display the result data if it exists
                if result.get("data"):
                    st.markdown("### 📊 Data Results")
                    df = pd.DataFrame(result["data"])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No results found.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

# Optional footer for a friendly touch
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<center><small>Built with 💜 by Aleeza</small></center>", unsafe_allow_html=True)
