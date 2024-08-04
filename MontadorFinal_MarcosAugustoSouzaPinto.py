"""
Trabalho: Montador Final
Autor: Marcos Augusto de Souza Pinto
Matrícula: 21755102
Disciplina: Organização de Computadores
"""

import re
import sys
from itertools import combinations

OPERACOES_4BITS={
    "ADD": "1000",
    "SHR": "1001",
    "SHL": "1010",
    "NOT": "1011",
    "AND": "1100",
    "OR": "1101",
    "XOR": "1110",
    "CMP": "1111",
    "LD": "0000",
    "ST": "0001",
}

OPERACOES_5BITS = {
    "IN": "01110",
    "OUT": "01111"
}

OPERACAO_FINALIZA = {
    "HALT" :"01000000"
}
OPERACOES_6BITS_RB_ADDR = {
    "DATA": "001000"
}
OPERACOES_6BITS_RB = {
    "JMPR": "001100"
}
OPERACOES_8BITS = {
    "CLF": "01100000"
}

OPERADORES_ESPERADOS = {
    "OPERACOES_4BITS":["Reg","Reg"],
    "OPERACOES_5BITS":["Str", "Reg"],
    "OPERACOES_6BITS_RB_ADDR":["Reg","Num"],
    "OPERACAO_FINALIZA": [],
    "OPERACOES_6BITS_RB":["Reg"],
    "JUMPS":["Num"],
    "OPERACOES_8BITS": []
}
REGISTRADORES = {
    "R0": "00",
    "R1": "01",
    "R2": "10",
    "R3": "11"
}

OPERANDOS_IN_OUT ={
    "ADDR" :"1",
    "DATA" :"0"
}
def remover_posicoes_vazias(lista):
    return [item for item in lista if item]

def tratar_espaco(linha):
    return [item.strip().upper() for sublist in linha for item in sublist.split(',')]

def gerar_combinacoes(letras):
    return [''.join(c) for i in range(1, len(letras) + 1) for c in combinations(letras, i)]

def gerar_padroes(letras, combinacoes):
    padroes = {}
    for combinacao in combinacoes:
        padrao = ['0'] * len(letras)
        for letra in combinacao:
            padrao[letras.index(letra)] = '1'
        padroes["J" + combinacao] = "0101" + ''.join(padrao)
    return padroes

def gerar_jumps_condicionais(letras):
    return gerar_padroes(letras, gerar_combinacoes(letras))

JUMPS = gerar_jumps_condicionais("CAEZ") 
JUMPS.update({"JMP": "01000000"})

OPERACOES = {}
OPERACOES['OPERACOES_4BITS'] = OPERACOES_4BITS
OPERACOES['OPERACOES_5BITS'] = OPERACOES_5BITS
OPERACOES['OPERACOES_6BITS_RB_ADDR'] = OPERACOES_6BITS_RB_ADDR
OPERACOES['OPERACOES_6BITS_RB'] = OPERACOES_6BITS_RB
OPERACOES['OPERACOES_8BITS'] = OPERACOES_8BITS
OPERACOES['JUMPS'] = JUMPS
OPERACOES['OPERACAO_FINALIZA'] = OPERACAO_FINALIZA

print(OPERACOES)
def validar_quantidade_operando(lista_operadores, operadores):
    if not operadores:
        return None if lista_operadores else True
    if len(operadores) > 2:
        return None
    tipos_operadores = [verificar_operando(operando)[0] for operando in operadores]
    if tipos_operadores != lista_operadores:
        return None
    return True

def verificar_operacao(dicionarios, instrucao):
    for nome_dic, dic in dicionarios.items():
        if instrucao in dic:
            return (nome_dic, dic[instrucao])
    return None

def verificar_hexadecimal(operando):
    if operando.startswith("0X"):
        operando = operando[2:]
    if re.match(r'^[0-9A-Fa-f]+$', operando):
        valor = int(operando, 16)
        if 0 <= valor <= 0xFF:
            return format(valor, '02X')
    return None

def verificar_binario(operando):
    if operando.startswith("0B"):
        operando = operando[2:]
    if re.match(r'^[01]+$', operando):
        valor = int(operando, 2)
        if 0 <= valor <= 0b11111111:
            return format(valor, '02X')
    return None

