from typing import OrderedDict
from dict2xml import dict2xml as dxml


class convertXML:

    def __init__(self,
                 codUgEmit,
                 anoDH,
                 codTipoDH,
                 dtEmis, dtVenc, codUgPgto, vlr, txtObser, txtProcesso,
                 dtAteste, codCredorDevedor, dtPgtoReceb, codIdentEmit,
                 dtEmisDocOrigem, numDocOrigem,
                 numSeqItemPco, codSit, codUgEmpe, numEmpe, codSubItemEmpe,
                 numClassA,
                 numSeqItemCusto, codCentroCusto, mesReferencia, anoReferencia,
                 codUgBenef, numSeqPai,
                 codTipoOB, banco, agencia, conta, contaGoverno
                 ):
        self.codUgEmit = codUgEmit
        self.anoDH = anoDH
        self.codTipoDH = codTipoDH
        self.dtEmis = dtEmis
        self.dtVenc = dtVenc
        self.codUgPgto = codUgPgto
        self.vlr = vlr
        self.txtObser = txtObser
        self.txtProcesso = txtProcesso
        self.dtAteste = dtAteste
        self.codCredorDevedor = codCredorDevedor
        self.dtPgtoReceb = dtPgtoReceb
        self.codIdentEmit = codIdentEmit
        self.dtEmisDocOrigem = dtEmisDocOrigem
        self.numDocOrigem = numDocOrigem
        self.numSeqItemPco = numSeqItemPco
        self.codSit = codSit
        self.codUgEmpe = codUgEmpe
        self.numEmpe = numEmpe
        self.codSubItemEmpe = codSubItemEmpe
        self.numClassA = numClassA
        self.numSeqItemCusto = numSeqItemCusto
        self.codCentroCusto = codCentroCusto
        self.mesReferencia = mesReferencia
        self.anoReferencia = anoReferencia
        self.codUgBenef = codUgBenef
        self.numSeqPai = numSeqPai
        self.codTipoOB = codTipoOB
        self.banco = banco
        self.agencia = agencia
        self.conta = conta
        self.contaGoverno = contaGoverno

    def incluirItem(self):
        lista_dados = {}
        dadosDH = OrderedDict()
        dadosDH['codUgEmit'] = self.codUgEmit
        dadosDH['anoDH'] = self.anoDH
        dadosDH['codTipoDH'] = self.codTipoDH
        
        dadosDH_dadosBasicos = OrderedDict()
        dadosDH_dadosBasicos["dtEmis"] = self.dtEmis
        dadosDH_dadosBasicos["dtVenc"] = self.dtVenc
        dadosDH_dadosBasicos["codUgPgto"] = self.codUgPgto
        dadosDH_dadosBasicos["vlr"] = self.vlr
        dadosDH_dadosBasicos["txtObser"] = self.txtObser
        dadosDH_dadosBasicos["txtProcesso"] = self.txtProcesso
        dadosDH_dadosBasicos["dtAteste"] = self.dtAteste
        dadosDH_dadosBasicos["codCredorDevedor"] = self.codCredorDevedor
        dadosDH_dadosBasicos["dtPgtoReceb"] = self.dtPgtoReceb
        dadosDH_dadosBasicos_docOrigem = OrderedDict()
        dadosDH_dadosBasicos_docOrigem["codIdentEmit"] = self.codIdentEmit
        dadosDH_dadosBasicos_docOrigem["dtEmis"] = self.dtEmisDocOrigem
        dadosDH_dadosBasicos_docOrigem["numDocOrigem"] = self.numDocOrigem
        dadosDH_dadosBasicos_docOrigem["vlr"] = self.vlr
        dadosDH_dadosBasicos["docOrigem"] = dadosDH_dadosBasicos_docOrigem
        dadosDH['dadosBasicos'] = dadosDH_dadosBasicos
        
        dadosDH_pco = OrderedDict()
        dadosDH_pco["numSeqItem"] = self.numSeqItemPco
        dadosDH_pco["codSit"] = self.codSit
        dadosDH_pco["codUgEmpe"] = self.codUgEmpe
        dadosDH_pco_pcoItem = OrderedDict()
        dadosDH_pco_pcoItem["numSeqItem"] = self.numSeqItemPco
        dadosDH_pco_pcoItem["numEmpe"] = self.numEmpe,
        dadosDH_pco_pcoItem["codSubItemEmpe"] = self.codSubItemEmpe
        dadosDH_pco_pcoItem["vlr"] = self.vlr
        dadosDH_pco_pcoItem["numClassA"] = self.numClassA
        dadosDH_pco["pcoItem"] = dadosDH_pco_pcoItem
        dadosDH['pco'] = dadosDH_pco

        dadosDH_centroCusto = OrderedDict()
        dadosDH_centroCusto["numSeqItem"] = self.numSeqItemCusto
        dadosDH_centroCusto["codCentroCusto"] = self.codCentroCusto
        dadosDH_centroCusto["mesReferencia"] = self.mesReferencia
        dadosDH_centroCusto["anoReferencia"] = self.anoReferencia
        dadosDH_centroCusto["codUgBenef"] = self.codUgBenef
        dadosDH_centroCusto_relPcoItem = OrderedDict()
        dadosDH_centroCusto_relPcoItem["numSeqPai"] = self.numSeqPai
        dadosDH_centroCusto_relPcoItem["numSeqItem"] = self.numSeqItemCusto
        dadosDH_centroCusto_relPcoItem["vlr"] = self.vlr
        dadosDH_centroCusto["relPcoItem"] = dadosDH_centroCusto_relPcoItem
        dadosDH['centroCusto'] = dadosDH_centroCusto

        dadosDH_dadosPgto = OrderedDict()
        dadosDH_dadosPgto["codCredorDevedor"] = self.codCredorDevedor
        dadosDH_dadosPgto["vlr"] = self.vlr
        dadosDH_dadosPgto_predoc = OrderedDict()
        dadosDH_dadosPgto_predoc["txtObser"] = self.txtObser
        dadosDH_dadosPgto_predoc_predocOB = OrderedDict()
        dadosDH_dadosPgto_predoc_predocOB["codTipoOB"] = self.codTipoOB
        dadosDH_dadosPgto_predoc_predocOB["codCredorDevedor"] = self.codCredorDevedor
        dadosDH_dadosPgto_predoc_predocOB_numDomiBancFavo = OrderedDict()
        dadosDH_dadosPgto_predoc_predocOB_numDomiBancFavo["banco"] = self.banco
        dadosDH_dadosPgto_predoc_predocOB_numDomiBancFavo["agencia"] = self.agencia
        dadosDH_dadosPgto_predoc_predocOB_numDomiBancFavo["conta"] = self.conta
        dadosDH_dadosPgto_predoc_predocOB_numDomiBancPgto = OrderedDict()
        dadosDH_dadosPgto_predoc_predocOB_numDomiBancPgto["conta"] = self.contaGoverno
        dadosDH_dadosPgto_predoc_predocOB["numDomiBancFavo"] = dadosDH_dadosPgto_predoc_predocOB_numDomiBancFavo
        dadosDH_dadosPgto_predoc_predocOB["numDomiBancPgto"] = dadosDH_dadosPgto_predoc_predocOB_numDomiBancPgto
        dadosDH_dadosPgto_predoc_predocOB["txtProcesso"] = self.txtProcesso
        dadosDH_dadosPgto_predoc["predocOB"] = dadosDH_dadosPgto_predoc_predocOB
        dadosDH_dadosPgto["predoc"] = dadosDH_dadosPgto_predoc
        dadosDH['dadosPgto'] = dadosDH_dadosPgto
        
        lista_dados['ns2:CprDhCadastrar'] = dadosDH

        return lista_dados


