##################################
# Camada Física da Computação
# Caio Tieri e Thomas Chabro
# Projeto 4 
# Aplicação
##################################

# Importando bibiotecas

import sys 
from enlace import *
import time
import numpy as np

# -----------------------------------------------------------------------------------------------------------------------------------
# Definindo funções necessárias
# -----------------------------------------------------------------------------------------------------------------------------------
def createHeader(tipo, sizePayload, id_arquivo, index, nPackages, h6, h7):
    header = bytearray()
    if tipo == "handhake_envio":
        header += b'\x01\x00\x00'
        h5 = id_arquivo.to_bytes(1, byteorder='little')
    elif tipo == "handhake_resposta":
        header += b'\x02\x00\x00'
    elif tipo == "dados":
        header += b'\x03\x00\x00'
        h5 = sizePayload.to_bytes(1, byteorder='little')
    elif tipo == "dados_resposta":
        header += b'\x04\x00\x00'
    elif tipo == "timeout":
        header += b'\x05\x00\x00'
    elif tipo == "erro":
        header += b'\x06\x00\x00'

    if h5 == None:
        h5 = b'\x00'

    header += nPackages.to_bytes(1, byteorder='little')
    header += index.to_bytes(1, byteorder='little')
    header += h5
    
    # Definindo o h6
    if h6 == None:
        header += b'\x00'
    else:
        header += h6.to_bytes(1, byteorder='little')
    
    # Definindo o h7
    header += h7.to_bytes(1, byteorder='little')

    header += b'\x00\x00'
    return header

def createEOP():
    eop = bytearray()
    eop += b'\xAA\xBB\xCC\xDD'
    return eop

def createPackage(tipo, sizePayload, id_arquivo, index, nPackages, h6, h7, payload):
    package = bytearray()
    package += createHeader(tipo, sizePayload, id_arquivo, index, nPackages, h6, h7)
    package += payload
    package += createEOP()

    return package