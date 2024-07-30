from crewai import Agent, Task, Crew
#from langchain.llms import OpenAI
from langchain_openai import OpenAI
from langchain.tools import DuckDuckGoSearchRun
from pydantic import BaseModel, Field
from typing import List

class Brand(BaseModel):
    name: str = Field(description="Nome da marca")
    industry: str = Field(description="Setor da indústria")
    target_audience: str = Field(description="Público-alvo da marca")
    values: List[str] = Field(description="Valores da marca")

class Influencer(BaseModel):
    name: str = Field(description="Nome do influencer")
    platform: str = Field(description="Plataforma principal do influencer")
    followers: int = Field(description="Número de seguidores")
    niche: str = Field(description="Nicho do influencer")
    engagement_rate: float = Field(description="Taxa de engajamento")

class Partnership(BaseModel):
    brand: Brand
    influencer: Influencer
    proposal: str = Field(description="Proposta de parceria")
    approach_strategy: str = Field(description="Estratégia de abordagem")

# Ferramentas auxiliares
search_tool = DuckDuckGoSearchRun()

# Agentes
brand_researcher = Agent(
    name="Pesquisador de Marcas",
    role="Especialista em identificar e analisar marcas potenciais para parcerias",
    goal="Encontrar marcas relevantes e analisar sua adequação para parcerias",
    backstory="Analista de mercado com vasta experiência em pesquisa de marcas e tendências de consumo",
    tools=[search_tool],
    llm=OpenAI(temperature=0.7)
)

influencer_researcher = Agent(
    name="Pesquisador de Influencers",
    role="Especialista em identificar e analisar influencers para parcerias",
    goal="Encontrar influencers relevantes e analisar sua adequação para parcerias",
    backstory="Especialista em marketing de influência com profundo conhecimento das principais plataformas sociais",
    tools=[search_tool],
    llm=OpenAI(temperature=0.7)
)

partnership_strategist = Agent(
    name="Estrategista de Parcerias",
    role="Especialista em desenvolver estratégias de parceria entre marcas e influencers",
    goal="Criar propostas de parceria personalizadas e estratégias de abordagem eficazes",
    backstory="Consultor experiente em marketing de influência e negociação de parcerias estratégicas",
    llm=OpenAI(temperature=0.5)
)

# Tarefas
task1 = Task(
    description="Pesquisar e identificar 5 marcas potenciais para parcerias no setor de tecnologia",
    agent=brand_researcher
)

task2 = Task(
    description="Pesquisar e identificar 10 influencers relevantes no nicho de tecnologia com mais de 100k seguidores",
    agent=influencer_researcher
)

task3 = Task(
    description="Analisar a compatibilidade entre as marcas e influencers identificados",
    agent=partnership_strategist
)

task4 = Task(
    description="Desenvolver propostas de parceria personalizadas para as 3 combinações mais promissoras",
    agent=partnership_strategist
)

task5 = Task(
    description="Criar uma estratégia de abordagem detalhada para cada parceria proposta",
    agent=partnership_strategist
)

# Criação da equipe
partnership_crew = Crew(
    agents=[brand_researcher, influencer_researcher, partnership_strategist],
    tasks=[task1, task2, task3, task4, task5],
    verbose=True
)

# Execução do processo
result = partnership_crew.kickoff()

print(result)

# Processamento e estruturação dos resultados
def process_results(result: str) -> List[Partnership]:
    # Esta função deve processar o resultado string e converter em objetos Partnership
    # Implementação depende do formato exato do resultado retornado pelo Crew
    pass

partnerships = process_results(result)

# Exemplo de uso dos resultados
for partnership in partnerships:
    print(f"Parceria proposta entre {partnership.brand.name} e {partnership.influencer.name}")
    print(f"Proposta: {partnership.proposal}")
    print(f"Estratégia de abordagem: {partnership.approach_strategy}")
    print("---")