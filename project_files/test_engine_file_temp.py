import sys
import unittest
from unittest.mock import patch
from ChessEngine import GameState, Move

class TestChessEngine(unittest.TestCase):
    def test_en_passant(self):
        gs = GameState()
        # White pawn e2 to e4
        move1 = Move((6, 4), (4, 4), gs.board)
        gs.makeMove(move1)
        
        # Black pawn a7 to a6
        move2 = Move((1, 0), (2, 0), gs.board)
        gs.makeMove(move2)
        
        # White pawn e4 to e5
        move3 = Move((4, 4), (3, 4), gs.board)
        gs.makeMove(move3)
        
        # Black pawn d7 to d5
        move4 = Move((1, 3), (3, 3), gs.board)
        gs.makeMove(move4)
        
        valid_moves = gs.getValidMoves()
        ep_move = None
        for move in valid_moves:
            if move.startRow == 3 and move.startCol == 4 and move.endRow == 2 and move.endCol == 3 and move.isEmpassantMove:
                ep_move = move
                break
        
        self.assertIsNotNone(ep_move, "En passant move should be valid.")
        
        gs.makeMove(ep_move)
        # White pawn should be at d6
        self.assertEqual(gs.board[2][3], "white-pawn", "White pawn should be on d6")
        # Black pawn at d5 should be removed
        self.assertEqual(gs.board[3][3], "--", "Black pawn on d5 should be captured")
        print("En passant test passed.")

    @patch('builtins.input', return_value='queen')
    def test_pawn_promotion(self, mock_input):
        gs = GameState()
        # Put white pawn on a7
        gs.board[1][0] = "white-pawn"
        gs.board[0][0] = "--"
        gs.whiteToMove = True
        
        valid_moves = gs.getValidMoves()
        promo_move = None
        for move in valid_moves:
            if move.startRow == 1 and move.startCol == 0 and move.endRow == 0 and move.endCol == 0 and move.isPawnPromotion:
                promo_move = move
                break
                
        self.assertIsNotNone(promo_move, "Pawn promotion move should be valid.")
        
        gs.makeMove(promo_move)
        
        # The pawn should be promoted to a queen
        self.assertEqual(gs.board[0][0], "white-queen", "Pawn should have promoted to queen")
        print("Pawn promotion test passed.")

if __name__ == '__main__':
    unittest.main()
