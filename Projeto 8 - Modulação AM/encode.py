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
    # audio = sd.rec(int(44100*duration), 44100, channels=1)
    
    # sd.wait()

    # sf.write('audio.wav', audio, 44100)
    

  
    print("gravacao finalizada")
    #salva audio
    
    audio = sf.read('audio.wav')


    dados = audio[0]
    print(dados)

    filtrado = f1.filtro(dados, 44100, 2200)
    # sd.play(filtrado, 44100)    
    # sd.wait()
    t = np.arange(0,5,1/44100)
    portadora = np.sin(2*np.pi*14000*t)
    modulada = filtrado*portadora
    normalizada = modulada/max(abs(modulada))
    sd.play(normalizada, 44100)
    sd.wait()






    print("...     FIM")
    # ----------- Fim da gravação -----------

    return 0




if __name__ == "__main__":
    main()