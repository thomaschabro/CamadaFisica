#####################################################
# Camada Física da Computação
# Carareto
# 11/08/2022
# Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.

from enlace import *
import time
import numpy as np
import random

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)

ImageR = "./img/pixel.png"

# ------------------------------------------------------------------------------------------------------------------------------------------
# Funções necessárias 
# ------------------------------------------------------------------------------------------------------------------------------------------

def createHeader(tipo, sizePayload, index, nPackages):
    header = bytearray()
    if tipo == "handshake":
        header += b'\x00'
    elif tipo == "info":
        header += b'\x01'
    elif tipo == "erro tamanho":
        header += b'\x02'
    elif tipo == "erro index":
        header += b'\x03'
    elif tipo == "resposta":
        header += b'\x04'

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
        print ("Iniciando Handshake")
        print ("")
        payload = bytearray()
        handshake = createPackage("handshake", 0, 0, 0, payload)
        
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
                            print('Enviou um pacote como Handshake' .format(txSize))
                            print("")
                            enviou_mensagem = True
                        break
                                
            if dif > 5:
                print (" ------------------------- ")
                print ("Tempo de espera esgotado")
                print ("")
                resposta = input ("Deseja tentar novamente? (s/n)")
                print ("")
                print (" ------------------------- ")

                if resposta == "s":
                    start = time.time()
                    enviou_mensagem = False

                if resposta == "n":
                    print ("Comunicação encerrada")
                    com1.disable()
                    break
            
            if  com1.rx.getBufferLen() != 0:
                rxSize = com1.rx.getBufferLen()       
                print('Recebeu um pacote de resposta do Handshake' .format(rxSize))
                print("")
                break

        # -----------------------------------------------------------------------------------------------------------------------------------
        # Criando lista de bytes para serem enviados 
        # -----------------------------------------------------------------------------------------------------------------------------------

        n_com = random.randint(10, 15)
        print(f'Serão enviados {n_com} comandos')

        lista_comandos = [b'\x00\xFA\x00\x00', b'\x00\x00\xFA\x00', b'\xFA\x00\x00', b'\x00\xFA\x00', b'\x00\x00\xFA', b'\x00\xFA', b'\xFA\x00', b'\x00', b'\xFA']
        separador = b'\x11'
        bytearray_comandos = bytearray()
        for i in range (0,n_com):
            comando = random.choice(lista_comandos)
            bytearray_comandos += comando
            bytearray_comandos += separador

        tamanho = len(bytearray_comandos)
        
        enviar = tamanho.to_bytes(1, byteorder='little')
        
        oficial = enviar + bytearray_comandos

        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print(" ---------------------------------------------------------------------- ")
        print("Abriu a comunicação")
        print(" ---------------------------------------------------------------------- ")
           
                  
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        
    
        txBuffer = oficial

        # -----------------------------------------------------------------------------------------------------------------------------------    
        # Declarando no terminal o tamanho do arquivo a ser enviado 
        # -----------------------------------------------------------------------------------------------------------------------------------

        print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
        print(f"São {len(txBuffer) - 1} bytes de comandos + 1 byte de tamanho")
        print ("")
        string_enviados =  str(txBuffer   ).replace("b", "").replace("'", "").split("11")
        for el in string_enviados:
            print (el)
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
       
            
        #finalmente vamos transmitir os todos. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmita arrays de bytes!
                       
        # -----------------------------------------------------------------------------------------------------------------------------------    
        # Enviando os dados 
        # -----------------------------------------------------------------------------------------------------------------------------------

        com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
          
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        
        # O método não deve estar fincionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
        
        while True:
            if  com1.tx.getStatus() != 0:
                txSize = com1.tx.getStatus()       
                print('enviou = {} bytes' .format(txSize))
                break
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.

    
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen

        print ("")
        print (" ---------------------------------------------------------------------- ")
        print ("Recebendo dados")
        print (" ---------------------------------------------------------------------- ")
    
        # -----------------------------------------------------------------------------------------------------------------------------------    
        # Recebendo os dados de retorno 
        # -----------------------------------------------------------------------------------------------------------------------------------

        while True:
            rxBuffer, nRx = com1.getData(1)
            if rxBuffer != None:
                tamanho_recebido = int.from_bytes(rxBuffer, byteorder='little')
                print ("O Server recebeu {} comandos" .format(tamanho_recebido))
                print ("")
                
            if (n_com) == tamanho_recebido:
                print ("Tamanho correto")
            else:
                print ("Tamanho incorreto")
            com1.disable()
            break

        # -----------------------------------------------------------------------------------
        # Verificando 


    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
