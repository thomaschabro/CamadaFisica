
#Importe todas as bibliotecas
import suaBibSignal as bib
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import math
import time


#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    #*****************************instruções********************************
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como:
    signal = bib.signalMeu() 
       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    sd.default.samplerate = 44100
    sd.default.channels = 2 #numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas
    duration =  3 # #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes) durante a gracação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação

    #faca um print na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
   
    #Ao seguir, faca um print informando que a gravacao foi inicializada

    #para gravar, utilize
    audio = sd.rec(int(44100*duration), 44100, channels=1)
    
    sd.wait()
    print("gravacao finalizada")
    
    dados = audio[:,0]
    print(dados)

    print("...     FIM")



    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista, isso dependerá so seu sistema, drivers etc...
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações). 
    
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    tempo = np.linspace(0, duration, len(dados))
    # plot do áudio gravado (dados) vs tempo! Não plote todos os pontos, pois verá apenas uma mancha (freq altas) . 
       
    ## Calcule e plote o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(dados, 44100)
    plt.figure(1)
    plt.plot(xf, yf)
    #plt.axis([0, 2000, 0, 3*44100])
    plt.title("Fourier")
    plt.show()
    
    #agora, voce tem os picos da transformada, que te informam quais sao as frequencias mais presentes no sinal. Alguns dos picos devem ser correspondentes às frequencias do DTMF!
    #Para descobrir a tecla pressionada, voce deve extrair os picos e compara-los à tabela DTMF
    #Provavelmente, se tudo deu certo, 2 picos serao PRÓXIMOS aos valores da tabela. Os demais serão picos de ruídos.

    # para extrair os picos, voce deve utilizar a funcao peakutils.indexes(,,)
    # Essa funcao possui como argumentos dois parâmetros importantes: "thres" e "min_dist".
    # "thres" determina a sensibilidade da funcao, ou seja, quao elevado tem que ser o valor do pico para de fato ser considerado um pico
    #"min_dist" é relatico tolerancia. Ele determina quao próximos 2 picos identificados podem estar, ou seja, se a funcao indentificar um pico na posicao 200, por exemplo, só identificara outro a partir do 200+min_dis. Isso evita que varios picos sejam identificados em torno do 200, uma vez que todos sejam provavelmente resultado de pequenas variações de uma unica frequencia a ser identificada.   
    # Comece com os valores:
    index = peakutils.indexes(yf, thres=0.05, min_dist=50)
    print("index de picos {}" .format(index)) #yf é o resultado da transformada de fourier
    frequencias = xf[index]

    print ("")

    # Verificando valores de frequencias
    frequencias = [int(el) for el in frequencias] 
    print (frequencias)
    for el in frequencias:
        v_697 = math.isclose(el, 697, rel_tol=1)
        v_770 = math.isclose(el, 770, rel_tol=1)
        v_852 = math.isclose(el, 852, rel_tol=1)
        v_941 = math.isclose(el, 941, rel_tol=1)
        v_1209 = math.isclose(el, 1209, rel_tol=1)
        v_1336 = math.isclose(el, 1336, rel_tol=1)
        v_1477 = math.isclose(el, 1477, rel_tol=1)
        v_1633 = math.isclose(el, 1633, rel_tol=1)

    
    if v_1209 and v_697:
        f1 = 1209
        f2 = 697
        print("A tecla captada foi 1")
    elif v_1336 and v_697:
        f1 = 1336
        f2 = 697
        print("A tecla captada foi 2")
    elif v_1477 and v_697:
        f1 = 1477
        f2 = 697
        print("A tecla captada foi 3")
    elif v_1209 and v_770:
        f1 = 1209
        f2 = 770
        print("A tecla captada foi 4")
    elif v_1336 and v_770:
        f1 = 1336
        f2 = 770
        print("A tecla captada foi 5")
    elif v_1477 and v_770:
        f1 = 1477
        f2 = 770
        print("A tecla captada foi 6")
    elif v_1209 and v_852:
        f1 = 1209
        f2 = 852
        print("A tecla captada foi 7")
    elif v_1336 and v_852:
        f1 = 1336
        f2 = 852
        print("A tecla captada foi 8")
    elif v_1477 and v_852:
        f1 = 1477
        f2 = 852
        print("A tecla captada foi 9")
    elif v_941 and v_1336:
        f1 = 941
        f2 = 1336
        print("A tecla captada foi 0")

    #printe os picos encontrados! 
    # Aqui você deverá tomar o seguinte cuidado: A funcao  peakutils.indexes retorna as POSICOES dos picos. Não os valores das frequências onde ocorrem! Pense a respeito
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print o valor tecla!!!
    #Se acertou, parabens! Voce construiu um sistema DTMF

    #Você pode tentar também identificar a tecla de um telefone real! Basta gravar o som emitido pelo seu celular ao pressionar uma tecla. 

      
    ## Exiba gráficos do fourier do som gravados 
    # fs = 44100
    # duracao = 5 
    # t = np.arange(0,duracao,1/fs)
    # s1 = np.sin(2*np.pi*f1*t)
    # s2 = np.sin(2*np.pi*f2*t)
    # s = s1 + s2
    # plt.plot(t,s)
    # plt.axis([0, 0.01, -2, 2])


    plt.show()

if __name__ == "__main__":
    main()
