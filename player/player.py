import deck
import config

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
        

    def hit(self, deck, second = False):
        if second:
            deck.dealCard(self, 1, True)
        else:
            deck.dealCard(self, 1)


    def split(self):
        self.second_hand.append(self.hand.pop())
     

    # 99 for bust
    # 100 for 21
    def checkHand(self, other, printWinner = True, second = False):
        if second:
            hand = self.second_hand
        else:
            hand = self.hand

        hasAce = False
        total = 0
        for i in hand:
            if i in config.valueTen:
                total += 10
            elif i == 'A':
                if (total + 11) <= 21:
                    total += 11
                    hasAce = True
                else: total += 1
            else:
                total += int(i)
        if hasAce and total > 21:
            total -= 10

        if total == 21:
            if printWinner: print('BlackJack! {} Wins!'.format(self.name))
            return 100
        elif total > 21:
            if printWinner: print('Bust! {} Wins!'.format(other.name))
            return 99
        else: return total

    def checkSplit(self):
        if len(self.hand) <= 1 or self.second_hand:
            return False
        return self.hand[0] == self.hand[1]


