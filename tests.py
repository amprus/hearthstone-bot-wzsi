from board import Board
from naive_bots import *

b = Board()
b.initialize_game()

ag = AggressiveBot()
ps = PassiveBot()


def agrr_make_move():
    ag.make_move(b)


def pass_make_move():
    ps.make_move(b)