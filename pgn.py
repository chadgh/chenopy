import hashlib
import re


def get_pgns(pgn_string):
    pgns = {}
    current_pgn = ''
    for line in pgn_string.strip().split("\n"):
        if line.startswith('[Event'):
            if current_pgn != '':
                pgn = PGN(current_pgn)
                pgns[pgn.unique_id] = pgn
                current_pgn = ''
        current_pgn += line + "\n"
    else:
        if current_pgn != '':
            pgn = PGN(current_pgn)
            pgns[pgn.unique_id] = pgn
    return pgns


class PGN(object):
    '''
    Represents a PGN (a single game).

    Example single game PGN:
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
    '''

    _valid_tags = ['event',
                   'site',
                   'date',
                   'white',
                   'black',
                   'whiteelo',
                   'blackelo',
                   'timecontrol',
                   'termination',
                   'result',
                   'round',
                   ]

    def __init__(self, pgn_string=None):
        '''Accept a pgn string to represent.'''
        self.pgn = pgn_string

    def __str__(self):
        return "PGN <{0} vs {1}>".format(self.tags['white'],
                                         self.tags['black'])

    @property
    def pgn(self):
        return self._pgn

    @pgn.setter
    def pgn(self, pgn):
        pgn = re.sub(r'\ +', ' ', pgn.strip())
        self.validate_lazy(pgn)
        self._pgn = pgn
        self.unique_id = self.generate_hash(pgn)
        self._parse()

    def _parse(self):
        moves = ''
        setattr(self, 'tags', {})
        for line in self.pgn.split("\n"):
            line = line.strip()
            if line.startswith('['):
                line = line.strip("[]").split(' ')
                attr = line[0].lower()
                value = " ".join(line[1:]).strip().strip('"')
                if attr not in self._valid_tags:
                    message = 'Tags "{0}" not in valid tags list: {1}'
                    raise ValueError(message.format(attr,
                                                    str(self._valid_tags)))
                self.tags[attr] = value
            else:  # moves
                if line != '':
                    moves += line + ' '
        setattr(self, 'moves_string', re.sub(r'\s+', ' ', moves.strip()))

    @staticmethod
    def generate_hash(pgn_string):
        return hashlib.sha224(pgn_string).hexdigest()

    @staticmethod
    def validate_lazy(pgn):
        if not pgn.startswith("[Event"):
            raise Exception("Not a valid PGN. Doesn't start with Event attr.")

if __name__ == '__main__':
    pgn_string = '''
[Event "Let's Play!"]
[Site "Chess.com"]
[Date "2013.09.16"]
[White "chadgh"]
[Black "Nickdpad"]
[Result "*"]
[WhiteElo "1458"]
[BlackElo "1318"]
[TimeControl "1 in 1 day"]

1.e4 c5 2.Bc4 d6 3.Nf3 h6 4.Nc3 Nf6 5.d4 cxd4 6.Nxd4 Nc6 7.Bb5 \
        Bd7 8.Be3 g6 9.Qd2 Bg7 10.O-O-O h5
 11.Nd5 Nxd5 12.exd5 Ne5 13.f4 Bxb5 *
    '''
    pgn = PGN(pgn_string)
    # print pgn.moves_string
    # print pgn.tags
    # print pgn.unique_id
    # print pgn.pgn
    assert pgn.tags['event'] == "Let's Play!"
    assert pgn.tags['white'] == "chadgh"

    pgn_file = '''
[Event "Beast Team Tournament - Round 2"]
[Site "Chess.com"]
[Date "2013.07.16"]
[White "chadgh"]
[Black "iandut2011"]
[Result "1/2-1/2"]
[WhiteElo "1422"]
[BlackElo "1358"]
[TimeControl "1 in 3 days"]
[Termination "Game drawn by repetition"]

1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nc6 5.Bb5 Bd7 6.Nc3 a6 7.Bc4 b5 8.Bd5\
        Nf6 9.Nf3 e6 10.e5 Nxd5
 11.Nxd5 exd5 12.Qxd5 Be7 13.exd6 Bf6 14.Bg5 Bxg5 15.Nxg5 Qf6 16.Nxh7 \
         Rxh7 17.O-O O-O-O 18.c4 Qg6 19.cxb5 axb5 20.a4 b4
 21.a5 Bh3 22.Qxc6+ Kb8 23.Qc7+ Ka8 24.Qxd8+ Ka7 25.Qc7+ Ka8 26.Qd8+ \
         Ka7 27.Qc7+ Ka8 28.Qd8+ 1/2-1/2


[Event "Beast Team Tournament - Round 2"]
[Site "Chess.com"]
[Date "2013.07.16"]
[White "shonbo"]
[Black "chadgh"]
[Result "0-1"]
[WhiteElo "1354"]
[BlackElo "1437"]
[TimeControl "1 in 3 days"]
[Termination "chadgh won by resignation"]

1.e4 c5 2.Nf3 d6 3.Bb5+ Bd7 4.Bxd7+ Qxd7 5.O-O e5 6.Nc3 Nf6 7.h3 \
        Be7 8.d3 Nc6 9.Nb5 a6 10.Nc3 O-O
 11.a3 d5 12.exd5 Nxd5 13.Nxd5 Qxd5 14.Be3 Rfd8 15.Bg5 f6 16.Bd2 a5\
         17.Re1 Nd4 18.Nxd4 cxd4 19.c4 Qc5 20.b4 axb4
 21.Bxb4 Qc7 22.Bxe7 Qxe7 23.Qb3 Kh8 24.Rab1 Rxa3 25.Qxb7 Qxb7 26.\
         Rxb7 Rxd3 27.c5 h6 28.Rc1 Rc3 29.Rbb1 Rc8 30.Rxc3 dxc3
 31.Rc1 Rxc5 32.Kf1 Kh7 33.Ke2 f5 34.Kd3 e4+ 35.Kd4 Rc8 36.Rxc3 Rxc3\
         37.Kxc3 g5 38.Kd4 Kg6 39.Ke5 h5 40.Kd4 Kf6
 41.Kd5 h4 42.Kd4 Ke6 43.Ke3 Ke5 44.Ke2 Kd4 45.Kd2 f4 46.Ke2 Kc3 47.\
         Kd1 Kd3 48.Ke1 e3 49.fxe3 fxe3 50.Kd1 e2+
 51.Ke1 Ke3 0-1


[Event "Beast Team Tournament - Round 2"]
[Site "Chess.com"]
[Date "2013.08.05"]
[White "chadgh"]
[Black "shonbo"]
[Result "1-0"]
[WhiteElo "1451"]
[BlackElo "1364"]
[TimeControl "1 in 3 days"]
[Termination "chadgh won by resignation"]

1.e4 e5 2.Nf3 Nc6 3.Bc4 d6 4.d3 h6 5.O-O Nf6 6.Nc3 Qe7 7.d4 exd4 8.Nxd4 Nxd4\
        9.Qxd4 c5 10.Qd2 a6
 11.Nd5 Nxe4 12.Qa5 Qd7 13.Re1 Be7 14.Rxe4 O-O 15.Rxe7 Qg4 16.Bxh6 Be6 17.Nf6+\
         gxf6 18.Bxf8 Kxf8 19.Bxe6 fxe6 20.Rxb7 Qe2
 21.Qc7 Qh5 22.Qg7+ 1-0
    '''
    pgns = get_pgns(pgn_file)
    for uid, pgn in pgns.items():
        print uid, str(pgn)
