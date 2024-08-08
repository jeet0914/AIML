import openai
from langchain_community.llms import OpenAI
from pypdf import PdfReader
from langchain.schema import Document
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from pinecone import Pinecone as PineconeClient
from langchain_community.vectorstores import Pinecone
import time
from langchain.chains.summarize import load_summarize_chain

def get_text(pdf):

    text = ""
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text




def create_docs(pdf_list, unique_id):
    docs = []
    for filename in pdf_list:
        chunks = get_text(filename)
        docs.append(Document(
            page_content=chunks,
            metadata = {"name": filename.name,"id":filename.file_id,
                        "type=":filename.type,"size":filename.size,"unique_id":unique_id},
        ))
    return docs


def create_embeddings():
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return embeddings


def push_to_pinecone(pinecone_api_key, pinecone_environment, pinecone_index_name,embeddings, docs ):
    PineconeClient(api_key=pinecone_api_key, environment = pinecone_environment) 
    index_name = pinecone_index_name
    Pinecone.from_documents(docs, embeddings, index_name=pinecone_index_name)


def pull_index_from_pinecone(pinecone_api_key, pinecone_environment, pinecone_index_name,embeddings):
    print("20secs delay...")
    time.sleep(20)
    PineconeClient(api_key=pinecone_api_key, environment=pinecone_environment)
    index_name = pinecone_index_name
    index = Pinecone.from_existing_index(index_name, embeddings)
    return index



def get_similar_docs(query,k,pinecone_apikey,pinecone_environment,pinecone_index_name,embeddings,unique_id):

    PineconeClient(api_key=pinecone_apikey, environment=pinecone_environment)


    index_name = pinecone_index_name

    index = pull_index_from_pinecone(pinecone_apikey,pinecone_environment,index_name,embeddings)
    similar_docs = index.similarity_search_with_score(query, int(k),{"unique_id":unique_id})
    #print(similar_docs)
    return similar_docs

def get_summary(text):
    llm = OpenAI(temperature = 0)
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run([text])
    return summary
















