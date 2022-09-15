##################################
# Camada Física da Computação
# Caio Tieri e Thomas Chabro
# Projeto 4 
# Aplicação
##################################

# Importando bibiotecas

from operator import truediv
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

    header += nPackages.to_bytes(1, byteorder='little')
    header += index.to_bytes(1, byteorder='little')

    # ----- Definindo o h5 -----
    try:
        header += h5
    except:
        header += b'\x00'    
    
    # ----- Definindo o h6 -----
    if h6 == None:
        header += b'\x00'
    else:
        header += h6.to_bytes(1, byteorder='little')
    
    # ----- Definindo o h7 ------
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


serialName = "COM3"                  # Windows(variacao de)
imagem = "./img/imagem.png"   # Imagem 


def main():
    try:
        inicia = False
        cont = 0
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        com1.enable()

        # -----------------------------------------------------------------------------------------------------------------------------------
        # Fazendo o HANDHSAKE
        # -----------------------------------------------------------------------------------------------------------------------------------
        print ("Iniciando comunicação HANDSHAKE")
        print ("")
        payload = bytearray()
        handshake = createPackage("handshake_envio", 0,1,0,0,0,0, payload)
        
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

                        inicia = True
                        cont   = 1
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
        # Fragmentando o arquivo de imagem
        # -----------------------------------------------------------------------------------------------------------------------------------
        com1.rx.clearBuffer()
        read_image = open(imagem, 'rb').read()
        size_image = len(read_image)
        print ("Tamanho total da imagem: ", size_image)

        # Definido o tamanho do payload
        n_packages = size_image // 114
        if size_image % 114 != 0:
            n_packages += 1


        # -----------------------------------------------------------------------------------------------------------------------------------
        # Inicia o envio de arquivos  
        # -----------------------------------------------------------------------------------------------------------------------------------
        while inicia:  
            if cont <= n_packages:
                com1.rx.clearBuffer()
                com1.tx.clearBuffer()
                payload = bytearray()
                payload = read_image[cont*114:(cont+1)*114]
                pacote_imagem = createPackage("info", len(payload), (cont+1), n_packages, payload)
                print ("")
                timer1 = time.time()
                timer2 = time.time()
                # Envia o pacotes para o servidor
                com1.sendData(np.asarray(pacote_imagem))
                
                rxBuffer, nRx = com1.getData(10)
                if rxBuffer[0] == 4:
                    #recebeu mensagem t4
                    pass


                    
                if len(rxBuffer)==0:
                    if time.time() - timer1 > 5:
                        com1.sendData(np.asarray(pacote_imagem))
                        timer1 = time.time()
                    else:
                        if time.time() - timer2 > 20:
                            pacote_timeout = createPackage("timeout", 0, 0, 0, 0, 0, 0, bytearray())
                            com1.sendData(np.asarray(pacote_timeout))
                            print('TIMEOUT')
                            print(">:-(")
                            com1.disable()
                            inicia = False
                        else:
                            rxBuffer, nRx = com1.getData(10)
                            if rxBuffer[0] == 6:
                                #recebeu mensagem t6
                                timer1 = time.time()
                                timer2 = time.time()

                            else:
                                pass

                
                

            

                while True:
                    if  com1.tx.getStatus() != 0:
                        txSize = com1.tx.getStatus()  
                        print(f'Pacote {cont+1} de {n_packages} enviado')
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
            else:
                cont = 1

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
    
if __name__ == "__main__":
    main()