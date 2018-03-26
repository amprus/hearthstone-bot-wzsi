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
        for action in Analyzer(board).generate_actions():
            new_board_state = deepcopy(board)
            new_action = deepcopy(action)
            new_actions = list(actions)
            new_actions.append(new_action)
            # Set new board for action to execute
            # Otherwise it will execute in main board!!!
            new_action.board = new_board_state
            new_board_state.execute_action(new_action)
            if isinstance(new_action, EndTurn):
                states.append((new_board_state, new_actions))
                continue
            self._generate_children(new_board_state, states, new_actions)

    def propagate_results(self, wins=0, loses=0):
        self.wins_count += wins
        self.loses_count += loses
        if not self.parent is None:
            self.parent.propagate_results(wins, loses)

    def _on_game_over(self, winning_player):
        if winning_player == 1:
            self.propagate_results(wins=1)
        else:
            self.propagate_results(loses=1)

    def __str__(self):
        return '  ' * self.level + 'TreeNode(L:{}, A:{})'.format(self.level, self.last_actions)

    def __repr__(self):
        return '  ' * self.level + 'TreeNode(L:{}, A:{})'.format(self.level, self.last_actions)


class TreeManager:
    def __init__(self, board):
        self.root = BoardTree(board_state=deepcopy(board),
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

    def a(self, node):
        delim = '\n' if node.children else ''
        return str(node) + delim + '\n'.join([self.a(child) for child in node.children])

    def __str__(self):
        return self.a(self.root)