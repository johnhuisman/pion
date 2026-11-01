"""Pion: stateless chess API; replay the entire move history on every request."""
import chess
from openings import library
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 65536

REASONS = {
    'CHECKMATE': 'Schaakmat', 'STALEMATE': 'Pat',
    'INSUFFICIENT_MATERIAL': 'Onvoldoende materiaal',
    'SEVENTYFIVE_MOVES': '75 zetten zonder pionzet of slagzet',
    'FIVEFOLD_REPETITION': 'Vijfmaal dezelfde stelling',
    'FIFTY_MOVES': 'Vijftigzettenregel', 'THREEFOLD_REPETITION': 'Driemaal dezelfde stelling',
}


def position(moves):
    if not isinstance(moves, list) or len(moves) > 6000:
        raise ValueError('Ongeldige zettenlijst.')
    board = chess.Board()
    history = []
    for uci in moves:
        if board.is_game_over():
            raise ValueError('De partij is al afgelopen.')
        move = chess.Move.from_uci(uci)
        if move not in board.legal_moves:
            raise ValueError('Deze zet is niet toegestaan.')
        history.append(board.san(move))
        board.push(move)
    return board, history


def state(board, history, claim=None):
    outcome = board.outcome()
    if claim:
        if claim == 'threefold' and board.can_claim_threefold_repetition():
            outcome = chess.Outcome(chess.Termination.THREEFOLD_REPETITION, None)
        elif claim == 'fifty' and board.can_claim_fifty_moves():
            outcome = chess.Outcome(chess.Termination.FIFTY_MOVES, None)
        else:
            raise ValueError('Deze remise kan nu niet worden geclaimd.')
    turn = 'Wit' if board.turn else 'Zwart'
    return {
        'pieces': {chess.square_name(s): p.symbol() for s, p in board.piece_map().items()},
        'legal': [m.uci() for m in board.legal_moves] if not outcome else [],
        'turn': turn, 'check': board.is_check(), 'history': history,
        'fen': board.fen(), 'last': board.peek().uci() if board.move_stack else None,
        'check_square': chess.square_name(board.king(board.turn)) if board.is_check() else None,
        'result': outcome.result() if outcome else None,
        'status': (REASONS[outcome.termination.name] if outcome else turn + ' aan zet' + (' — schaak!' if board.is_check() else '')),
        'claims': [] if outcome else [k for k, ok in [('threefold', board.can_claim_threefold_repetition()), ('fifty', board.can_claim_fifty_moves())] if ok],
    }


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/api/openings')
def api_openings():
    return jsonify(library())


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.post('/api/position')
def api_position():
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            raise ValueError('Ongeldig verzoek.')
        board, history = position(data.get('moves', []))
        return jsonify(state(board, history, data.get('claim')))
    except (ValueError, TypeError, AttributeError) as exc:
        return jsonify(error=str(exc)), 400


if __name__ == '__main__':
    app.run(debug=True)
