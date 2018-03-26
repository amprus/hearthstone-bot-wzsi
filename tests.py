from board import Board
from naive_bots import *

b = None


def agrr_make_move(ag, bb):
    ag.make_move(bb)


def pass_make_move(ps, bb):
    ps.make_move(bb)


def play(r, ag, ps, bb):
    for i in range(r):
        agrr_make_move(ag, bb)
        pass_make_move(ps, bb)


def play_times(r, bc):
    for i in range(r):
        bc = Board()
        bc.initialize_game()
        agg = AggressiveBot()
        pss = PassiveBot()
        print("Aggressive player: {}\nPassive Player: {}".format(bc.active_player + 1, 1 if bc.active_player == 1 else 2))
        while not bc.over:
            play(1, agg, pss, bc)
