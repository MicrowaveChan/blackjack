class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.second_hand = []
        self.wallet = 200

    def __str__(self):
        if self.second_hand: 
                return str(self.hand) + str(self.second_hand)
        return str(self.hand)
		

    def showDealerHand(self):
        print('Dealer [\'{}\', \'{}\']'.format(self.hand[0],'*'))
