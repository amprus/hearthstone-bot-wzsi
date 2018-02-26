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

    def battle(self, target):
        if self.can_attack:
            self.health -= target.attack
            target.health -= self.attack
            self.can_attack = False

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
        return '({}) {}, {} [{}/{}]'.format(self.cost, self.name, self.type, self.attack, self.health)


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


class Hero(Card):
    type = 'hero'

    def __init__(self, name, health):
        super(Hero, self).__init__(name, [], 0)
        self.health = health

    @classmethod
    def from_dict(cls, hero_def):
        return cls(
            name=hero_def['name'],
            health=hero_def['health']
        )

    def __str__(self):
        return '({}) {} {}'.format(self.health, self.name.upper())


class Coin(Card):
    type = 'spell'

    def __init__(self):
        super(Coin, self).__init__('Coin', [{'addmana': 1}], 0)

    def __str__(self):
        return '({}) {}'.format(self.cost, self.name)