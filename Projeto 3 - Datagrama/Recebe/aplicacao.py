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
serialName = "/dev/cu.usbmodem141101"                  # Windows(variacao de)

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
            if True: #not com1.rx.getIsEmpty():
                rxBuffer, nRx = com1.getData(10)
                print("")
                if rxBuffer != None:
                    header = str(rxBuffer)
                    tipo = rxBuffer[0]
                    index = rxBuffer[1] + rxBuffer[2] + rxBuffer[3]
                    sizePayload = rxBuffer[4] + rxBuffer[5] + rxBuffer[6]
                    nPackages = rxBuffer[7] + rxBuffer[8] + rxBuffer[9]
                    print("")
                    print( "Handshake recebido")
                    print(" ------------------ ")
                    print("")
                    
                    # Limpando EOP
                    eop = com1.rx.getNData(4)

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
        ultimo_index = 0

        # Recebendo o primeiro pacote
        com1.rx.clearBuffer()
        while end:
            if not com1.rx.getIsEmpty():
                # Pega o header do pacote
                rxBuffer, nRx = com1.getData(10)
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
                    n = len(rxBuffer)
                    imagem += rxBuffer # Soma com a variável imagem
                    if (sizePayload) != (n + 4):
                        print ("Erro no tamanho do payload")
                        time.sleep(1)
                        erro_tamanho_payload = createPackage("erro tamanho", 0, 0, 0, bytearray())
                        com1.sendData(np.asarray(erro_tamanho_payload))
                        break

                    # Pega o EOP
                    rxBuffer, nRx = com1.getData(4)
                    if rxBuffer != b'\xff\xff\xff\xff':
                        print ("ERROR: EOP não encontrado")
                        time.sleep(1)
                        erro_eop = createPackage("erro eop", 0, 0, 0, bytearray())
                        com1.sendData(np.asarray(erro_eop))
                        break

                    if index != ultimo_index + 1:
                        print ("ERROR: Index errado")
                        time.sleep(1)
                        erro_index = createPackage("erro index", 0, 0, 0, bytearray())
                        com1.sendData(np.asarray(erro_index))
                        break

                    # Verifica se o pacote é o último
                    if index == nPackages:
                        time.sleep(1)
                        fim = createPackage("fim", 0, 0, 0, bytearray())
                        com1.sendData(np.asarray(fim))
                        print ("Enviando pacote de resposta ", index)
                        print ("")
                        print ("Terminou de receber o arquivo")
                        f = open(ImageW, 'wb')
                        f.write(imagem)
                        f.close()
                        end = False
                        com1.disable()
                    else:
                        end = True
                        recebeu_pacote = createPackage("resposta", 0, index, 0, bytearray())
                        time.sleep(1)
                        com1.sendData(np.asarray(recebeu_pacote))
                        print ("Enviando pacote de resposta ", index)
                        ultimo_index = index
                        # if ultimo_index == 3:
                        #     ultimo_index = 2

        

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
