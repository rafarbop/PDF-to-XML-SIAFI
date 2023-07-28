from urllib.parse import quote
from CleanData import zfillConta,lstripConta
from ProcessPdf import ProcessPdf
from ConverttoXML import convertXML,receberXML
from PIL import Image
import streamlit as st
from datetime import date


st.set_page_config(
    page_title="PDF to XML-SIAFI",
    layout="wide",
    initial_sidebar_state="expanded",
)

DadostxtObserPreDoc = ''

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


def processDatatoXML(dadosDH: dict, dadosAuxilios: dict,DadostxtObserPreDoc: str,numDocOrigemEspecifico: str ,dadosPagamentoAlunos: list):
    """Recebe os dados incluidos pelo usuário, os dados extraídos do PDF e envia para função que converte para XML."""
    lista_de_detalhes = []

    for dados_aluno in dadosPagamentoAlunos:
        detalhe_xml_aluno = convertXML(
            codUgEmit=dadosDH["ugResponsavel"],
            anoDH=dadosDH["anoReferencia"],
            codTipoDH='RP',
            dtEmis=dadosDH["dataGeracao"],
            dtVenc=dadosAuxilios['dataPagamentoPrevista'],
            codUgPgto=dadosDH["ugResponsavel"],
            vlr=dados_aluno[6],
            txtObser=f'{dadosAuxilios["tipoAuxilio"]} - Mês {dadosAuxilios["mesCompetenciaAuxilio"]}/{dadosAuxilios["anoCompetenciaAuxilio"]} - {dadosAuxilios["processoSEI"]} - {dados_aluno[0][:20]}',
            txtProcesso=dadosAuxilios["processoSEI"],
            dtAteste=dadosAuxilios['dataAteste'],
            codCredorDevedor=dados_aluno[1],
            dtPgtoReceb=dadosAuxilios['dataPagamentoPrevista'],
            codIdentEmit=dadosDH["ugResponsavel"],
            dtEmisDocOrigem=dadosAuxilios['dataAteste'],
            numDocOrigem=numDocOrigemEspecifico[:17],
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
            txtObserPreDoc=f'{DadostxtObserPreDoc} - Mês {dadosAuxilios["mesCompetenciaAuxilio"]}/{dadosAuxilios["anoCompetenciaAuxilio"]} - {dadosAuxilios["processoSEI"]} - {dados_aluno[0][:20]}',
            banco=dados_aluno[2],
            agencia=dados_aluno[3],
            conta=dados_aluno[5],
            contaGoverno='UNICA',
        )
        lista_de_detalhes.append(detalhe_xml_aluno.incluirItem())

    arquivoXML = receberXML(lista_de_detalhes,dadosDH)

    return arquivoXML



# Ajust layout and visual of streamlit

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

