from Player import Player
from Deck import Deck

# Settings
numDecks = 4
validHits = ['Hit','H','h','hit','HIT']
validStands = ['Stand','S','s','stand','STAND']
valueTen = ['J','Q','K']

def showHands(player, dealer, hidden):
    if hidden == True:
        dealer.showDealerHand()
    else:
        print('Dealer ',dealer)
    print('Player ', player)

def hit(self):
    deck.dealCard(self, 1)

# 99 for bust
# 0 for ok
# 100 for 21
def checkHand(self, other):
    hasAce = False
    total = 0
    for i in self.hand:
        if i in valueTen:
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
        print('BlackJack! {} Wins!'.format(self.name))
        return 100
    elif total > 21:
        print('Bust! {} Wins!'.format(other.name))
        return 99
    else: return total

# start of game
deck = Deck(numDecks)

print('---------------------')
print('| B L A C K J A C K |')
print('---------------------')
player = Player('Player')
dealer = Player('Dealer')

print('Dealing cards...')

# game loop
winner = False
hidden = True
while not winner:
    deck.dealCard(player, 2)
    deck.dealCard(dealer, 2)
    showHands(player, dealer, hidden)
    if(checkHand(player, dealer) == 100):
        winner = True

    while not winner:
        try:
            print('Player\'s turn')
            print('Hit or Stand?')
            choice = input('> ')
            # will catch invalid inputs
            if choice not in validHits and choice not in validStands:
                raise ValueError

            elif choice in validHits:
                hit(player)
                showHands(player, dealer, hidden)
                if checkHand(player, dealer) >= 99:
                    winner = True
            # player stands
            else:
                print('Dealer\'s turn')
                showHands(player, dealer, hidden)
                hidden = False
                showHands(player, dealer, hidden)
                while checkHand(dealer, player) <= 17:
                    print('Dealer hits.')
                    hit(dealer)
                    showHands(player, dealer, hidden)
                if checkHand(dealer, player) >= 99:
                    winner = True
                else:
                    # TODO: compare hands
                    pass
        except ValueError:
            print('Invalid input.')

    winner = True
