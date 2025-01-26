import streamlit as st
import pandas as pd
import re
from PyPDF2 import PdfReader

# Funzione per estrarre i dati dal PDF
def extract_data_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    cod_list = []
    qt_list = []

    for page in reader.pages:
        text = page.extract_text()

        # Trova le righe con i dati di interesse
        lines = text.split("\n")
        for line in lines:
            # Regex per trovare codice e quantità
            match = re.search(r"(\bT\d{6,}\b)\s+(\d+)pz", line)
            if match:
                cod = match.group(1)
                qt = match.group(2)
                cod_list.append(cod)
                qt_list.append(qt)

    return cod_list, qt_list

# Titolo dell'app
st.title("PDF to CSV Converter")

# Caricamento del file PDF
uploaded_file = st.file_uploader("Carica un file PDF", type="pdf")

if uploaded_file is not None:
    # Estrazione dei dati
    cod_list, qt_list = extract_data_from_pdf(uploaded_file)

    # Creazione del DataFrame
    data = {
        "COD": cod_list,
        "QT": qt_list,
        "NOTE": [""] * len(cod_list)  # Colonna NOTE vuota
    }
    df = pd.DataFrame(data)

    # Mostra il DataFrame
    st.write("Ecco i dati estratti dal PDF:")
    st.dataframe(df)

    # Scarica il CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="Scarica il file CSV",
        data=csv,
        file_name="output.csv",
        mime="text/csv"
    )