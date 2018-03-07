def _get_best_choices(cards_table, card_list, cost):
    best_choices = []
    i = len(card_list)
    j = cost
    while i > 0:
        if cards_table[i][j] != cards_table[i - 1][j]:
            best_choices.append((card_list[i - 1], i - 1))
            j -= card_list[i - 1].cost
        i -= 1
    return best_choices


def _dyn_table(card_list, total_cost, bot_rating_func):
    cards = [[0] * (total_cost + 1) for _ in range(len(card_list) + 1)]
    for card in range(1, len(card_list) + 1):
        card_value = bot_rating_func(card_list[card - 1])
        for mana_cost in range(1, total_cost + 1):
            if card_list[card - 1].cost <= mana_cost:
                candidate1 = cards[card - 1][mana_cost]
                candidate2 = cards[card - 1][mana_cost - card_list[card - 1].cost] + card_value
                cards[card][mana_cost] = max(candidate1, candidate2)
            else:
                cards[card][mana_cost] = cards[card - 1][mana_cost]
    return cards


def _min_attack_card(cards):
    min_attack = 100
    index_of_min = -1
    for i in range(0, len(cards)):
        if cards[i][0].attack < min_attack:
            min_attack = cards[i][0].attack
            index_of_min = i
    return min_attack, index_of_min


class Algorithms:

    def __init__(self):
        pass

    @staticmethod
    def knapsack_for_cards(cards_list, cost, bot_rating_func):
        card_table = _dyn_table(cards_list, cost, bot_rating_func)
        return _get_best_choices(card_table, cards_list, cost)

    @staticmethod
    def subsets_sum_for_attack(cards_to_play, target):
        target_health = target[0].health
        target_index = target[1]
        cards_to_attack = []
        while target_health > 0 and len(cards_to_play) > 0:
            min_attack, index_of_min = _min_attack_card(cards_to_play)
            target_health -= min_attack
            cards_to_attack.append(cards_to_play.pop(index_of_min))
        return cards_to_attack, target_index
