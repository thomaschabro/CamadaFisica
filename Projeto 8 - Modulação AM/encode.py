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
    
    audio = sf.read('audio.wav',44100,5)


    dados = audio[0]
    print(dados)

    filtrado = f1.filtro(dados, 44100, 2200)
    sd.play(dados, 44100)    
    sd.wait()



    print("...     FIM")
    # ----------- Fim da gravação -----------

    return 0




if __name__ == "__main__":
    main()