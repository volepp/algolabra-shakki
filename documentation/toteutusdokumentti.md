# Toteutusdokumentti

Ohjelma koostuu ennen kaikkea pelilogiikasta, pelaajaa vastaan pelaavasta tekoälystä ja käyttöliittymästä.

Board-kansiosta löytyy pelilogiikan toteuttava koodi. Tähän kuuluu esimerkiksi laillisten siirtojen etsiminen asemasta ja pelin määrittäminen. Lisäksi moduuli sisältää esimerkiksi liikkumislogiikan jokaiselle eri nappulatyypille (piece-alimoduuli). 

Engine-moduulista puolestaan löytyy pelaajaa vastaan pelaava tekoäly. random.py-tiedostossa oleva implementaatio on testaamista varten ja valitsee joka vuorolla vain satunnaisen siirron. Engine-luokka on varsinainen tekoälytoteutus, joka perustuu minmax-algoritmiin alpha-beta pruningilla tehostettuna. 

Käyttöliittymä on game-moduulissa ja se on toteutettu kolmannen osapuolen kirjastoja (python-chess ja Lichessin Python-kirjasto) käyttäen.

## Minmax

Minmaxia on parannettu alpha-beta-karsinnalla. Alpha-beta-karsinnan performanssia on taas pyritty parantamaan siirtojen läpikäyntijärjestystä parantamalla. 

Algoritmissa on käytössä iteratiivinen syveneminen. Käytännössä tämä tarkoittaa sitä, että tilanne analysoidaan ensin syvyydellä 1 (evaluoidaan vain jokainen siirto ilman rekursiota), jonka jälkeen lähdetään analysoimaan syvyydellä 2. Kun haku on valmis, tarkistetaan menikö hakuun yli 5 sekuntia. Jos ei, siirrytään seuraavaan syvyyteen (syvyyteen 3), analysoidaan sillä, ja taas varmistetaan kauanko hakuun meni. Kun syvyyden analysointiin menee ensimmäisen kerran yli 5 sekuntia, ei siirrytä seuraavaan syvyyteen ja palautetaan edellisellä iteraatiolla löydetty paras siirto.

Läpikäyntijärjestystä parannetaan syvyydelle 2 siten, että jokainen siirto arvoidaan (syvyys 1) ja järjestetään evaluaationsa perusteella. Hakua tehdessä aina paras syvyydellä löydetty siirto talletetaan muistiin. Myöhemmillä syvyyksillä, jos positio löytyy välimuistista, nostetaan paras siirto läpikäytävien siirtojen listassa ensimmäiseksi. Tämä tehostaa alpha-beta-karsintaa nostamalla alpha- ja beta-katkaisujen todennäköisyyttä. 

## Evaluointialgoritmi

Laudan tilannetta arvioidaan heuristisesti minmax-algoritmissa, kun ohjelma etsii parasta mahdollista siirtoa. Tämän hetkinen algoritmi perustuu kahteen asiaan: materiaalin määrään sekä kontrolloitujen ruutujen määrään ja laatuun. 

Tilanteen pisteytyksen pohjaksi algoritmi ottaa materiaalitilanteen. Yksinkertaisuudessaan lasketaan valkean materiaalin määrän ja mustan materiaalin määrän erotus perinteisiä nappuloiden arvoja käyttäen (sotilas=1, ratsu&lähetti=3, torni=5, kuningatar=9).

Toinen tekijä positiota arvioidessa on pelaajien kontrolloimien ruutujen määrä ja laatu. Jokaiselle ruudulle lasketaan välillä [0,1] oleva paino. Tällä hetkellä painot ovat asetettu siten, että laudan keskimmäisille neljälle ruudulle annetaan painoarvo, jonka jälkeen muut ruudut saavat painokseen keskiruudun_painoarvo/etäisyys_keskustasta. Toisin sanoin mitä kauempana ruudut ovat keskustasta, sitä pienempi painoarvo niillä on. Jatkossa tätä voisi parantaa esimerkiksi painottamalla ruutuja vastustajan kuninkaan ympärillä ja muillakin tavoilla pyrkiä etsimään mielenkiintoisia "hotspotteja" laudalta. Lopulta positiota evaluoidessa erotetaan mustien kontrolloimien ruutujen painojen summa valkean kontrolloimien ruutujen painojen summasta.

Kun sekä materiaalin määrien erotus, että kontrolloitujen ruutujen painojen summien erotus ovat laskettu, palautetaan lopullisena pisteytyksenä näiden kahden tekijän summa.

Evaluointialgoritmia on tehostettu siten, että pelkän position lisäksi se ottaa parametriksi myös tehtävän siirron. Siirron perusteella tilanteesta laskettua "pohjaevaluaatiota" (kuvattu yllä) päivitetään siirron perusteella. Tämä vähentää huomattavasti laskentaa, joka minmaxin tarvitsee pohjatasolla tehdä (syvyys 0), koska tehtävää siirtoa ei tarvitse "simuloida" laudalla vaan sen perusteella vain päätellään, miten evaluaatio muuttuu suhteessa laudan tilanteeseen ennen siirron tekemistä.

## Aikavaativuus

Minmax on rekursiivinen algoritmi, joka käy läpi kaikki mahdolliset siirtokombinaatiot. Sen aikavaativuus kasvaa täten eksponentiaalisesti suhteessa mahdollisten siirtojen määrään (O(b^d), missä b on haarojen määrä ja d minmaxissa käytetty haun syvyys).

Alpha-beta pruningin avulla pahimmassa tapauksessa aikavaativuus ei muutu minmaxiin verrattuna. Parhaassa tapauksessa alpha-beta pruning voi kuitenkin tiputtaa aikavaativuuden neliöjuureen: O(sqrt(b^d)). 

## Tilavaativuus

Muistia käytetään oikeastaan vain pelilaudan tilanteen ylläpitämiseen. Pelilaudan positio on esitetty 8x8 taulukon avulla. Tämän lisäksi rekursiivista algoritmiä varten menneitä positioita pidetään pinossa, josta edellinen tilanne on helppo palauttaa. Täten tilan käyttö on riippuvainen siirtojen määrästä n (tilavaativuus O(n)).

## Lähteet

https://en.wikipedia.org/wiki/Minimax
https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning