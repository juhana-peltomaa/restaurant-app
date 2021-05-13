# Ravintolasovellus

Sovelluksen nykytila löytyy täältä: https://tsoha-restaurants.herokuapp.com

## Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovellus esittää tietyn alueen ravintolat kartalla, joista käyttäjä etsiä tietoa sekä lukea arvioita.

Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä. Ylläpitäjä voi lisätä uusia sekä poistaa olemassa olevia ravintoloita sovelluksesta. Käyttäjät voivat lisätä arvosteluita sovelluksessa olevien ravintoloiden tietoihin.

Käyttäjä voi myös halutessaan poistaa kaikki tietonsa sovelluksesta. 

## Käyttäjät

Sovelluksella kaksi käyttäjäroolia ns. _normaali käyttäjä_ tai _ylläpitäjä_.

## Perusversion tarjoama toiminnallisuus

### Ennen kirjautumista

- käyttäjä voi luoda järjestelmään tilin:
  - [x] uniikin käyttäjätunnuksen ja salasanan tallentaminen tietokantaan 
  - [ ] käyttäjätunnuksen tulee olla vähintään 4 merkkiä
  - [ ] salasanan tulee olla vähintään 4 merkkiä

- käyttäjä voi kirjautua järjestelmään kirjautumislomakkeella, jos:
  - [x] lomakkeelle syötetty käyttäjätunnus sekä salasana löytyvät tietokannasta 
  - [x] jos kirjautuminen epäonnistuu, järjestelmä ilmoittaa tästä käyttäjälle 

### Kirjautumisen jälkeen

- kirjautunut _normaali käyttäjä_ voi:
  - [ ] tarkastella kaikkia ravintoloita kartalla / näkymässä 
  - [ ] listata ravintolat paremmuusjärjestykseen (esim. arvosteluiden perusteella)
  - [ ] tarkastella yksittäisen ravintolan tietoja (kuvaus, aukioloajat, muiden arvostelut)
  - [ ] lisätä ravintolaan liittyvän arvostelun (sanallinen arvostelu sekä tähtiä)
  - [ ] muokata lisäämiään arvosteluita
  - [ ] etsiä lisättyjä ravintoloita hakusanoilla

- kirjautunut _ylläpitäjä_ voi (ylläolevan lisäksi):
  - [ ] lisätä uusia ravintoloita sovellukseen
  - [ ] poistaa olemassa olevia ravintoloita sovelluksesta
  - [ ] muokata sekä poistaa ravintoloihin liittyviä tietoja
  - [ ] luoda kategorioita ravintoloista (voi kuulua yhteen tai useampaan ryhmään)

- [x] käyttäjä voi kirjautua ulos järjestelmästä 

- [ ] käyttäjä voi poistaa kaikki tietonsa (käyttäjän poistaminen)

## Jatkokehitysideoita

_TBA_
