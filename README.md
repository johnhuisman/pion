# Pion
Python-schaakatelier met Flask en python-chess (GPL-3.0-or-later).

## Starten
```
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000. Twee spelers op één bord; nog geen computertegenstander.

Alle zetten worden op de server gecontroleerd, inclusief rokade, en passant en onderpromotie. De volledige zettenhistorie blijft behouden voor herhaling en de vijftigzettenregel. Driemaal herhaling en 50 zetten zijn claimbaar (ook via een mogelijke volgende zet); vijfmaal herhaling en 75 zetten zijn automatisch remise. Schaakmat heeft voorrang. De partij wordt lokaal in de browser opgeslagen; er is geen account of online multiplayer.

## Render
Python web service, build `pip install -r requirements.txt`, start `gunicorn app:app --bind 0.0.0.0:$PORT`, health `/health`. Geen database nodig. Het project gebruikt GPL-3.0-or-later wegens python-chess.

## Tests
`python -m unittest discover -s tests -v`

## Openingstrainer
Twintig klassieke openingsfamilies, elk met twee inleidende varianten. Kies een opening, variant en kleur en druk op Start. Pion speelt de andere kleur; afwijkende legale zetten worden als afwijkingen van de gekozen oefenlijn uitgelegd. Hint onthult de zet. De eindstelling sluit de les af. De Nederlandse uitleg bestaat uit een strategisch variantplan plus een concrete beschrijving van iedere zet; dit is vaste lesinhoud, geen computeranalyse of evaluatie.

Bordstijlen: klassiek hout, groen en blauwgrijs. De keuze wordt op het apparaat bewaard. SVG-stukken worden geleverd door python-chess. Openingsnamen en korte lijnen zijn schaakfeiten; de naamgevingsreferentie is https://github.com/lichess-org/chess-openings (CC0). De commentaren zijn voor Pion geschreven.
