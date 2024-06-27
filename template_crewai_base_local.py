from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv, find_dotenv
from langchain.tools import tool
import os
import openai
import requests
from langchain_openai import ChatOpenAI

load_dotenv(find_dotenv())

#API ONLINE
#os.environ["OPENAI_API_KEY"]


#API LOCAL
api_key = os.getenv('OPENAI_API_KEY', 'NA')
api_base_url = os.getenv('OPENAI_API_BASE_URL', 'http://localhost:1234/v1/')
model_name = os.getenv('MODEL_NAME', 'NA')


default_llm = ChatOpenAI(
openai_api_base=api_base_url,
openai_api_key=api_key,
model_name=model_name
)


gentle_responder = Agent(
    role='Atendente Cortês',
    goal='Responder com gentileza a uma saudação',
    verbose=True,  # Habilitar modo verboso para mostrar mais detalhes durante a execução
    backstory=(
        "Você é um assistente sempre pronto para oferecer uma resposta amigável e cortês."
        " Com uma atitude positiva, você valoriza a cordialidade e o respeito nas interações."
    ),
    allow_delegation=False,
    llm=default_llm
)


respond_task = Task(
    description=(
        "Responder a uma saudação de entrada com uma frase gentil."
    ),
    expected_output='Uma frase de gentileza como resposta.',
    agent=gentle_responder
)


# Criando a equipe com apenas nosso agente
gentle_crew = Crew(
    agents=[gentle_responder],
    tasks=[respond_task]
)

result = gentle_crew.kickoff()