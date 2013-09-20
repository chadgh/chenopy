import re


def valid_san(san_string):
    pass


class Move(object):
    pawn = 'P'
    king = 'K'
    queen = 'Q'
    bishop = 'B'
    knight = 'N'
    rook = 'R'

    castle_kingside = 'O-O'
    castle_queenside = 'O-O-O'

    check = '+'
    checkmate = '#'
    promotion = '='
    capture = 'x'

    valid_pieces = [pawn,
                    king,
                    queen,
                    bishop,
                    knight,
                    rook]

    valid_promotions = [queen,
                        bishop,
                        knight,
                        rook]

    valid_castle_moves = [castle_kingside,
                          castle_queenside,
                          ]

    valid_rank = range(1, 9)
    valid_file = 'abcdefgh'

    san_re = re.compile(r'''([a-h]          # pawn move
                            ([1-8]|       # simple move
                             x[a-h][1-8]  # move with capture
                             )(=[QBNR])?  # promotion
                           |
                           [KQBNR]        # other piece move
                            [a-h]?        # file disambiguation
                            [1-8]?        # rank disambiguation
                            x?            # capture?
                            [a-h][1-8]    # move location
                           |
                           O\-O(\-O)?     # castle move
                          )\+?\#?         # optional check or checkmate''',
                        re.VERBOSE)

    def __init__(self, san, parent=None, previous=None):
        self.san = san
        if not self.san_re.match(san):
            raise ValueError(san + " not valid")
        self.is_check = False
        self.is_checkmate = False
        self.is_capture = False
        self.is_promotion = False
        self.is_castle = False
        self.promotion_to = None
        self.piece_moved = None
        self.new_square = None
        self.parent_move = parent      # pieces last move
        self.previous_move = previous  # previous move in game
        self._parse()

    def _parse(self):
        parts = list(self.san)
        if parts[0] in self.valid_pieces:
            self.piece_moved = parts[0]
        elif parts[0] in self.valid_file:
            self.piece_moved = self.pawn
        elif self.san in self.valid_castle_moves:
            self.piece_moved = self.king
            self.is_castle = True

        if self.check in parts:
            self.is_check = True

        if self.checkmate in parts:
            self.is_check = True
            self.is_checkmate = True

        if self.promotion in parts:
            self.promotion = True
            index = parts.index(self.promotion) + 1
            if parts[index] in self.valid_promotions:
                self.promotion_to = parts[index]

        if self.capture in parts:
            self.is_capture = True

        matches = re.findall(r'[a-h][1-8]', self.san)
        if len(matches) != 0:
            self.new_square = matches[-1]


if __name__ == '__main__':
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
