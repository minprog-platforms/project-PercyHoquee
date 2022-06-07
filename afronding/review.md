# Review
Dit document bevat een code review uitgevoerd door de schrijver van de code review (Percy Hoquee, 12711926).
Deze review is introspectief, omdat door omstandigheden geen partners beschikbaar waren om de review door uit te laten voeren.
De review is gericht op de kwaliteit van de code (i.e., organisatie, begrijpelijkheid, stijl). 

## views .py
Op het gebied van organisatie en begrijpelijkheid komen weinig problemen naar voren.
De organisatie vloeide redelijk natuurlijk van basisfuncties naar de overige functies met product- en gerechtgerelateerde functies om en om.
Binnen de functie is er geen bewuste volgorde genomen bij het definiëren van variabelen.
Die vloeide ook meer natuurlijk uit de rol van variabelen binnen de functie en/of parameters van de functie,
voorbeeld: een variabele "favorite" komt meestal na "products" of "meals", maar binnen de functie "favorites" komt "favs" als eerst. 
Verder zijn de functies redelijk woordelijk wat ze eenvoudiger maakt om te begrijpen.
Zo had de schrijver 5 maanden niet aan de code gewerkt en waren er in views .py geen opstartproblemen toen hij weer begon.
Als gevolg waren er ook relatief weinig extra comments nodig buiten de functie comments.
Dit voelde onwennig, maar de schrijver wilde ook niet onnodig comments toevoegen. 
Stijlistisch zijn er meer opmerkingen.
Allereerst had het filteren van de verschillende klasses meer gestandaardiseerd kunnen worden door vaak na elkaar volgende filters in functies te stoppen.
Voorbeelden hiervan zijn:
```
diary = request.user.diary
entry = diary.entries.get(date=date)
```
```
products = Product.objects.filter()
meals = Meal.objects.filter()
```
Verder gebeurt het voorkomen van errors op verschillende plekken door te hardcoden waarbij de gebruiker
geen extra bericht krijgt anders dan de hulp informatie die in de sidebar staat. 
```
if  date == '':
	return  HttpResponseRedirect(reverse("index"))
else:
	return  HttpResponseRedirect(reverse("alt", args=(date,)))
```
views .py lijn 180
```
if  amount == '':
	return HttpResponseRedirect(reverse("add_product",args=(product_id, date,)))
```
views .py lijn 192
Op de plek waar wel een error message gebruikt wordt, weerhoudt dat de schrijver ook gelijk van het gebruiken van een HttpResponseRedirect:
```
return  render(request, "food_tracker/add_meal.html", {
	"meal": Meal.objects.get(id=meal_id),
	"date": date,
	"message": "Er Zijn Nog Geen Voorkeuren Ingesteld Voor Dit Product"
	})
```
views .py lijn 555
Een oplossing voor beide was het gebruik van een custom template tag file die de verschillende errors bevat.
Hiermee kunnen errors, zoals een niet ingevulde variabele,
worden verwerkt door het html bestand en kan in views .py een HttpResponseRedirect gebruikt worden om de actie aan te geven die volgt op een error.
Deze oplossing is ook verkent door de schrijver, maar de documentatie die het gebruik uitlegt, was te moeilijk om te implementeren in een kort tijdsbestek. 
Als laatste had de herhaling van bepaalde functies, vergelijkbare functies voor product en gerecht,
voorkomen kunnen worden als het gebruik van optionele parameters in django's urls .py intensiever verkent was.
Functies als "add_product_favorite" en "add_meal_favorite" zijn identiek aan elkaar op het gebruik van een "product_id" en
"meal_id" na en hadden samengevoegd kunnen worden. 
## HTML
In de html bestanden vallen twee dingen op. Ten eerste is het ontwerp van "meal.html" inefficiënt.
Door in de functie "meal" in views .py een variabele mee te geven die de producten bevat, had de "results_layout" gebruikt kunnen worden en
had herhaling van de "wrapper-grid" en alles daarbinnen voorkomen kunnen worden. Ten tweede het volgende stukje dat voorkomt in "add_meal.html" en "default.html":
```
{% for product in meal.product.all %}
	<!--Attempt to use preference amounts-->
	{% if product in products %}
		{% for default in defaults %}
			{% if product == default.product %}
				<label  for="preference">{{ product.name }} 		({{ product.unit }})</label>
				<input  id="preference"  type="number"  name="{{ product.id }}"  value="{{ default.amount }}"  min="0">
			{% endif %}
		{% endfor %}
	{% else %}
```
add_meal.html lijn 35
Het doel van dit stukje code is om een input tag te vullen met een waarde die de gebruiker opgeslagen heeft.
De meerdere loops en if-statements maken het stukje code moeilijk te begrijpen waarbij het doel ook niet duidelijk naar voren komt.
Op het eerste oog lijken "meal.product.all" en "products" om dezelfde waarden te gaan, terwijl dat niet het geval is.
Betere variabele namen zouden iets meer duidelijkheid kunnen geven.
Verder heeft de schrijver lang geprobeerd om betere code te schrijven voor dit stukje, maar is dat niet gelukt.
Een mogelijke oplossing die tijdens de review naar boven komt, is een nieuwe klasse maken die alle informatie bevat die de loops produceren,
maar ook dat lijkt de schrijver niet heel efficient. 

