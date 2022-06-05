
# Design Document Food Tracker
Deze applicatie streeft ernaar om mensen te ondersteunen richting
hun gewichtsdoelen. 
De applicatie doet dit door een structuur te bieden waarin zij alle 
feiten rondom hun dagelijkse voeding snel en eenvoudig vast kunnen
leggen.











## Authors

- [@Percy Hoquee](https://github.com/PercyHoquee)


## HTML
Overzicht van de momenteel benodigde html pagina's voor dit 
project.
De eerste alinea voor elke pagina geeft een beschrijving van
hoe de pagina eruit zal komen te zien. 
De tweede alinea beschrijft de geanticipeerde code uitdagingen
voor het creëren van de pagina's.
- Layout:
    - Zorgt ervoor dat als de gebruiker ingelogd is elke 
      andere pagina een sidebar krijgt met daarin links naar 
      pagina's voor de food diary, de opgeslagen
      gerechten van de gebruiker en het aanmaken van nieuwe
      producten en gerechten. 
      Ingelogde gebruikers hebben daarnaast de mogelijkheid om uit
      te loggen via de sidebar.
      Niet ingelogde gebruikers krijgen daartegenover twee links
      te zien: een link naar een inlog pagina en een link naar een
      registreer pagina.
    - In de head zal de Bootstrap stylesheet toegevoegd moeten 
      worden om toegang te krijgen tot de Bootstrap sidebar.
      In de body wordt een sidebar en main div gecreëerd.
      De sidebar div krijgt een html if statement of de gebruiker
      ingelogd is. 
      Dit statement heeft de instructies die hierboven beschreven
      staan. 
      De main div krijgt een block body statement.
- Index:
    - De index pagina toont een dag overzicht van de gebruikers
      voeding. 
      Dit overzicht bestaat uit 4 delen: Ontbijt, Lunch, Avondeten
      en Tussendoortjes. 
      Er zijn links naar pagina's om producten en gerechten aan dit 
      overzicht toe te voegen. 
      Bovenaan de pagina is een samenvatting te zien van de
      gebruikers voeding op een bepaalde dag:
      het aantal geconsumeerde calorieën, koolhydraten, eiwitten en
      vetten.
      De gebruiker kan naar overzichten van andere dagen navigeren
      via pijlen of via een kalender functie. 
    - Deze html pagina zal geroepen worden via twee url paden. 
      Als er geen datum variabele wordt gespecificeerd in de url
      wordt het overzicht van de huidige datum geladen.
      Anders, wordt het overzicht van de opgegeven datum getoond.
      De block body wordt gevuld met 4 tabellen; 
      voor elk gedeelte van het overzicht een. 
      Elke tabel krijgt vervolgens een for statement zodat alle 
      producten en gerechten een row krijgen.
- Login:
    - De pagina heeft twee invulvelden: één voor een 
      gebruikersnaam en één voor een wachtwoord. 
      Daarnaast heeft de pagina ook een inlog button. 
    - Wacht af of orginele code gebruikt kan worden.
- Registreer:
    - De pagina heeft 3 invulvelden: één voor een gebruikersnaam, 
      één voor een wachtwoord en één voor het bevestigen van
      het wachtwoord. 
      Daarnaast heeft de pagina een button waarmee de registratie
      bevestigd kan worden.
    - Wacht af of orginele code gebruikt kan worden.
- Voeg Product Toe / Voeg Gerecht Toe:
    - Gebruiker kan in een zoekbalk een zoekopdracht invullen voor
      het product of gerecht dat toegevoegd moet worden aan het 
      dagboek. 
      Naast de balk bevindt zich een button om de zoekopdracht te
      enteren.
    - De body van de pagina bevat een form met action post om de 
      producten en gerechten te kunnen vinden die aan de zoekopdracht
      voldoen. 
- Zoek Resultaten:
    - De pagina toont de producten en gerechten die voldoen aan de
      zoekopdracht van de gebruiker. 
      Als er op de producten en gerechten wordt geklikt, wordt de
      gebruiker naar een pagina genomen waar de hoeveelheden voor dat
      product of producten binnen een gerecht aangegeven kunnen worden.
    - Vanuit de functie die de pagina aanroept, worden variabelen
      meegegeven die producten en gerechten bevatten.
      Voor beide variabelen wordt binnen een unordered list (ul), een for
      statement gemaakt om voor elk product of gerecht een list item
      (li) aan te maken. In deze li zit dan een link naar de 
      landingspagina.
- Product Landingspagina:
    - Bovenaan de pagina staat de naam van het product. 
      Daaronder staan de voedingswaarden van het product per een
      bepaalde hoeveelheid, bijvoorbeeld per 100 gram of per 100 
      milliliter. 
    - De functie geeft aan om welk product het gaat. 
      Binnen een ul kan de pagina een li aanmaken voor elk attribuut
      van het product dat betrekking heeft op de voedingswaarden. 
- Gerecht Landingspagina:
    - Bovenaan de pagina staat de naam van het gerecht.
      Vervolgens staan de producten waar het gerecht uit is opgebouwd
      onder elkaar. 
      De producten zijn links naar de landingspagina's van de 
      producten
    - Als het gerecht is aangemaakt door de gebruiker, heeft hij/zij
      de mogelijkheid om een button te klikken om naar een pagina te
      gaan waar aanpassingen aan het gerecht gemaakt kunnen worden.
- Mijn Gerechten:
    - Alle gerechten die zijn aangemaakt door de gebruiker worden
      getoond.
      De gerechten zijn links naar de landingspagina's van de 
      gerechten.
    - De gerechten aangemaakt door de gebruiker kunnen verzameld 
      worden via de related name tussen het gerecht model en het 
      gebruikers model. 
      Deze gerechten kunnen vervolgens in een ul geplaatst worden 
      met een for statement om de li's te creëren.
- Nieuw Product:
    - Invulvelden voor de naam van het product, de 
      eenheid waarin de hoeveelheid wordt gemeten en de 
      voedingswaarden per 100 eenheden. 
    - Een form class zal aangemaakt worden (NewProductForm) die alle
      velden bevat. 
- Nieuw Gerecht:
    - Zoekveld om te zoeken naar producten die de gebruiker toe
      wil voegen aan het gerecht. 
      Gebruiker krijgt een lijst te zien met alle zoekresultaten.
      Als de gebruiker op een product klikt, wordt de pagina met het
      zoekveld opnieuw geladen met het aangeklikte product als 
      toegevoegd product. 
    - Body krijgt een form met als type search en action post naar 
      de zoekresultaten pagina. 
      Onder dit form komt een ul met de producten die al zijn 
      toegevoegd.
- Hoeveelheden:
- Edit Gerecht:


