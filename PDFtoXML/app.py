from datetime import date
from urllib.parse import quote
from ProcessPdf import ProcessPdf
from ConverttoXML import convertXML,receberXML
import streamlit as st

dadosGeraisDH = {
    "codigoSituacaoDH": "",
    "sequecialGeracao": "",
    "anoReferencia": "",
    "ugResponsavel": "",
    "cpfResponsavel": "",
    "dataGeracao": "",
}

dadosGeraisAuxilios = {
    "tipoAuxilio": "",
    "mesCompetenciaAuxilio": "",
    "anoCompetenciaAuxilio": "",
    "processoSEI": "",
    "dataAteste": "",
    "dataPagamentoPrevista": "",
    "numeroEmpenho": "",
}



def processDatatoXML(dadosDH: dict, dadosAuxilios: dict):
    item1 = convertXML(
        codUgEmit=dadosDH["ugResponsavel"],
        anoDH=dadosDH["anoReferencia"],
        codTipoDH='RP',
        dtEmis=dadosDH["dataGeracao"],
        dtVenc='2021-12-31',
        codUgPgto=dadosDH["ugResponsavel"],
        vlr='300',
        txtObser=f'{dadosAuxilios["tipoAuxilio"]}-{dadosAuxilios["mesCompetenciaAuxilio"]}/{dadosAuxilios["anoCompetenciaAuxilio"]}-{dadosAuxilios["processoSEI"]}- Abrão Abreu',
        txtProcesso=dadosAuxilios["processoSEI"],
        dtAteste=dadosAuxilios['dataAteste'],
        codCredorDevedor=11111111100,
        dtPgtoReceb=dadosAuxilios['dataPagamentoPrevista'],
        codIdentEmit=dadosDH["ugResponsavel"],
        dtEmisDocOrigem=['dataAteste'],
        numDocOrigem=dadosAuxilios["mesCompetenciaAuxilio"][:18],
        numSeqItemPco='1',
        codSit=dadosDH["codigoSituacaoDH"],
        codUgEmpe=dadosDH["ugResponsavel"],
        numEmpe=dadosAuxilios["numeroEmpenho"],
        codSubItemEmpe='1',
        numClassA='394110100',
        numSeqItemCusto='1',
        codCentroCusto='CC-GENERICO',
        mesReferencia=dadosAuxilios["mesCompetenciaAuxilio"],
        anoReferencia=dadosAuxilios["anoCompetenciaAuxilio"],
        codUgBenef=dadosDH["ugResponsavel"],
        numSeqPai='1',
        codTipoOB='OBC',
        banco='104',
        agencia='1111',
        conta='11111111',
        contaGoverno='UNICA',
    )

    item2 = convertXML(
        codUgEmit=dadosDH["ugResponsavel"],
        anoDH=dadosDH["anoReferencia"],
        codTipoDH='RP',
        dtEmis=dadosDH["dataGeracao"],
        dtVenc='2021-12-31',
        codUgPgto=dadosDH["ugResponsavel"],
        vlr='300',
        txtObser=f'{dadosAuxilios["tipoAuxilio"]}-{dadosAuxilios["mesCompetenciaAuxilio"]}/{dadosAuxilios["anoCompetenciaAuxilio"]}-{dadosAuxilios["processoSEI"]}- Bernardo Broia',
        txtProcesso=dadosAuxilios["processoSEI"],
        dtAteste=dadosAuxilios['dataAteste'],
        codCredorDevedor=22222222200,
        dtPgtoReceb=dadosAuxilios['dataPagamentoPrevista'],
        codIdentEmit=dadosDH["ugResponsavel"],
        dtEmisDocOrigem=['dataAteste'],
        numDocOrigem=dadosAuxilios["mesCompetenciaAuxilio"][:18],
        numSeqItemPco='1',
        codSit=dadosDH["codigoSituacaoDH"],
        codUgEmpe=dadosDH["ugResponsavel"],
        numEmpe=dadosAuxilios["numeroEmpenho"],
        codSubItemEmpe='1',
        numClassA='394110100',
        numSeqItemCusto='1',
        codCentroCusto='CC-GENERICO',
        mesReferencia=dadosAuxilios["mesCompetenciaAuxilio"],
        anoReferencia=dadosAuxilios["anoCompetenciaAuxilio"],
        codUgBenef=dadosDH["ugResponsavel"],
        numSeqPai='1',
        codTipoOB='OBC',
        banco='104',
        agencia='2222',
        conta='22222222',
        contaGoverno='UNICA',
    )

    testeXML = receberXML(
        lista_de_detalhes=[item1.incluirItem(),item2.incluirItem()]
    )

    st.code(testeXML)

    linkxml = f'<a href="data:file/xml,{quote(testeXML)}" download="lista_pagamentos.xml">Download XML</a>'

    st.markdown(linkxml,unsafe_allow_html=True)



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
Auxilios Estudantis - SISAE do IFCE, procura uma lista de alunos para \
pagamentos de Auxilios estudantis e exporta os dados no formato XML com \
layout reconhecido pelo SIAFI para *Carga de Dados* em processamento Batch.  
Mais informações: [Processamento Bacth do Siafi](https://www.gov.br/\
tesouronacional/pt-br/siafi/siafi-web/informacoes-tecnicas/arquivos-batch) 
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

    with st.expander("Visualise os dados extraídos do PDF processado.", expanded=False):
        tableFromPDF = st.dataframe(df_data_students)
    
    with st.form("formDadosGeraisSIAFI"):
        st.markdown("### **Dados Gerais do Documento Hábil Siafi**")
        st.markdown("---")
        dadosGeraisDH['codigoSituacaoDH'] = st.text_input(
            "Código da Situação a ser usada na apropriação Documento Hábil",
            value="DSP061"
            )
        dadosGeraisDH['sequecialGeracao'] = st.number_input(
            "Sequencial de arquivos submetidos no SIAFI pela UG no dia.",
            min_value=0,
            value=1,
            step=1
        )
        dadosGeraisDH['anoReferencia'] = st.number_input(
            "Ano Corrente na data de Apropriação do Documento Hábil",
            value=2021,
            step=1,
            min_value=2021,
            max_value=2025
        )
        dadosGeraisDH['ugResponsavel'] = st.text_input(
            "UG do operador ao fazer o upload do arquivo no SIAFI",
            value="158953",
            max_chars=6
        )
        dadosGeraisDH['cpfResponsavel'] = st.text_input(
            "CPF do operador que fará o upload do arquivo no SIAFI",
            max_chars=11,
            value="",
            help="Apenas números, sem traços ou pontos"
        )
        dadosGeraisDH['dataGeracao'] = st.date_input(
            "Data de upload do arquivo no SIAFI"
        )

        st.form_submit_button("Confirmar Dados Gerais DH")
    
    with st.form("formDadosMesAuxilioSISAE"):
        st.markdown("### **Dados Gerais dos Auxilios**")
        st.markdown("---")
        dadosGeraisAuxilios['tipoAuxilio'] = st.text_input(
            "Informe o tipo de auxílio estudantil a ser pago aos alunos",
            value="Auxílio Emergêncial"
            )
        dadosGeraisAuxilios['mesCompetenciaAuxilio'] = st.text_input(
            "Informe o mês competência dos Auxilios com dois dígitos - Ex.: 06"
        )
        dadosGeraisAuxilios['anoCompetenciaAuxilio'] = dadosGeraisDH['anoReferencia']
        dadosGeraisAuxilios["processoSEI"] = st.text_input(
            "Informe o número processo no SEI"
        )
        dadosGeraisAuxilios["dataAteste"] = st.date_input(
            "Informe a data de ateste desse processo de pagamento"
        )
        dadosGeraisAuxilios['dataPagamentoPrevista'] = st.date_input(
            "Informe a data de pagamento prevista"
        )
        dadosGeraisAuxilios["numeroEmpenho"] = st.text_input(
            "Informe o número do Empenho que será utilizado na liquidação e pagamentos dos auxílios"
        )
        

        st.form_submit_button("Confirmar Dados Gerais dos Auxilios")

    if dadosGeraisDH['cpfResponsavel'] != "" and dadosGeraisAuxilios["mesCompetenciaAuxilio"] != "":
        with st.spinner('Processando os dados e convertendo para XML...'):
            processDatatoXML(
                dadosGeraisDH,
                dadosGeraisAuxilios
            )
        
    else:
        st.warning("Informe o CPF do responsável e Mẽs de competência para continuar")


    