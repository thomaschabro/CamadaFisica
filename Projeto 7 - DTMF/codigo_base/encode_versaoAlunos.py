
#importe as bibliotecas
import sys
import suaBibSignal as bib
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)




def main():
    BibSignal = bib.signalMeu()
   
    #********************************************instruções*********************************************** 
    # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    # agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    # Essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # Lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    # O tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Construa com amplitude 1.
    # Some as senoides. A soma será o sinal a ser emitido.
    # Utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # Grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    

    print("Inicializando encoder")
    dicionario = {'1':(697,1209), '2':(697,1336), '3':(697,1477), '4':(770,1209), '5':(770,1336), '6':(770,1477), '7':(852,1209), '8':(852,1336), '9':(852,1477),  '0':(941,1336)}
    numero = input("Digite um numero de 0 a 9: ")
    print("Aguardando usuário")
    print("Voce digitou o numero: ", numero)
    f1,f2 = dicionario[numero]
    print("Frequencias: ", f1, f2)
    fs = 44100
    duracao = 5 
    t = np.arange(0,duracao,1/fs)
    s1 = np.sin(2*np.pi*f1*t)
    s2 = np.sin(2*np.pi*f2*t)
    s = s1 + s2

    print("Gerando Tons base")
    print("Executando as senoides (emitindo o som)")
    print("Gerando Tom referente ao símbolo : {}".format(numero))
    sd.play(s, fs)
    # Exibe gráficos
    # aguarda fim do audio
    sd.wait()
    BibSignal.plotFFT(s, fs)
    plt.figure()
    plt.plot(t,s)
    # plt.legend(['s'])
    plt.axis([0, 0.01, -2, 2])
    plt.show()
    

if __name__ == "__main__":
    main()
