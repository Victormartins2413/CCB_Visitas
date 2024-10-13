import streamlit as st
import smtplib
from email.mime.text import MIMEText
from fpdf import FPDF
from PIL import Image  # Importar biblioteca para carregar imagens

# Função para enviar email (sem alterações)
def send_email(user_email):
    sender_email = "tuguitosmartins@gmail.com"
    subject = "Irmão auxiliar! Visita cadastrada."
    body = "Irmão auxiliar! Visita cadastrada com sucesso."

    # Configure a mensagem do email
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = user_email

    # Enviar o email pelo servidor SMTP do Gmail
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, "SUA_SENHA_DO_GMAIL")
            server.sendmail(sender_email, user_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False

# Função para gerar PDF (sem alterações)
def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    pdf_file = "dados_cadastro.pdf"
    pdf.output(pdf_file)
    return pdf_file

# Título e Cabeçalho
st.title("Congregação Cristã no Brasil")
st.subheader("Cadastro de Participação da Reunião de Jovens e Menores Jd. São Pedro")

# Carregar e exibir a imagem
image_path = "CCB_JD_São_Pedro.png"  # Caminho para a imagem
image = Image.open(image_path)  # Abrir a imagem
st.image(image, caption='Igreja Congregação Cristã no Brasil - Jd. São Pedro', use_column_width=True)

# Formulário
with st.form(key="cadastro_form"):
    user_email = st.text_input("Seu Email:", placeholder="Digite seu email aqui")
    nome = st.text_input("Nome:")
    idade = st.number_input("Idade:", min_value=0)
    data_nascimento = st.date_input("Data de Nascimento:")
    
    batizado = st.radio("É batizado?", options=["Sim", "Não"])
    if batizado == "Sim":
        data_batismo = st.date_input("Data do Batismo:")
    
    musico = st.text_input("É músico/organista/estudando a música? (Digite a resposta)")
    
    st.subheader("Nome dos Responsáveis (1)")
    nome_responsavel_1 = st.text_input("Nome (1):")
    grau_parentesco_1 = st.text_input("Grau de Parentesco (1):")
    responsavel_batizado_1 = st.text_input("O responsável é batizado? (Digite Sim ou Não) (1)")
    
    st.subheader("Nome dos Responsáveis (2)")
    nome_responsavel_2 = st.text_input("Nome (2):")
    grau_parentesco_2 = st.text_input("Grau de Parentesco (2):")
    responsavel_batizado_2 = st.text_input("O responsável é batizado? (Digite Sim ou Não) (2)")
    
    telefone = st.text_input("Telefones para Contato:")
    endereco = st.text_area("Endereço Residencial:")
    
    st.subheader("Informações de Estudo")
    estuda = st.radio("A criança/moço(a) estuda?", options=["Sim", "Não"])
    if estuda == "Sim":
        serie = st.text_input("Qual série?")
        escola = st.text_input("Escola:")
    
    submit_button = st.form_submit_button(label="Enviar")

# Após o envio, mostrar uma mensagem de agradecimento e enviar o email
if submit_button:
    st.write("### Deus abençoe os irmãos! 😊🙏")
    
    data = {
        "Nome": nome,
        "Idade": idade,
        "Data de Nascimento": str(data_nascimento),
        "É batizado": batizado,
        "Data do Batismo": str(data_batismo) if batizado == "Sim" else "Não",
        "Músico/Organista/Estudando Música": musico,
        "Nome Responsável 1": nome_responsavel_1,
        "Grau de Parentesco 1": grau_parentesco_1,
        "Responsável Batizado 1": responsavel_batizado_1,
        "Nome Responsável 2": nome_responsavel_2,
        "Grau de Parentesco 2": grau_parentesco_2,
        "Responsável Batizado 2": responsavel_batizado_2,
        "Telefones para Contato": telefone,
        "Endereço Residencial": endereco,
        "A criança/moço(a) estuda": estuda,
        "Série": serie if estuda == "Sim" else "Não",
        "Escola": escola if estuda == "Sim" else "Não",
    }

    if send_email(user_email):
        st.success("Email enviado com sucesso para você!")
    else:
        st.error("Houve um erro ao enviar o email.")
    
    pdf_file = generate_pdf(data)
    st.success(f"PDF gerado com sucesso! Você pode baixá-lo [aqui](data:application/pdf;base64,{pdf_file}).")
