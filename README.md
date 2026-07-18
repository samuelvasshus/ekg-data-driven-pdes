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


En feil!

Ikke glattet ut i staten. Når jeg rekner ut initialverdiene blir de utrolig støyete. Jeg må rekne deriverte på en eller annen måte slik at støyen ikke påvirker. Det gjør at hele greia divergerer.

Det virker som om kost funksjonen er feil. Når jeg plotter og ser hva som passer best visuelt, sier costfunksjonen noe helt annet. 

Jeg hadde nå konstan på venstre og konstant på høyre siden polynomaldegree right var 1 automatisk. Får fikse det etterpå. Men kanskje var dette riktig. At jeg hadde litt flaks. Egentlig misforstod jeg, men formen på difflikningen ble a1u + a2u_t + a3u_tt = a4, som var det jeg ville ha. når pol degree = 1. altså konstant. Når jeg setter a2 = 1, får jeg bedre løsning enn a1 = 1. mister periodisitet. 

når a3 tvinges lik 1 divergerer løsningen mot uendelig. 