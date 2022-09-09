#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from cgi import print_directory
import string
from enlace import *
import time
import numpy as np

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)

ImageW = './img/RecebidaCopia.png'

# ------------------------------------------------------------------------------------------------------------------------------------------
# Funções necessárias 
# ------------------------------------------------------------------------------------------------------------------------------------------


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


# -----------------------------------------------------------------------------------------------------------------------------------
def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        com1.enable()


        # -----------------------------------------------------------------------------------------------------------------------------------
        # Fazendo o HANDHSAKE
        # -----------------------------------------------------------------------------------------------------------------------------------
        print("Esperando sinal de HANDSHAKE")
        print("")
        
        
        while True:
            if not com1.rx.getIsEmpty():
                rxBuffer, nRx = com1.getData(10)
                print(rxBuffer)
                print("")
                if rxBuffer != None:
                    header = str(rxBuffer)
                    tipo = rxBuffer[0]
                    index = rxBuffer[1] + rxBuffer[2] + rxBuffer[3]
                    sizePayload = rxBuffer[4] + rxBuffer[5] + rxBuffer[6]
                    nPackages = rxBuffer[7] + rxBuffer[8] + rxBuffer[9]
                    print("Tipo: ", tipo)
                    print("Index: ", index)
                    print("SizePayload: ", sizePayload)
                    print("nPackages: ", nPackages)
                    print("")
                    print( "Handshake recebido")
                    print(" ------------------ ")
                    print("")
                    break
                break
        
        time.sleep(1)
        if tipo == 0:
            print ("Respondendo Handshake")
            print ("")
            handshake_response = createPackage("handshake_r", 0, 0, 0, bytearray())
            com1.sendData(np.asarray(handshake_response))
            while True:
                if com1.tx.getStatus() != 0:
                    txsize = com1.tx.getStatus()
                    print (f'Enviou resposta do Handshake')
                    print ("")
                    print (" ------------------ ")
                    break

        # -----------------------------------------------------------------------------------------------------------------------------------
        # Recebendo o arquivo em pacotes
        # -----------------------------------------------------------------------------------------------------------------------------------
        print("Recebendo arquivo")
        print("")
        print(" ------------------ ")
        print("")
        print("Recebendo pacotes")
        print("")

        # Variáveis globais para depois ter certeza de que tudo foi certo
        imagem = bytearray()
        nPackages = 0
        end = True

        # Recebendo o primeiro pacote
        while end:
            if not com1.rx.getIsEmpty():
                # Pega o header do pacote
                rxBuffer, nRx = com1.getData(10)
                print(rxBuffer)
                print("")

                # Pega as informações
                if rxBuffer != None:
                    header = str(rxBuffer)
                    tipo = rxBuffer[0]
                    index = rxBuffer[1] + rxBuffer[2] + rxBuffer[3]
                    sizePayload = rxBuffer[4] + rxBuffer[5] + rxBuffer[6]
                    nPackages = rxBuffer[7] + rxBuffer[8] + rxBuffer[9]

                    # Pega o payload
                    rxBuffer, nRx = com1.getData(sizePayload)
                    imagem += rxBuffer # Soma com a variável imagem

                        
        

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
