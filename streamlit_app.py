import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from fpdf import FPDF  # Importar biblioteca para gerar PDF

def send_email(user_email, pdf_file=None):
    sender_email = "tuguitosmartins@gmail.com"  # Seu email
    subject = "Irmão auxiliar! Visita cadastrada."
    body = "Irmão auxiliar! Visita cadastrada com sucesso."

    # Configure a mensagem do email
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = user_email  # Usar o email do usuário

    # Anexar o PDF se fornecido
    if pdf_file:
        with open(pdf_file, "rb") as f:
            pdf_attachment = MIMEApplication(f.read(), _subtype="pdf")
            pdf_attachment.add_header("Content-Disposition", f"attachment; filename={pdf_file}")
            msg.attach(pdf_attachment)

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

def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    pdf_file = "dados_cadastro.pdf"
    pdf.output(pdf_file)
    return pdf_file

# URL da imagem de fundo
background_image_url = "https://raw.githubusercontent.com/Victormartins2413/CCB_Visitas/main/CCB_JD_São_Pedro.png"  # Ajuste conforme necessário

# Adiciona CSS para a imagem de fundo
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{background_image_url}");
        background-size: cover;  /* Ajusta o tamanho da imagem para cobrir todo o fundo */
        background-position: center;  /* Centraliza a imagem */
        background-repeat: no-repeat;  /* Não repete a imagem */
    }}
    </style>
""", unsafe_allow_html=True)

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

    # Criar dicionário com os dados do formulário
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

    # Gerar PDF com os dados
    pdf_file = generate_pdf(data)

    # Enviar o email após o formulário ser submetido
    if send_email(user_email, pdf_file):
        st.success("Email enviado com sucesso para você com o PDF anexo!")
    else:
        st.error("Houve um erro ao enviar o email.")
