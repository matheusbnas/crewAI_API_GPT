import streamlit as st
from crewai import Agent, Task, Crew
from langchain_openai import OpenAI
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuração da página Streamlit
st.set_page_config(page_title="Agente de Captação de Parcerias", layout="wide")
st.title("Agente de Captação de Parcerias")

# Inicialização do OpenAI
openai_api_key = st.sidebar.text_input("Digite sua chave API do OpenAI", type="password")
if not openai_api_key:
    st.warning("Por favor, insira sua chave API do OpenAI para continuar.")
    st.stop()

# Configurações de e-mail
st.sidebar.subheader("Configurações de E-mail")
email_sender = st.sidebar.text_input("Seu e-mail Gmail")
email_password = st.sidebar.text_input("Senha de App do Gmail", type="password", help="Use uma Senha de App gerada nas configurações de segurança do Google")
smtp_server = "smtp.gmail.com"
smtp_port = 587

st.sidebar.markdown("[Como criar uma Senha de App?](https://support.google.com/accounts/answer/185833?hl=pt-BR)")

# Criação dos agentes
partnership_agent = Agent(
    name="Agente de Captação de Parcerias",
    role="Especialista em identificar e propor parcerias entre marcas e influencers",
    goal="Encontrar e propor parcerias mutuamente benéficas",
    backstory="Profissional experiente em marketing de influência e parcerias estratégicas",
    llm=OpenAI(api_key=openai_api_key, temperature=0.7)
)

# Função para gerar proposta de parceria
def generate_partnership_proposal(brand_info, influencer_info):
    task = Task(
        description=f"Analise as informações da marca: {brand_info} e do influencer: {influencer_info}. "
                    f"Crie uma proposta de parceria detalhada e uma estratégia de abordagem.",
        expected_output="Uma proposta de parceria detalhada e uma estratégia de abordagem.",
        agent=partnership_agent
    )

    crew = Crew(agents=[partnership_agent], tasks=[task], verbose=True)
    result = crew.kickoff()
    return result

# Função para enviar e-mail
def send_email(recipient, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_sender, email_password)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Erro ao enviar e-mail: {str(e)}")
        return False

# Interface do usuário
st.header("Informações da Marca")
brand_name = st.text_input("Nome da Marca")
brand_industry = st.text_input("Setor da Indústria")
brand_target = st.text_input("Público-alvo")
brand_email = st.text_input("E-mail da Marca")

st.header("Informações do Influencer")
influencer_name = st.text_input("Nome do Influencer")
influencer_email = st.text_input("E-mail do Influencer")
influencer_followers = st.number_input("Número total de Seguidores", min_value=0)

# Múltiplas redes sociais
social_networks = st.multiselect(
    "Redes Sociais",
    ["Instagram", "TikTok", "YouTube", "Twitter", "Facebook", "LinkedIn"]
)

social_media_info = {}
for network in social_networks:
    followers = st.number_input(f"Seguidores no {network}", min_value=0)
    username = st.text_input(f"Username no {network}")
    social_media_info[network] = {"followers": followers, "username": username}

if st.button("Gerar Proposta"):
    if brand_name and brand_email and influencer_name and influencer_email:
        with st.spinner("Gerando proposta..."):
            brand_info = f"{brand_name} (Setor: {brand_industry}, Público-alvo: {brand_target})"
            influencer_info = f"{influencer_name} (Total de Seguidores: {influencer_followers}, Redes Sociais: {social_media_info})"
            
            proposal = generate_partnership_proposal(brand_info, influencer_info)
            
            st.session_state['proposal'] = proposal
            st.session_state['brand_email'] = brand_email
            st.session_state['influencer_email'] = influencer_email

            st.subheader("Proposta de Parceria Gerada")
            st.text_area("Revise e edite a proposta se necessário:", value=proposal, height=300, key="edited_proposal")
            
            if st.button("Enviar E-mails"):
                edited_proposal = st.session_state.edited_proposal
                
                if send_email(influencer_email, f"Proposta de Parceria - {brand_name}", edited_proposal):
                    st.success(f"E-mail enviado para o influencer: {influencer_email}")
                
                if send_email(brand_email, f"Proposta de Parceria com {influencer_name}", edited_proposal):
                    st.success(f"E-mail enviado para a marca: {brand_email}")
    else:
        st.warning("Por favor, preencha todos os campos obrigatórios (nome e e-mail da marca e do influencer).")

# Rodapé
st.sidebar.markdown("---")
st.sidebar.info("Este é um exemplo de aplicação do Agente de Captação de Parcerias usando Streamlit e crewAI.")