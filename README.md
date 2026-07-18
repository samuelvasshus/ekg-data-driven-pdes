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

Fremtidig:
*Leste noe om koplede systemer av diff likninger som reproduserer. Går ann å se på senere.

I tillegg noe om å sette høyreside lik en sum sin og cos. Forier aktig. Og ignorere homogen løsning siden disse går mot 0. Og hvis de divergerer gir ikke det mening heller. Hjerterytme hos en frisk person er jo en stabil prosess. U_k = H(ikw_0)*F(k)
Men hvis man skal se på unormale hjerteslag er sikkert homogen løsning mer interesann. 
handler om hvordan systemet forsterker og reduserer forskjellige frekvenser.
hvis H(ikw) er kompleks får man også faseforskyvning.

U_k omtrent= 1/N * u_hat

Ordenen sier noe om hvor mye intern dynamikk eller hukommelse et system har. 

Planen blir å få det til å fungere med et polynom først. Og deretter kan jeg utforske med sum av sin og cos på høyreside. 

noen ting å huske på:

Hvilke frekvenser:
samme som fft for time_series
Da er det hvertfall lett å ta foriertransform og gjøre least square
Men skal man da gjø least square i det hele tatt?

filtrere bort høye støyfrekvenser.
Vi bør ikke bruke mange frekvenser. helst samme kompleksitet som venstre side for tolkbarhet. 


Least squares:
Har implementert funksjonalitet for least squares slik at det tar hnsyn til hvilken koefisient man setter = 1. Least square returnerer også cost. 

Første resultat:

Ser ut til å fungere relativt greit. Det er hvertfall riktig størrelsesorden. Litt usikker på det at difflikningen blir kompleks. Er dette siden realdelen av en kompleks difflikning er den beste løsningen, eller er det siden det er så mye støy i dataen. imaginære tall introduserer jo ofte mer sin og cos vil jeg tro, og det kan jo gi mening med EKG som er periodisk. Jeg vil tro at det å ta med imaginære delen blir litt likt som å ha et system av difflikninger. Det blir jo feil men kanskje det kan være interessant. 