import unittest
import chess
from app import app, position, state

class Rules(unittest.TestCase):
    def test_start(self):
        b,h=position([])
        self.assertEqual(len(state(b,h)['pieces']),32)
        self.assertEqual(len(state(b,h)['legal']),20)
    def test_illegal(self):
        with self.assertRaises(ValueError): position(['e2e5'])
    def test_castling(self):
        b,h=position('e2e4 e7e5 g1f3 b8c6 f1c4 g8f6 e1g1'.split())
        self.assertEqual(b.piece_at(chess.F1).symbol(),'R')
        self.assertEqual(b.piece_at(chess.G1).symbol(),'K')
    def test_castle_through_check(self):
        b=chess.Board('4kr2/8/8/8/8/8/8/4K2R w K - 0 1')
        self.assertNotIn(chess.Move.from_uci('e1g1'),b.legal_moves)
    def test_ep(self):
        b,h=position('e2e4 a7a6 e4e5 d7d5 e5d6'.split())
        self.assertIsNone(b.piece_at(chess.D5))
        self.assertEqual(b.piece_at(chess.D6).symbol(),'P')
    def test_ep_expired(self):
        b,h=position('e2e4 a7a6 e4e5 d7d5 a2a3 a6a5'.split())
        self.assertNotIn(chess.Move.from_uci('e5d6'),b.legal_moves)
    def test_ep_exposes_king(self):
        b=chess.Board('k3r3/8/8/3pP3/8/8/8/4K3 w - d6 0 1')
        self.assertNotIn(chess.Move.from_uci('e5d6'),b.legal_moves)
    def test_promotion(self):
        b=chess.Board('7k/P7/8/8/8/8/8/7K w - - 0 1')
        self.assertEqual(len([m for m in b.legal_moves if m.from_square==chess.A7]),4)
        b.push_uci('a7a8n');self.assertEqual(b.piece_at(chess.A8).symbol(),'N')
    def test_repetition_claim(self):
        b,h=position('g1f3 g8f6 f3g1 f6g8 g1f3 g8f6 f3g1 f6g8'.split())
        self.assertIn('threefold',state(b,h)['claims'])
        self.assertIsNone(state(b,h)['result'])
        self.assertEqual(state(b,h,'threefold')['result'],'1/2-1/2')
    def test_fivefold(self):
        b,h=position('g1f3 g8f6 f3g1 f6g8'.split()*4)
        self.assertEqual(state(b,h)['result'],'1/2-1/2')
    def test_fifty_and_seventyfive(self):
        b=chess.Board('7k/8/8/8/8/8/R7/K7 w - - 100 51')
        self.assertIn('fifty',state(b,[])['claims'])
        self.assertEqual(state(b,[],'fifty')['result'],'1/2-1/2')
        b.halfmove_clock=150
        self.assertEqual(state(b,[])['status'],'75 zetten zonder pionzet of slagzet')
    def test_mate(self):
        b,h=position('f2f3 e7e5 g2g4 d8h4'.split())
        self.assertEqual(state(b,h)['result'],'0-1')
        self.assertEqual(state(b,h)['legal'],[])
    def test_stalemate_and_material(self):
        self.assertEqual(state(chess.Board('7k/5Q2/6K1/8/8/8/8/8 b - - 0 1'),[])['status'],'Pat')
        self.assertEqual(state(chess.Board('7k/8/6K1/8/8/8/8/8 w - - 0 1'),[])['status'],'Onvoldoende materiaal')
    def test_api(self):
        c=app.test_client()
        self.assertEqual(c.get('/').status_code,200)
        self.assertEqual(c.post('/api/position',json={'moves':['e2e4']}).json['turn'],'Zwart')
        self.assertEqual(c.post('/api/position',json={'moves':['e2e5']}).status_code,400)
        self.assertEqual(c.post('/api/position',json={'moves':[],'claim':'fifty'}).status_code,400)

if __name__=='__main__': unittest.main()
