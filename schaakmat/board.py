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
from collections import namedtuple
from itertools import count
from operator import or_


# Position is a class that can hold data about the state of a chess game. It
# somewhat matches Forsytch-Edwards Notation in both state contents and order.
#
# IMPORTANT: A chess position is a *state*, not a location.
#
# board - 64-character string that holds the board pieces as Unicode
#         characters, and empty squares as spaces. The first character is A8 on
#         the chess board.
# whites_turn - Boolean value of whether the current turn is white's turn.
# castling_white - Sequence of two boolean values that determine the kingside
#                  and queenside castling rights of white.
# castling_black - Sequence of two boolean values that determine the kingside
#                  and queenside castling rights of black.
# en_passant_target - Index position of the spot behind the pawn that can be
#                     captured.
# half_move_clock - Amount of half-moves since the last capture or pawn move.
# move_count - Total amount of full moves.
Position = namedtuple("Position", ["board", "whites_turn", "castling_white",
                                   "castling_black", "en_passant_target",
                                   "half_move_clock", "move_count"])

Move = namedtuple("Move", ["origin", "destination"])

CastlingRights = namedtuple("CastlingRights", ["kingside", "queenside"])

KING_WHITE = '♔'
QUEEN_WHITE = '♕'
ROOK_WHITE = '♖'
BISHOP_WHITE = '♗'
KNIGHT_WHITE = '♘'
PAWN_WHITE = '♙'
WHITES = set([
    KING_WHITE, QUEEN_WHITE, ROOK_WHITE, BISHOP_WHITE, KNIGHT_WHITE, PAWN_WHITE
])

KING_BLACK = '♚'
QUEEN_BLACK = '♛'
ROOK_BLACK = '♜'
BISHOP_BLACK = '♝'
KNIGHT_BLACK = '♞'
PAWN_BLACK = '♟'
BLACKS = set([
    KING_BLACK, QUEEN_BLACK, ROOK_BLACK, BISHOP_BLACK, KNIGHT_BLACK, PAWN_BLACK
])

KINGS = set([KING_WHITE, KING_BLACK])
QUEENS = set([QUEEN_WHITE, QUEEN_BLACK])
ROOKS = set([ROOK_WHITE, ROOK_BLACK])
BISHOPS = set([BISHOP_WHITE, BISHOP_BLACK])
KNIGHTS = set([KNIGHT_WHITE, KNIGHT_BLACK])
PAWNS = set([PAWN_WHITE, PAWN_BLACK])

NORTH, EAST, SOUTH, WEST = -8, 1, 8, -1

DIRECTIONS_WHITE = {
    KING_WHITE: set([NORTH, NORTH+EAST, EAST, EAST*2, SOUTH+EAST, SOUTH,
                     SOUTH+WEST, WEST*2, NORTH+WEST]),
    QUEEN_WHITE: set([NORTH, NORTH+EAST, EAST, SOUTH+EAST, SOUTH, SOUTH+WEST,
                      WEST, NORTH+WEST]),
    ROOK_WHITE: set([NORTH, EAST, SOUTH, WEST]),
    BISHOP_WHITE: set([NORTH+EAST, SOUTH+EAST, SOUTH+WEST, NORTH+WEST]),
    KNIGHT_WHITE: set([NORTH*2+EAST, NORTH+EAST*2, SOUTH+EAST*2, SOUTH*2+EAST,
                       SOUTH*2+WEST, SOUTH+WEST*2, NORTH+WEST*2,
                       NORTH*2+WEST]),
    PAWN_WHITE: set([NORTH, NORTH*2, NORTH+EAST, NORTH+WEST])
}

DIRECTIONS_BLACK = {
    KING_BLACK: set([NORTH, NORTH+EAST, EAST, EAST*2, SOUTH+EAST, SOUTH,
                     SOUTH+WEST, WEST*2, NORTH+WEST]),
    QUEEN_BLACK: set([NORTH, NORTH+EAST, EAST, SOUTH+EAST, SOUTH, SOUTH+WEST,
                      WEST, NORTH+WEST]),
    ROOK_BLACK: set([NORTH, EAST, SOUTH, WEST]),
    BISHOP_BLACK: set([NORTH+EAST, SOUTH+EAST, SOUTH+WEST, NORTH+WEST]),
    KNIGHT_BLACK: set([NORTH*2+EAST, NORTH+EAST*2, SOUTH+EAST*2, SOUTH*2+EAST,
                       SOUTH*2+WEST, SOUTH+WEST*2, NORTH+WEST*2,
                       NORTH*2+WEST]),
    PAWN_BLACK: set([SOUTH+EAST, SOUTH, SOUTH*2, SOUTH+WEST])
}

NORTH_BORDER = set([i for i in range(8)])
EAST_BORDER = set([i*8 for i in range(8)])
SOUTH_BORDER = set([i for i in range(56, 64)])
WEST_BORDER = set([i*8+7 for i in range(8)])

INITIAL_BOARD = (
    "♜♞♝♛♚♝♞♜"  # 0-7
    "♟♟♟♟♟♟♟♟"  # 8-15
    "        "  # 16-23
    "        "  # 24-31
    "        "  # 32-39
    "        "  # 40-47
    "♙♙♙♙♙♙♙♙"  # 48-55
    "♖♘♗♕♔♗♘♖"  # 56-63
)

INITIAL_POSITION = Position(board=INITIAL_BOARD, whites_turn=True,
                            castling_white=CastlingRights(True, True),
                            castling_black=CastlingRights(True, True),
                            en_passant_target=None, half_move_clock=0,
                            move_count=0)


