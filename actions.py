from utils import safe_get
from cards import Hero, Minion, Spell


class Action:
    def __init__(self, board):
        self.board = board
    
    def execute(self):
        raise NotImplementedError()


class DrawCard(Action):
    def __init__(self, board, card_idx):
        super(DrawCard, self).__init__(board)
        self.card_idx = card_idx

    def execute(self):
        active_player = self.board.get_active_player()
        active_player.draw_card(self.card_idx)


class EndTurn(Action):
    def __init__(self, board):
        super(EndTurn, self).__init__(board)

    def execute(self):
        self.board.get_active_player().end_turn()
        self.board.change_active_player()
        self.board.get_active_player().start_turn()
        fatigue = self.board.get_active_player().fatigue
        self.board.get_active_side()[0].take_dmg(fatigue)
        for card in self.board.get_active_side():
            if isinstance(card, Minion):
                card.can_attack = True


class Attack(Action):
    def __init__(self, board, atk_idx, def_idx):
        super(Attack, self).__init__(board)
        self.atk_idx = atk_idx
        self.def_idx = def_idx
    
    def execute(self):
        active_side = self.board.get_active_side()
        other_side = self.board.get_other_side()
        attacker = safe_get(active_side, self.atk_idx)
        defender = safe_get(other_side, self.def_idx)
        if not attacker or not defender:
            return
        taunts = self.get_opponent_taunts()
        if taunts and not self.def_idx in taunts:
            return
        attacker.battle(defender)
        if attacker.is_dead():
            active_side.pop(self.atk_idx)
        if defender.is_dead():
            if isinstance(defender, Hero):
                self.board.game_over(self.board.get_active_idx())
            other_side.pop(self.def_idx)

    def get_opponent_taunts(self):
        other_side = self.board.get_other_side()
        taunts = []
        for idx, card in enumerate(other_side):
            if card.taunt:
                taunts.append(idx)
        return taunts


class PlayMinion(Action):
    def __init__(self, board, card_idx):
        super(PlayMinion, self).__init__(board)
        self.card_idx = card_idx

    def execute(self):
        if len(self.board.get_active_side()) < 7:
            if not isinstance(self.board.get_active_player().hand.cards[self.card_idx], Minion):
                return
            card = self.board.get_active_player().play_card(self.card_idx)
            if card:
                self.board.get_active_side().append(card)


class CastSpell(Action):
    def __init__(self, board, card_idx, target_idx):
        super(CastSpell, self).__init__(board)
        self.card_idx = card_idx
        self.target_idx = target_idx

    def execute(self):
        other_side = self.board.get_other_side()
        target = safe_get(other_side, self.target_idx)
        if not target:
            return
        active_player = self.board.get_active_player()
        if not isinstance(active_player.hand.cards[self.card_idx], Spell):
            return
        spell = active_player.play_card(self.card_idx)
        spell.deal_damage(target)
        if target.is_dead():
            if isinstance(defender_card, Hero):
                self.board.game_over(self.board.get_active_idx())
            other_side.pop(self.target_idx)


class ActionFactory:
    def __init__(self, board):
        self.board = board
    
    def attack(self, atk_idx, def_idx):
        return Attack(self.board, atk_idx, def_idx)

    def draw(self, idx):
        return DrawCard(self.board, idx)

    def end_turn(self):
        return EndTurn(self.board)

    def play_minion(self, card_idx):
        return PlayMinion(self.board, card_idx)

    def cast_spell(self, card_idx, target_idx):
        return CastSpell(self.board, card_idx, target_idx)