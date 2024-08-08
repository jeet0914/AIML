import streamlit as st
from utils import generate_script


if 'API_Key' not in st.session_state:
    st.session_state['API_Key'] = ""

st.title('Generate YouTube Script')


st.sidebar.title('API_Key')
st.session_state['API_Key']=st.sidebar.text_input('What is your API Key', type='password')
st.sidebar.image('./Youtube.jpg', width=300,use_column_width=True)


prompt = st.text_input('Enter your prompt', key='prompt')
video_length = st.text_input('Enter the expected video length', key='video_length')
creativity = st.slider('What should be the creativity', key='creativity')

submit = st.button('Generate Script for me')

if submit:
    if st.session_state['API_Key']:
        
        
        # lets generate the script
        title, script, search_result = generate_script(prompt, video_length, creativity, st.session_state['API_Key'])

        st.success('Hope you like the script')


        # Display title
        st.subheader('TITLE')
        st.write(title)


        #Display Script
        st.subheader('SCRIPT')
        st.write(script)


        #Display search result

        st.subheader('Checkout the search result from DuckDuckGo')
        with st.expander('Show me'):
            st.info(search_result)
    
    else:
        st.error('Oops!! Pl provide API key')