def receberXML(lista_de_detalhes,dados_header):
    dados_arquivos = OrderedDict()
    split_dataGeracao = str(dados_header['dataGeracao']).split('-')
    data_geracao_validada = f'{split_dataGeracao[2]}/{split_dataGeracao[1]}/{split_dataGeracao[0]}'
    dados_sb_header = OrderedDict()
    dados_sb_header["sb:codigoLayout"] = 'DH001'
    dados_sb_header["sb:dataGeracao"] = data_geracao_validada
    dados_sb_header["sb:sequencialGeracao"] = dados_header['sequecialGeracao']
    dados_sb_header["sb:anoReferencia"] = dados_header['anoReferencia']
    dados_sb_header["sb:ugResponsavel"] = dados_header['ugResponsavel']
    dados_sb_header["sb:cpfResponsavel"] = dados_header['cpfResponsavel']

    dados_arquivos['sb:header'] = dados_sb_header
    dados_arquivos['sb:detalhes'] = {"sb:detalhe": lista_de_detalhes}
    dados_arquivos['sb:trailler'] = {
                "sb:quantidadeDetalhe": len(lista_de_detalhes)
            }

    dados = OrderedDict()
    dados["sb:arquivo"] = dados_arquivos

    dados_xml = dxml(dados)

    dados_xml_namespace = dados_xml.replace(
        "<sb:arquivo>",
        '<sb:arquivo xmlns:ns2="http://services.docHabil.cpr.siafi.\
tesouro.fazenda.gov.br/" xmlns:sb="http://www.tesouro.gov.br/siafi/submissao">'
        )

    # f = open("xml.xml", "w")
    # try:
    #     f.writelines(dados_xml_namespace)
    # finally:
    #     f.close()
    return dados_xml_namespace
