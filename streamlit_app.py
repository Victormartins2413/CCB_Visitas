import streamlit as st
import smtplib
from email.mime.text import MIMEText

def send_email(user_email):
    sender_email = "tuguitosmartins@gmail.com"  # Seu email
    subject = "Irmão auxiliar! Visita cadastrada."
    body = "Irmão auxiliar! Visita cadastrada com sucesso."

    # Configure a mensagem do email
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = user_email  # Usar o email do usuário

    # Enviar o email pelo servidor SMTP do Gmail
    try:
        # Conectando ao servidor Gmail SMTP (SSL)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, "SUA_SENHA_DO_GMAIL")  # Substitua pela sua senha do Gmail ou senha de aplicativo
            server.sendmail(sender_email, user_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False

# Título e Cabeçalho
st.title("Congregação Cristã no Brasil")
st.subheader("Cadastro de Participação da Reunião de Jovens e Menores Jd. São Pedro")

# Formulário
with st.form(key="cadastro_form"):
    # Campo para Email do usuário
    user_email = st.text_input("Seu Email:", placeholder="Digite seu email aqui")
    
    # Campos para Nome, Idade e Data de Nascimento
    nome = st.text_input("Nome:")
    idade = st.number_input("Idade:", min_value=0)
    data_nascimento = st.date_input("Data de Nascimento:")

    # Seção de batismo e música
    batizado = st.radio("É batizado?", options=["Sim", "Não"])
    if batizado == "Sim":
        data_batismo = st.date_input("Data do Batismo:")

    # Campo para digitar a resposta sobre música
    musico = st.text_input("É músico/organista/estudando a música? (Digite a resposta)")

    # Seção de responsáveis - repetida duas vezes com os ajustes de nomes
    st.subheader("Nome dos Responsáveis (1)")
    nome_responsavel_1 = st.text_input("Nome (1):")
    grau_parentesco_1 = st.text_input("Grau de Parentesco (1):")
    responsavel_batizado_1 = st.text_input("O responsável é batizado? (Digite Sim ou Não) (1)")

    st.subheader("Nome dos Responsáveis (2)")
    nome_responsavel_2 = st.text_input("Nome (2):")
    grau_parentesco_2 = st.text_input("Grau de Parentesco (2):")
    responsavel_batizado_2 = st.text_input("O responsável é batizado? (Digite Sim ou Não) (2)")

    # Telefone e Endereço
    telefone = st.text_input("Telefones para Contato:")
    endereco = st.text_area("Endereço Residencial:")

    # Informações de estudo
    st.subheader("Informações de Estudo")
    estuda = st.radio("A criança/moço(a) estuda?", options=["Sim", "Não"])
    if estuda == "Sim":
        serie = st.text_input("Qual série?")
        escola = st.text_input("Escola:")

    # Botão para envio
    submit_button = st.form_submit_button(label="Enviar")

# Após o envio, mostrar uma mensagem de agradecimento e enviar o email
if submit_button:
    st.write("### Deus abençoe os irmãos! 😊🙏")
    
    # Mostrar os dados preenchidos
    st.write("### Dados Cadastrados:")
    st.write(f"**Nome:** {nome}")
    st.write(f"**Idade:** {idade}")
    st.write(f"**Data de Nascimento:** {data_nascimento}")
    st.write(f"**É batizado?** {batizado}")
    if batizado == "Sim":
        st.write(f"**Data do Batismo:** {data_batismo}")
    st.write(f"**É músico/organista/estudando a música?** {musico}")

    st.write("### Informações dos Responsáveis (1):")
    st.write(f"**Nome (1):** {nome_responsavel_1}")
    st.write(f"**Grau de Parentesco (1):** {grau_parentesco_1}")
    st.write(f"**Responsável é batizado (1)?** {responsavel_batizado_1}")

    st.write("### Informações dos Responsáveis (2):")
    st.write(f"**Nome (2):** {nome_responsavel_2}")
    st.write(f"**Grau de Parentesco (2):** {grau_parentesco_2}")
    st.write(f"**Responsável é batizado (2)?** {responsavel_batizado_2}")

    st.write(f"**Telefones para Contato:** {telefone}")
    st.write(f"**Endereço Residencial:** {endereco}")
    st.write("### Informações de Estudo:")
    st.write(f"**A criança/moço(a) estuda?** {estuda}")
    if estuda == "Sim":
        st.write(f"**Série:** {serie}")
        st.write(f"**Escola:** {escola}")

    # Enviar o email após o formulário ser submetido
    if send_email(user_email):
        st.success("Email enviado com sucesso para você!")
    else:
        st.error("Houve um erro ao enviar o email.")
