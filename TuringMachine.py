# Lembrar da palavra "" (lambda)

import json
import sys # Ler linha de comando


# Variáveis globais
mt = {}

trilhas = []
qnt_trilhas = 0

estados = {} # estado : (id, isFinal) // Tupla
estado_inicial = 0 # TODO: Verificar se o estado inicial está nos 'estados'
estados_finais_lista = [] # TODO: Verificar se os 'estados finais' estão nos 'estados'
estados_lista = []

alfabeto_entrada = [] # TODO: Verificar se o 'alfabeto de entrada' está no 'alfabeto da fita'
alfabeto_fita = [] # TODO: Verificar se os 'símbolos de escrita' e de 'leitura' pertencem ao 'alfabeto da fita'

simbolo_inicio = ""
simbolo_vazio = ""

transicoes = {}
transicoes_lista = []

palavra = ""


def ler_maquina_turing(nome_arquivo : str) -> dict:
    try:
        with open(nome_arquivo) as file:
            return json.load(file)
    except FileNotFoundError:
        print(f'Arquivo {nome_arquivo} não foi encontrado')
        exit()
    except Exception as e:
        print(e)
        exit()

def separar_elementos(): # Colocar cada informação em cada variável
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

    # +2 porque tira o 'x' e o 'y' que pegamos em mt[4] e mt[5] e que não fazem parte do alfabeto da fita
    alfabeto_fita = mt[3][(2 + len(alfabeto_entrada)):] 

    simbolo_inicio = mt[4]
    simbolo_vazio = mt[5]

    transicoes_lista = mt[6]

    estado_inicial = mt[7]
    estados_finais_lista = mt[8]

def verificar_palavra_esta_alfabeto_entrada():
    for letra in palavra:
        if letra not in alfabeto_entrada:
            print(f'A letra "{letra}" da palavra de entrada "{palavra}" não está no alfabeto de entrada "{alfabeto_entrada}"') # TODO: printar 'Não' ou apenas o 'aviso'
            exit()

def atribuir_numero_estado(): # Atribuir um número para cada estado (id) : Não trabalhar com strings por exemplo
    global estados
    global estados_lista
    global estados_finais_lista

    id = 1

    for estado in estados_lista: # O(n * m) -> O(n^2)
        if estado in estados_finais_lista:
            estados.update({estado: (id, True)}) # É Estado Final
        else:
            estados.update({estado: (id, False)}) # Não é Estado Final
        
        id += 1

def colocar_transicoes_hash(): # Colocando as transições em Hash com a chave sendo o estado atual -> Pesquisa será O(1)
    global transicoes_lista

    for transicao in transicoes_lista:
        estado_atual = transicao[0]

        if estado_atual not in transicoes:
            transicoes[estado_atual] = [transicao[1:]]
        else:
            transicoes[estado_atual].append(transicao[1:])
    
    for estado in estados_lista: # colocar vazio nos estados que não tem transições
        if estado not in transicoes:
            transicoes[estado] = []
        
def fazer_trilhas():
    global palavra
    global trilhas
    global simbolo_inicio
    global simbolo_vazio

    VALOR = 1 # Adicionar 1 devido ao Lambda

    palavra_lista = list(palavra) # Lista de caracteres da palavra de entrada
    palavra_lista.insert(0, simbolo_inicio) # Coloca o símbolo de ínicio no primeiro índice

    # Adicionar um branco à direita (Caso tenha 'lamba')
    palavra_lista.extend(simbolo_vazio for _ in range(VALOR))

    trilhas.append(palavra_lista)

    if qnt_trilhas > 1:
        # Coloca trilhas em branco 'qnt de trilhas - 1' vezes, pois a primeira trilha é a entrada
        trilhas.extend([simbolo_vazio for _ in range(len(palavra_lista))] for _ in range(qnt_trilhas - 1))

def executar_maquina() -> bool: # Retornar se a palavra faz parte da linguagem ou não
    global estados
    global estado_inicial

    global transicoes
    
    global trilhas

    global alfabeto_entrada
    global alfabeto_fita

    global simbolo_inicio
    global simbolo_vazio

    global palavra

    cabecote = 1 # Começa no índice 1 (Um depois do símbolo de início da primeira trilha)
    estado_atual = estado_inicial

    while True:
        transicao = checar_transicao(estado_atual, cabecote)

        if transicao is None: # Não há transição definida
            break

        novo_estado = transicao[qnt_trilhas] # Pois indexa no 0
        simbolos_escrita = transicao[qnt_trilhas + 1:-1]
        mov = transicao[-1] # Ultimo elemento da lista

        # Vai para a esquerda e já está na primeira posição da trilha
        if mov == '<' and cabecote == 0:
            return False
        
        estado_atual = novo_estado

        indice_simbolo_escrita = 0

        for trilha in trilhas: # Escrever nas trilhas
            trilha[cabecote] = simbolos_escrita[indice_simbolo_escrita]
            indice_simbolo_escrita += 1

        if mov == '>': # Direita
            cabecote += 1

            if cabecote >= len(trilhas[0]): # Passou do tamanho da trilha, entao adicionar um branco já que é ilimitado à direita
                adicionar_branco_direita()

        else:
            cabecote -= 1

    return isFinalState(estado_atual)

def checar_transicao(estado, cabecote : int) -> list: # Caso retorne lista vazia, não há transição. Caso contrário, retorna transicao
    global transicoes
    global simbolo_inicio
    global simbolo_vazio
    global trilhas

    transicoes_validas_lista = transicoes[estado] # Todas as transições de 'estado'

    for transicao_valida in transicoes_validas_lista:
        simbolos_leitura = transicao_valida[:qnt_trilhas]

        possivel = True

        for i in range(qnt_trilhas): # Todos devem dar certo
            if trilhas[i][cabecote] != simbolos_leitura[i]:
                possivel = False
                break
        
        if possivel:
            return transicao_valida

    return None

def adicionar_branco_direita(): # Ter quantos brancos o computador conseguir
    global trilhas
    global qnt_trilhas
    global simbolo_vazio

    for i in range(qnt_trilhas):
        trilhas[i].append(simbolo_vazio)

def isFinalState(estado) -> bool:
    return estados[estado][1]

def verificar_trilhas(): # PRINT: Verificar se está montando as trilhas corretamente
    global trilhas

    for trilha in trilhas:
        print(trilha)

def verificar_transicoes(): # PRINT: Verificar se está armazenando as transições de forma correta
    global transicoes

    for chave in transicoes:
        for valor in transicoes[chave]: # Valor: transição do estado 'chave'
            print(f'Estado {chave}: {valor}')
        print()

def verificar_estados(): # PRINT: Verificar se está atribuindo a cada estado seu 'id' e se é estado final corretamente
    global estados

    for estado in estados:
        print(f'Estado: {estado}: {estados[estado]}')


argumentos = sys.argv # Primeiro argumento é o nome do programa python3

if len(argumentos) != 3:
    print("Usar: python3 TuringMachine.py [MT] [Word]")
    exit()

nome_arquivo = argumentos[1]
palavra = argumentos[2]

mt = ler_maquina_turing(nome_arquivo)['mt']

separar_elementos()
# verificar_palavra_esta_alfabeto_entrada() # Andrei disse que vai estar tudo em ordem
atribuir_numero_estado()

# verificar_estados()
# print()

colocar_transicoes_hash()
# verificar_transicoes()
# print()

fazer_trilhas()
# verificar_trilhas()

resposta = executar_maquina()

if resposta:
    print("Sim")
else:
    print("Não")   