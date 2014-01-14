# -*- coding: utf-8 -*-
"""Tools to parse and use SAN strings."""

from __future__ import unicode_literals

import re


class Move(object):

    """Represents a simple valid move in SAN."""

    PAWN = 'P'
    KING = 'K'
    QUEEN = 'Q'
    BISHOP = 'B'
    KNIGHT = 'N'
    ROOK = 'R'

    CASTLE_KINGSIDE = 'O-O'
    CASTLE_QUEENSIDE = 'O-O-O'

    CHECK = '+'
    CHECKMATE = '#'
    PROMOTION = '='
    CAPTURE = 'x'

    VALID_PIECES = "{0}{1}{2}{3}{4}".format(KING,
                                            QUEEN,
                                            BISHOP,
                                            KNIGHT,
                                            ROOK)

    VALID_PROMOTIONS = "{0}{1}{2}{3}".format(QUEEN,
                                             BISHOP,
                                             KNIGHT,
                                             ROOK)

    VALID_CASTLE_MOVES = [
        CASTLE_KINGSIDE,
        CASTLE_QUEENSIDE,
    ]

    VALID_RANK = range(1, 9)
    VALID_FILE = 'abcdefgh'

    SAN_CASTLE_RE = r'^O\-O(\-O)?'
    SAN_CHECKS_RE = r'(\+?|\#?)'
    SAN_PAWN_MOVE_RE = r'^[a-h]([1-8]|x[a-h][1-8])(\=[QBNR])?'
    SAN_MAJOR_PIECE_MOVE_RE = r'^[KQBNR]([a-h]?[1-8]?)?x?[a-h][1-8]'
    SAN_ALL_RE = r'({pawn}|{major}|{castle}){checks}$'
    SAN_RE = re.compile(SAN_ALL_RE.format(castle=SAN_CASTLE_RE,
                                          checks=SAN_CHECKS_RE,
                                          pawn=SAN_PAWN_MOVE_RE,
                                          major=SAN_MAJOR_PIECE_MOVE_RE))

    def __init__(self, san):
        self.san = san
        self.san_parts = list(self.san)
        self.is_check = False
        self.is_checkmate = False
        self.is_capture = False
        self.is_promotion = False
        self.is_castle = False
        self.promotion_to = None
        self.piece_moved = None
        self.new_square = None

        if self.SAN_RE.match(san):
            self._parse()
        else:
            self._raise_value_error()

    def _parse(self):
        self._which_piece_moved()
        self._check_checks()
        self._is_promotion()

        if self.CAPTURE in self.san_parts:
            self.is_capture = True

        matches = re.findall(r'[a-h][1-8]', self.san)
        if len(matches) != 0:
            self.new_square = matches[-1]

    def _is_promotion(self):
        if self.PROMOTION in self.san_parts:
            self.is_promotion = True
            index = self.san_parts.index(self.PROMOTION) + 1
            if self.san_parts[index] in self.VALID_PROMOTIONS:
                self.promotion_to = self.san_parts[index]

    def _check_checks(self):
        if self.CHECK in self.san_parts:
            self.is_check = True

        if self.CHECKMATE in self.san_parts:
            self.is_check = True
            self.is_checkmate = True

    def _which_piece_moved(self):
        if self.san_parts[0] in self.VALID_PIECES:
            self.piece_moved = self.san_parts[0]
        elif self.san_parts[0] in self.VALID_FILE:
            self.piece_moved = self.PAWN
        elif self.san in self.VALID_CASTLE_MOVES:
            self.piece_moved = self.KING
            self.is_castle = True

    def _raise_value_error(self):
        raise ValueError("{0} is not valid SAN.".format(self.san))
