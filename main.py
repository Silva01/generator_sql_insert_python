import csv
import os
from configparser import ConfigParser


def init():
    config = ConfigParser()
    config.read("config.properties")

    for _,_,arquivos in os.walk(config["ConfigFile"]["planilha.url"]):
        for arquivo in arquivos:
            print(arquivo)
            path = '{}{}'.format(config["ConfigFile"]["planilha.url"], arquivo)
            print(path)
            linha = -1
            with open(path, 'r') as dados_csv:
                print(dados_csv)
                dados = csv.reader(dados_csv, delimiter=';')
                dados.__next__()
                arquivo_aberto = True

                for row in dados:
                    linha = linha + 1
                    if linha >= int(config["tabelaContrucao"]["tabela.linha"]):
                        if arquivo_aberto:
                            print("Abrindo arquivo")
                            novoArquivo = open('{}{}.sql'.format(config["ConfigFile"]["planilha.saida"], arquivo.split(".")[0]), 'w')
                            arquivo_aberto = False

                        query_dado = 'INSERT INTO {} ({}) VALUES ('.format(
                            config["tabelaContrucao"]["tabela.nome"],
                            config["tabelaContrucao"]["tabela.colunas"]
                        )

                        virgula = 0
                        parans = ''
                        for d in row:
                            if virgula > 0:
                                parans = parans + ','
                            parans = parans + '{}'.format(isInt(d))
                            virgula = virgula + 1

                        query_dado = query_dado + parans
                        query_dado.join(')')
                        novoArquivo.write(query_dado)
                        novoArquivo.write('\n')


def isInt(value):
  try:
    return int(value)
  except:
    return '\'{}\''.format(value)

if __name__ == '__main__':
    init()
