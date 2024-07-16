from dotenv import load_dotenv, find_dotenv
from crewai import Agent, Task, Crew, Process

import os

from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv(find_dotenv())

api_key = os.getenv('GROQ_API_KEY')
model_name = os.getenv('MODEL', 'mixtral-8x7b-32768')

default_llm = ChatGroq(
    groq_api_key=api_key,
    model=model_name
)


def search_viagens(query):
    search_tool = DuckDuckGoSearchRun()

    results = search_tool.run(query=query)

    recipes = [result['title'] for result in results if 'recipe' in result['title'].lower()]

    return recipes[:3]


consultor_viagens = Agent(

    role="Consultor de viagens",
    goal="Consultor responsável de mostrar lugares diponíveis para viajar pesquisando na internet",
    verbose=True,  # Retornar no terminal
    tool=[search_viagens],
    allow_delegation=False,
    backstory="Você deve consultar os melhores lugares no mundo para viajar."
              "e responder as dúvidas sobre destinos pelo mundo como custos, hotelaria, comida e outros fatores importantes sobre viagens.",
    llm=default_llm
)

viagem_task = Task(
    description="Você deve pesquisar no duckduckgo os melhores luagres para viajar no mundo e listar um top rank com 5 lugares paradisíacos",
    agent=consultor_viagens,
    expected_output="Listar com top rank com 5 luagres paradisíacos para viagens."
)

teste = (Crew(agents=[consultor_viagens],
              tasks=[viagem_task],
              process=Process.sequential).kickoff(inputs={'query': 'Listar em português pt-BR os 5 lugares paradisíacos no Brasil'}) # kickoff é um método que roda o projeto
         )

print(teste)
