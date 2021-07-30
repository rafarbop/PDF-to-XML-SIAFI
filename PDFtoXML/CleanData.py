# Functions for cleaning some data of the dataframes


def name_split(name):
    name = name.split(' (', maxsplit=1)[0]
    name = name.split('(', maxsplit=1)[0]
    return name


def cleanCPF(cpf):
    cpf = cpf.replace('.', '').replace('-', '')
    return cpf


def cleanAG(ag):
    ag = str(ag).replace('.', '').replace('-', '')
    return ag


def cleanConta(conta):
    conta = conta.replace('.', '').replace('-', '')
    return conta


def cleanValor(valor):
    valor = valor.replace('R$ ', '').replace(',', '.')
    return valor