# Istoric

Versiunile de lucru prin care a trecut jocul, pastrate ca sa poti compara sau reveni la ceva.
Versiunea actuala este in `src/game.html` (sursa) si `index.html` (gata de jucat).

## versiuni/

Fisierele sunt sursa jocului din acel moment (fara fonturile incluse, deci textele pot arata cu alt font).
Se deschid direct in browser.

| Fisier | Ce aducea |
|---|---|
| `01-v1.0-tiny-junctions-prima-versiune.html` | Prima versiune jucabila (numele de lucru era "Tiny Junctions"): case, magazine, drumuri si in diagonala, cai ferate, trenuri, bariere, pauza si viteza. |
| `02-v1.1-magazine-care-cresc-semafoare-giratorii-camioane.html` | Echilibrare, magazine care cresc, semafoare, sensuri giratorii, camioane de marfa. |
| `03-v1.2-alegi-orice-bonus-atribuire-pe-depozite.html` | Alegi orice bonus la sfarsit de saptamana, trenurile si camioanele se pun pe depozite, performanta. Aspectul acestei versiuni a ramas cel final. |
| `04-v1.4-sine-si-sosele-cu-panou-flota-renuntat.html` | Numele "Sine si Sosele", bonusuri noi, panoul "Flota" si litere pe depozite. **Renuntat** (aspectul nu a placut). |
| `05-v1.0-flota-si-telefon-renuntat.html` | Prima versiune de telefon, tot cu panoul "Flota". **Renuntat**. |
| `06-v1.0-aspect-clasic-telefon-pasaj-7.html` | Refacut pe aspectul din 1.2: panoul de depozit, telefon, pasaj pana la 7 patratele. |

Dupa 06 au urmat: fara notificari jos, panoul de depozit nu se mai deschide singur, `+` doar din vehiculele libere,
pasaj pana la 10 patratele, bonusuri +2 trenuri / +2 camioane. Acela este jocul actual.

## patch-uri/

Scripturile Python cu care s-au facut modificarile intre versiuni (inlocuiri de text in `src/game.html`).
Sunt pastrate doar ca istoric: au cai absolute din mediul in care au fost rulate si se aplica
doar pe versiunea pentru care au fost scrise.
