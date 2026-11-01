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
