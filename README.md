Log

Implementerte forier ting:
*får ikke like mange frekvenser som
 fourier koefisienter.
*Må ta hensyn til dette i 
 Least Square Methode mtp nyquist
 har med komplekskonjugert å gjøre
 og siden reelt signal vil 
 komplekskonjugert bare bli kopi. 
 Derfor bruke rfft og rfftfreq for samme lengde. 


Implementere build funskjon:

*Vi kan dele opp polynomet ved å ta antall foriertransformer lik
 graden til polynomet + 1.

Plotte hjerterytmer 10 sek
*ser ut som det varierer mye med amplitude. Mye med hvor de forskjellige spikes oppstår
 og i tillegg er det mye variasjon i støy. 