Schoonheid: 
- De radio opties voor het toevoegen van producten hebben nog de Engelse vertaling voor ontbijt en avondeten. Oplossing: simpelweg aanpassen in html bestand.
- De cijfers in de tabellen op de index pagina worden niet beperkt tot een bepaald aantal decimalen, waardoor de tabellen vervormd kunnen raken als er een
dwalende decimaal wordt meegegeven. Oplossing: javascript's (niet gebruikt voor deze opdracht) toFixed() functie beperkt het aantal decimalen tot het aantal aangegeven door de schrijver.
- Als de gebruiker besluit geen naam mee te geven aan een product of gerecht, wordt het kaartje van dat product of gerecht anders dan die met naam. 
De kaartjes zonder naam zijn korter van zichzelf, maar als ze naast eentje met naam staan worden ze uitgestrekt, waardoor de "voeg toe" button niet meer op de juiste 
plek staat en er onderaan het kaartje een wit gebied te zien is. (Deel)oplossing: required toevoegen aan de "naam" input regelt dat er tenminste iets ingevuld moet worden, maar dan alsnog kan de gebruiker alleen een spatie invullen.
## CSS
Binnen de css bestanden is duidelijk de keuze gemaakt om meer te letten op het organiseren van deel tot deel dan totale efficiëntie,
zie indeling van "form.scss" met de verschillende soorten forms als indeling.
Voor de styling van het project heeft de schrijver gebruik gemaakt van de code van verschillende programmeurs.
Deze hebben allemaal hun eigen stijl. De schrijver heeft gekozen om de stijl van deze programmeurs aan te houden en
de code alleen aan te passen om hem werkend te krijgen.
De verschillende css files die de applicatie gebruikt zijn dan ook niet uniform in style, 
zo gebruikt de programmeur op wie "results.scss" exclusief rem als eenheid, terwijl de andere files voornamelijk pixels gebruiken voor margins, padding etc.:
```
margin: 0.5rem  2rem;
```
results.scss lijn 35
vs.
```
margin: 0px;
```
layout.scss lijn 13
Verder had er meer gebruikt gemaakt kunnen worden van relatieve eenheden om afmetingen aan te geven. 
```
grid-template-rows: 0.4fr  0.4fr  minmax(500px, auto) 1fr;
```
layout.scss lijn 163
Indien de schrijver voor de minmax gebruik maakte van twee relatieve afmetingen,
bijvoorbeeld minmax(100%, auto), werkte het niet naar wens, waardoor de schrijver heeft gekozen om in deze instantie 500px te hardcoden.
De oplossing hiervoor zou zijn om simpelweg langer tijd te besteden om de relatieve eenheden passend en werkend te maken.
