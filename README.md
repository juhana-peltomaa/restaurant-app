# Ravintolasovellus

Sovelluksen nykytila löytyy täältä: https://tsoha-restaurants.herokuapp.com

Sovelluksen testaamista varten voi luoda uuden käyttäjän tai käyttää valmiiksi luotua _normaalikäyttäjää_
 - Käyttäjätunnus: **test@test.fi**
 - Salasana: **test**
tai _ylläpitäjä_ toiminnallisuuksilla olevaa käyttäjää
 - Käyttäjätunnus: **admin@admin.fi**
 - Salasana: **admin**

Tällä hetkellä sovelluksessa olevat toiminnallisuudet näkyvillä listauksessa alla.

## Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovellukseen voidaan lisätä ravintoloita, arvosteluja sekä tarkastella ravintoloiden tietoja. 

Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä. Ylläpitäjä voi lisätä uusia sekä poistaa olemassa olevia ravintoloita sovelluksesta. Käyttäjät voivat lisätä arvosteluita sovelluksessa olevien ravintoloiden tietoihin.

## Käyttäjät

Sovelluksella kaksi käyttäjäroolia ns. _normaali käyttäjä_ tai _ylläpitäjä_.

## Perusversion tarjoama toiminnallisuus

### Ennen kirjautumista

- käyttäjä voi luoda järjestelmään tilin:
  - [x] uniikin käyttäjätunnuksen ja sähköpostin tallentaminen tietokantaan 
  - [x] jos annetut tiedot eivät ole uniikkeja, sovellus ilmoittaa tästä käyttäjälle

- käyttäjä voi kirjautua järjestelmään kirjautumislomakkeella, jos:
  - [x] lomakkeelle syötetty sähköposti sekä salasana löytyvät tietokannasta 
  - [x] jos kirjautuminen epäonnistuu, sovellus ilmoittaa tästä käyttäjälle 

- kirjatumaton käyttäjä voi: 
  - [x] tarkastella olemassa olevia ravintoloita
  - [x] lukea ravintoloiden arvosteluja, mutta ei luoda uusia 

### Kirjautumisen jälkeen

- kirjautunut _normaali käyttäjä_ voi:
  - [x] lisätä ravintolaan liittyviä arvosteluita (sanallinen sekä tähtiä)
  - [x] poistaa lisäämiään arvosteluita 
  - [x] muokata lisäämiään arvosteluita
  - tarkastella ravintolaan liittyviä tietoja:
    - [x] kuvausta
    - [x] kaikki arvostelut
  - [x] tarkastella ravintoloita kategorioittain  
  - [x] lisätä ravintolan suosikkilistaan 
  - tarkastella profiiliaan, jossa
    - [x] näkee käyttäjän perustiedot (sähköposti ja käyttäjätunnus)
    - [x] kaikki lempiravintolansa 

- kirjautunut _ylläpitäjä_ voi (ylläolevan lisäksi):
  - [x] lisätä uusia ravintoloita sovellukseen
  - [x] poistaa olemassa olevia ravintoloita sovelluksesta
  - [x] muokata lisättyjen ravintoloiden tietoja
  - [x] lisätä ravintolan kategoriaan

- [x] käyttäjä voi kirjautua ulos järjestelmästä 

## Jatkokehitysideoita

- Ravintoloiden listaaminen kartalla
- Käyttäjän profiilin muokkaaminen / kuvan lisääminen
- Etsiä lisättyjä ravintoloita hakusanoilla
- Listata ravintolat paremmuusjärjestykseen (esim. arvosteluiden perusteella)
- Käyttäjän toimintoihin liittyvää statistiikkaa (lisättyjen arvosteluiden määrät, keskiarvot yms)
- Käyttäjä voi poistaa kaikki tietonsa (käyttäjän poistaminen)

