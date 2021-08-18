# Functions for cleaning some data of the dataframes


def name_split(name):
    name = name.split(' (', maxsplit=1)[0]
    name = name.split('(', maxsplit=1)[0]
    return name


def cleanCPF(cpf):
    cpf = cpf.replace('.', '').replace('-', '')
    return cpf


def fillZerosBCO(ag):
    ag = str(ag).zfill(3)
    return ag


def cleanAG(ag):
    ag = str(ag).replace('.', '').replace('-', '')
    return ag


def fillZerosAG(ag):
    ag = str(ag).zfill(4)
    return ag


def removeAG_DV(ag):
    ag = str(ag)[0:4]
    return ag


def cleanConta(conta):
    conta = conta.replace('.', '').replace('-', '').replace(' ', '')
    return conta


def cleanContaBB(conta):
    conta = conta.replace('X', '0')
    return conta


def cleanValor(valor):
    valor = valor.replace('R$ ', '').replace(',', '.')
    return valor