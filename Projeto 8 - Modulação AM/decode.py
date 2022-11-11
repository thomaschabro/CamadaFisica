#Importe todas as bibliotecas
import suaBibSignal as bib
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import soundfile as sf
import math
import time
import filtro as f1


def main():
    signal = bib.signalMeu() 
    sd.default.samplerate = 44100
    sd.default.channels = 2
    duration = 5  # seconds


    
    # ----------- Obtendo o sinal modulado -----------
    audio = sf.read('modulada.wav')
    print(audio[0])
    t = np.arange(0,duration,1/44100)
    portadora = np.sin(2*np.pi*14000*t)
    desmodulada = audio[0]*portadora


    filtrada = f1.filtro(desmodulada, 44100, 2200)

    sd.play(filtrada, 44100)
    sd.wait()

    #graficos
    plt.figure(0)
    plt.plot(t, desmodulada)
    plt.title("Sinal de áudio desmodulado")
    plt.xlabel("Tempo")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()

    plt.figure(1)
    signal.plotFFT(desmodulada, 44100)
    plt.title("Fourier do sinal de áudio desmodulado")
    plt.xlabel("Frequência")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()

    plt.figure(2)
    signal.plotFFT(filtrada, 44100)
    plt.title("Sinal de áudio filtrado")
    plt.xlabel("Frequência")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()


    
if __name__ == "__main__":
    main()