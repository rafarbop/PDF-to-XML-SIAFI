from ProcessPdf import ProcessPdf
import streamlit as st


# Ajust layout and visual of streamlit
st.set_page_config(
    page_title="PDF to XML-SIAFI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and Description of Application
st.markdown("# Converter PDF para Arquivo XML do SIAFI")
st.markdown(
    '''
    Esta aplicação processa um arquivo PDF extraído do Sistema de \
Auxílios Estudantis - SISAE do IFCE, procura uma lista de alunos para \
pagamentos de auxílios estudantis e exporta os dados no formato XML com \
layout reconhecido pelo SIAFI para *Carga de Dados* em processamento Batch.  
Mais informações: [Processamento Bacth do Siafi](https://www.gov.br/\
tesouronacional/pt-br/siafi/siafi-web/informacoes-tecnicas/arquivos-batch): 
    '''
)
st.markdown("---")

fileUploaded = st.sidebar.file_uploader(
    "Faça upload do arquivo PDF:",
    type="pdf",
)

if fileUploaded is not None:
    processPdf = ProcessPdf()
    df_data_students = processPdf.toDataframe(fileUploaded)

    if processPdf.isValidPdf:
        st.sidebar.info(
            f"A tabela com a lista de pagamentos encontrou \
{processPdf.lenDataframe()} aluno(s)."
        )
        processPdf.cleanDataframe()

    with st.beta_expander("Visualise a tabela extraído do PDF importando", expanded=True):
        tableFromPDF = st.dataframe(df_data_students)
    
    with st.form("formDadosGeraisSIAFI"):
        codigoSituacaoDH = st.text_input(
            "Código da Situação a ser usada na apropriação Documento Hábil",
            value="DSP061"
            )
        sequecialGeracao = st.number_input(
            "Sequencial de arquivos submetidos no SIAFI pela UG no dia.",
            min_value=0,
            value=1,
            step=1
        )
        anoReferencia = st.number_input(
            "Ano Corrente na data de Apropriação do Documento Hábil",
            value=2021,
            step=1,
            min_value=2021,
            max_value=2025
        )
        ugResponsavel = st.text_input(
            "UG do operador ao fazer o upload do arquivo no SIAFI",
            value="158953",
            max_chars=6
        )
        cpfResponsavel = st.text_input(
            "CPF do operador que fará o upload do arquivo no SIAFI",
            max_chars=11,
            help="Apenas números, sem traços ou pontos"
        )
        dataGeracao = st.date_input(
            "Data de upload do arquivo no SIAFI"
        )

        st.form_submit_button("Confirmar Dados")

    if cpfResponsavel != "" and cpfResponsavel is not None:
        st.success("Iremos processar agora!")
    else:
        st.warning("Informe o CPF do responsável acima para continuar")

        