from deck import DeckInitializer, Hand
from player import Player
from random import random
from cards import Minion, Hero
from actions import ActionFactory
import sys


class Board:
    def __init__(self):
        self.actions = ActionFactory(self)
        self.deck1 = []
        self.deck2 = []
        self.players = []
        self.sides = [[], []]
        self.active_player = 0
        self.over = False

    def initialize_game(self):
        initializer = DeckInitializer()
        self.deck1 = initializer.make_std_deck()
        self.deck2 = initializer.make_std_deck()
        p1_starts = self._player1_starts()
        self.active_player = 0 if p1_starts else 1 
        self.players = [
            Player(id=1, deck=self.deck1, hand=Hand(self.deck1), starts=p1_starts),
            Player(id=2, deck=self.deck2, hand=Hand(self.deck2), starts=not p1_starts)
        ]
        self.sides = [[initializer.create_hero('jaina')], [initializer.create_hero('jaina')]]

    def _player1_starts(self):
        return random() < 0.5

    def play_minion(self, index):
        self.execute_action(self.actions.play_minion(index))

    def cast_spell(self, card_idx, target_idx, safe=False):
        self.execute_action(self.actions.cast_spell(card_idx, target_idx, safe))

    def end_turn(self, safe=False):
        self.execute_action(self.actions.end_turn(safe))

    def active_draw_card(self, card_idx):
        self.execute_action(self.actions.draw(card_idx))

    def attack(self, atk_idx, def_idx, safe=False):
        self.execute_action(self.actions.attack(atk_idx, def_idx, safe))

    def execute_action(self, action):
        action.execute()

    def change_active_player(self):
        self.active_player = self.get_other_idx()

    def get_active_hand(self):
        return self.get_active_player().hand

    def get_other_hand(self):
        return self.get_other_player().hand

    def get_active_idx(self):
        return self.active_player

    def get_other_idx(self):
        return 1 if self.active_player == 0 else 0

    def get_active_side(self):
        return self.sides[self.get_active_idx()]

    def get_other_side(self):
        return self.sides[self.get_other_idx()]

    def get_active_player(self):
        return self.players[self.get_active_idx()]

    def get_other_player(self):
        return self.players[self.get_other_idx()]

    def game_loop(self):
        pass

    def game_over(self, active):
        print('Player #{} won!'.format(active+1))
        self.over = True

    def __str__(self):
        board_str = ''
        for player in self.players:
            board_str += str(player) + '\n'
        i = 1
        board_str += '\n\n'
        for side in self.sides:
            board_str += 'SIDE OF PLAYER #{}:\n'.format(i)
            i += 1
            for card in side:
                board_str += '{}\n'.format(card)
        return board_str
