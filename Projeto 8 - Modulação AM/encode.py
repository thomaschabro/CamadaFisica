#Importe todas as bibliotecas
import suaBibSignal as bib
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import math
import time
import soundfile as sf
import filtro as f1
import filtro2 as f2

def main():
    signal = bib.signalMeu() 
    sd.default.samplerate = 44100
    sd.default.channels = 2
    duration = 5  # seconds
    
    # ----------- Gravando o sinal -----------
    audio = sd.rec(int(44100*duration), 44100, channels=1)
    
    sd.wait()

    sf.write('audio.wav', audio, 44100)
    

    
    print("gravacao finalizada")
    #salva audio
    
    
    t = np.arange(0,5,1/44100)

    dados = audio[:,0]
    dados_norm = dados/np.max(abs(dados))
    

    print(dados)

    filtrado = f1.filtro(dados, 44100, 2200)
    # sd.play(filtrado, 44100)    
    # sd.wait()

    
    portadora = np.sin(2*np.pi*14000*t)
    modulada = filtrado*portadora
    normalizada = modulada/max(abs(modulada))
    sf.write('modulada.wav', normalizada, 44100)
    


    # PLOTANDO GRAFICOS
    plt.figure(0)
    plt.plot(t, dados_norm)
    plt.title("Sinal de áudio original normalizado")
    plt.xlabel("Tempo")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()

    plt.figure(1)
    plt.plot(t, filtrado)
    plt.title("Sinal de áudio filtrado")
    plt.xlabel("Tempo")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()

    plt.figure(2)
    signal.plotFFT(filtrado, 44100)
    plt.title("Fourier do sinal filtrado")
    plt.show()

    plt.figure(3)
    plt.plot(t, modulada)
    plt.title("Sinal de áudio modulado")
    plt.xlabel("Tempo")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()

    plt.figure(4)
    signal.plotFFT(modulada, 44100)
    plt.title("Fourier do sinal modulado")
    plt.show()

    




    print("...     FIM")
    # ----------- Fim da gravação -----------


if __name__ == "__main__":
    main()