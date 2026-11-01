"""Twenty classical opening families, two introductory lines each.
Move sequences are chess facts; Dutch teaching notes are original to Pion.
"""
import chess

# name, strategic introduction, (variation, SAN sequence, variation plan)
CATALOG = [
('Spaans', 'Wit ontwikkelt rustig en verhoogt de druk op e5. Het centrum blijft vaak lang gespannen.', [
('Gesloten variant','e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7 Re1 b5 Bb3 d6 c3 O-O','Met c3 bereidt wit d4 voor. Zwart houdt het centrum stevig en ontwikkelt eerst.'),
('Ruilvariant','e4 e5 Nf3 Nc6 Bb5 a6 Bxc6 dxc6 O-O f6 d4 exd4 Qxd4 Qxd4 Nxd4','Wit geeft het loperpaar op voor een gunstiger pionnenstructuur. Zwart krijgt actieve lopers.')]),
('Italiaans', 'De loper op c4 richt zich op f7. Snelle ontwikkeling en een goed getimede d4 zijn belangrijke thema’s.', [
('Giuoco Piano','e4 e5 Nf3 Nc6 Bc4 Bc5 c3 Nf6 d4 exd4 cxd4 Bb4+ Nc3 Nxe4 O-O','Wit bouwt met c3 en d4 een centrum op. Zwart reageert actief op de centrale pionnen.'),
('Tweepaardenspel','e4 e5 Nf3 Nc6 Bc4 Nf6 Ng5 d5 exd5 Na5 Bb5+ c6 dxc6 bxc6 Be2','De aanval op f7 dwingt zwart tot actief tegenspel. Met d5 opent zwart het centrum.')]),
('Schots', 'Wit opent vroeg het centrum met d4. Daardoor worden ontwikkeling en concrete zetten direct belangrijk.', [
('Klassieke variant','e4 e5 Nf3 Nc6 d4 exd4 Nxd4 Bc5 Be3 Qf6 c3 Nge7','Zwart ontwikkelt met tempo tegen het paard op d4. Wit houdt het centrum onder controle.'),
('Schots gambiet','e4 e5 Nf3 Nc6 d4 exd4 Bc4 Bc5 c3 Nf6 cxd4 Bb4+ Nc3','Wit stelt het terugslaan op d4 uit en geeft ontwikkeling voorrang. Let op aanvallen op f7.')]),
('Russisch', 'Zwart valt e4 meteen aan in plaats van e5 te verdedigen. Vaak ontstaat een symmetrische centrale structuur.', [
('Klassieke variant','e4 e5 Nf3 Nf6 Nxe5 d6 Nf3 Nxe4 d4 d5 Bd3 Bd6 O-O O-O','Beide spelers bouwen een centrum op en brengen hun koning in veiligheid.'),
('Steinitz-aanval','e4 e5 Nf3 Nf6 d4 exd4 e5 Ne4 Qxd4 d5 exd6 Nxd6','Wit wint ruimte met e5. De zet exd6 is hier en passant: de pion op d5 wordt geslagen.')]),
('Vierpaardenspel', 'Beide spelers ontwikkelen eerst hun paarden. Een rustige opbouw kan snel overgaan in een open centrum.', [
('Spaanse variant','e4 e5 Nf3 Nc6 Nc3 Nf6 Bb5 Bb4 O-O O-O d3 d6','De symmetrische ontwikkeling vraagt om een goed voorbereid centraal plan.'),
('Schotse variant','e4 e5 Nf3 Nc6 Nc3 Nf6 d4 exd4 Nxd4 Bb4 Nxc6 bxc6 Bd3 d5','De ruil op c6 verandert de pionnenstructuur. Zwart antwoordt met een centrale doorbraak.')]),
('Koningsgambiet', 'Wit biedt de f-pion aan om lijnen te openen. De witte koning wordt kwetsbaarder; ontwikkeling moet compensatie geven.', [
('Aangenomen gambiet','e4 e5 f4 exf4 Nf3 g5 h4 g4 Ne5 Nf6','Zwart probeert de extra pion vast te houden. Wit tast de pionnenketen aan met h4.'),
('Geweigerd gambiet','e4 e5 f4 Bc5 Nf3 d6 Nc3 Nf6 Bc4 Nc6','Zwart neemt het offer niet aan en ontwikkelt rustig. Wit behoudt meer ruimte in het centrum.')]),
('Weens', 'Wit ontwikkelt het damepaard vóór het koningspaard en houdt de mogelijkheid f4 open.', [
('Weens gambiet','e4 e5 Nc3 Nf6 f4 d5 fxe5 Nxe4 Nf3 Be7','Zwart beantwoordt de flankaanval met d5 in het centrum. Wit ontwikkelt om de open lijnen te benutten.'),
('Rustige opbouw','e4 e5 Nc3 Nc6 Bc4 Nf6 d3 Bc5 Nf3 d6','Beide partijen ontwikkelen en ondersteunen hun centrum. Rokeren ligt voor de hand.')]),
('Siciliaans', 'Met c5 bestrijdt zwart d4 vanaf de flank. De ongelijke pionnenstructuur geeft beide spelers verschillende plannen.', [
('Najdorf','e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 a6 Be3 e5 Nb3 Be6','De zet a6 houdt witte stukken van b5. Met e5 wint zwart ruimte maar verzwakt d5.'),
('Draak','e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Be3 Bg7 f3 O-O Qd2 Nc6','De loper op g7 kijkt over de lange diagonaal. Wit bereidt vaak lange rokade en een koningsaanval voor.')]),
('Frans', 'Zwart ondersteunt d5 met e6. De loper op c8 heeft minder ruimte, maar zwart kan het witte centrum met c5 aanvallen.', [
('Doorschuifvariant','e4 e6 d4 d5 e5 c5 c3 Nc6 Nf3 Qb6','Wit wint ruimte met e5. Zwart richt druk op de basis van de keten: d4.'),
('Winawer','e4 e6 d4 d5 Nc3 Bb4 e5 c5 a3 Bxc3+ bxc3 Ne7','Zwart ruilt een loper voor structurele schade. Wit krijgt het loperpaar en ruimte.')]),
('Caro-Kann', 'Met c6 bereidt zwart d5 voor zonder de loper op c8 op te sluiten.', [
('Klassieke variant','e4 c6 d4 d5 Nc3 dxe4 Nxe4 Bf5 Ng3 Bg6 h4 h6','Zwart ontwikkelt de loper buiten de pionnenketen. Wit wint tempo door die loper aan te vallen.'),
('Doorschuifvariant','e4 c6 d4 d5 e5 Bf5 Nf3 e6 Be2 c5 O-O Nc6','Wit houdt ruimte. Zwart valt de keten later met c5 aan en ontwikkelt de stukken daarachter.')]),
('Scandinavisch', 'Zwart valt e4 onmiddellijk aan. Na een vroege dameruil of dame-uitval moet zwart op ontwikkeling letten.', [
('Dame naar a5','e4 d5 exd5 Qxd5 Nc3 Qa5 d4 Nf6 Nf3 c6 Bc4 Bf5','Wit ontwikkelt met tempo tegen de dame. Op a5 kan de dame druk over de vijfde rij uitoefenen.'),
('Moderne variant','e4 d5 exd5 Nf6 d4 Nxd5 Nf3 g6 Bc4 Nb6 Bb3 Bg7','Zwart ontwikkelt eerst een paard en haalt de pion later terug. De loper komt op de lange diagonaal.')]),
('Pirc', 'Zwart laat wit een breed centrum innemen en wil dat later met pionnen en stukken aanvallen.', [
('Klassieke variant','e4 d6 d4 Nf6 Nc3 g6 Nf3 Bg7 Be2 O-O O-O','Wit ontwikkelt rustig. Zwart zoekt later tegenspel met e5 of c5.'),
('Oostenrijkse aanval','e4 d6 d4 Nf6 Nc3 g6 f4 Bg7 Nf3 O-O Bd3 Na6','Wit bouwt een groot pionnencentrum. Zwart moet tijdig druk op dat centrum organiseren.')]),
('Aljechin', 'Zwart lokt witte pionnen naar voren en probeert het vooruitgeschoven centrum later aan te vallen.', [
('Moderne variant','e4 Nf6 e5 Nd5 d4 d6 Nf3 Bg4 Be2 e6 O-O','Wit ontwikkelt achter zijn pionnen. Zwart verhoogt de druk op d4 en de verdediger op f3.'),
('Ruilvariant','e4 Nf6 e5 Nd5 d4 d6 c4 Nb6 exd6 cxd6 Nc3 g6','Wit vereenvoudigt de centrale spanning. Zwart krijgt een halfopen c-lijn en een centrale pionnenmeerderheid.')]),
('Damegambiet', 'Wit biedt de c-pion aan om de zwarte d-pion van het centrum weg te lokken.', [
('Geweigerd: orthodox','d4 d5 c4 e6 Nc3 Nf6 Bg5 Be7 e3 O-O Nf3 Nbd7','Zwart houdt d5 stevig vast. Wit ontwikkelt en houdt de spanning tussen c4 en d5 in stand.'),
('Aangenomen','d4 d5 c4 dxc4 Nf3 Nf6 e3 e6 Bxc4 c5 O-O a6','Wit haalt de pion met ontwikkeling terug. Zwart probeert met c5 het witte centrum aan te vallen.')]),
('Slavisch', 'Zwart ondersteunt d5 met c6 en houdt de diagonaal voor de loper op c8 open.', [
('Hoofdvariant','d4 d5 c4 c6 Nf3 Nf6 Nc3 dxc4 a4 Bf5 e3 e6','Met a4 voorkomt wit dat zwart de extra pion gemakkelijk met b5 ondersteunt.'),
('Ruilvariant','d4 d5 c4 c6 cxd5 cxd5 Nc3 Nf6 Nf3 Nc6 Bf4 Bf5','De symmetrische structuur maakt actieve stukplaatsing en controle over de c-lijn belangrijk.')]),
('Nimzo-Indisch', 'Zwart pent het paard op c3 en bestrijdt e4 met stukken. Een ruil op c3 kan witte dubbelpionnen geven.', [
('Rubinstein','d4 Nf6 c4 e6 Nc3 Bb4 e3 O-O Bd3 d5 Nf3 c5 O-O','Wit ontwikkelt solide. Zwart zet druk op het centrum voordat wit e4 kan doorzetten.'),
('Klassiek: Dc2','d4 Nf6 c4 e6 Nc3 Bb4 Qc2 O-O a3 Bxc3+ Qxc3 b6','De dame kan op c3 terugslaan zonder dubbelpionnen. Dat kost wit wel ontwikkeltijd.')]),
('Konings-Indisch', 'Zwart geeft wit ruimte en zoekt later tegenaanval met e5 of c5. De loper op g7 is een belangrijk stuk.', [
('Klassieke variant','d4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Nf3 O-O Be2 e5 O-O Nc6 d5 Ne7','Het centrum sluit. Wit kan op de damevleugel spelen; zwart bereidt vaak f5 op de koningsvleugel voor.'),
('Sämisch','d4 Nf6 c4 g6 Nc3 Bg7 e4 d6 f3 O-O Be3 c5 d5 e6','Met f3 ondersteunt wit e4 en houdt de mogelijkheid van lange rokade. Zwart valt het centrum aan.')]),
('Grünfeld', 'Zwart laat wit een groot centrum vormen en valt het direct aan met d5, c5 en de loper op g7.', [
('Ruilvariant','d4 Nf6 c4 g6 Nc3 d5 cxd5 Nxd5 e4 Nxc3 bxc3 Bg7 Nf3 c5','Wit krijgt een breed pionnencentrum. Zwart richt zijn stukken en pionnen tegen d4.'),
('Russische variant','d4 Nf6 c4 g6 Nc3 d5 Nf3 Bg7 Qb3 dxc4 Qxc4 O-O e4','Wit haalt de pion met de dame terug en houdt het centrum breed. Zwart krijgt tempo’s tegen die dame.')]),
('Hollands', 'Met f5 bestrijdt zwart e4. De zet geeft ruimte op de koningsvleugel maar verzwakt ook de eigen koning.', [
('Stonewall','d4 f5 g3 Nf6 Bg2 e6 Nf3 d5 O-O Bd6 c4 c6','De pionnen op f5, e6, d5 en c6 vormen een muur. Het veld e5 en de loper op c8 vragen aandacht.'),
('Leningrader','d4 f5 g3 Nf6 Bg2 g6 Nf3 Bg7 O-O O-O c4 d6 Nc3','Zwart combineert f5 met een fianchetto. De voorbereiding van e5 is vaak het centrale plan.')]),
('Engels', 'Wit begint met c4 en beïnvloedt d5 vanaf de flank. De opbouw kan flexibel naar andere structuren overgaan.', [
('Omgekeerd Siciliaans','c4 e5 Nc3 Nf6 g3 d5 cxd5 Nxd5 Bg2 Nb6 Nf3 Nc6','Wit speelt een Siciliaanse structuur met omgekeerde kleuren en een extra tempo.'),
('Symmetrische variant','c4 c5 Nc3 Nc6 g3 g6 Bg2 Bg7 Nf3 Nf6 O-O O-O','Beide spelers ontwikkelen symmetrisch. Een goed getimede d4-doorbraak kan de symmetrie verbreken.')]),
]