def verificar_decimal(operando):
    if operando.isdigit():
        valor = int(operando)
        if 0 <= valor <= 255:
            return format(valor, '02X')
    return None


def verificar_operando(operando):
    operando = operando.upper()
    
    if operando in REGISTRADORES:
        return "Reg", REGISTRADORES[operando]
    
    if operando in OPERANDOS_IN_OUT:
        return "Str", OPERANDOS_IN_OUT[operando]
    
    for verificador in [verificar_hexadecimal, verificar_binario, verificar_decimal]:
        resultado = verificador(operando)
        print(resultado)
        if resultado:
            return "Num", resultado
    
    return None

def obter_instrucoes(linha):
    return tratar_espaco(linha.strip().split())

def binario_para_hexadecimal(binario):
    valor_decimal = int(binario, 2)
    return format(valor_decimal, '02X')

def validar_instrucao(instrucoes):
    dicionario, instrucao_principal = verificar_operacao(OPERACOES,instrucoes[0])
    if instrucao_principal is None:
        print(f"Instrução '{instrucoes[0]}' não é válida.")
        return None

    if(dicionario == "OPERACAO_FINALIZA" ):
        instrucoes_binarias = [instrucao_principal]
        instrucoes_binarias.append('maike616')
    else:
        instrucoes_binarias = [instrucao_principal]
        operandos = remover_posicoes_vazias(instrucoes[1:])
        if(validar_quantidade_operando(OPERADORES_ESPERADOS[dicionario], operandos) is None):
            print(f"Operandos incorretos para a instrução '{instrucoes[0]}' ela espera algo no formato {OPERADORES_ESPERADOS[dicionario]}.")
            return None
        else:
            for operando in operandos:
                print(operando)
                operando_verificado = verificar_operando(operando)
                if operando_verificado is None:
                    print(f"Operando '{operando}' não é válido.")
                    return None
                tipo_operando, valor = operando_verificado
                if tipo_operando == "Reg":
                    instrucoes_binarias[0] += valor
                elif tipo_operando == "Str":
                    instrucoes_binarias[0] += valor
                else:
                    instrucoes_binarias.append(valor)
    instrucoes_binarias[0] = binario_para_hexadecimal(instrucoes_binarias[0])
    return instrucoes_binarias

def gerar_arquivo_memoria(memory, arq_output):
    with open(arq_output, 'w') as arquivo:
        arquivo.write('v3.0 hex words addressed\n')
        for endereco, instrucao in enumerate(memory):
            if instrucao == 'maike616':
                instrucao = format(endereco - 1, '02x')
            arquivo.write(f'{endereco:02x}: {instrucao}\n')


def ler_arquivo_assemble(arq_input):
    try:
        with open(arq_input, 'r') as arquivo:
            linhas = [linha.rstrip('\n') for linha in arquivo if linha.strip()]
    except FileNotFoundError:
        print(f"O arquivo {arq_input} não foi encontrado.")
        return []
    except IOError:
        print(f"Erro ao ler o arquivo {arq_input}.")
        return []
    memory = []
    indice = 0
    for linha in linhas:
        instrucoes = obter_instrucoes(linha.upper())
        print(instrucoes, indice)
        if (instrucoes[0] != "SWAP"):
            instrucao_validada = validar_instrucao(instrucoes)
            if instrucao_validada is None:
                print(f"Não vai ser possível gerar o {sys.argv[2]} porque a instrucão {obter_instrucoes(linha)} não é valida ou esta faltando operadores (Os espaços excedentes serão tratados em instruções válidas)")
                return None
            else:
                memory.extend(instrucao_validada)
        if instrucoes[0] == "SWAP":
            operandos = remover_posicoes_vazias(instrucoes[1:])
            nova_lista = []
            nova_lista.append(["XOR", operandos[0], operandos[1]])
            nova_lista.append(["XOR", operandos[1], operandos[0]])
            nova_lista.append(nova_lista[0])
            
            for elemento in nova_lista:
                instrucao_validada = validar_instrucao(elemento)
                memory.extend(instrucao_validada)
    return memory


input_file_name = sys.argv[1]
output_file_name = sys.argv[2]
memory = ler_arquivo_assemble(input_file_name)
if(memory is not None):
    print(f'Arquivo de saida: {output_file_name} gerado com sucesso!')
    gerar_arquivo_memoria(memory, output_file_name)

