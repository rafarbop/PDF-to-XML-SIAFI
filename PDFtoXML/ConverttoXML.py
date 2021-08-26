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
        dadosDH['dadosBasicos'] = {
            "dtEmis": self.dtEmis,
            "dtVenc": self.dtVenc,
            "codUgPgto": self.codUgPgto,
            "vlr": self.vlr,
            "txtObser": self.txtObser,
            "txtProcesso": self.txtProcesso,
            "dtAteste": self.dtAteste,
            "codCredorDevedor": self.codCredorDevedor,
            "dtPgtoReceb": self.dtPgtoReceb,
            "docOrigem": {
                "codIdentEmit": self.codIdentEmit,
                "dtEmis": self.dtEmisDocOrigem,
                "numDocOrigem": self.numDocOrigem,
                "vlr": self.vlr,
            },
        }
        dadosDH['pco'] = {
            "numSeqItem": self.numSeqItemPco,
            "codSit": self.codSit,
            "codUgEmpe": self.codUgEmpe,
            "pcoItem": {
                "numSeqItem": self.numSeqItemPco,
                "numEmpe": self.numEmpe,
                "codSubItemEmpe": self.codSubItemEmpe,
                "vlr": self.vlr,
                "numClassA": self.numClassA,
            },
        }
        dadosDH['centroCusto'] = {
            "numSeqItem": self.numSeqItemCusto,
            "codCentroCusto": self.codCentroCusto,
            "mesReferencia": self.mesReferencia,
            "anoReferencia": self.anoReferencia,
            "codUgBenef": self.codUgBenef,
            "relPcoItem": {
                "numSeqPai": self.numSeqPai,
                "numSeqItem": self.numSeqItemCusto,
                "vlr": self.vlr,
            },
        }
        dadosDH['dadosPgto'] = {
            "codCredorDevedor": self.codCredorDevedor,
            "vlr": self.vlr,
            "predoc": {
                "txtObser": self.txtObser,
                "predocOB": {
                    "codTipoOB": self.codTipoOB,
                    "codCredorDevedor": self.codCredorDevedor,
                    "numDomiBancFavo": {
                        "banco": self.banco,
                        "agencia": self.agencia,
                        "conta": self.conta,
                    },
                    "numDomiBancPgto": {"conta": self.contaGoverno},
                },
            },
        }
        lista_dados['ns2:CprDhCadastrar'] = dadosDH

        return lista_dados


def receberXML(lista_de_detalhes):
    dados_arquivos = OrderedDict()
    dados_arquivos['sb:header'] = {
                "sb:codigoLayout": "DH001",
                "sb:dataGeracao": "01/12/2020",
                "sb:sequencialGeracao": "2",
                "sb:anoReferencia": "2020",
                "sb:ugResponsavel": "158953",
                "sb:cpfResponsavel": "60032673302",
            }
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
