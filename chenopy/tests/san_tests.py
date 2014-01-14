"""Tests for the SAN parser."""
from __future__ import unicode_literals

from nose.tools import ok_, eq_, raises

import chenopy.san as san

VALID_SAN = ['e4', 'e5', 'Nf3', 'Nc6', 'Bb5', 'a6', 'Ba4', 'Nf6', 'O-O-O',
             'Be7', 'Re1', 'b5', 'Bb3', 'd6', 'c3', 'O-O', 'h3', 'Nb8',
             'd4', 'Nbd7', 'c4', 'c6', 'cxb5', 'axb5', 'Nc3', 'Bb7',
             'Bg5', 'b4', 'Nb1', 'h6', 'Bh4', 'c5', 'dxe5', 'Nxe4', 'Bxe7',
             'Qxe7', 'exd6', 'Qf6', 'Nbd2', 'Nxd6', 'Nc4', 'Nxc4', 'Bxc4',
             'Nb6', 'Ne5', 'Rae8', 'Bxf7+', 'Rxf7', 'Nxf7', 'Rxe1+',
             'Qxe1', 'Kxf7', 'Qe3', 'Qg5', 'Qxg5', 'hxg5', 'b3', 'Ke6',
             'a3', 'Kd6', 'axb4', 'cxb4', 'Ra5', 'Nd5', 'f3', 'Bc8', 'Kf2',
             'Bf5', 'Ra7', 'g6', 'Ra6+', 'Kc5', 'Ke1', 'Nf4', 'g3', 'Nxh3',
             'Kd2', 'Kb5', 'Rd6', 'Kc5', 'Ra6', 'Nf2', 'g4', 'Bd3', 'Re6',
             'fxe1=Q']


INVALID_SAN = ['z2', '2f', 'xe1', 'a', '1', 'asdf', '', 't2', 'bb2', 'Bh9',
               'KQb2', '0-0', 'fxe1=K', 'f20', 'e13', 'Kb20', 'Qxxf3', ' ']


def test_valid_san():
    for m in VALID_SAN:
        yield check_san, m


def check_san(move):
    m = san.Move(move)
    eq_(m.san, move, "{0} is not valid.".format(m.san))


def test_invalid_move():
    for m in INVALID_SAN:
        yield check_invalid_san, m


@raises(ValueError)
def check_invalid_san(move):
    san.Move(move)


def test_parsing():
    m1 = san.Move('e4')
    m2 = san.Move('Qxe4+')
    m3 = san.Move('e8=N#')

    # e4
    eq_(m1.is_capture, False, "{0} shouldn't be a capture.".format(m1.san))
    eq_(m1.is_check, False, "{0} shouldn't be a check.".format(m1.san))
    eq_(m1.is_checkmate, False, "{0} shouldn't be a checkmate.".format(m1.san))
    eq_(m1.is_promotion, False, "{0} shouldn't be a promotion.".format(m1.san))
    eq_(m1.promotion_to, None,
        "{0.san} shouldn't be a promotion: {0.promotion_to}".format(m1))
    eq_(m1.new_square, 'e4',
        "{0.san} has wrong square: {0.new_square}.".format(m1))
    eq_(m1.piece_moved, m1.PAWN,
        "{0.san} was a pawn move: {0.piece_moved}".format(m1))

    # Qxe4+
    eq_(m2.is_capture, True, "{0} should be a capture.".format(m2.san))
    eq_(m2.is_check, True, "{0} should be a check.".format(m2.san))
    eq_(m2.is_checkmate, False, "{0} shouldn't be a checkmate.".format(m2.san))
    eq_(m2.is_promotion, False, "{0} shouldn't be a promotion.".format(m2.san))
    eq_(m2.promotion_to, None,
        "{0.san} shouldn't be a promotion: {0.promotion_to}".format(m2))
    eq_(m2.new_square, 'e4',
        "{0.san} has wrong square: {0.new_square}.".format(m2))
    eq_(m2.piece_moved, m2.QUEEN,
        "{0.san} was a queen move: {0.piece_moved}".format(m2))

    # e8=N#
    eq_(m3.is_capture, False, "{0} shouldn't be a capture.".format(m3.san))
    eq_(m3.is_check, True, "{0} should be a check.".format(m3.san))
    eq_(m3.is_checkmate, True, "{0} should be a checkmate.".format(m3.san))
    eq_(m3.is_promotion, True, "{0} should be a promotion.".format(m3.san))
    eq_(m3.promotion_to, m3.KNIGHT,
        "{0.san} should be a promotion to N: {0.promotion_to}".format(m3))
    eq_(m3.new_square, 'e8',
        "{0.san} has wrong square: {0.new_square}.".format(m3))
    eq_(m3.piece_moved, m3.PAWN,
        "{0.san} was a pawn move: {0.piece_moved}".format(m3))
