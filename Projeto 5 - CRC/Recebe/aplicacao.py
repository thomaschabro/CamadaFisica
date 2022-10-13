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
from datetime import date
from crc import CrcCalculator, Crc16

serialName = "COM4"                  # Windows(variacao de)

ImageW = './img/RecebidaCopia.png'



# -----------------------------------------------------------------------------------------------------------------------------------
# Definindo funções necessárias
# -----------------------------------------------------------------------------------------------------------------------------------
def createHeader(tipo, h5, index, nPackages, h6, h7):
    header = bytearray()
    if tipo == "handshake_envio":
        header += b'\x01\x00\x00'
    
    elif tipo == "handshake_resposta":
        header += b'\x02\x00\x00'
    elif tipo == "dados":
        header += b'\x03\x00\x00'

    elif tipo == "dados_resposta":
        header += b'\x04\x00\x00'
    elif tipo == "timeout":
        header += b'\x05\x00\x00'
    elif tipo == "erro":
        header += b'\x06\x00\x00'

    

    header += nPackages.to_bytes(1, byteorder='little')
    header += index.to_bytes(1, byteorder='little')
    header += h5.to_bytes(1, byteorder='little')
    
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

def createPackage(tipo, h5, index, nPackages, h6, h7, payload):
    package = bytearray()
    package += createHeader(tipo, h5, index, nPackages, h6, h7)
    package += payload
    package += createEOP()

    return package

def main():
    # INICIANDO CRC
    crc = CrcCalculator(Crc16.CCITT)
    try:
        img = bytearray()
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        com1.enable()
        log_txt = ''

        # -----------------------------------------------------------------------------------------------------------------------------------
        # Fazendo o HANDHSAKE
        # -----------------------------------------------------------------------------------------------------------------------------------
        print("Esperando sinal de HANDSHAKE")
        log_txt += '[' + f'{date.today()} - {time.strftime("%H:%M:%S")}' + '] ' + "Esperando sinal de Handshake\n"
        print("")
        
        ocioso = True
        esperando = True
        cont = 0
        n_pacotes = 1000000

        
        while ocioso:
          
            if not com1.rx.getIsEmpty():
                
                rxBuffer, nRx = com1.getData(10)
          
                if rxBuffer[0] ==1:
                    print("Recebido sinal de HANDSHAKE")
                    log_txt += '[' + f'{date.today()} - {time.strftime("%H:%M:%S")}' + '] ' + "Recebeu Handshake T1 / 14 bytes\n"
                    print("")
                    #pega eop
                    rxBuffer, nRx = com1.getData(4)
                    ocioso = False
            time.sleep(1)
        
        # -----------------------------------------------------------------------------------------------------------------------------------
        # Enviando resposta do HANDSHAKE
        # -----------------------------------------------------------------------------------------------------------------------------------
        print("Enviando resposta do HANDSHAKE")
        print("")

        com1.sendData(createPackage("handshake_resposta", 0, 0, 0, None, 0, b''))
        cont=1
        com1.rx.clearBuffer()
        log_txt += '[' + f'{date.today()} - {time.strftime("%H:%M:%S")}' + '] ' + "Enviou Handshake T2 / 14 bytes\n"
        
        
        #5 segundos parado print de 1 em 1 segundo
        
        print(com1.rx.getIsEmpty())
        #rxBuffer, nRx = com1.getData(40)
        while cont<= n_pacotes:
            timer1 = time.time()
            timer2 = time.time()
            esperando = True
            while esperando:
            
                
                if not com1.rx.getIsEmpty():
                    
                    rxBuffer, nRx = com1.getData(10)
                    n_pacotes = rxBuffer[3]
                    tipo = rxBuffer[0]
                    index = rxBuffer[4]
                    tamanho = rxBuffer[5]
                    ultimo_sucesso = rxBuffer[6]
                    expected = crc.crcexpected(rxBuffer[8:9])
                
                    if tipo == 3:
                       
                        
                        rxBuffer, nRx, = com1.getData(tamanho)
                        payload = rxBuffer
                       
                        rxBuffer, nRx = com1.getData(4)
                        if len(payload) == tamanho and rxBuffer == b'\xaa\xbb\xcc\xdd' and index == cont and payload == expected:
                            print("Recebido pacote de dados")
                            print("")
                            log_txt += '[' + f'{date.today()} - {time.strftime("%H:%M:%S")}' + '] ' + "Recebeu pacote de dados T3 " + f'{index}/{n_pacotes} / ' + f'{tamanho + 14}' + " bytes\n"
                            img += payload

                            com1.sendData(createPackage("dados_resposta", 0, index, 0, None, index-1, b'') )
                            print("Enviando resposta de pacote de dados")
                            log_txt += '[' + f'{date.today()} - {time.strftime("%H:%M:%S")}' + '] ' + "Enviou pacote de confirmacao de recebimento T4 / " + f'{tamanho + 14}' + " bytes\n"
                            print("")
                            esperando = False
                            cont += 1
                        else:
                            print("Erro no pacote de dados")
                            print("")
                            x = createPackage("erro", 0, index, 0, cont, index-1, b'')
                            com1.sendData(x)
                            print("Enviando resposta de erro")
                            print("")
                            log_txt += '[' + f'{date.today()} - {time.strftime("%H:%M:%S")}' + '] ' + f"Enviou pacote de erro T6 / {len(x)} bytes\n"
                            esperando = False
                            
                    else:
                        time.sleep(1)
                        if time.time() -timer2 >20:
                            ocioso = True
                            com1.sendData(createPackage("timeout",0 , 0, 0, None, 0, b'')) 
                            log_txt += '[' + f'{date.today()} - {time.strftime("%H:%M:%S")}' + '] ' + "Enviou pacote de timeout T5 / 14 bytes\n"
                            esperando = False
                            print(">:-(")
                            com1.disable()
                        else:
                            if time.time() - timer1>2:
                                #envia mensagem t4???
                                timer1 = time.time()
                            else:
                                esperando = True
        
        f = open(ImageW, 'wb')
        f.write(img)
        log_txt += '[' + f'{date.today()} - {time.strftime("%H:%M:%S")}' + '] ' + "Imagem recebida com sucesso\n"
        f.close()

        # Escrevendo log
        with open('log_client.txt', 'w') as f:
            f.write(log_txt)
            f.close()

        com1.disable()  


# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

 # -----------------------------------------------------------------------------------------------------------------------------------

 # -----------------------------------------------------------------------------------------------------------------------------------

 # -----------------------------------------------------------------------------------------------------------------------------------

                        



    except Exception as erro:
        log_txt += '[' + f'{date.today()} - {time.strftime("%H:%M:%S")}' + '] ' + "Erro: " + str(erro) + "\n"
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
