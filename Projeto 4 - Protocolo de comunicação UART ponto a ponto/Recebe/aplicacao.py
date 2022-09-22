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

serialName = "/dev/cu.usbmodem142101"                  # Windows(variacao de)

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
    try:
        img = bytearray()
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        com1.enable()


        # -----------------------------------------------------------------------------------------------------------------------------------
        # Fazendo o HANDHSAKE
        # -----------------------------------------------------------------------------------------------------------------------------------
        print("Esperando sinal de HANDSHAKE")
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
                    
                    print("o index é", index)
                    print("a cont é", cont)
                    
                    if tipo == 3:
                       
                        
                        rxBuffer, nRx, = com1.getData(tamanho)
                        payload = rxBuffer
                       
                        rxBuffer, nRx = com1.getData(4)
                        if len(payload) == tamanho and rxBuffer == b'\xaa\xbb\xcc\xdd' and index == cont:
                            print("Recebido pacote de dados")
                            print("")
                            print(payload)
                            img += payload

                            com1.sendData(createPackage("dados_resposta", 0, index, 0, None, index-1, b'') )
                            print("Enviando resposta de pacote de dados")
                            print("")
                            esperando = False
                            cont += 1
                        else:
                            print("Erro no pacote de dados")
                            print("")
                            com1.sendData(createPackage("erro", 0, index, 0, cont, index-1, b''))
                            print("Enviando resposta de erro")
                            print("")
                            esperando = False
                            
                    else:
                        print ("entrou no else")
                        time.sleep(1)
                        if time.time() -timer2 >20:
                            ocioso = True
                            com1.sendData(createPackage("timeout",0 , 0, 0, None, 0, b'')) 
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
        f.close()
        com1.disable()  


# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

 # -----------------------------------------------------------------------------------------------------------------------------------

 # -----------------------------------------------------------------------------------------------------------------------------------

 # -----------------------------------------------------------------------------------------------------------------------------------

                        



    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
