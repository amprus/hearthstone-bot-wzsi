class Player:
    def __init__(self, id, hand, hero, starts=False):
        self.id = id
        self.hand = hand
        self.hero = hero
        self.has_turn = starts
        self.turn = 1 if starts else 0 
        for i in range(3):
            self.draw_card()
        if starts:
            self.mana = 1
        else:
            self.hand.add_coin()
            self.mana = 0
        self.fatigue = 0

    def start_turn(self):
        self.has_turn = True
        self.turn += 1
        self.mana = self.turn if self.turn <= 10 else 10
        self.draw_card()
        
    def end_turn(self):
        self.has_turn = False
    
    def draw_card(self):
        try:
            self.hand.draw()
        except:
            self.fatigue += 1
            self.hero.health -= self.fatigue

    def play_card(self, index):
        if self.mana >= self.hand.cards[index].cost:
            card = self.hand.play_card(index)
            self.mana -= card.cost
            return card
        else:
            return None

    def has_lost(self):
        return self.hero.health <= 0

    def __str__(self):
        player_str = 'PLAYER #{} {}:\n'.format(self.id, '(ACTIVE)' if self.has_turn else '')
        player_str += 'HEALTH: {} MANA: {}\n'.format(self.hero.health, self.mana)
        player_str += str(self.hand)
        return player_str

    