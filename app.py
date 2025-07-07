import streamlit as st
from parser import extract_data_from_excel
from prompt_engine import generate_analysis_for_all_pillars
from report_generator import generate_word_report
import os
from dotenv import load_dotenv
import tempfile

# Charger la clé API depuis le .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

st.title("📊 Barka Impact - Business Assessment Report Generator")

# Chargement du fichier Excel par l'utilisateur
uploaded_file = st.file_uploader("📤 Upload your Excel assessment file", type=["xlsx"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    st.success("✅ File uploaded. Starting analysis...")

    # Étape 1 : Extraction des données
    scores, responses = extract_data_from_excel(tmp_path)

    # Étape 2 : Génération des analyses par GPT-4
    st.info("🧠 Analyzing responses with GPT-4...")
    analyses = generate_analysis_for_all_pillars(responses, api_key)

    # Étape 3 : Génération du rapport Word
    output_path = os.path.join(tempfile.gettempdir(), "generated_report.docx")
    generate_word_report(scores, analyses, output_path)

    # Étape 4 : Téléchargement
    with open(output_path, "rb") as file:
        st.download_button(
            label="📥 Download Investment Readiness Report",
            data=file,
            file_name="Barka_Assessment_Report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
