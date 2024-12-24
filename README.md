# Platformer Game

## Descrierea ideii jocului

Povestea jocului il are ca protagonist pe eroul **Naruto**, fiind inspirata din
binecunoscutul serial de animatie *Naruto*. Pe parcursul aventurii, Naruto
dobandeste treptat puteri si abilitati speciale, infruntand diverse provocari
si inamici. In nivelul final, acesta se confrunta cu inamicul suprem, **Orochimaru**,
intr-o lupta epica pentru a-l salva pe prietenul sau **Sasuke**.

## Arhitectura jocului

Jocul foloseste biblioteca **Pygame** pentru a crea o aventura 2D.
Acesta are un sistem de invatare si interactiune cu diferite tipuri de inamici
si obiecte. Clasa `Game` este responsabila pentru gestionarea principalelor
componente ale jocului, inclusiv initierea, rularea si afisarea elementelor pe ecran. 
In constructorul clasei, sunt incarcate diverse resurse, cum ar fi imagini,
animatii si sunete, care sunt folosite pentru a afisa si controla playerul,
inamicii, proiectilele si efectele vizuale (norii sau particulele).

Metoda `load_level` : Este utilizata pentru a incarca un nivel, extragand
datele dintr-un fisier **JSON**. De asemenea, sunt initiate diferite obiecte,
precum **ramen-ul** si **informatiile**, care apar pe harta.

Metoda `run` : Este metoda principala a jocului, care gestioneaza cursul jocului,
actualizeaza pozitia si actiunile playerului (**Naruto**), inamicilor si
proiectilelor, afiseaza animatiile si verifica conditiile de castig sau pierdere.
De asemenea, se realizeaza actiuni precum verificarea coliziunilor, gestionarea
vietii eroului si afisarea vietii ramase pe ecran.

**Actualizarea scroll-ului** : Pentru a actualiza valorile scroll-ului, ecranul urmeaza 
pozitia jucatorului, dar se misca gradual, astfel incat sa se creeze un efect de fluiditate.
De exemplu, "self.scroll[0]" se deplaseaza lent catre pozitia jucatorului pe axa **X**.

In acest cod, **eroii** si **inamicii** sunt dotati cu proiectile, care sunt obiecte care se
misca pe ecran si interactioneaza cu mediul si cu alti obiecti, inclusiv cu jucatorul si inamicii.
Eroul si inamicii pot trage cu proiectile, obiecte care se
misca pe ecran si interactioneaza cu mediul si cu alte personaje. Pentru a le gestiona,
se utilizeaza o lista de proiectile, fiecare proiectil fiind reprezentat de un tuplu
ce contine trei elemente: pozitia, directia si un timer, pentru a nu ramane pe
ecran la infinit.

Codul gestioneaza evenimentele de intrare ale utilizatorului in joc prin verificarea 
acestora cu pygame.event.get(). La apasarea unei taste, sunt activate actiuni, precum
miscarea jucatorului, saritura, dash-ul sau atacul. Cand o tasta este eliberata, se opreste 
miscarea corespunzatoare. 

## Nivelurile

- **Primul nivel** este unul introductiv, in care prin atingerea semnului "i" (de la info),
  jucatorul afla detalii despre obiectivele jocului. Ramen (supa) va fi prezent la sfarsitul
  nivelului si va debloca o superputere: **double jump**, **dash**, prin care eroul omoara inamici, si
  trasul cu proiectile. Astfel, primul nivel se parcurge rapid.

- **Al doilea nivel** contine **double jump-ul** si trebuie evitate coliziunile cu inamicii pentru a nu muri.
  Acesti inamici nu ataca, doar nu trebuie atinsi (**potato_enemy**).

- **In al treilea nivel**, apar inamici care pot ataca cu proiectile, iar eroul poate contraataca prin **dash**.

- **In al patrulea nivel**, eroul poate ataca cu proiectile si se va lupta cu inamicul suprem, **Orochimaru**,
  pentru a-l recupera pe **Sasuke**.

## Clasele utilizate pentru personajele jocului

Clasa `PhysicsEntity` reprezinta o entitate fizica din joc, care poate 
fi un jucator sau un inamic (enemy, potato_enemy, smart_enemy).
Aceasta contine diverse atribute pentru a gestiona pozitia, dimensiunile, 
viteza, coliziunile si animatiile entitatii.

Metoda **`update(tilemap, movement)`**: Actualizeaza pozitia entitatii
in functie de miscarile curente si de coliziunile cu obiectele din harta. 
Verifica coliziunile pe axele x si y si ajusteaza pozitia entitatii pentru
a evita trecerea prin obiecte. De asemenea, aplica gravitatia, 
accelerand viteza pe axa y pana la o valoare maxima.

### Eroul

Clasa `Player` este o subclasa a clasei PhysicsEntity si reprezinta 
jucatorul din joc (Naruto). Aceasta clasa gestioneaza actiunile 
specifice ale jucatorului, cum ar fi saritura, dash-ul, atacul cu proiectile si
diverse puteri ce pot fi deblocate in timpul jocului. De asemenea, 
aceasta include si mecanisme de coliziune, update-uri ale animatiilor
si gestionarea sanatatii jucatorului.

- **`update(tilemap, movement)`**: Actualizeaza pozitia si actiunile 
jucatorului pe baza miscarilor si coliziunilor cu elementele din harta. 
De asemenea, gestioneaza animatiile si efectele de dash.

- **`check_fall()`**: Verifica daca jucatorul a cazut de pe harta.
Daca acesta e prea jos pe ecran, isi pierde viata si jocul se reincepe de 
la nivelul curent.

