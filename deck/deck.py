import random

class Deck:
    deck = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K',
            'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K',
            'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K',
            'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K',]
    def __init__(self, amount):
        self.deck *= amount
        for i in range(1000):
            random.shuffle(self.deck)

    def __str__(self):
        return  str(self.deck)

    def dealCard(self, Player, amount, second = False):
        for i in range(amount):
            if second:
                Player.second_hand.append(self.deck.pop())
            else:
                Player.hand.append(self.deck.pop())
