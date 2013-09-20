import hashlib
import re


def get_pgns(pgn_string):
    pgns = {}
    current_pgn = ''
    for line in pgn_string.strip().split("\n"):
        if line.startswith('[Event'):
            if current_pgn != '':
                pgn = Game(current_pgn)
                pgns[pgn.unique_id] = pgn
                current_pgn = ''
        current_pgn += line + "\n"
    else:
        if current_pgn != '':
            pgn = Game(current_pgn)
            pgns[pgn.unique_id] = pgn
    return pgns


class Game(object):
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

    def __init__(self, pgn_string=None, lazy_parsing=False):
        '''Accept a pgn string to represent.'''
        self.lazy = lazy_parsing
        self.tags = {}
        self.move_string = {}
        self.moves = []
        self.pgn = pgn_string

    def __str__(self):
        return "Game <{0} vs {1}>".format(self.tags.get('white', 'white'),
                                          self.tags.get('black', 'black'))

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
        for line in self.pgn.split("\n"):
            line = line.strip()
            if line.startswith('['):
                line = line.strip("[]").split(' ')
                attr = line[0].lower().strip()
                value = " ".join(line[1:]).strip().strip('"')
                if attr not in self._valid_tags and not self.lazy:
                    message = 'Tags "{0}" not in valid tags list: {1}'
                    raise ValueError(message.format(attr,
                                                    str(self._valid_tags)))
                # set in tags dict for safe access of tags
                self.tags[attr] = value
                # set as attribute of object for simple access of known tags
                setattr(self, attr, value)
            else:  # moves
                if line != '':
                    moves += line + ' '

        self.moves_string = re.sub(r'\s+', ' ', moves.strip())

    @staticmethod
    def generate_hash(pgn_string):
        return hashlib.sha224(pgn_string).hexdigest()

    @staticmethod
    def validate_lazy(pgn):
        if not pgn.startswith("[Event"):
            raise Exception("Not a valid PGN. Doesn't start with Event attr.")
