# -*- coding: utf-8 -*-
#!/usr/bin/env python
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

try:
    from unittest import mock
except ImportError:
    import mock
import unittest
from schaakmat import board


class TestBoard(unittest.TestCase):

    def test_get_teams(self):
        self.assertEqual(board.get_teams(whites_turn=True), (board.WHITES,
                                                             board.BLACKS))
        self.assertEqual(board.get_teams(whites_turn=False), (board.BLACKS,
                                                              board.WHITES))

    def test_opponent(self):
        self.assertEqual(board.opponent(board.WHITES), board.BLACKS)
        self.assertEqual(board.opponent(board.BLACKS), board.WHITES)

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
