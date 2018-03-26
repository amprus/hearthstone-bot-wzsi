from actions import ActionFactory


class Analyzer:
    def __init__(self, board):
        self.board = board
        self.actions = ActionFactory(board)
        self.reviewer = BoardReviewer(board)

    def generate_actions(self):
        if self.board.is_game_over():
            return []
        all_actions = []
        all_actions.extend(self.generate_playing_minions())
        all_actions.extend(self.generate_attacks())
        all_actions.extend(self.generate_casting_spells())
        all_actions.extend(self.generate_ending_turn())
        # all_actions.extend(self.generate_card_draw())
        return all_actions

    def grade_board(self):
        return self.reviewer.grade_board()

    def generate_playing_minions(self):
        player = self.board.get_active_player()
        actions = []
        for idx, card in enumerate(player.hand.cards):
            if card.cost <= player.mana:
                if card.type == 'minion':
                    actions.append(self.actions.play_minion(idx))
        return actions

    def generate_ending_turn(self):
        return [self.actions.end_turn()]

    def generate_attacks(self):
        active_side = self.board.get_active_side()
        other_side = self.board.get_other_side()
        actions = []
        for idx, minion in enumerate(active_side):
            # Skip the hero
            if idx == 0: continue
            if minion.can_attack:
                taunts = [c for c in other_side if c.taunt]
                for enemyidx, enemy in enumerate(other_side):
                    if taunts and enemy.taunt:
                        actions.append(self.actions.attack(idx, enemyidx))
                    elif not taunts:
                        actions.append(self.actions.attack(idx, enemyidx))
        return actions

    def generate_casting_spells(self):
        active_player = self.board.get_active_player()
        other_side = self.board.get_other_side()
        actions = []
        for cardidx, card in enumerate(active_player.hand.cards):
            if card.type != 'spell': continue
            if card.cost > active_player.mana: continue
            for enemyidx, _ in enumerate(other_side):
                actions.append(self.actions.cast_spell(cardidx, enemyidx))
        return actions

    def generate_card_draw(self):
        deck = self.board.get_active_deck()
        card_scores = [self.reviewer.grade_card(c) for c in deck.cards]
        max_score_idx = card_scores.index(max(card_scores))
        return [self.actions.draw(max_score_idx)]


class BoardReviewer:
    def __init__(self, board):
        self.board = board

    def grade_card(self, c):
        score = 0
        if c.type == 'minion':
            score += c.attack + c.health
            score += 2 if c.taunt else 0
            score += 2 if c.protection else 0
        if c.type == 'spell':
            score += 1.5 * c.attack
        return score

    def grade_board(self):
        hands_score = self._grade_hands()
        board_cards_score = self._grade_cards_on_board()
        return hands_score + board_cards_score

    def _grade_hands(self):
        active_hand = self.board.get_active_hand()
        other_hand = self.board.get_other_hand()
        score = 0
        for card in active_hand.cards:
            score += self.grade_card(card)
        for card in other_hand.cards:
            score -= self.grade_card(card)
        return score

    def _grade_cards_on_board(self):
        active_side = self.board.get_active_side()
        other_side = self.board.get_other_side()
        score = 0
        for card in active_side:
            score += 1.5 * self.grade_card(card)
        for card in other_side:
            score -= 1.5 * self.grade_card(card)
        return score