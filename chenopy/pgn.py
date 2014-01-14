# -*- coding: utf-8 -*-
"""Tools to parse PGN."""

from __future__ import unicode_literals

import re


class Game(object):

    """ Represents a PGN (a single game)."""

    _VALID_TAGS = [
        'event',
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
        self.lazy = lazy_parsing
        self.tags = {}
        self.moves_string = {}
        self.moves = []
        self._pgn = ''
        self.pgn = pgn_string

    def __str__(self):
        return "Game <{0} vs {1}>".format(self.tags.get('white', 'white'),
                                          self.tags.get('black', 'black'))

    @property
    def pgn(self):
        """Return the pgn property."""
        return self._pgn

    @pgn.setter
    def pgn(self, pgn):
        """Check and set the pgn property."""
        pgn = re.sub(r'\ +', ' ', pgn.strip())
        self.validate_lazy(pgn)
        self._pgn = pgn
        self._parse()

    def _parse(self):
        moves = ''
        for line in self.pgn.split("\n"):
            line = line.strip()
            if line.startswith('['):
                line = line.strip("[]").split(' ')
                attr = line[0].lower().strip()
                value = " ".join(line[1:]).strip().strip('"')
                if attr not in self._VALID_TAGS and not self.lazy:
                    message = 'Tags "{0}" not in valid tags list: {1}'
                    raise ValueError(message.format(attr,
                                                    str(self._VALID_TAGS)))
                # set in tags dict for safe access of tags
                self.tags[attr] = value
                # set as attribute of object for simple access of known tags
                setattr(self, attr, value)
            else:  # moves
                if line != '':
                    moves += line + ' '

        self.moves_string = re.sub(r'\s+', ' ', moves.strip())

    @staticmethod
    def validate_lazy(pgn):
        """Validate the pgn string."""
        if not pgn.startswith("[Event"):
            raise TypeError("Not a valid PGN. Doesn't start with Event attr.")


def get_pgns(pgn_string):
    """Return a list of Game instance based on the pgn string."""
    pgns = []
    current_pgn = ''
    for line in pgn_string.strip().split("\n"):
        if line.startswith('[Event'):
            if current_pgn != '':
                pgn = Game(current_pgn)
                pgns.append(pgn)
                current_pgn = ''
        current_pgn += line + "\n"

    if current_pgn != '':
        pgn = Game(current_pgn)
        pgns.append(pgn)

    return pgns
