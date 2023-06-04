import json
import sys ## Ler linha de comando


def ler_maquina_turing(nome_arquivo : str) -> dict:
    with open(nome_arquivo) as file:
        return json.load(file)


argumentos = sys.argv ## Primeiro argumento é o nome do programa python3
nome_arquivo = argumentos[1]
palavra = argumentos[2]

mt = ler_maquina_turing(nome_arquivo)['mt']

qnt_trilhas = mt[0]
estados = mt[1]
alfabeto_entrada = mt[2]

qnt_elementos_alfabeto_entrada = len(alfabeto_entrada)

alfabeto_fita = mt[3][(2 + qnt_elementos_alfabeto_entrada):]
simbolo_inicio = mt[4]
simbolo_vazio = mt[5]

transicoes = mt[6]

estado_inicial = mt[7]
estados_finais = mt[8]

print(f'{simbolo_inicio}\n{simbolo_vazio}')