with st.sidebar:
    col1_sidedar,col2_sidedar = st.columns([1,5])
    with col1_sidedar:
        st.image(Image.open("public/images/GitHub-Mark-64px.png"),width=48)
    with col2_sidedar:
        st.write('Código do Projeto disponível no GitHub: [Repósitório](https://github.com/rafarbop/PDF-to-XML-SIAFI)')
    st.caption('Arquivo exemplo de Folha de Pagamentos - SISAE')
    st.caption('[Modelo_Folha_Pagamentos_Auxilios.pdf](https://github.com/rafarbop/PDF-to-XML-SIAFI/blob/11348cb5d772f4047ed143f22f77035d113e4e37/public/examples/Modelo_Folha_Pagamento_auxilios_SISAE.pdf)')
    st.write('---')
    st.write('Parametros de processamento: ')
    alterarAgenciasBancosDigitais = st.checkbox('Alterar as Agências de Bancos Digitais para 9999', help='(Nubank - Código 260, PicPay - Código 380 e C6 Bank - Código 336)')
    alterarPoupancasCaixa = st.checkbox('Alterar Poupança da CAIXA(Operação 013)', help='Incluir 13 no começo da conta')
    alterarObservacoesPredocOB = st.checkbox('Alterar "Observações" do Pre-doc OB', help='Caso não selecionado, será colocado texto padrão',value=False)
    alterarNumDocOrigemDadosBasicos = st.checkbox('Alterar "numDocOrigem" do Dados Básicos do DH', help='Caso não selecionado, será colocado texto padrão',value=False)


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

        if alterarAgenciasBancosDigitais:
            df_data_students['AG. No'].loc[df_data_students['BCO No'] == '260'] = '9999'
            df_data_students['AG. No'].loc[df_data_students['BCO No'] == '380'] = '9999'
            df_data_students['AG. No'].loc[df_data_students['BCO No'] == '336'] = '9999'

        if alterarPoupancasCaixa:
            df_data_students['C/C'] = df_data_students['C/C'].apply(zfillConta)
            df_data_students.loc[(df_data_students['OP. No'] == '013') & (df_data_students['BCO No'] == '104'),'C/C'] = '13'+df_data_students['C/C']
            df_data_students['C/C'] = df_data_students['C/C'].apply(lstripConta)


    with st.expander("Visualise os dados extraídos do PDF processado.", expanded=True):
        st.dataframe(df_data_students)
    st.markdown('### Dados Gerais do Documento Hábil')
    with st.expander('Mostrar/Ocultar Informações',expanded=True):
        with st.form("formDadosGeraisSIAFI"):

            col1,col2 = st.columns(2)
            col3,col4 = st.columns(2)
            col5,col6 = st.columns(2)
            with col1:
                dadosGeraisDH['codigoSituacaoDH'] = st.text_input(
                    "Código da Situação a ser usada na apropriação Documento Hábil",
                    value="DSP061"
                    )
            with col2:
                dadosGeraisDH['sequecialGeracao'] = st.number_input(
                    "Sequencial de arquivos submetidos no SIAFI pela UG no dia.",
                    min_value=0,
                    value=1,
                    step=1
            )
            with col3:
                dadosGeraisDH['dataGeracao'] = st.date_input(
                    "Data de upload do arquivo no SIAFI"
                )
            with col4:
                dadosGeraisDH['anoReferencia'] = st.number_input(
                    "Ano Corrente na data de Apropriação do Documento Hábil",
                    value=date.today().year,
                    step=1,
                    min_value=2022,
                    max_value=2030
                )
            with col5:
                dadosGeraisDH['ugResponsavel'] = st.text_input(
                    "UG do operador ao fazer o upload do arquivo no SIAFI",
                    value="158953",
                    max_chars=6
                )
            with col6:
                dadosGeraisDH['cpfResponsavel'] = st.text_input(
                    "CPF do operador que fará o upload do arquivo no SIAFI",
                    max_chars=11,
                    value="",
                    help="Apenas números, sem traços ou pontos"
                )
            submit_dadosGeraisDH = st.form_submit_button("Confirmar Dados Gerais DH")
    st.markdown('### Dados Gerais dos Auxílios')
    with st.expander('Mostrar/Ocultar Informações',expanded=True):
        with st.form("formDadosMesAuxilioSISAE"):
            col1,col2 = st.columns(2)
            col3,col4 = st.columns(2)
            col5,col6 = st.columns(2)
            col7,col8 = st.columns(2)
            with col1:
                dadosGeraisAuxilios['tipoAuxilio'] = st.text_input(
                    "Tipo de Auxílio - Informação será utilizada em 'Observações'",
                    help="Mês/Ano, Processo e Nome do Aluno serão também incluídos automaticamente no Campo Observações.",
                    value="Auxílio Estudantil"
                )
            with col2:
                dadosGeraisAuxilios['mesCompetenciaAuxilio'] = st.text_input(
                    "Informe o mês competência dos Auxilios com dois dígitos - Ex.: 06",
                    max_chars=2
                )
            dadosGeraisAuxilios['anoCompetenciaAuxilio'] = dadosGeraisDH['anoReferencia']
            with col3:
                dadosGeraisAuxilios["dataAteste"] = st.date_input(
                    "Informe a data de ateste desse processo de pagamento"
                )
            with col4:
                dadosGeraisAuxilios['dataPagamentoPrevista'] = st.date_input(
                    "Informe a data de pagamento prevista"
                )
            with col5:
                dadosGeraisAuxilios["processoSEI"] = st.text_input(
                    "Informe o número processo no SEI",
                    placeholder='23255.000123/2022-00'
                )
            with col6:
                dadosGeraisAuxilios["numeroEmpenho"] = st.text_input(
                    "Informe o Empenho a ser utilizado na liquidação e pagamentos",
                    max_chars=12,
                    placeholder='2024NE000001'
                )
            with col7:
                if alterarObservacoesPredocOB:
                    DadostxtObserPreDoc = st.text_input(
                        label="Informe o texto de 'Observações' do Pre-doc OB"
                    )
                else:
                    DadostxtObserPreDoc = dadosGeraisAuxilios['tipoAuxilio']
            with col8:
                if alterarNumDocOrigemDadosBasicos:
                    numDocOrigemEspecifico = st.text_input(
                        label="Informe o 'numDocOrigem' - Campo de Documento de Origem em Dados Básicos do DH",
                        max_chars=17
                    )
                else:
                    numDocOrigemEspecifico=f'{dadosGeraisAuxilios["mesCompetenciaAuxilio"]}/{dadosGeraisAuxilios["anoCompetenciaAuxilio"]}'[:18]
            submit_dadosGeraisAuxilios = st.form_submit_button("Confirmar Dados Gerais dos Auxilios")


    isDatasInputsOK = False
    if dadosGeraisDH['cpfResponsavel'] == "":
        st.warning('Informe o CPF do responsável')
    elif dadosGeraisAuxilios['mesCompetenciaAuxilio'] == "":
        st.warning('Informe o mẽs do competência dos auxílios')
    elif dadosGeraisAuxilios['processoSEI'] == "":
        st.warning('Informe o número do processo SEI')
    elif dadosGeraisAuxilios['numeroEmpenho'] == "":
        st.warning('Informe o Empenho a ser utilizado')
    else:
        isDatasInputsOK = True

    if st.button('Processar Dados e Gerar Arquivo XML'):
        if isDatasInputsOK:
            with st.spinner('Processando os dados e convertendo para XML...'):
                arquivoXML = processDatatoXML(
                    dadosGeraisDH,
                    dadosGeraisAuxilios,
                    DadostxtObserPreDoc,
                    numDocOrigemEspecifico,
                    df_data_students.values.tolist()
                )
                with st.expander("Visualise os dados extraídos do PDF processado.", expanded=False):
                    st.code(arquivoXML)
            

            st.success('Os dados foram processados com sucesso e o arquivo XML pode ser baixado no botão abaixo')
            st.download_button("Download Arquivo XML",data=arquivoXML,file_name="lista_pagamentos.xml")
        else:
            st.error('Necessário informar os dados completos para gerar o Arquivo XML!')
            st.warning('Verifique se confirmou os dados apertando nos botões de confirmar!')
    