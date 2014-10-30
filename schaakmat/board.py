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

from collections import namedtuple


# Position is a class that can hold data about the state of a chess game. It
# somewhat matches Forsytch-Edwards Notation in both state contents and order.
#
# board - TODO
# whites_turn - Boolean value of whether the current turn is white's turn.
# white_castling - Sequence of two boolean values that determine the kingside
#                  and queenside castling rights of white.
# black_castling - Sequence of two boolean values that determine the kingside
#                  and queenside castling rights of black.
# en_passant_target - TODO
# half_move_clock - Amount of half-moves since the last capture or pawn move.
# move_count - Total amount of full moves.
Position = namedtuple("Position", ["board", "whites_turn", "white_castling",
                                   "black_castling", "en_passant_target",
                                   "half_move_clock", "move_count"])

KING_WHITE = '♔'
QUEEN_WHITE = '♕'
ROOK_WHITE = '♖'
BISHOP_WHITE = '♗'
KNIGHT_WHITE = '♘'
PAWN_WHITE = '♙'
WHITES = set([KING_WHITE, QUEEN_WHITE, ROOK_WHITE, BISHOP_WHITE, KNIGHT_WHITE,
              PAWN_WHITE])

KING_BLACK = '♚'
QUEEN_BLACK = '♛'
ROOK_BLACK = '♜'
BISHOP_BLACK = '♝'
KNIGHT_BLACK = '♞'
PAWN_BLACK = '♟'
BLACKS = set([KING_BLACK, QUEEN_BLACK, ROOK_BLACK, BISHOP_BLACK, KNIGHT_BLACK,
              PAWN_BLACK])

KINGS = set([KING_WHITE, KING_BLACK])
QUEENS = set([QUEEN_WHITE, QUEEN_BLACK])
ROOKS = set([ROOK_WHITE, ROOK_BLACK])
BISHOPS = set([BISHOP_WHITE, BISHOP_BLACK])
KNIGHTS = set([KNIGHT_WHITE, KNIGHT_BLACK])
PAWNS = set([PAWN_WHITE, PAWN_BLACK])

INITIAL_BOARD = (
    "♜♞♝♛♚♝♞♜"  # 0-7
    "♝♝♝♝♝♝♝♝"  # 8-15
    "        "  # 16-23
    "        "  # 24-31
    "        "  # 32-39
    "        "  # 40-47
    "♙♙♙♙♙♙♙♙"  # 48-55
    "♖♘♗♕♔♗♘♖"  # 56-63
)


def to_index(notation):
    """Return an index location for an algebraic notation (e.g., 'A8' -> 0)"""
    letter, number = notation[0].upper(), int(notation[1])
    return (ord(letter)-65) + (-(number-8) * 8)


def to_notation(index):
    """Return an algebraic notation for an index position (e.g., 63 -> 'H1')"""
    remainder, quotient = divmod(index, 8)
    return chr(remainder+65) + str(-(quotient-8))
