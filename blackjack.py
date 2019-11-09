import os
from Player import Player
from Deck import Deck

# Settings
numDecks = 4
validHits = ['Hit','H','h','hit','HIT']
validStands = ['Stand','S','s','stand','STAND']
valueTen = ['J','Q','K']

def clearScreen():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def showHands(player, dealer, hidden = False):
    clearScreen()
    print('---------------------')
    print('| B L A C K J A C K |')
    print('---------------------')
    print()
    if hidden:
        dealer.showDealerHand()
    else:
        print('Dealer ',dealer)
    print('Player ', player)
    print()

def hit(player):
    deck.dealCard(player, 1)

# 99 for bust
# 100 for 21
def checkHand(player, other, printWinner = True):
    hasAce = False
    total = 0
    for i in player.hand:
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
        if printWinner: print('BlackJack! {} Wins!'.format(player.name))
        return 100
    elif total > 21:
        if printWinner: print('Bust! {} Wins!'.format(other.name))
        return 99
    else: return total

# start of game
deck = Deck(numDecks)

player = Player('Player')
dealer = Player('Dealer')

done = False
# game loop
while not done:
    winner = False
    while not winner:
        deck.dealCard(player, 2)
        deck.dealCard(dealer, 2)
        showHands(player, dealer, True)
        if(checkHand(player, dealer) == 100):
            winner = True
        try:
            print('Player\'s turn')
            print('Hit or Stand?')
            choice = input('> ')
            # will catch invalid inputs
            if choice not in validHits and choice not in validStands:
                raise ValueError

            elif choice in validHits:
                hit(player)
                showHands(player, dealer, True)
                if checkHand(player, dealer) >= 99:
                    winner = True
            # player stands
            else:
                print('Dealer\'s turn')
                showHands(player, dealer, True)
                # at this point, dealer cards are shown
                showHands(player, dealer)
                while checkHand(dealer, player, False) < 17:
                    print('Dealer hits.')
                    hit(dealer)
                    showHands(player, dealer)

                if checkHand(dealer, player) >= 99:
                    winner = True
                else:
                    if(checkHand(player, dealer, False) > checkHand(dealer, player, False)):
                        print('Dealer stands.')
                        winner = True
                        print('Player Wins!')
                    elif(checkHand(player, dealer, False) == checkHand(dealer, player, False)):
                        print('Dealer push.')
                        player.hand.clear()
                        dealer.hand.clear()
                    else:
                        print('Dealer stands.')
                        winner = True
                        print('Dealer Wins!')
        except ValueError:
            print('Invalid input.')
    choice = input('Play again?')
    if choice == 'n':
        done = True
    else:
        player.hand.clear()
        dealer.hand.clear()
