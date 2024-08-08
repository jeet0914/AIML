import streamlit as st
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.example_selector import LengthBasedExampleSelector

from dotenv import load_dotenv
load_dotenv()

def generateText(query, age_option, tasktype_option):
    
    llm = OpenAI()
    
    # examples for few shot training
    examples = [
        {
            "query": "What is a mobile?",
            "answer": "A mobile is a magical device that fits in your pocket, like a mini-enchanted playground. It has games, videos, and talking pictures, but be careful, it can turn grown-ups into screen-time monsters too!"
        }, {
            "query": "What are your dreams?",
            "answer": "My dreams are like colorful adventures, where I become a superhero and save the day! I dream of giggles, ice cream parties, and having a pet dragon named Sparkles.."
        }, {
            "query": " What are your ambitions?",
            "answer": "I want to be a super funny comedian, spreading laughter everywhere I go! I also want to be a master cookie baker and a professional blanket fort builder. Being mischievous and sweet is just my bonus superpower!"
        }, {
            "query": "What happens when you get sick?",
            "answer": "When I get sick, it's like a sneaky monster visits. I feel tired, sniffly, and need lots of cuddles. But don't worry, with medicine, rest, and love, I bounce back to being a mischievous sweetheart!"
        }, {
            "query": "How much do you love your dad?",
            "answer": "Oh, I love my dad to the moon and back, with sprinkles and unicorns on top! He's my superhero, my partner in silly adventures, and the one who gives the best tickles and hugs!"
        }, {
            "query": "Tell me about your friend?",
            "answer": "My friend is like a sunshine rainbow! We laugh, play, and have magical parties together. They always listen, share their toys, and make me feel special. Friendship is the best adventure!"
        }, {
            "query": "What math means to you?",
            "answer": "Math is like a puzzle game, full of numbers and shapes. It helps me count my toys, build towers, and share treats equally. It's fun and makes my brain sparkle!"
        }, {
            "query": "What is your fear?",
            "answer": "Sometimes I'm scared of thunderstorms and monsters under my bed. But with my teddy bear by my side and lots of cuddles, I feel safe and brave again!"
        }
        ]
    
    
    example_template = """
    Question: {query}
    Response: {answer}
    """
    
    example_prompt = PromptTemplate(input_variables=['query','answer'],
                                   template = example_template)
    
    
    prefix = """You are a {template_ageoption}, and {template_tasktype_option}: 
    Here are some examples: 
    """

    suffix = """
    Question: {template_userInput}
    Response: 
    """
    
    
    
    example_selector = LengthBasedExampleSelector(
        examples=examples,
        example_prompt=example_prompt,
        max_length=200
    )
    
    
    few_shots_prompt = FewShotPromptTemplate(example_selector=example_selector,
                                     example_prompt=example_prompt,
                                     suffix=suffix,
                                     prefix=prefix,
                                     input_variables=['template_userInput','template_ageoption','template_tasktype_option'],
                                             example_separator="\n")
    
    
    few_shots = few_shots_prompt.format(template_userInput = query,
                                       template_ageoption = age_option,
                                       template_tasktype_option = tasktype_option)
    
    response = llm.invoke(few_shots)
    
    return response    



st.set_page_config(page_title="Marketing App",
                   page_icon=":robot:")

st.header("Your Personalized Marketing Campaign")

query = st.text_area('Whats your question ?',height=275)

age_option = st.selectbox('For which age group', 
                          ('Kids','Senior Citizen', 'Adult'),
                          key=1)


tasktype_option = st.selectbox(
    'Please select the action to be performed?',
    ('Write a sales copy', 'Create a tweet', 'Write a product description'),key=2)

submit = st.button('Generate')

if submit:

    st.write(generateText(query,age_option,tasktype_option))