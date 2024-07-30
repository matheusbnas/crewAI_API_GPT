import streamlit as st
from crewai import Agent, Task, Crew, Process

# Configuração do agente de marketing
marketing_assistant = Agent(
    role='Assistente de Marketing',
    goal='Responder e-mails para influencers e marcas de maneira profissional e personalizada. Garanta que as respostas sejam claras, concisas e abordem todas as preocupações mencionadas no e-mail recebido.',
    backstory='Você é especializado em marketing digital e comunicação, com habilidades em criação de conteúdo e relacionamento com clientes. Você tem uma compreensão profunda das tendências de marketing e sabe como se comunicar efetivamente com diferentes públicos.',
    verbose=True,
    memory=True,
)

# Configuração da tarefa de resposta de e-mails
def create_email_response_task(email_content, recipient_type):
    description = f'''
    Responder e-mails recebidos de {recipient_type}s. Use um tom profissional e personalizado, abordando as principais preocupações e fornecendo informações relevantes sobre nossa marca ou campanha.
    
    Exemplo de E-mail Recebido:
    "Olá, estamos interessados em colaborar com sua marca para uma campanha de mídia social. Gostaríamos de saber mais detalhes sobre suas ofertas e como podemos trabalhar juntos."

    Exemplo de Resposta Esperada:
    "Olá [Nome],
    Obrigado por entrar em contato. Ficamos muito felizes com seu interesse em colaborar conosco. Nossas ofertas incluem [detalhes das ofertas]. Adoraríamos discutir mais detalhes sobre como podemos trabalhar juntos para uma campanha bem-sucedida. Por favor, me avise se você estiver disponível para uma reunião esta semana.
    Atenciosamente,
    [Seu Nome]"
    '''
    task = Task(
        description=description,
        expected_output='Uma resposta por e-mail bem estruturada e profissional, seguindo o exemplo fornecido.',
        agent=marketing_assistant,
        async_execution=False,
    )
    return task

# Função para processar o e-mail e gerar a resposta
def process_email(email_content, recipient_type):
    email_response_task = create_email_response_task(email_content, recipient_type)
    crew = Crew(
        agents=[marketing_assistant],
        tasks=[email_response_task],
        process=Process.sequential
    )
    result = crew.kickoff(inputs={'email_content': email_content})
    return result

# Interface do Streamlit
st.title("Assistente de Marketing para Responder E-mails")

# Seleção do tipo de destinatário
recipient_type = st.selectbox("Tipo de Destinatário", ["Influencer", "Marca"])

email_content = st.text_area("E-mail Recebido", height=300)
if st.button("Gerar Resposta"):
    if email_content:
        response = process_email(email_content, recipient_type)
        st.text_area("Resposta Gerada", response, height=300)
    else:
        st.warning("Por favor, insira o conteúdo do e-mail recebido.")