def get_piece(index, board):
    return board[index].strip()


def active_team(whites_turn):
    return WHITES if whites_turn else BLACKS


def opponent(team):
    return BLACKS if team is WHITES else WHITES


def directions(team):
    return DIRECTIONS_WHITE if team is WHITES else DIRECTIONS_BLACK


def castling_rights(team, position):
    return (position.castling_white if team is WHITES
            else position.castling_black)


def legal_moves(origin, position):
    global EAST, WEST

    piece = get_piece(origin, position.board)
    team = active_team(position.whites_turn)
    king = piece in KINGS
    if king:
        under_siege = set(besieged(team, position))
        current_check = origin in under_siege

    for move in _accessible_moves(origin, position):
        if king:
            offset = move.origin - move.destination
            half_offset = offset / 2
            if move.destination in under_siege:
                continue
            if (offset in (EAST*2, WEST*2)
                    and (current_check
                         or
                         half_offset in under_siege)):
                continue
        elif is_check(do_move(move, position, force=True)):
            continue

        yield move


def besieged(team, position):
    opposing_team = opponent(team)

    siege_set = set([])

    for i, piece in enumerate(position.board):
        if piece in opposing_team:
            for move in _accessible_moves(i, position):
                destination = move.destination
                if destination not in siege_set:
                    yield destination
                    siege_set.add(destination)


def is_check(team, position):
    global KINGS

    under_siege = besieged(team, position)

    for index in position.board:
        piece = get_piece(index, position.board)
        if piece in team and piece in KINGS:
            if index in under_siege:
                return True
    return False


def is_move_legal(move, position):
    team = active_team(position.whites_turn)
    piece = get_piece(move.origin, position.board)
    destination_piece = get_piece(move.destination, position.board)

    if piece not in team or destination_piece in team:
        return False
    if move in legal_moves(move.origin, position):
        return True

    return False


def do_move(move, position, force=False):
    team = active_team(position.whites_turn)
    origin_piece = get_piece(move.origin, position.board)

    if force or is_move_legal(move, position):
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


def _accessible_moves(origin, position):
    """Generator that yields all plausible moves for a single piece."""
    global NORTH, NORTH_BORDER, EAST, SOUTH, SOUTH_BORDER, WEST, Move

    piece = get_piece(origin, position.board)
    if piece in WHITES:
        team = WHITES
    elif piece in BLACKS:
        team = BLACKS
    else:
        raise Exception()  # TODO
    pawn = piece in PAWNS
    king = piece in KINGS

    for offset in directions(team)[piece]:
        for destination in count(origin + offset, offset):
            destination_piece = get_piece(destination, position.board)

            # Destination occupied by piece of same colour?
            if destination_piece in team:
                break
            # Offset is a castling move and castling not possible/allowed?
            if (king
                    and (offset == EAST*2
                         and get_piece(origin+EAST)
                         and not castling_rights(team, position).kingside
                         or
                         offset == WEST*2
                         and get_piece(origin+WEST)
                         and get_piece(origin+WEST*3)
                         and not castling_rights(team, position).queenside)):
                break
            if pawn:
                # Offset is a vertical move forward and destination is an enemy
                # piece?
                if (destination_piece
                        and offset in (NORTH, NORTH*2, SOUTH, SOUTH*2)):
                    break
                # Offset is a two-squares move forward and pawn is not in its
                # initial spot? (White)
                if (offset == NORTH*2
                        and (get_piece(origin+NORTH, position.board)
                             or origin not in [index+NORTH for index in
                                               SOUTH_BORDER])):
                    break
                # Offset is a two-squares move forward and pawn is not in its
                # initial spot? (Black)
                if (offset == SOUTH*2
                        and (get_piece(origin+SOUTH, position.board)
                             or origin not in [index+SOUTH for index in
                                               NORTH_BORDER])):
                    break
                # Offset is a diagonal move and destination is not an enemy
                # piece or destination is not an en passant target?
                if (offset in (NORTH+EAST, SOUTH+EAST, SOUTH+WEST, NORTH+EAST)
                        and not destination_piece
                        and destination != position.en_passant_target):
                    break
            # Piece in the bounds of the board?
            if not _in_bounds(destination - offset, destination):
                break

            # Move is legal.
            yield Move(origin, destination)

            # Piece cannot do multiple steps in the same direction?
            if piece in reduce(or_, [KINGS, KNIGHTS, PAWNS]):
                break

            # The destination was a capture move and the direction is therefore
            # further blocked?
            if destination_piece in opponent(team):
                break


def _in_bounds(origin, destination):
    """If a single move is applied to a piece, test whether it left the bounds
    of the board.

    This function is extremely limited in scope, and should be considered an
    implementation detail.
    """
    global EAST, EAST_BORDER, WEST, WEST_BORDER

    # North illegal?
    if destination < 0:
        return False
    # East illegal?
    if origin in EAST_BORDER and destination in WEST_BORDER:
        return False
    # Twice east illegal? (Knight)
    if (destination in WEST_BORDER
            and origin in [index+WEST for index in EAST_BORDER]
            or
            origin in EAST_BORDER
            and destination in [index+EAST for index in WEST_BORDER]):
        return False
    # South illegal?
    if destination > 63:
        return False
    # West illegal?
    if origin in WEST_BORDER and destination in EAST_BORDER:
        return False
    # Twice west illegal? (Knight)
    if (destination in EAST_BORDER
            and origin in [index+EAST for index in WEST_BORDER]
            or
            origin in WEST_BORDER
            and destination in [index+WEST for index in EAST_BORDER]):
        return False
    return True
