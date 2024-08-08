from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import OpenAI


load_dotenv()

def get_respose(data, query):

    df = pd.DataFrame(data)
    llm = OpenAI()

    agent = create_pandas_dataframe_agent(llm=llm, df=df, verbose=True)

    return agent.invoke(query)