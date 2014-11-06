#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Schaakmat is a chess engine.
# Copyright (C) 2014  Ruben Bakker <rubykuby@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
import unittest
from schaakmat import board


class TestBoard(unittest.TestCase):

    def test_get_piece(self):
        self.assertEqual(board.get_piece(0, board.INITIAL_BOARD), "♜")
        self.assertFalse(board.get_piece(16, board.INITIAL_BOARD))

    def test_active_team(self):
        self.assertEqual(board.active_team(whites_turn=True), board.WHITES)
        self.assertEqual(board.active_team(whites_turn=False), board.BLACKS)

    def test_opponent(self):
        self.assertEqual(board.opponent(board.WHITES), board.BLACKS)
        self.assertEqual(board.opponent(board.BLACKS), board.WHITES)

    def test_directions(self):
        self.assertEqual(board.directions(board.WHITES),
                         board.DIRECTIONS_WHITE)
        self.assertEqual(board.directions(board.BLACKS),
                         board.DIRECTIONS_BLACK)

    def test_castling_rights(self):
        self.assertIs(board.castling_rights(board.WHITES,
                                            board.INITIAL_POSITION),
                      board.INITIAL_POSITION.castling_white)
        self.assertIs(board.castling_rights(board.BLACKS,
                                            board.INITIAL_POSITION),
                      board.INITIAL_POSITION.castling_black)

    def test_legal_moves(self):
        pass

    def test_besieged(self):
        expected = set([i for i in range(16, 24)])
        self.assertEqual(set(board.besieged(board.WHITES,
                                            board.INITIAL_POSITION)),
                         expected)

    def test_besieged_rook_blocks(self):
        test_board = (
            "♜   ♚   "  # 0-7
            "    ♙   "  # 8-15
            "        "  # 16-23
            "        "  # 24-31
            "        "  # 32-39
            "        "  # 40-47
            "♙♙♙♙ ♙♙♙"  # 48-55
            "♖♘♗♕♔♗♘♖"  # 56-63
        )
        position = board.Position(test_board, True,
                                  board.CastlingRights(True, True),
                                  board.CastlingRights(True, True), None, 0, 0)
        expected = set([1, 2, 3, 5, 8, 11, 12, 13, 16, 24, 32, 40, 48])
        self.assertEqual(set(board.besieged(board.WHITES, position)), expected)

    def test_besieged_lone_queen(self):
        test_board = (
            "♕       "  # 0-7
            "        "  # 8-15
            "        "  # 16-23
            "        "  # 24-31
            "        "  # 32-39
            "        "  # 40-47
            "        "  # 48-55
            "        "  # 56-63
        )
        position = board.Position(test_board, True,
                                  board.CastlingRights(True, True),
                                  board.CastlingRights(True, True), None, 0, 0)
        expected = set([1, 2, 3, 4, 5, 6, 7, 8, 16, 24, 32, 40, 48, 56, 9, 18,
                        27, 36, 45, 54, 63])
        self.assertEqual(set(board.besieged(board.BLACKS, position)), expected)

    def test_besieged_knight(self):
        test_board = (
            "        "  # 0-7
            "        "  # 8-15
            "        "  # 16-23
            "        "  # 24-31
            "        "  # 32-39
            "    ♟ ♙ "  # 40-47
            "        "  # 48-55
            "     ♞  "  # 56-63
        )
        position = board.Position(test_board, True,
                                  board.CastlingRights(True, True),
                                  board.CastlingRights(True, True), None, 0, 0)
        expected = set([46, 53, 51, 55])
        self.assertEqual(set(board.besieged(board.WHITES, position)), expected)

    def test_is_check(self):
        self.assertEqual(board.is_check(board.WHITES, board.INITIAL_POSITION),
                         False)
        self.assertEqual(board.is_check(board.BLACKS, board.INITIAL_POSITION),
                         False)

    def test_is_move_legal(self):
        pass

    def test_do_move(self):
        expected_board = (
            "♜♞♝♛♚♝♞♜"  # 0-7
            "♟♟♟♟♟♟♟♟"  # 8-15
            "        "  # 16-23
            "        "  # 24-31
            "♙       "  # 32-39
            "        "  # 40-47
            " ♙♙♙♙♙♙♙"  # 48-55
            "♖♘♗♕♔♗♘♖"  # 56-63
        )
        expected = board.Position(expected_board, False,
                                  board.CastlingRights(True, True),
                                  board.CastlingRights(True, True),
                                  40, 0, 0)
        self.assertEqual(board.do_move(board.Move(48, 32),
                                       board.INITIAL_POSITION),
                         expected)

        expected_board = (
            "♜ ♝♛♚♝♞♜"  # 0-7
            "♟♟♟♟♟♟♟♟"  # 8-15
            "♞       "  # 16-23
            "        "  # 24-31
            "♙       "  # 32-39
            "        "  # 40-47
            " ♙♙♙♙♙♙♙"  # 48-55
            "♖♘♗♕♔♗♘♖"  # 56-63
        )
        expected_2 = board.Position(expected_board, True,
                                    board.CastlingRights(True, True),
                                    board.CastlingRights(True, True),
                                    None, 1, 1)
        self.assertEqual(board.do_move(board.Move(1, 16), expected),
                         expected_2)

    def test_to_index(self):
        notations = [letter + str(number) for number in reversed(range(1, 9))
                     for letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']]

        for index, notation in enumerate(notations):
            self.assertEqual(board.to_index(notation), index)

    def test_to_notation(self):
        notations = [letter + str(number) for number in reversed(range(1, 9))
                     for letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']]

        for index, notation in enumerate(notations):
            self.assertEqual(board.to_notation(index), notation)

    def test__accessible_moves(self):
        pass

    def test__in_bounds(self):
        pass

    def test__apply_move(self):
        test_board = (
            "♕       "  # 0-7
            "        "  # 8-15
            "        "  # 16-23
            "        "  # 24-31
            "        "  # 32-39
            "        "  # 40-47
            "        "  # 48-55
            "        "  # 56-63
        )
        expected_board = (
            "        "  # 0-7
            "        "  # 8-15
            "        "  # 16-23
            "        "  # 24-31
            "        "  # 32-39
            "        "  # 40-47
            "        "  # 48-55
            "       ♕"  # 56-63
        )
        self.assertEqual(board._apply_move(board.Move(0, 63), test_board),
                         expected_board)

    def test__apply_move_replace(self):
        test_board = (
            "        "  # 0-7
            " ♕      "  # 8-15
            "        "  # 16-23
            "        "  # 24-31
            "        "  # 32-39
            "        "  # 40-47
            "      ♜ "  # 48-55
            "        "  # 56-63
        )
        expected_board = (
            "        "  # 0-7
            "        "  # 8-15
            "        "  # 16-23
            "        "  # 24-31
            "        "  # 32-39
            "        "  # 40-47
            "      ♕ "  # 48-55
            "        "  # 56-63
        )
        self.assertEqual(board._apply_move(board.Move(9, 54), test_board),
                         expected_board)

    def test__place_piece(self):
        test_board = (
            "        "  # 0-7
            "        "  # 8-15
            "        "  # 16-23
            "        "  # 24-31
            "        "  # 32-39
            "        "  # 40-47
            "        "  # 48-55
            "        "  # 56-63
        )
        expected_board = (
            "♕       "  # 0-7
            "        "  # 8-15
            "        "  # 16-23
            "        "  # 24-31
            "        "  # 32-39
            "        "  # 40-47
            "        "  # 48-55
            "        "  # 56-63
        )
        self.assertEqual(board._place_piece(0, '♕', test_board),
                         expected_board)

    def test__clear(self):
        test_board = (
            "♕       "  # 0-7
            "        "  # 8-15
            "        "  # 16-23
            "        "  # 24-31
            "        "  # 32-39
            "        "  # 40-47
            "        "  # 48-55
            "        "  # 56-63
        )
        expected_board = (
            "        "  # 0-7
            "        "  # 8-15
            "        "  # 16-23
            "        "  # 24-31
            "        "  # 32-39
            "        "  # 40-47
            "        "  # 48-55
            "        "  # 56-63
        )
        self.assertEqual(board._clear(0, test_board), expected_board)
