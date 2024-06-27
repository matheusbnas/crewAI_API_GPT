from dotenv import load_dotenv, find_dotenv
import os
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_groq import ChatGroq


load_dotenv(find_dotenv())


api_key = os.getenv('GROQ_API_KEY')
model_name = os.getenv('MODEL', 'mixtral-8x7b-32768')


default_llm = ChatGroq(
groq_api_key=api_key,
model=model_name
)


def search_recipes(query):

    search_tool = DuckDuckGoSearchRun()

    results = search_tool.run(query=query)

    recipes = [result['title'] for result in results if 'recipe' in result['title'].lower()]

    return recipes[:3]


researcher = Agent(
    role='Researcher',
    goal='Search for homemade sweet recipes.',
    verbose=True,
    memory=True,
    backstory=(
        "As a dedicated researcher, you thrive on discovering new and exciting "
        "recipes that can be made at home. Your mission is to explore various sources "
        "to find the most delicious, easy-to-make sweet recipes for home cooks."
    ),
    tool=[search_recipes],
    llm=default_llm,
    allow_delegation=False
)


writer = Agent(
    role='Writer',
    goal='Generate a list with a top 3 tasty homemade sweet recipes.',
    verbose=True,
    memory=True,
    backstory=(
        "You are a skilled writer with a passion for culinary arts. Your task is to "
        "compile and narrate the top three sweet recipes found by your research team, "
        "creating an engaging list in Portuguese for an audience eager to cook at home."
    ),
    allow_delegation=True
)


research_task = Task(
    description=(
        "Explore various online platforms and databases to find delicious, "
        "easy-to-make sweet recipes suitable for home cooking. Identify a wide range "
        "of recipes, focusing on simplicity and popularity."
    ),
    expected_output='A list of at least 3 potential sweet recipes, each accompanied by its source URL.',
    agent=researcher
)

write_task = Task(
    description=(
        "From the recipes provided by the research team, select the top three based "
        "on taste, ease of preparation, and uniqueness. write a short article with up to 300 tokens "
        "in Portuguese, listing these recipes with brief descriptions and why they "
        "are recommended for home cooks."
    ),
    expected_output=(
        "An engaging article in Português PT-BR featuring the top three sweet recipes, "
        "formatted as a blog post with headings, bullet points, and a friendly tone."
    ),
    agent=writer
)



crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential  # Execução sequencial para garantir que a escrita comece após a pesquisa
)



result = crew.kickoff(inputs={'query': 'sweet recipes for home'})





