#####################################################
# Camada Física da Computação
# Carareto
# 11/08/2022
# Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.

import sys
from enlace import *
import time
import numpy as np
import random

# -----------------------------------------------------------------------------------------------------------------------------------
# Definindo funções necessárias
# -----------------------------------------------------------------------------------------------------------------------------------

def createHeader(tipo, sizePayload, index, nPackages):
    header = bytearray()
    if tipo == "handshake":
        header += b'\x00'
    elif tipo == "handshake_r":
        header += b'\x01'
    elif tipo == "info":
        header += b'\x02'
    elif tipo == "erro tamanho":
        header += b'\x03'
    elif tipo == "erro index":
        header += b'\x04'
    elif tipo == "resposta":
        header += b'\x05'
    elif tipo == "erro eop":
        header += b'\x06'
    elif tipo == "fim":
        header += b'\x07'

    header += index.to_bytes(3, byteorder='little')
    header += sizePayload.to_bytes(3, byteorder='little')
    header += nPackages.to_bytes(3, byteorder='little')

    return header

def createEOP():
    eop = bytearray()
    eop += b'\xff\xff\xff\xff'
    return eop

def createPackage(tipo, sizePayload, index, nPackage, payload):
    package = bytearray()
    package += createHeader(tipo, sizePayload, index, nPackage)
    package += payload
    package += createEOP()

    return package

sys.path.insert(0, 'C:/Users/55119/OneDrive/Área de Trabalho/Insper/4 SEMESTRE/CAMFIS/CamadaFisica/Projeto 3 - Datagrama/functions.py')

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)

imagem = "./img/pixil-frame-0.png" # Imagem 

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        com1.enable()

        # -----------------------------------------------------------------------------------------------------------------------------------
        # Fazendo o HANDHSAKE
        # -----------------------------------------------------------------------------------------------------------------------------------
        print ("Iniciando Handshake")
        print ("")
        payload = bytearray()
        handshake = createPackage("handshake", 0,0,0, payload)
        
        enviou_mensagem = False
        start = time.time()
        while True:
            dif = time.time() - start
            if dif < 5:
                com1.sendData(np.asarray(handshake))
                while True:
                    if  com1.tx.getStatus() != 0:
                        txSize = com1.tx.getStatus()  
                        if enviou_mensagem == False:
                            print('Enviou um pacote como Handshake')
                            print("")
                            enviou_mensagem = True
                        break



                if not com1.rx.getIsEmpty():
                    print("Recebeu um pacote")
                    rxBuffer, nRx = com1.getData(10)
                    if rxBuffer[0] == 1:
                        print (" ------------------------- ")
                        print ("")
                        print ("Handshake recebido")
                        print ("")
                        print (" ------------------------- ")
                        break
                                
            if dif > 5:
                print (" ------------------------- ")
                print ("")
                print ("Tempo de espera esgotado")
                print ("")
                resposta = input ("Deseja tentar novamente? (s/n) ")
                print ("")
                print (" ------------------------- ")

                if resposta == "s":
                    start = time.time()
                    enviou_mensagem = False

                if resposta == "n":
                    print ("Comunicação encerrada")
                    com1.disable()
                    break

        # -----------------------------------------------------------------------------------------------------------------------------------
        # Fragmentando o arquivo de imagem em partes
        # -----------------------------------------------------------------------------------------------------------------------------------
        com1.rx.clearBuffer()
        read_image = open(imagem, 'rb').read()
        size_image = len(read_image)
        print ("Tamanho total da imagem: ", size_image)

        # Definido o tamanho do payload
        n_packages = size_image // 114
        if size_image % 114 != 0:
            n_packages += 1


        time.sleep(3)
        # Criando o payload
        payload = bytearray()
        for i in range(n_packages):
            payload = read_image[i*114:(i+1)*114]
            pacote_imagem = createPackage("info", len(payload), (i+1), n_packages, payload)
            print ("")
            
            # Envia o pacote i para o servidor
            com1.sendData(np.asarray(pacote_imagem))
            while True:
                if  com1.tx.getStatus() != 0:
                    txSize = com1.tx.getStatus()  
                    print(f'Pacote {i+1} de {n_packages} enviado')
                    break

            # Recebe a resposta do servidor de que recebeu o pacote
            while True:
                if not com1.rx.getIsEmpty():
                    rxBuffer, nRx = com1.getData(10)
                    if rxBuffer[0] == 5:
                        print(f'Confirmação recebida')
                        com1.rx.clearBuffer()
                        break
                    elif rxBuffer[0] == 4:
                        print(f'Erro no index')
                        com1.rx.clearBuffer()
                        com1.disable()
                        break
                    elif rxBuffer[0] == 3:
                        print(f'Erro no tamanho')
                        com1.rx.clearBuffer()
                        com1.disable()
                        break
                    elif rxBuffer[0] == 6:
                        print(f'Erro no EOP')
                        com1.rx.clearBuffer()
                        com1.disable()
                        break
                    elif rxBuffer[0] == 7:
                        print(f'Pacote enviado com sucesso')
                        com1.rx.clearBuffer()
                        com1.disable()
                        break
        

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
