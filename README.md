# Ravintolasovellus

Sovelluksen nykytila löytyy täältä: https://tsoha-restaurants.herokuapp.com

Tällä hetkellä sovelluksessa olevat toiminnallisuudet näkyvillä listauksessa alla.

## Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovellukseen voidaan lisätä ravintoloita, arvosteluja sekä tarkastella ravintoloiden tietoja. 

Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä. Ylläpitäjä voi lisätä uusia sekä poistaa olemassa olevia ravintoloita sovelluksesta. Käyttäjät voivat lisätä arvosteluita sovelluksessa olevien ravintoloiden tietoihin.

Käyttäjä voi myös halutessaan poistaa kaikki tietonsa sovelluksesta. 

## Käyttäjät

Sovelluksella kaksi käyttäjäroolia ns. _normaali käyttäjä_ tai _ylläpitäjä_.

## Perusversion tarjoama toiminnallisuus

### Ennen kirjautumista

- käyttäjä voi luoda järjestelmään tilin:
  - [x] uniikin käyttäjätunnuksen ja salasanan tallentaminen tietokantaan 
  - [x] jos annetut tiedot eivät ole uniikkeja, sovellus ilmoittaa tästä käyttäjälle

- käyttäjä voi kirjautua järjestelmään kirjautumislomakkeella, jos:
  - [x] lomakkeelle syötetty käyttäjätunnus sekä salasana löytyvät tietokannasta 
  - [x] jos kirjautuminen epäonnistuu, sovellus ilmoittaa tästä käyttäjälle 

### Kirjautumisen jälkeen

- kirjautunut _normaali käyttäjä_ voi:
  - [x] lisätä uusia ravintoloita sovellukseen
  - [x] lisätä ravintolaan liittyviä arvosteluita (sanallinen sekä tähtiä)
  - [x] poistaa lisäämiään arvosteluita 
  - [x] muokata lisäämiään arvosteluita
  - tarkastella ravintolaan liittyviä tietoja:
    - [ ] kuvaus/aukioloajat
    - [x] kaikki arvostelut
  - [ ] etsiä lisättyjä ravintoloita hakusanoilla
  - [ ] listata ravintolat paremmuusjärjestykseen (esim. arvosteluiden perusteella)

- kirjautunut _ylläpitäjä_ voi (ylläolevan lisäksi):
  - [ ] lisätä uusia ravintoloita sovellukseen
  - [ ] poistaa olemassa olevia ravintoloita sovelluksesta
  - [ ] muokata sekä poistaa ravintoloihin liittyviä tietoja
  - [ ] luoda kategorioita ravintoloista (voi kuulua yhteen tai useampaan ryhmään)

- [x] käyttäjä voi kirjautua ulos järjestelmästä 

- [ ] käyttäjä voi poistaa kaikki tietonsa (käyttäjän poistaminen)

## Jatkokehitysideoita

- Ravintoloiden listaaminen kartalla
- Käyttäjän profiilin muokkaaminen / kuvan lisääminen
