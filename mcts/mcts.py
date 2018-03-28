from .tree import TreeManager

from interruptingcow import timeout 
from time import time
from random import random
from math import sqrt

class MonteCarloPlayer:
    def __init__(self):
        self.EXP_CONST = 1.0 / sqrt(2)

    def make_move(self, board, seconds_for_move, max_children, print_res=False):
        player = board.get_active_idx() + 1
        tm = TreeManager(board, max_children, player)
        time_start = time()
        # while time() < time_start + seconds_for_move:
        try:
            with timeout(seconds_for_move, exception=RuntimeError):
                while True:
                    self.tree_policy(tm)
                    self.default_policy(tm)
                    self.backup(tm)
        except RuntimeError:
            tm.go_to_root()
            if print_res:
                print(tm)
            best_idx = tm.get_best_child_index_for_current()
            tm.switch_to_child(best_idx)
            actions = tm.get_actions_for_current()
            if print_res:
                print(actions)
            for action in actions:
                action.board = board
                board.execute_action(action)

    def tree_policy(self, tm):
        while not tm.is_current_leaf():
            if not tm.current.expanded:
                tm.make_children_for_current()
            idx = tm.get_first_not_visited_child_idx()
            if idx is not None:
                self.expand(tm, idx)
                break
            else:
                best_idx = tm.get_best_child_index_for_current(self.EXP_CONST)
                tm.switch_to_child(best_idx)
                
    def expand(self, tm, idx):
        tm.switch_to_child(idx)
        if not tm.current.expanded:
            tm.make_children_for_current()

    def default_policy(self, tm):
        while not tm.is_current_leaf():
            if not tm.current.expanded:
                tm.make_children_for_current()
            tm.switch_to_random_child()

    def backup(self, tm):
        tm.propagate_results_from_current()
        tm.go_to_root()


class ExceededSetTimeError(RuntimeError):
    pass
