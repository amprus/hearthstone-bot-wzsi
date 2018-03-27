from board import Board
from naive_bots import AggressiveBot, PassiveBot
from mcts.board_analyzer import Analyzer
from mcts.tree import TreeManager
from mcts.mcts import MonteCarloPlayer

from copy import deepcopy


b = Board(exit_on_game_over=True)
# b = Board()
b.initialize_game()

ag = AggressiveBot()
ps = PassiveBot()
mt = MonteCarloPlayer()


def agrr_make_move():
    ag.make_move(b)


def pass_make_move():
    ps.make_move(b)


def mt_make_move():
    mt.make_move(b, 20, 100, print_res=True)


def p():
    print(b)

p()
analyzer = Analyzer(b)

# Show available actions for this moment
def pa():
    actions = analyzer.generate_actions()
    for action in actions:
        print(action)