class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def __str__(self):
        return str(self.hand)

    def showDealerHand(self):
        print('Dealer [\'{}\', \'{}\']'.format(self.hand[0],'*'))
