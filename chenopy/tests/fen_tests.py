"""Tests for the FEN parser."""
from __future__ import unicode_literals

from nose.tools import eq_, raises

import chenopy.fen as fen


FEN_START = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
FEN_BAD = 'rnbqnr/pppppp/8/8/8/8/PPPPPPPP/RNBQKBNR wKQkq - 0 1'

VALID_FENS = [
    'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
    'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1',
    'rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2',
    'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2',
    'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1',
    '4k3/8/8/8/8/8/4P3/4K3 w - - 5 39',
    'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2',
]


def test_fen_parse():
    f = fen.fen_parse(FEN_START)
    eq_(len(f), 6)
    eq_(type(f[4]), int)
    eq_(type(f[5]), int)


@raises(ValueError)
def test_bad_fen_parse():
    fen.fen_parse(FEN_BAD)


def test_default_fen():
    f = fen.Position()
    eq_(f.fen_str, FEN_START)
    eq_(f.turn, 'White')


def test_board_string():
    f = fen.Position()
    board = "r|n|b|q|k|b|n|r...p|p|p|p|p|p|p|p... | | | | | | | ... | | | | | | | ... | | | | | | | ... | | | | | | | ...P|P|P|P|P|P|P|P...R|N|B|Q|K|B|N|R"
    eq_(f.display_board('...', '|'), board)


def test_board_graphical():
    f = fen.Position()
    board = "\u265c \u265e \u265d \u265b \u265a \u265d \u265e \u265c\n\u265f \u265f \u265f \u265f \u265f \u265f \u265f \u265f\n               \n               \n               \n               \n\u2659 \u2659 \u2659 \u2659 \u2659 \u2659 \u2659 \u2659\n\u2656 \u2658 \u2657 \u2655 \u2654 \u2657 \u2658 \u2656"
    eq_(f.display_board(graphical=True), board)


def test_board_with_rank():
    f = fen.Position()
    board = "1|r|n|b|q|k|b|n|r...2|p|p|p|p|p|p|p|p...3| | | | | | | | ...4| | | | | | | | ...5| | | | | | | | ...6| | | | | | | | ...7|P|P|P|P|P|P|P|P...8|R|N|B|Q|K|B|N|R"
    eq_(f.display_board('...', '|', True), board)


def test_graphical_piece_representation():
    f = fen.Position()
    eq_(f._get_graphical_piece('K'), "\u2654")
    eq_(f._get_graphical_piece('K', True), ("\u265a", 'w'))
    eq_(f._get_graphical_piece('k', True), ("\u265a", 'b'))
    eq_(f._get_graphical_piece('k'), "\u265a")


def test_position_instances():
    for f in VALID_FENS:
        yield check_position_instance, f


def check_position_instance(fen_str):
    p = fen.Position(fen_str)
    f = fen.fen_parse(fen_str)
    eq_(p.fen_str, fen_str)
    eq_(p.fen_board, f[0])
    eq_(p.active_color, f[1])
    eq_(str(p), fen_str)
    eq_(repr(p), "chenopy.fen.Position('{0}')".format(fen_str))
