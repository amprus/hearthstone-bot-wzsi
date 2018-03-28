from board import Board
from .board_analyzer import Analyzer

from actions import EndTurn

from copy import deepcopy
from random import choice
from math import log, sqrt


class BoardTree:
    def __init__(self, board_state=None, last_actions=[], parent=None, children=[], max_children=20):
        self.children = children
        self.parent = parent
        self.last_actions = last_actions
        self.board_state = board_state
        self.level = 0 if parent is None else parent.level + 1
        self.wins_count = 0
        self.losses_count = 0
        self.expanded = False
        self.visited = False
        self.max_children = max_children

    def make_childen(self):
        self.visited = True
        states = []
        self._generate_children(self.board_state, states, [])
        self.expanded = True
        self.children = [BoardTree(board_state=state, last_actions=actions, parent=self, children=[]) for state, actions in states]

    def _generate_children(self, board, states, actions):
        if self.is_leaf():
            return
        stack = []
        stack.append((board, actions))
        while stack:
            s_board, s_actions = stack.pop()
            if len(states) >= self.max_children:
                return
            for action in Analyzer(s_board).generate_actions():
                new_board_state = deepcopy(s_board)
                new_actions = list(s_actions)
                new_actions.append(action)
                # Set new board for action to execute
                # Otherwise it will execute in main board!!!
                action.board = new_board_state
                new_board_state.execute_action(action)
                if isinstance(action, EndTurn):
                    states.append((new_board_state, new_actions))
                    continue
                if new_board_state.is_game_over():
                    states.append((new_board_state, new_actions))
                    continue
                # self._generate_children(new_board_state, states, new_actions)
                stack.append((new_board_state, new_actions))

    def get_score(self):
        total_count = self.wins_count + self.losses_count
        return float(self.wins_count) / total_count if total_count != 0 else 0.0

    def get_best_child_index(self, exp_const):
        self_total_visits = self.wins_count + self.losses_count
        scores = [c.get_score() for c in self.children]
        total_visits = [c.wins_count + c.losses_count for c in self.children]
        total_scores = []
        for score, visits in zip(scores, total_visits):
            if visits == 0:
                total_scores.append(0.0)
                continue
            c = exp_const * sqrt(2.0 * log(self_total_visits) / visits)
            total_scores.append(score + c)
        return total_scores.index(max(total_scores))

    def is_leaf(self):
        return self.board_state.is_game_over()

    def propagate_results(self, wins=0, losses=0):
        self.wins_count += wins
        self.losses_count += losses
        if not self.parent is None:
            self.parent.propagate_results(wins, losses)

    def was_chosen(self):
        return (self.wins_count + self.losses_count) != 0

    def __str__(self):
        return '  ' * self.level + 'TreeNode(L:{}, A:{}, W:{}/{})'.format(self.level, self.last_actions, self.wins_count, self.losses_count)

    def __repr__(self):
        return '  ' * self.level + 'TreeNode(L:{}, A:{}, W:{}/{})'.format(self.level, self.last_actions, self.wins_count, self.losses_count)


class TreeManager:
    def __init__(self, board, max_children, player_no):
        new_board = deepcopy(board)
        new_board.exit_on_game_over = False
        self.root = BoardTree(board_state=new_board,
                              parent=None,
                              last_actions=[],
                              children=[],
                              max_children=max_children)
        self.current = self.root
        self.player_no = player_no

    def make_children_for_current(self):
        self.current.make_childen()

    def switch_to_parent(self):
        parent = self.current.parent
        self.current = parent if parent is not None else self.current

    def get_best_child_index_for_current(self, exp_const=0.0):
        return self.current.get_best_child_index(exp_const)

    def switch_to_child(self, idx):
        self.current = self.current.children[idx]

    def switch_to_random_child(self):
        indices = list(range(len(self.current.children)))
        idx = choice(indices)
        self.switch_to_child(idx)

    def get_actions_for_current(self):
        return self.current.last_actions

    def go_to_root(self):
        self.current = self.root

    def is_current_leaf(self):
        return self.current.is_leaf()

    def propagate_results_from_current(self):
        winner = self.current.board_state.winner
        if winner == self.player_no:
            self.current.propagate_results(wins=1)
        else:
            self.current.propagate_results(losses=1)

    def was_current_visited(self):
        return self.current.was_chosen()

    def get_first_not_visited_child_idx(self):
        for idx, c in enumerate(self.current.children):
            if not c.was_chosen():
                return idx
        return None

    def a(self, node):
        delim = '\n' if node.children else ''
        return str(node) + delim + '\n'.join([self.a(child) for child in node.children])

    def __str__(self):
        # return self.a(self.root) + '\n# of children: {}'.format(len(self.current.children))
        string = str(self.root) + '\n'
        for c in self.root.children:
            string += str(c) + '\n'
        return string