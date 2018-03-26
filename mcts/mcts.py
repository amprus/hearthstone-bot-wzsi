from .tree import TreeManager

class MonteCarloPlayer:
    def make_move(self, board):
        tm = TreeManager(board)
        tm.make_children_for_current()
        # TODO: search tree etc