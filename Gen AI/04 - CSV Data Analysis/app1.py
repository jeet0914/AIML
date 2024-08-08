import streamlit as st
from dotenv import load_dotenv
from utils1 import get_respose

load_dotenv()


st.header("Ask you file ?")

data = st.file_uploader("Upload CSV")

query = st.text_area('Ask you question here?')
button = st.button("Find response")

if button:
    answer = get_respose(data=data, query=query)
    st.write(answer)