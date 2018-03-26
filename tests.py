from board import Board
from naive_bots import AggressiveBot, PassiveBot
from mcts.board_analyzer import Analyzer
from mcts.tree import TreeManager

from copy import deepcopy


b = Board()
b.initialize_game()

ag = AggressiveBot()
ps = PassiveBot()


def agrr_make_move():
    ag.make_move(b)


def pass_make_move():
    ps.make_move(b)


def p():
    print(b)

p()
analyzer = Analyzer(b)

# Show available actions for this moment
def pa():
    actions = analyzer.generate_actions()
    for action in actions:
        print(action)


# Show grade for this state of board
def ps():
    score = analyzer.grade_board()
    print(score)


# Use this method to show decision tree in-game
def tree():
    tm = TreeManager(b)
    tm.make_children_for_current()
    print(tm)    

# Demo with expanding left-most part of the tree
def tree_demo():
    tm = TreeManager(b)
    for i in range(6):
        tm.make_children_for_current()
        tm.switch_to_child(0)
    print(tm)