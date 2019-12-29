import os, time
from Player import Player
from Deck import Deck

# Settings
numDecks = 4
wait_time = 1.5
validHits = ['h', 'hit']
validStands = ['s','stand', 'st']
validSplits = ['split','sp']
validDouble = ['d', 'double', 'dd']
valueTen = ['J','Q','K']

def clearScreen():
    if os.name == 'nt':
        # on windows
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

# for second hand
def hit_second(player):
    deck.dealCard(player, 1, True)


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
    deck.dealCard(player, 2)
    deck.dealCard(dealer, 2)
    while not winner:
        showHands(player, dealer, True)
        if(checkHand(player, dealer) == 100):
            winner = True
            break
        try:
            canSplit = False
            print('Player\'s turn')
            #TODO: Check for split
            if(checkSplit(player):
                print('Hit, Stand, Double Down or split?')
                canSplit = True
            else:
                print('Hit, Stand or Double Down?')

            choice = input('> ')
            # will catch invalid inputs
            if choice.lower() not in validHits and choice.lower() not in validStands and choice.lower() not in validDouble:
                raise ValueError
            
            # player hits
            elif choice.lower() in validHits:
                hit(player)
                showHands(player, dealer, True)
                if checkHand(player, dealer) >= 99:
                    winner = True
            # player double downs
            elif choice.lower() in validDouble:
                # TODO: double bet
                hit(player)
                showHands(player, dealer, True)
                if checkHand(player, dealer) >= 99:
                    winner = True
                else:
                    showHands(player, dealer, True)
                    print('Dealer\'s turn')
                    # at this point, dealer cards are shown
                    showHands(player, dealer)
                    print('Dealer card revealed.')
                    time.sleep(wait_time)
                    while checkHand(dealer, player, False) < 17:
                        print('Dealer hits.')
                        time.sleep(wait_time)
                        hit(dealer)
                        showHands(player, dealer)

                    if checkHand(dealer, player) >= 99:
                        winner = True
                    else:
                        if(checkHand(player, dealer, False) > checkHand(dealer, player, False)):
                            print('Dealer stands.')
                            time.sleep(wait_time)
                            winner = True
                            print('Player Wins!')
                        elif(checkHand(player, dealer, False) == checkHand(dealer, player, False)):
                            print('Dealer push.')
                            break
                        else:
                            print('Dealer stands.')
                            time.sleep(wait_time)
                            winner = True
                            print('Dealer Wins!')
            # player splits
            elif canSplit and choice.lower() in validSplits:
                #TODO: split
            # player stands
            else:
                showHands(player, dealer, True)
                print('Dealer\'s turn')
                time.sleep(wait_time)
                # at this point, dealer cards are shown
                showHands(player, dealer)
                print('Dealer card revealed.')
                time.sleep(wait_time)
                while checkHand(dealer, player, False) < 17:
                    print('Dealer hits.')
                    time.sleep(wait_time)
                    hit(dealer)
                    showHands(player, dealer)

                if checkHand(dealer, player) >= 99:
                    winner = True
                else:
                    if(checkHand(player, dealer, False) > checkHand(dealer, player, False)):
                        print('Dealer stands.')
                        time.sleep(wait_time)
                        winner = True
                        print('Player Wins!')
                    elif(checkHand(player, dealer, False) == checkHand(dealer, player, False)):
                        print('Dealer push.')
                        break
                    else:
                        print('Dealer stands.')
                        time.sleep(wait_time)
                        winner = True
                        print('Dealer Wins!')
        except ValueError:
            print('Invalid input.')
    print('Play again?')
    choice = input('> ')
    if choice.lower() == 'n' or choice.lower() == 'no':
        done = True
    else:
        player.hand.clear()
        dealer.hand.clear()
