from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.chains import LLMChain


def generate_script(prompt, video_length, creativity, api_key):

    

      # Template for generating 'Title'
    title_template = PromptTemplate(
        input_variables = ['subject'], 
        template='Please come up with a title for a YouTube video on the  {subject}.'
        )

    # Template for generating 'Video Script' using search engine
    script_template = PromptTemplate(
        input_variables = ['title', 'DuckDuckGo_Search','duration'], 
        template='Create a script for a YouTube video based on this title for me. TITLE: {title} of duration: {duration} minutes using this search data {DuckDuckGo_Search} '
    )
    llm = ChatOpenAI(temperature=creativity, openai_api_key=api_key)
    
    title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True )
    script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True)

    search_engine = DuckDuckGoSearchRun()

    title = title_chain.invoke(prompt)
    search_result = search_engine.run(prompt)

    script = script_chain.run(title=title, DuckDuckGo_Search=search_result, duration = video_length)

    return title, script, search_result


