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



def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
        
           
                  
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        
        #txBuffer = imagem em bytes!
       
            
        #finalmente vamos transmitir os todos. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmita arrays de bytes!

        
               
        
        # com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
          
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        
        # O método não deve estar fincionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
        
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.

        print(" ---------------------------------------------------------------------- ")
    
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        inicio  = time.time()
        diferenca = 0
        while diferenca < 5:
            diferenca = time.time() - inicio
            if not com1.rx.getIsEmpty():
                rxBuffer, nRx = com1.getData(1)
                if rxBuffer != None:
                    tamanho = int.from_bytes(rxBuffer, byteorder='little')
                    
                    
                    rxBuffer, nRx = com1.getData(tamanho)
                        
                    comandos_recebidos = rxBuffer        
                            
                    lista_comandos = str(comandos_recebidos).replace("b", "").replace("'", "").split("11")   
                    lista_comandos.remove("")
                    print (lista_comandos)
                    print (f"Foram recebidos {len(lista_comandos)} comandos")
                    for el in lista_comandos:
                        print (el)
                        
                    print("Fim da aplicação")


                    # ------------------------------------------------------------------------------------------------------------
                    # Vai enviar para o Client o tamanho recebido
                    print ("")
                    print (" ---------------------------------------------------------------------- ")
                    print ("Enviando 'relatório' para o Client")
                    print (" ---------------------------------------------------------------------- ")

                    txbuffer = len(lista_comandos).to_bytes(4, byteorder='little')
                    com1.sendData(np.asarray(txbuffer))

                    while True:
                        if  com1.tx.getStatus() != 0:
                            txSize = com1.tx.getStatus()       
                            print(f'Avisou o Client que recebeu {len(lista_comandos)} comandos' .format(txSize))
                            break

                    # ------------------------------------------------------------------------------------------------------------
                    
                
                    # Encerra comunicação
                    print("")
                    print("-------------------------")
                    print("Comunicação encerrada")
                    print("-------------------------")
                    com1.disable()
                    break

        if diferenca > 5:
            print ("Tempo excedido (5 segundos)")
            com1.disable()
            

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
