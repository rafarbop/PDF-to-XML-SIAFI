from CleanData import name_split,cleanAG,cleanConta,cleanCPF,cleanValor
import pandas
import tabula
import streamlit as st


class ProcessPdf:
    '''Process a File PDF Uploaded for the user in a dataframe'''
    def __init__(self) -> None:
        self.table_raw_list = []
        self.table_dataframe = pandas.DataFrame()
        self.isValidPdf = False
        self.colunms_to_use =  [
            "NOME",
            "C.P.F.",
            "BCO No",
            "AG. No",
            "C/C",
            "VALOR"
        ]
    
    def toDataframe(self, file):
        '''Convert table in PDF into Dataframe'''
        try:
            with st.spinner('Lendo e Processando dados do PDF...'):
                self.table_raw_list = tabula.read_pdf(
                    file,
                    pages="all"
                )[2:]
            st.success("O arquivo foi processado com sucesso!")
            if file is not None and len(self.table_raw_list) > 0:
                if len(self.table_raw_list) > 1:
                    self.table_dataframe = self.table_raw_list[0]
                    for k in range(1, len(self.table_raw_list)):
                        self.table_dataframe = pandas.concat(
                            [self.table_dataframe, self.table_raw_list[k]],
                            ignore_index=True)
                elif len(self.table_raw_list) == 1:
                    self.table_dataframe = self.table_raw_list[0]
                self.table_dataframe = pandas.DataFrame(
                    self.table_dataframe,
                    columns=self.colunms_to_use
                )
                self.isValidPdf = True
        except:
            st.error("Ocorreu um erro no processamento do arquivo.\n\
Verifique se o arquivo é um pdf extraído do SISAE.")
        finally:
            return self.table_dataframe
    
    def lenDataframe(self):
        return len(self.table_dataframe.index)
    
    def cleanDataframe(self):
        if self.isValidPdf:
            self.table_dataframe['NOME'] = self.table_dataframe['NOME'].apply(name_split)
            self.table_dataframe['C.P.F.'] = self.table_dataframe['C.P.F.'].apply(cleanCPF)
            self.table_dataframe['AG. No'] = self.table_dataframe['AG. No'].apply(cleanAG)
            self.table_dataframe['C/C'] = self.table_dataframe['C/C'].apply(cleanConta)
            self.table_dataframe['VALOR'] = self.table_dataframe['VALOR'].apply(cleanValor)
            self.table_dataframe['VALOR'] = pandas.to_numeric(self.table_dataframe['VALOR'])
