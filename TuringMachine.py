import json
import sys ## Ler linha de comando


## Variáveis globais
mt = {}

qnt_trilhas = 0

estados = {} ## chave : (id, isFinal) // Tupla
estado_inicial = 0
estados_finais_lista = []
estados_lista = []

alfabeto_entrada = []
alfabeto_fita = []

simbolo_inicio = ""
simbolo_vazio = ""

transicoes = {}
transicoes_lista = []


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

def separar_elementos():
    global qnt_trilhas
    global estado_inicial
    global estados_finais_lista
    global estados_lista
    global alfabeto_entrada
    global alfabeto_fita
    global simbolo_inicio
    global simbolo_vazio
    global transicoes_lista

    qnt_trilhas = mt[0]
    estados_lista = mt[1]
    alfabeto_entrada = mt[2]

    alfabeto_fita = mt[3][(2 + len(alfabeto_entrada)):]

    simbolo_inicio = mt[4]
    simbolo_vazio = mt[5]

    transicoes_lista = mt[6]

    estado_inicial = mt[7]
    estados_finais_lista = mt[8]

def atribuir_numero_estado(): ## Atribuir um número para cada estado : Não trabalhar com strings por exemplo
    global estados
    global estados_lista
    global estados_finais_lista

    id = 1

    for estado in estados_lista:
        if estado in estados_finais_lista:
            estados.update({estado: (id, True)}) ## É Estado Final
        else:
            estados.update({estado: (id, False)}) ## Não é Estado Final
        
        id += 1

def verificar_estados(): ## Verificar se está atribuindo certo
    global estados

    for chave in estados:
        print(f'Chave: {chave}: {estados[chave]}')

def colocar_transicoes_hash(): ## Colocando as transições em Hash com a chave sendo o estado atual
    for transicao in transicoes_lista:
        estado_atual = transicao[0]

        if estado_atual not in transicoes:
            transicoes[estado_atual] = [transicao[1:]]
        else:
            transicoes[estado_atual].append(transicao[1:])

def verificar_transicoes(): ## Teste para verificar se está armazenando de forma correta
    for chave in transicoes:
        for valor in transicoes[chave]:
            print(f'Chave: {chave}: {valor}')

argumentos = sys.argv ## Primeiro argumento é o nome do programa python3

if len(argumentos) != 3:
    print("Usar: python3 TuringMachine.py [MT] [Word]")
    exit

nome_arquivo = argumentos[1]
palavra = argumentos[2]

mt = ler_maquina_turing(nome_arquivo)['mt']

separar_elementos()
atribuir_numero_estado()

verificar_estados()
print()

colocar_transicoes_hash()
verificar_transicoes()


