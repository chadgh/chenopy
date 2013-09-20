single_pgn = """[Event "Event name"]
[Site "Chess.com"]
[Date "2013.01.01"]
[White "username1"]
[Black "username2"]
[Result "0-1"]
[WhiteElo "1200"]
[BlackElo "1200"]
[TimeControl "1 in 3 days"]
[Termination "username2 won by checkmate"]

1.e4 d5 2.Nc3 d4 3.Nb5 e5 4.d3 Bd7 5.Qh5 Nc6 6.Bg5 Nf6 7.Qh4 a6 8.Nxc7+ Qxc7\
        9.Bxf6 Nb4 10.Rc1 Nxa2
 11.Bg5 Nxc1 12.Bxc1 Qxc2 13.Qg5 Bb4+ 14.Bd2 Ba4 15.Be2 Qc1+ 16.Bd1 Qxd1# 0-1
"""

multiple_pgn = """
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

1.e4 d5 2.Nc3 d4 3.Nb5 e5 4.d3 Bd7 5.Qh5 Nc6 6.Bg5 Nf6 7.Qh4 a6 8.Nxc7+ Qxc7\
        9.Bxf6 Nb4 10.Rc1 Nxa2
 11.Bg5 Nxc1 12.Bxc1 Qxc2 13.Qg5 Bb4+ 14.Bd2 Ba4 15.Be2 Qc1+ 16.Bd1 Qxd1# 0-1

[Event "Event name 2"]
[Site "Chess.com"]
[Date "2013.01.01"]
[White "username3"]
[Black "username1"]
[Result "0-1"]
[WhiteElo "1200"]
[BlackElo "1200"]
[TimeControl "1 in 3 days"]
[Termination "username1 won by checkmate"]

1.e4 d5 2.Nc3 d4 3.Nb5 e5 4.d3 Bd7 5.Qh5 Nc6 6.Bg5 Nf6 7.Qh4 a6 8.Nxc7+ Qxc7\
        9.Bxf6 Nb4 10.Rc1 Nxa2
 11.Bg5 Nxc1 12.Bxc1 Qxc2 13.Qg5 Bb4+ 14.Bd2 Ba4 15.Be2 Qc1+ 16.Bd1 Qxd1# 0-1
"""


def test_single_pgn(single_pgn):
    from pgn import PGN
    pgn = PGN(single_pgn)
    _test(pgn.tags['event'] == 'Event name',
          "Event name: " + pgn.tags['event'])
    _test(pgn.tags['result'] == '0-1',
          "Result: " + pgn.tags['result'])
    _test(pgn.moves_string == '1.e4 d5 2.Nc3 d4 3.Nb5 e5 4.d3 Bd7 5.Qh5 Nc6 \
6.Bg5 Nf6 7.Qh4 a6 8.Nxc7+ Qxc7 9.Bxf6 Nb4 10.Rc1 Nxa2 11.Bg5 Nxc1 \
12.Bxc1 Qxc2 13.Qg5 Bb4+ 14.Bd2 Ba4 15.Be2 Qc1+ 16.Bd1 Qxd1# 0-1',
          "move string does't match: " + pgn.moves_string)
    # assert type(pgn.moves) == type(list)


def test_multiple_pgns(multiple_pgn):
    from pgn import get_pgns
    pgns = get_pgns(multiple_pgn)
    _test(len(pgns) == 2)
    test_single_pgn(pgns.values()[0].pgn)


def test_sans():
    from san import Move
    move = Move('e4')
    move = Move('Qe4+')
    move = Move('O-O-O')
    move = Move('exd5')
    move = Move('Qe4xd5+')
    assert move.new_square == 'd5'
    assert move.piece_moved == move.queen
    assert move.is_capture
    assert move.is_check
    assert not move.is_checkmate
    assert not move.is_promotion

    move = Move('e4')
    assert move.new_square == 'e4'
    assert move.piece_moved == move.pawn

    move = Move('O-O')
    assert move.piece_moved == move.king, move.piece_moved
    assert move.is_castle
    assert not move.is_capture
    assert not move.is_check


def _test(condition, error_message=None):
    if not condition:
        raise AssertionError(error_message)

if __name__ == '__main__':
    test_single_pgn(single_pgn)
    test_multiple_pgns(multiple_pgn)
    test_sans()
