import streamlit as st
import uuid
from utils import *
from dotenv import load_dotenv

if "unique_id" not in st.session_state:
    st.session_state["unique_id"] =""




def main():

    load_dotenv()

    st.set_page_config(page_title="HR Screening App")
    st.title("HR RESUME SCREENING")
    st.subheader("I can help you in resume screening process")

    job_description = st.text_area("Add the Job Description", key='1')
    document_count = st.text_input("No. of resumes to retreive", key='2')
    #pdf = st.file_uploader("Upload documents here", accept_multiple_files=True, type=['pdf'])
    pdf = st.file_uploader("Upload resumes here, only PDF files allowed", type=["pdf"],accept_multiple_files=True)


    submit = st.button('Help me with Analysis')

    if submit:
        with st.spinner("In progress"):

            st.write("our process")
            
            st.session_state['unique_id'] = uuid.uuid4().hex

            final_docs_list = create_docs(pdf, st.session_state['unique_id'])

            st.write("Documents Uploaded: " + str(len(final_docs_list)))


            embeddings = create_embeddings()

            push_to_pinecone("ENTER YOUR KEY","us-east-1","hrresume",
                             embeddings,final_docs_list) 
            
            relevant_docs = get_similar_docs(job_description,3,"ENTER YOUR KEY","us-east-1","hrresume",
                             embeddings,st.session_state['unique_id'])
            

            
            st.write(":heavy_minus_sign:" * 30)

            st.write(len(relevant_docs))

            for item in range(len(relevant_docs)):

                st.subheader("👉 "+str(item+1))
                st.write("**File** : "+ relevant_docs[item][0].metadata['name'])

                with st.expander("Show me:"):
                    st.info("**Match Score** : "+str(relevant_docs[item][1]))

                    summary = get_summary(relevant_docs[item][0])
                    st.write("**Summary**  :  "+summary)
        st.success("Hope I was able to save your time❤️")













if __name__=="__main__":
    main()