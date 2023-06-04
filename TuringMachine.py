import json
import sys ## Ler linha de comando


def ler_maquina_turing(nome_arquivo : str) -> dict:
    try:
        with open(nome_arquivo) as file:
            return json.load(file)
    except FileNotFoundError:
        print(f'Arquivo {nome_arquivo} não foi encontrado')
        exit
    except Exception as e:
        print(e)
        exit
    
argumentos = sys.argv ## Primeiro argumento é o nome do programa python3

if len(argumentos) != 3:
    print("Usar: python3 TuringMachine.py [MT] [Word]")
    exit

nome_arquivo = argumentos[1]
palavra = argumentos[2]

mt = ler_maquina_turing(nome_arquivo)['mt']

qnt_trilhas = mt[0]
estados_lista = mt[1]
alfabeto_entrada = mt[2]

qnt_elementos_alfabeto_entrada = len(alfabeto_entrada)

alfabeto_fita = mt[3][(2 + qnt_elementos_alfabeto_entrada):]
simbolo_inicio = mt[4]
simbolo_vazio = mt[5]

transicoes_lista = mt[6] ## Separar as transições para cada estado | Uso de hash?

estado_inicial = mt[7]
estados_finais_lista = mt[8] ## Utilizar hash


estados = {} ## chave : {id, isFinal}
id = 1

## Atribuir um número para cada estado : Não trabalhar com strings por exemplo
for estado in estados_lista:
    if estado in estados_finais_lista:
        estados.update({estado: (id, True)}) ## É Estado Final
    else:
        estados.update({estado: (id, False)}) ## Não é Estado Final
        
    id += 1



print(f'{simbolo_inicio}\n{simbolo_vazio}')