- **`attack()`**: Lanseaza un atac cu proiectil (disponibil doar pentru un nivel), 
daca cooldown-ul pentru atac este activ si efectueaza animatia corespunzatoare.

- **`check_ramen()`**: Verifica daca jucatorul a atins (collide) ramenul,
in ideea de a-l colecta, iar in functie de nivelul curent, deblocheaza 
superputeri precum double jump, dash sau proiectile. Ne-am folosit de acest
ramen si pentru a incarca nivelul urmator.

- **`check_info()`**: Verifica daca jucatorul a ajuns la un punct de informatie (un semn cu 
un i rosu), iar daca da, afiseaza un mesaj pe ecran (cu rolul de a-l indruma) si 
activeaza un overlay intunecat.

- **`jump()`**: Permite jucatorului sa sara, iar daca double jump-ul este activ, 
acesta poate fi folosit pentru o a doua saritura.

- **`dash()`**: Permite jucatorului sa efectueze un dash, care este o miscare rapida ce
 poate lovi inamicii si omoara. Aceasta superputere este disponibila de la
 al treilea nivel.

### Inamicii 

Clasa `potato_enemy` reprezinta un inamic simplu din joc, care se misca 
pe o directie si se intoarce atunci cand intalneste un gol in fata sa. 
Jucatorul trebuie sa evite acesti inamici, sa nu ii atinga, pentru
a-si pastra sanatatea intacta. Acesti inamici nu ataca, doar pot fi omorati.

Clasa `Enemy` reprezinta un inamic care se misca si interactioneaza cu jucatorul.
Spre deosebrie de potato_enemy, acesta poate ataca cu proiectile. Cand se opreste,
va trage un proiectil daca distanta fata de jucator este mica (mai putin de 16 pixeli).
Directia proiectilului depinde de pozitia inamicului si de starea de flip 
(daca e cu fata sau cu spatele).

Clasa `smart_enemy` reprezinta un inamic avansat, mai agil si mai adaptiv, 
care poate urmari si ataca jucatorul intr-un mod inteligent. Pentru a fi
invins, trebuie atacat, dar dispune de 10 puncte de viata. El apare la finalul
jocului si trage proiectile catre jucator daca acesta se afla in raza de tragere 
(shooting_distance). Directia si viteza gloantelor sunt ajustate in functie de
pozitia jucatorului.


## Editorul de harti

Editorul de harti este o aplicatie dezvoltata in Python folosind 
biblioteca pygame, avand ca scop facilitarea crearii si modificarii hartilor 
in format JSON printr-o interfata grafica interactiva. Acesta are multe
functionalitati intuitive: 
* Plasare tile-uri: Click stanga pentru a adauga un tile si click dreapta
pentru a sterge unul.
* Autotile: Apasand T, editorul ajusteaza automat tile-urile pentru a arata mai bine.
* Schimbare tile-uri: LShift permite selectarea variantelor unui tile, iar 
scroll-ul prin lista de tipuri de tile-uri se face cu rotita mouse-ului.
* Controlul camerei: Miscare cu tastele W, A, S, D.
* Mod on/off-grid: LCtrl activeaza/dezactiveaza grila, permitand plasarea libera a tile-urilor.
* Salvare harta: Apasand O, harta este salvata intr-un fisier JSON.

Acest editor de harti a fost realizat dupa ce am cautat si ne-am documentat
pe internet despre cum se pot crea astfel de aplicatii, deoarece nu aveam 
cunostintele necesare pentru a-l dezvolta complet de la zero.

#### Grafica jocului

Am creat personajele, elementele de peisaj si alte detalii grafice 
folosind **Libresprite**.
In cadrul acestui proces, am realizat atat modelele pentru diferitele 
personaje ale jocului, cat si diversele componente ale peisajului,
precum decoruri si alte elemente care contribuie la atmosfera jocului.

#### Sunetul

Efectele sonore utilizate in joc au fost preluate de pe internet.


## Resurse

Pentru realizarea jocului, am utilizat ca baza tutorialul realizat 
de DaFluffyPotato pe YouTube, disponibil la urmatorul link: 

https://www.youtube.com/watch?v=2gABYM5M0ww&t=20648s&ab_channel=DaFluffyPotato. 

Desi tutorialul a oferit un punct de plecare solid, am adaugat 
functionalitati suplimentare, precum colectarea de ramen, lupta cu inamicul final etc., 
care nu erau incluse in tutorial. Acestea au fost dezvoltate de noi pe parcurs, 
pentru a extinde si imbogati experienta jocului.

## Concluzie

Am avut un interes extraordinar in dezvoltarea acestui joc, 
motiv pentru care am depus o mare atentie in detaliile implementarii 
si am investit mult timp si energie pentru a-l aduce la forma dorita. 

Ne-am blocat la cateva bug-uri la finalul proiectului, care au necesitat 
timp pentru a fi depistate si corectate. Am intampinat, de asemenea, 
probleme cu afisarea textului pe ecran si cu intarzierile la redarea sunetului,
impreuna cu alte mici dificultati tehnice care au necesitat solutii improvizate 
sau ajustari ale codului pentru a functiona corect.

Acest proiect ne-a inspirat si ne-a permis sa ne testam abilitatile 
de programare si creativitatea, iar satisfactia de a-l finaliza ne-a 
dat o motivatie suplimentara pe parcursul intregului proces.

* Pentru a rula jocul, utilizatorii trebuie sa deschida terminalul
si sa execute comanda python3 game.py (sau cu executabilul)

* link github proiect: https://github.com/cuculetz11/Joculet


