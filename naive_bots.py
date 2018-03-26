import utils
from algorithms import Algorithms
from cards import Spell, Minion, Hero


class NaiveBot:
    def __init__(self):
        self.possible_moves = []  # best cards on board
        self.possible_cards = []  # best cards in hand
        self.targets = []
        self.battles = []
        self.side = None
        self.hand = None
        self.mana = None

    def make_move(self, board):
        self.init_move(board)
        self.choose_cards_to_play()
        self.define_possible_moves()
        self.choose_targets(board.sides[0] if board.active_player == 1 else board.sides[1])
        self.create_battles()
        self.fight_battles(board)
        self.play_cards(board)
        self.end_turn(board)

    def init_move(self, board):
        self.side = board.sides[board.active_player]
        self.hand = board.players[board.active_player].hand
        self.mana = board.players[board.active_player].mana

    def choose_cards_to_play(self):
        self.possible_cards = Algorithms.knapsack_for_cards(self.hand.cards, self.mana, self.card_rating)

    def define_possible_moves(self):
        for index, minion in enumerate(self.side):
            if not isinstance(minion, Hero) and minion.can_attack:
                self.possible_moves.append((minion, index))
        # add spells to possible moves
        for i in range(len(self.possible_cards), 0, -1):
            if isinstance(self.possible_cards[i - 1][0], Spell):
                self.possible_moves.append(self.possible_cards.pop(i - 1))

    def create_battles(self):
        for target in self.targets:
            self.battles.append(Algorithms.subsets_sum_for_attack(self.possible_moves, target))

    def play_cards(self, board):
        self.possible_cards.sort(key=lambda x: x[1], reverse=True)
        for card, index in self.possible_cards:
            if isinstance(card, Minion) and not isinstance(card, Hero):
                board.play_minion(index)

    def fight_battles(self, board):
        for battle_index, battle in enumerate(self.battles):
            attacking_cards, target_index = battle[0], battle[1]
            attacking_cards.sort(key=lambda x: x[1], reverse=True)
            for i in range(len(attacking_cards)):
                card, hand_index = attacking_cards[i]
                if isinstance(card, Spell):
                    board.cast_spell(hand_index, target_index, safe=True)
                    self.repair_hand_indexes(hand_index)
                    self.repair_other_battles(hand_index, battle_index)
                elif isinstance(card, Minion):
                    board.attack(hand_index, target_index, safe=True)

    def end_turn(self, board, silent=True):
        self.__init__()
        board.end_turn(safe=True)
        if not silent:
            print(board)

    def choose_taunts(self, opponent_side):
        for position, card in enumerate(opponent_side):
            if card.has_taunt():
                self.targets.append((card, position))

    def choose_targets(self, opponent_side):
        raise NotImplementedError

    def card_rating(self, card):
        raise NotImplementedError

    def repair_hand_indexes(self, hand_index):
        for index, card in enumerate(self.possible_cards):
            if card[1] > hand_index:
                self.possible_cards[index] = (card[0], card[1] - 1)

    def repair_other_battles(self, hand_index, battle_index):
        for index, battle in enumerate(self.battles):
            if index > battle_index:
                cards = battle[0]
                for idx, card in enumerate(cards):
                    if isinstance(card[0], Spell) and card[1] > hand_index:
                        cards[idx] = (card[0], card[1] - 1)
                        self.battles[index] = (cards, battle[1])


class AggressiveBot(NaiveBot):

    def choose_targets(self, opponent_side):
        self.choose_taunts(opponent_side)
        for position, card in enumerate(opponent_side):
            if card.attack >= 4 or card.health > 4:
                self.targets.append((card, position))
        self.targets.append((opponent_side[0], 0))

    def card_rating(self, card):
        rating = (2*card.attack)
        if isinstance(card, Minion):
            rating += (0.75 * card.health)
            if card.has_taunt():
                rating += 2
        return rating


class PassiveBot(NaiveBot):

    def choose_targets(self, opponent_side):
        self.choose_taunts(opponent_side)
        for position, card in enumerate(opponent_side):
            if card.attack >= 2:
                self.targets.append((card, position))
        self.targets.append((opponent_side[0], 0))

    def card_rating(self, card):
        if isinstance(card, Spell):
            return card.attack * (3 / 5)
        elif isinstance(card, Minion):
            rating = card.health + (card.attack * (3 / 5))
            if card.has_taunt():
                rating += 2
            return rating
