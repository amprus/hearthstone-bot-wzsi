import numpy as np

from cards import Hero, Minion, Spell, Coin
from card_defs import card_defs, hero_defs

class Deck:
  cards = []

  #def __init__(self):        #dummy one
  #  for i in range(0, 20):
  #    self.cards.append(Card(i))

  def __init__(self, cards):
    self.cards = cards

  def show_deck(self):
    for card in self.cards:
        card.show_card()

  def shuffle(self):
    np.random.shuffle(self.cards)

  def pop_card(self):
    return self.cards.pop()

  def has_cards(self):
    return len(self.cards) > 0


class Hand:
    def __init__(self, deck):
        self.deck = deck
        self.cards = []

    def draw(self):
        card = self.deck.pop_card()
        if len(self.cards) < 10:
            self.cards.append(card)

    def play_card(self, index):
        return self.cards.pop(index)

    def add_coin(self):
        self.cards.append(Coin())

    def __str__(self):
        hand_str = 'HAND:\n'
        for card in self.cards:
            hand_str += str(card) + '\n'
        return hand_str


class DeckInitializer:
    def make_std_deck(self):
        cards = [self._make_card_from_def(cdef) for cdef in card_defs] + [self._make_card_from_def(cdef) for cdef in card_defs]
        deck = Deck(cards)
        deck.shuffle()
        return deck

    def create_hero(self, name):
        return Hero.from_dict(hero_defs[name])

    def _make_card_from_def(self, cdef):
        if cdef['type'] == 'minion':
            return Minion.from_dict(cdef)
        elif cdef['type'] == 'spell':
            return Spell.from_dict(cdef)
        elif cdef['type'] == 'hero':
            return Hero.from_dict(cdef)