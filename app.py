import streamlit as st
import pandas as pd
import tabula as tb

# Ajust layout and visual of streamlit
st.set_page_config(
    page_title="PDF to XML-SIAFI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and Description of Application
st.markdown("# Converter PDF para Arquivo XML do SIAFI")
st.markdown("---")

st.sidebar.title('Rafa')

fileUploaded = st.sidebar.file_uploader(
    "PDF",
    type="pdf",
)