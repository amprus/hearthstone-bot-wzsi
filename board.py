from deck import DeckInitializer, Hand
from player import Player
from random import random
from cards import Minion


class Board:
    def __init__(self):
        self._initialize_game()
        self.sides = [[], []]

    def _initialize_game(self):
        initializer = DeckInitializer()
        self.deck1 = initializer.make_std_deck()
        self.deck2 = initializer.make_std_deck()
        p1_starts = self._player1_starts()
        self.active_player = 0 if p1_starts else 1 
        self.players = [
            Player(id=1, hand=Hand(self.deck1), hero=initializer.create_hero('jaina'), starts=p1_starts),
            Player(id=2, hand=Hand(self.deck2), hero=initializer.create_hero('jaina'), starts=not p1_starts)
        ]

    def _player1_starts(self):
        return random() < 0.5

    def play_card(self, index):
        if len(self.sides[self.active_player]) < 7:
            card = self.players[self.active_player].play_card(index)
            if card:
                self.sides[self.active_player].append(card)

    def end_turn(self):
        self.players[self.active_player].end_turn()
        self.active_player = 1 if self.active_player == 0 else 0
        self.players[self.active_player].start_turn()
        for card in self.sides[self.active_player]:
            if isinstance(card, Minion):
                card.can_attack = True

    def use_card(self, index1, index2):
        pass

    def attack(self, index1, index2):
        other_player = 1 if self.active_player == 0 else 1
        attacker = self.sides[self.active_player][index1]
        defender = self.sides[other_player][index2]
        attacker.battle(defender)
        if attacker.health <= 0:
            self.sides[self.active_player].pop(index1)
        if defender.health <= 0:
            self.sides[other_player].pop(index2)

    def game_loop(self):
        pass

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