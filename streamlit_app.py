import streamlit as st
import smtplib
from email.mime.text import MIMEText
from fpdf import FPDF
from PIL import Image
import requests

# Função para enviar email
def send_email(user_email):
    sender_email = "tuguitosmartins@gmail.com"
    subject = "Irmão auxiliar! Visita cadastrada."
    body = "Irmão auxiliar! Visita cadastrada com sucesso."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = user_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, "SUA_SENHA_DO_GMAIL")
            server.sendmail(sender_email, user_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False

# Função para gerar PDF
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
image_path = "https://github.com/SEU_USUÁRIO/SEU_REPOSITORIO/raw/main/CCB_JD_São_Pedro.png"  # Atualize com a URL correta
image = Image.open(requests.get(image_path, stream=True).raw)  # Abrir a imagem diretamente da URL
st.image(image, caption='Igreja Congregação Cristã no Brasil - Jd. São Pedro', use_column_width=True)

# Usar CSS para posicionar os campos sobre a imagem
st.markdown("""
    <style>
    .form-container {
        position: absolute;
        top: 100px; /* Ajuste a posição vertical conforme necessário */
        left: 50%;
        transform: translateX(-50%);
        background-color: rgba(255, 255, 255, 0.8); /* Fundo branco semi-transparente */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Formulário
with st.form(key="cadastro_form", clear_on_submit=True):
    st.markdown('<div class="form-container">', unsafe_allow_html=True)  # Início do contêiner do formulário

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
    
    st.markdown('</div>', unsafe_allow_html=True)  # Fim do contêiner do formulário

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
