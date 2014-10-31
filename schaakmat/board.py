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
# IMPORTANT: A chess position is a *state*, not a location.
#
# board - 64-character string that holds the board pieces as Unicode or ASCII
#         characters, and empty squares as spaces. The first character is A8 on
#         the chess board.
# BLACK_turn - Boolean value of whether the current turn is white's turn.
# white_castling - Sequence of two boolean values that determine the kingside
#                  and queenside castling rights of white.
# black_castling - Sequence of two boolean values that determine the kingside
#                  and queenside castling rights of black.
# en_passant_target - Index position of the spot behind the pawn that can be
#                     captured.
# half_move_clock - Amount of half-moves since the last capture or pawn move.
# move_count - Total amount of full moves.
Position = namedtuple("Position", ["board", "whites_turn", "white_castling",
                                   "black_castling", "en_passant_target",
                                   "half_move_clock", "move_count"])

TeamContainer = namedtuple("TeamContainer", ["active_team", "opposing_team"])

KING_WHITE = '♔'
KING_WHITE_ASCII = 'K'
QUEEN_WHITE = '♕'
QUEEN_WHITE_ASCII = 'Q'
ROOK_WHITE = '♖'
ROOK_WHITE_ASCII = 'R'
BISHOP_WHITE = '♗'
BISHOP_WHITE_ASCII = 'B'
KNIGHT_WHITE = '♘'
KNIGHT_WHITE_ASCII = 'N'
PAWN_WHITE = '♙'
PAWN_WHITE_ASCII = 'P'
WHITES = set([
    KING_WHITE, KING_WHITE_ASCII, QUEEN_WHITE, QUEEN_WHITE_ASCII, ROOK_WHITE,
    ROOK_WHITE_ASCII, BISHOP_WHITE, BISHOP_WHITE_ASCII, KNIGHT_WHITE,
    KNIGHT_WHITE_ASCII, PAWN_WHITE, PAWN_WHITE_ASCII
])

KING_BLACK = '♚'
KING_BLACK_ASCII = 'k'
QUEEN_BLACK = '♛'
QUEEN_BLACK_ASCII = 'q'
ROOK_BLACK = '♜'
ROOK_BLACK_ASCII = 'r'
BISHOP_BLACK = '♝'
BISHOP_BLACK_ASCII = 'b'
KNIGHT_BLACK = '♞'
KNIGHT_BLACK_ASCII = 'n'
PAWN_BLACK = '♟'
PAWN_BLACK_ASCII = 'p'
BLACKS = set([
    KING_BLACK, KING_BLACK_ASCII, QUEEN_BLACK, QUEEN_BLACK_ASCII, ROOK_BLACK,
    ROOK_BLACK_ASCII, BISHOP_BLACK, BISHOP_BLACK_ASCII, KNIGHT_BLACK,
    KNIGHT_BLACK_ASCII, PAWN_BLACK, PAWN_BLACK_ASCII
])

KINGS = set([KING_WHITE, KING_WHITE_ASCII, KING_BLACK, KING_BLACK_ASCII])
QUEENS = set([QUEEN_WHITE, QUEEN_WHITE_ASCII, QUEEN_BLACK, QUEEN_BLACK_ASCII])
ROOKS = set([ROOK_WHITE, ROOK_WHITE_ASCII, ROOK_BLACK, ROOK_BLACK_ASCII])
BISHOPS = set([BISHOP_WHITE, BISHOP_WHITE_ASCII, BISHOP_BLACK,
               BISHOP_BLACK_ASCII])
KNIGHTS = set([KNIGHT_WHITE, KNIGHT_WHITE_ASCII, KNIGHT_BLACK,
               KNIGHT_BLACK_ASCII])
PAWNS = set([PAWN_WHITE, PAWN_WHITE_ASCII, PAWN_BLACK, PAWN_BLACK_ASCII])

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

INITIAL_BOARD_ASCII = (
    "rnbqkbnr"  # 0-7
    "pppppppp"  # 8-15
    "        "  # 16-23
    "        "  # 24-31
    "        "  # 32-39
    "        "  # 40-47
    "PPPPPPPP"  # 48-55
    "RNBQKBNR"  # 56-63
)


def get_teams(whites_turn):
    if whites_turn:
        return TeamContainer(WHITES, BLACKS)
    else:
        return TeamContainer(BLACKS, WHITES)


def opponent(team):
    if team is WHITES:
        return BLACKS
    else:
        return WHITES


def is_move_legal(from_index, to_index, position):
    active_team, opposing_team = get_teams(position.whites_turn)
    from_piece = position.board[from_index].strip()
    to_piece = position.board[to_index].strip()

    if from_piece in opposing_team or not from_piece:
        return False

    return True


def move(from_index, to_index, position):
    active_team, opposing_team = get_teams(position.whites_turn)
    from_piece = position.board[from_index].strip()

    if is_move_legal(from_index, from_piece, to_index, to_piece, position,
                     active_team, opposing_team):
        return Position()  # TODO
    else:
        raise Exception()  # TODO


def to_index(notation):
    """Return an index location for an algebraic notation (e.g., 'A8' -> 0)"""
    letter, number = notation[0].upper(), int(notation[1])
    return (ord(letter)-65) + (-(number-8) * 8)


def to_notation(index):
    """Return an algebraic notation for an index position (e.g., 63 -> 'H1')"""
    remainder, quotient = divmod(index, 8)
    return chr(quotient+65) + str(-(remainder-8))
