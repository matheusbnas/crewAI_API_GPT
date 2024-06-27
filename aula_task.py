from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_groq import ChatGroq
from crewai_tools import ScrapeWebsiteTool
from dotenv import load_dotenv

import os

load_dotenv()

api_key = os.getenv('GROQ_API_KEY')
model_name = os.getenv('MODEL', 'mixtral-8x7b-32768')
default_llm = ChatGroq(groq_api_key=api_key, model=model_name)
search_tool = ScrapeWebsiteTool()

writer = Agent(
    role='Writer about {topic}',
    goal='Escrever artigos envolventes sobre {topic}',
    tool=[search_tool],
    llm=default_llm,
    backstory="você é um ótimo escrito para descrever adequadamente qualquer assunto fornecido de forma clara e objetiva"
)

write_task = Task(
    description=(
        "Escreva um artigo detalhado sobre as tendências atuais em inteligência artificial."
        "O artigo deve ser informativo e cativante, visando a clareza e acessibilidade para leitores não especializados."
    ),
    expected_output='Um artigo de 500 palavras em formato csv em português.',
    agent=writer,
    output_file='artigo-sobre-IA.csv'
)

crew = Crew(agents=[writer],
            tasks=[write_task]
            )

result = crew.kickoff(inputs={'topic': 'Inteligência Artificial'})

print(result)
