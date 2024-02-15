from django.test import TestCase
import unittest
from game.helpers import checkWin


class TestCheckWin(unittest.TestCase):

    def test_checkWin_empty_board(self):
        board = {
            "0": "", "1": "", "2": "",
            "3": "", "4": "", "5": "",
            "6": "", "7": "", "8": ""
        }
        self.assertIsNone(checkWin(board), "No winner expected on an empty board")

    def test_checkWin_horizontal_win(self):
        # Test horizontal win on the top row
        board = {
            "0": "X", "1": "X", "2": "X",
            "3": "", "4": "", "5": "",
            "6": "", "7": "", "8": ""
        }
        self.assertEqual(checkWin(board), "X", "Expected 'X' to win on the top row")

    def test_checkWin_vertical_win(self):
        # Test vertical win on the first column
        board = {
            "0": "O", "1": "", "2": "",
            "3": "O", "4": "", "5": "",
            "6": "O", "7": "", "8": ""
        }
        self.assertEqual(checkWin(board), "O", "Expected 'O' to win on the first column")

    def test_checkWin_diagonal_win(self):
        # Test diagonal win from top-left to bottom-right
        board = {
            "0": "X", "1": "", "2": "",
            "3": "", "4": "X", "5": "",
            "6": "", "7": "", "8": "X"
        }
        self.assertEqual(checkWin(board), "X", "Expected 'X' to win diagonally from top-left to bottom-right")

    def test_checkWin_no_win(self):
        # Test scenario where no one wins
        board = {
            "0": "X", "1": "O", "2": "X",
            "3": "O", "4": "X", "5": "O",
            "6": "O", "7": "X", "8": "O"
        }
        self.assertIsNone(checkWin(board), "No winner expected on this board")



if __name__ == '__main__':
    unittest.main()
