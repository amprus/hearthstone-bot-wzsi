class Card:
    type = 'card'

    def __init__(self, name, keywords, cost):
        self.name = name
        self.keywords = keywords
        self.cost = cost

    def showCard(self):
        print(str(self))

    def __str__(self):
        return '({}) {}, {}'.format(self.cost, self.name, self.type)


class Minion(Card):
    type = 'minion'

    def __init__(self, name, keywords, cost, attack, health):
        super(Minion, self).__init__(name, keywords, cost)
        self.attack = attack
        self.health = health
        self.can_attack = False
        self.protection = False
        self.taunt = False
        if 'divine_shield' in keywords:
            self.protection = True
        if 'taunt' in keywords:
            self.taunt = True

    def battle(self, target):
        if self.can_attack:
            self.take_dmg(target.attack)
            target.take_dmg(self.attack)
            self.can_attack = False

    def take_dmg(self, dmg):
        if self.protection and dmg > 0:
            print(self, self.protection)
            self.protection = False
            return
        self.health -= dmg


    @classmethod
    def from_dict(cls, dict_def):
        return cls(
            name=dict_def['name'],
            keywords=dict_def['keywords'],
            cost=dict_def['cost'],
            attack=dict_def['attack'],
            health=dict_def['health']    
        )

    def __str__(self):
        format_str = '({}) {}, {} [{}/{}]'.format(self.cost, self.name, self.type, self.attack, self.health)
        if self.protection:
            format_str += ' [DIVINE SHIELD]'
        if self.taunt:
            format_str += ' [TAUNT]'
        if not self.can_attack:
            format_str += ' ZZzzZZ...'
        return format_str

class Spell(Card):
    type = 'spell'

    def __init__(self, name, keywords, cost, damage):
        super(Spell, self).__init__(name, keywords, cost)
        self.damage = damage

    def deal_damage(self, target):
        target.health -= self.damage

    @classmethod
    def from_dict(cls, dict_def):
        return cls(
            name=dict_def['name'],
            keywords=dict_def['keywords'],
            cost=dict_def['cost'],
            damage=dict_def['damage']
        )

    def __str__(self):
        return '({}) {}, {} [dmg: {}]'.format(self.cost, self.name, self.type, self.damage)


class Hero(Minion):
    type = 'hero'

    def __init__(self, name, health):
        super(Hero, self).__init__(name=name, keywords=[], cost=0, attack=0, health=health)
        self.health = health

    @classmethod
    def from_dict(cls, hero_def):
        return cls(
            name=hero_def['name'],
            health=hero_def['health']
        )

    def battle(self, target):
        pass

    def __str__(self):
        return '({}) {}, {}'.format(self.health, self.name.upper(), self.type)


class Coin(Card):
    type = 'spell'

    def __init__(self):
        super(Coin, self).__init__('Coin', [{'addmana': 1}], 0)

    def __str__(self):
        return '({}) {}'.format(self.cost, self.name)