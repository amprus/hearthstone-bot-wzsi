from board import Board
from .board_analyzer import Analyzer

from actions import EndTurn

from copy import deepcopy


class BoardTree:
    def __init__(self, board_state=None, last_actions=[], parent=None, children=[]):
        self.children = children
        self.parent = parent
        self.last_actions = last_actions
        self.board_state = board_state
        self.level = 0 if parent is None else parent.level + 1
        self.wins_count = 0
        self.loses_count = 0

    def make_childen(self):
        states = []
        self._generate_children(self.board_state, states, [])
        self.children = [BoardTree(board_state=state, last_actions=actions, parent=self, children=[]) for state, actions in states]

    def _generate_children(self, board, states, actions):
        if self.is_leaf():
            return
        for action in Analyzer(board).generate_actions():
            new_board_state = deepcopy(board)
            new_actions = list(actions)
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
            self._generate_children(new_board_state, states, new_actions)

    def is_leaf(self):
        return self.board_state.is_game_over()

    def propagate_results(self, wins=0, loses=0):
        self.wins_count += wins
        self.loses_count += loses
        if not self.parent is None:
            self.parent.propagate_results(wins, loses)

    def __str__(self):
        return '  ' * self.level + 'TreeNode(L:{}, A:{}, W:{}/{})'.format(self.level, self.last_actions, self.wins_count, self.loses_count)

    def __repr__(self):
        return '  ' * self.level + 'TreeNode(L:{}, A:{}, W:{}/{})'.format(self.level, self.last_actions, self.wins_count, self.loses_count)


def on_game_over(node):
    def func(winning_player):
        node.propagate_results(winning_player)
    return func


class TreeManager:
    def __init__(self, board):
        new_board = deepcopy(board)
        new_board.exit_on_game_over = False
        self.root = BoardTree(board_state=new_board,
                              parent=None,
                              last_actions=[],
                              children=[])
        self.current = self.root

    def make_children_for_current(self):
        self.current.make_childen()

    def switch_to_parent(self):
        parent = self.current.parent
        self.current = parent if parent is not None else self.current

    def switch_to_child(self, idx):
        self.current = self.current.children[idx]

    def go_to_root(self):
        self.current = self.root

    def is_current_leaf(self):
        return self.current.is_leaf()

    def propagate_results_from_current(self):
        winner = self.current.board_state.winner
        if winner == 1:
            self.current.propagate_results(wins=1)
        else:
            self.current.propagate_results(loses=1)

    def a(self, node):
        delim = '\n' if node.children else ''
        return str(node) + delim + '\n'.join([self.a(child) for child in node.children])

    def __str__(self):
        return self.a(self.root) + '\n# of children: {}'.format(len(self.current.children))