Data er hentet av Chat-Gpt og forklart av Chat-gpt. 

1. Henter alle 18 tidsseriene fra MIT-BIH Normal Sinus Rhythm Database
2. Leser et intervall på f.eks. 10 sekunder fra hver person
3. Lagrer signalene i én NumPy-array med shape:
   (18, antall_tidspunkter)
4. Lagrer også record-navn, tid og sampling rate

