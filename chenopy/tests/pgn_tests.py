"""Tests for the PGN parser."""
from __future__ import unicode_literals

from nose.tools import eq_, raises
import os

import chenopy.pgn as pgn

GOOD_PGN = """
[Event "Event name"]
[Site "Chess.com"]
[Date "2013.01.01"]
[White "username1"]
[Black "username2"]
[Result "0-1"]
[WhiteElo "1200"]
[BlackElo "1200"]
[TimeControl "1 in 3 days"]
[Termination "username2 won by checkmate"]

1.e4 d5 2.Nc3 d4 3.Nb5 e5 4.d3 Bd7 5.Qh5 Nc6 6.Bg5 Nf6 7.Qh4 a6 8.\
        Nxc7+ Qxc7 9.Bxf6 Nb4 10.Rc1 Nxa2
    11.Bg5 Nxc1 12.Bxc1 Qxc2 13.Qg5 Bb4+ 14.Bd2 Ba4 15.Be2 Qc1+ 16.\
            Bd1 Qxd1# 0-1
"""

BAD_PGN = """
[Event "Event name"]
[Site "Chess.com"]
[Date "2013.01.01"]
[White "username1"]
[Black "username2"]
[Result "0-1"]
[WhiteElo "1200"]
[BlackElo "1200"]
[TimeControl "1 in 3 days"]
[Termination "username2 won by checkmate"]
[SomethingRandom "blah"]

1.e4 d5 2.Nc3 d4 3.Nb5 e5 4.d3 Bd7 5.Qh5 Nc6 6.Bg5 Nf6 7.Qh4 a6 8.\
        Nxc7+ Qxc7 9.Bxf6 Nb4 10.Rc1 Nxa2
    11.Bg5 Nxc1 12.Bxc1 Qxc2 13.Qg5 Bb4+ 14.Bd2 Ba4 15.Be2 Qc1+ 16.\
            Bd1 Qxd1# 0-1
"""


def test_game_instance():
    game = pgn.Game(GOOD_PGN)
    eq_(game.event, 'Event name')
    eq_(game.tags.get('event'), 'Event name')
    eq_(game.site, 'Chess.com')
    eq_(game.white, 'username1')
    eq_(game.result, '0-1')
    eq_(game.termination, 'username2 won by checkmate')
    eq_(game.tags.get('round'), None)
    eq_(str(game), "Game <username1 vs username2>")


@raises(ValueError)
def test_bad_pgn():
    game = pgn.Game(BAD_PGN)


@raises(TypeError)
def test_not_pgn_string():
    game = pgn.Game("blah")


def test_get_pgns_good():
    pgn_string = ''
    location = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(location, "db-kas96.pgn"), "r") as pgn_file:
        pgn_string = pgn_file.read()
    games = pgn.get_pgns(pgn_string)
    eq_(len(games), 6)


@raises(ValueError)
def test_get_pgns_bad():
    bad_pgn = '[Event "blah"]\n[Events "blah"]'
    games = pgn.get_pgns(bad_pgn)
