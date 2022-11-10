#Importe todas as bibliotecas
import suaBibSignal as bib
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import math
import time

def main():
    signal = bib.signalMeu() 
    sd.default.samplerate = 44100
    sd.default.channels = 2
    duration = 5  # seconds
    
    # ----------- Gravando o sinal -----------
    audio = sd.rec(int(44100*duration), 44100, channels=1)

    sd.wait()
    print("gravacao finalizada")
    
    dados = audio[:,0]
    print(dados)

    print("...     FIM")
    # ----------- Fim da gravação -----------

    return 0




if __name__ == "__main__":
    main()