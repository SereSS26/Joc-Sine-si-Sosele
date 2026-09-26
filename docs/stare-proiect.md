# Sine si Sosele - stare proiect (versiunea 1.0)

Joc minimalist de trafic, inspirat de Mini Motorways: masini + trenuri + camioane.
Versiunea 1.0 merge pe calculator si pe telefon.

## Decizii de design
- Aspectul ramane cel cu **panoul de depozit** (click pe depozit -> panou mic langa el). Panoul **Flota**
  si literele de pe depozite au fost **scoase** (s-a incercat in 1.4, dar aspectul clasic a placut mai mult).
- Atribuirea vehiculelor e **strict manuala**, din panoul de depozit:
  - `+` pune pe depozit doar un vehicul **liber**; fara vehicule libere butonul e inactiv
    (NU ia vehicule de la alte depozite).
  - `-` scoate imediat vehiculul (devine liber, marfa din drum se anuleaza).
    Mutarea intre depozite = `-` la depozitul vechi, apoi `+` la cel nou.
  - Bulinele colorate aleg ce culori de magazine aprovizioneaza depozitul.
  - Vehiculele castigate la bonusul saptamanal raman libere; panoul NU se deschide singur.
- **Fara notificari in timpul jocului**: mesajele din partea de jos sunt dezactivate. Raman: clipirea
  butonului unei resurse epuizate, textele de pe harta (+1, ACCIDENT, NIVEL) si ecranul "Cum se joaca".
- Meniurile sunt fara diacritice.

## Ce contine jocul
- Harta pe grid 48x30 care se mareste in fiecare saptamana. 5 orase: Cluj, Timisoara, Brasov, Constanta,
  Bucuresti (deblocare cu 80 de livrari in orasul anterior).
- Case colorate -> magazine de aceeasi culoare; drumuri si in diagonala.
- Magazinele cresc pe 3 niveluri (20 / 50 de livrari).
- Marfa: trenuri (6 lazi, cale ferata) si camioane (4 lazi, drum).
- Treceri la nivel: fara bariera pot aparea accidente; bariera opreste masinile cand vine trenul.
- **Pasaj (drum suspendat)**: in linie dreapta sau pe diagonala, peste pana la **10 patratele** (`VIA_MAX=10`).
  Trece peste cale ferata, apa, munti si alte drumuri (nu peste cladiri). Costa 1 pasaj, capetele devin drum.
  Apasat pe o trecere la nivel o transforma in pasaj. Stergerea unui capat il scoate si da pasajul inapoi.
- Intersectii (3+ drumuri): fara control trec pe rand; semafor; sens giratoriu.
- Resurse la start: 36 drum, 18 sina, 3 poduri, 1 bariera, 1 semafor; depozitul are 1 tren si 1 camion.
- Bonus saptamanal: +15 drum si un bonus ales dintre toate: trenuri +2, camioane +2, cale ferata +20,
  drumuri +30, poduri +7, bariere +2, pasaj +1, semafoare +5, sens giratoriu +3.

## Telefon
- Un deget construieste; doua degete = zoom si mutare; buton de reincadrare; rotita = zoom pe calculator.
- Interfata compacta; pe orizontal bara de unelte e verticala in stanga. Panoul de depozit apare jos
  (vertical) sau in dreapta (orizontal).
- Pachet instalabil (PWA) in `mobile/`, merge offline; `sine-si-sosele-web.zip` pentru itch.io.
- Testat pe iPhone 13 (vertical si orizontal) si Pixel 7 emulate, cu atingeri reale.

## Tehnic
- Un singur fisier HTML/JavaScript (canvas 2D), fonturi incluse, pas fix 1/60 s.
- Grid cu muchii in 8 directii (`roadE`/`railE`), Dijkstra cu heap si cache per magazin/depozit
  (pasajele sunt muchii lungi in `JUMPS`).
- Trafic pe cozi pe segmente; intersectii cu `canEnter`, faze de semafor, arce de sens giratoriu.
- Desenare pe 3 straturi: teren (offscreen), static (drumuri, cai ferate, cladiri), dinamic (vehicule).
- Masurat la sfarsit de joc: simulare ~0,04 ms/pas, desenare ~0,35 ms/cadru, redesenare la construire ~1 ms.
- Salvare in `localStorage` (`tinyjunctions_save_v1`, nume pastrat pentru compatibilitate).
- Aplicatie desktop Electron 44 + electron-builder 26 (Sine si Sosele.exe / .app), testata.
- Echilibru: botul din `unelte/bot-echilibru.js` supravietuia in medie ~8-11 saptamani
  (masurat inainte de marirea bonusurilor, deci jocul e acum ceva mai usor).

## Pasi urmatori
1. Test cu jucatori reali si ajustarea dificultatii.
2. Publicare versiune de telefon (itch.io / Netlify), verificarea numelui.
3. Steamworks + Steam Direct, pagina Coming Soon, trailer.
4. Idei de continut nou: vezi [idei-viitoare.md](idei-viitoare.md).
