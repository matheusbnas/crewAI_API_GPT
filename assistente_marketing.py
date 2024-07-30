import os
import openai
import requests
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

#API ONLINE
os.environ["OPENAI_API_KEY"]


# Definindo o agente de marketing
marketing_assistant = Agent(
    role='Assistente de Marketing',
    goal='Responder e-mails para influencers e marcas de maneira profissional e personalizada.',
    backstory='Você é especializado em marketing digital e comunicação, com habilidades em criação de conteúdo e relacionamento com clientes.',
    verbose=True,
    memory=True,
)

# Definindo a tarefa de resposta de e-mails
email_response_task = Task(
    description='Responder e-mails recebidos de influencers e marcas. Utilize um tom profissional e personalizado, abordando as principais preocupações e fornecendo informações relevantes sobre nossa marca ou campanha.',
    expected_output='Uma resposta por e-mail bem estruturada e profissional.',
    agent=marketing_assistant,
    async_execution=False,
)

# Criando a equipe e iniciando o processo
crew = Crew(
    agents=[marketing_assistant],
    tasks=[email_response_task],
    process=Process.sequential
)

# Iniciando o processo
result = crew.kickoff()
print(result)