def move_note(board, move):
    """Concrete explanation for each move, supplemented by the variation plan."""
    who = 'Wit' if board.turn else 'Zwart'
    piece = board.piece_at(move.from_square)
    target = chess.square_name(move.to_square)
    if board.is_castling(move):
        return f'{who} rokeert: de koning gaat veiliger staan en de toren komt dichter bij het centrum.'
    if board.is_en_passant(move):
        return f'{who} slaat en passant op {target}. Dat mag alleen direct na de dubbele pionzet.'
    if board.is_capture(move):
        return f'{who} slaat op {target} en verandert daarmee de spanning en de pionnenstructuur of stukverdeling.'
    if piece.piece_type == chess.PAWN:
        if target in ['e4','d4','e5','d5']:
            return f'{who} bezet {target} met een pion en maakt aanspraak op het centrum.'
        if target in ['c4','c5','c6','e6','d6','c3','f4','f5']:
            return f'{who} speelt {target}: deze pion beïnvloedt het centrum en bepaalt waar de stukken ruimte krijgen.'
        return f'{who} speelt de pion naar {target}. Let op de velden die de pion ondersteunt én de velden die hij achterlaat.'
    label = {chess.KNIGHT:'het paard',chess.BISHOP:'de loper',chess.ROOK:'de toren',chess.QUEEN:'de dame',chess.KING:'de koning'}[piece.piece_type]
    return f'{who} brengt {label} naar {target}. Kijk welke centrale velden en vijandelijke stukken het nu beïnvloedt.'


def library():
    result=[]
    for i,(name,intro,variants) in enumerate(CATALOG):
        group={'id':str(i),'name':name,'intro':intro,'variants':[]}
        for j,(title,line,plan) in enumerate(variants):
            board=chess.Board(); moves=[]; notes=[]; sans=[]
            for san in line.split():
                move=board.parse_san(san)
                notes.append(move_note(board,move));sans.append(board.san(move));moves.append(move.uci());board.push(move)
            group['variants'].append({'id':f'{i}-{j}','name':title,'moves':moves,'san':sans,'notes':notes,'plan':plan})
        result.append(group)
    return result
