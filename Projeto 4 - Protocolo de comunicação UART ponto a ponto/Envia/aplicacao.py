##################################
# Camada Física da Computação
# Caio Tieri e Thomas Chabro
# Projeto 4 
# Aplicação
##################################

# Importando bibiotecas

from operator import truediv
from enlace import *
import time
import numpy as np
from datetime import date

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

    # ----- Definindo o h5 -----
    header += h5.to_bytes(1, byteorder='little')
    
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

def createPackage(tipo, h5, index, nPackages, h6, h7, payload):
    package = bytearray()
    package += createHeader(tipo, h5, index, nPackages, h6, h7)
    package += payload
    package += createEOP()

    return package


serialName = "COM3"           # Windows(variacao de)
imagem     = "./img/imagem.png"   # Imagem 


# -----------------------------------------------------------------------------------------------------------------------------------
# Criando arquivo de texto para escrever o log
# -----------------------------------------------------------------------------------------------------------------------------------


def main():
    try:
        inicia = False
        cont = 0
        log_txt = ''
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        com1.enable()

        # -----------------------------------------------------------------------------------------------------------------------------------
        # Fazendo o HANDHSAKE
        # -----------------------------------------------------------------------------------------------------------------------------------
        print ("Iniciando comunicação HANDSHAKE")
        print ("")
        log_txt += '[' + f'{date.today()} - {time.strftime("%H:%M:%S")}' + '] ' + "Iniciando comunicacao HANDSHAKE\n"

        payload = bytearray()
        handshake = createPackage("handshake_envio",0,0,0, None,0, payload)
        
        enviou_mensagem = False
        start = time.time()
        while True:
            dif = time.time() - start
            if dif < 5:
                if enviou_mensagem == False:
                    com1.sendData(np.asarray(handshake))
                    enviou_mensagem = True
                    while True:
                        if  com1.tx.getStatus() != 0:
                            txSize = com1.tx.getStatus()  
                            print('Enviou um pacote como Handshake')
                            print("")
                            log_txt += '[' + f'{date.today()} - {time.strftime("%H:%M:%S")}' + '] ' + "Enviou Handshake T1 / " + str(txSize) + " bytes\n" 
                            break

                if not com1.rx.getIsEmpty():
                    print("Recebeu um pacote")
                    rxBuffer, nRx = com1.getData(10)
                    if rxBuffer[0] == 2:
                        print (" ------------------------- ")
                        print ("")
                        print ("Handshake recebido")
                        print ("")
                        print (" ------------------------- ")
                        log_txt += '[' + f'{date.today()} - {time.strftime("%H:%M:%S")}' + '] ' + "Recebeu resposta de Hanshake T2 / 14 bytes\n"

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
                log_txt += '[' + f'{date.today()} - {time.strftime("%H:%M:%S")}' + '] ' + "Tempo de espera de Handshake esgotado (5 segundos)\n"

                if resposta == "s":
                    start = time.time()
                    enviou_mensagem = False

                if resposta == "n":
                    print ("Comunicação encerrada")
                    log_txt += '[' + f'{date.today()} - {time.strftime("%H:%M:%S")}' + '] ' + "Comunicacao encerrada"
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
        
 

        print ("Iniciando comunicação")
        print ("")
        while inicia:  
            if cont <= n_packages:
                nao_tem_t4 = True
                print ("Enviando pacote ", cont, " de ", n_packages)
                com1.rx.clearBuffer()
                com1.fisica.flush()
                payload = bytearray()
                payload = read_image[(cont-1)*114:(cont)*114]
                pacote_imagem = createPackage("dados", len(payload), (cont), n_packages, 0, 0, payload)
                log_txt += '[' + f'{date.today()} - {time.strftime("%H:%M:%S")}' + '] ' + "Enviou pacote T3 " + f'{cont}/{n_packages}' + f'/ {len(pacote_imagem)} bytes'
                timer1 = time.time()
                timer2 = time.time()
                # Envia o pacotes para o servidor
                com1.sendData(np.asarray(pacote_imagem))
                time.sleep(0.05)
                print ("Pacote enviado")
                

                
                print (" - Esperando resposta do servidor")
                while nao_tem_t4:
                    
                    if not com1.rx.getIsEmpty():
                        rxBuffer, nRx = com1.getData(10)
                        if rxBuffer[0] == 4:
                            #recebeu mensagem t4
                            print (" - Pacote enviado com sucesso!")
                            print ("")
                            log_txt += '[' + f'{date.today()} - {time.strftime("%H:%M:%S")}' + '] ' + "Recebeu resposta T4 / 14 bytes\n"
                            rxBuffer, nRx = com1.getData(4)
                            cont += 1
                            nao_tem_t4 = False    

                        if rxBuffer[0] == 6:
                            print ("Recebeu Erro no pacote")
                            log_txt += '[' + f'{date.today()} - {time.strftime("%H:%M:%S")}' + '] ' + "Recebeu pacote de erro T6 / 14 bytes\n"
                            #recebeu mensagem t6
                            timer1 = time.time()
                            timer2 = time.time()
                            
                            # Corrige contagem de pacotes para reiniciar
                            cont = rxBuffer[6]
                            nao_tem_t4 = False
                    else:
                        if time.time() - timer1 > 5:
                            com1.sendData(np.asarray(pacote_imagem))
                            time.sleep(0.05)
                            timer1 = time.time()

                        if time.time() - timer2 > 20:
                            pacote_timeout = createPackage("timeout", 0, 0, 0, 0, 0, bytearray())
                            log_txt += '[' + f'{date.today()} - {time.strftime("%H:%M:%S")}' + '] ' + "Enviou pacote de timeout T5 / 14 bytes"
                            com1.sendData(np.asarray(pacote_timeout))
                            time.sleep(0.05)
                            print('TIMEOUT')
                            print(">:-(")
                            com1.disable()
                            inicia = False
                            nao_tem_t4 = False
                            break
                            
            else:
                print ("Comunicação encerrada")
                com1.disable()
                inicia = False
            
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

    with open("log.txt", "w") as log:
        log.write(log_txt)
        log.close()

if __name__ == "__main__":
    main()