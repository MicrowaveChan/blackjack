import os
import time
import config
import player
import deck


def clearScreen():
    if os.name == 'nt':
        # on windows
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def showHands(p1, dealer, hidden = False):
    clearScreen()
    print('---------------------')
    print('| B L A C K J A C K |')
    print('---------------------')
    print()
    if hidden:
        dealer.showDealerHand()
    else:
        print('Dealer ',dealer)
    print('Player ', p1)
    print()


def hit(p1):
    deck.dealCard(p1, 1)


# for second hand
def hit_second(p1):
    deck.dealCard(p1, 1, True)


def split(p1):
    p1.second_hand.append(p1.hand.pop())
    

# 99 for bust
# 100 for 21
def checkHand(p1, other, printWinner = True, second = False):
    if second:
        hand = p1.second_hand
    else:
        hand = p1.hand

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
        if printWinner: print('BlackJack! {} Wins!'.format(p1.name))
        return 100
    elif total > 21:
        if printWinner: print('Bust! {} Wins!'.format(other.name))
        return 99
    else: return total

def checkSplit(p1):
    if len(p1.hand) <= 1 or p1.second_hand:
        return False
    return p1.hand[0] == p1.hand[1]


# start of game
deck = deck.Deck(config.numDecks)

p1 = player.Player('Player')
dealer = player.Player('Dealer')

done = False
# game loop
while not done:
    winner = False
    deck.dealCard(p1, 2)
    deck.dealCard(dealer, 2)
    while not winner:
        showHands(p1, dealer, True)
        if(checkHand(p1, dealer) == 100):
            winner = True
            break
        try:
            print('Player\'s turn')
            #TODO: Check for split
            if(checkSplit(p1)):
                print('Hit, Stand, Double Down or split?')
            else:
                print('Hit, Stand or Double Down?')

            choice = input('> ')
            # will catch invalid inputs
            if choice.lower() not in config.validHits and choice.lower() not in config.validStands and choice.lower() not in config.validDouble and choice.lower() not in config.validSplits:
                raise ValueError
            
            # player hits
            elif choice.lower() in config.validHits:
                hit(p1)
                showHands(p1, dealer, True)
                if checkHand(p1, dealer) >= 99:
                    winner = True
            # player double downs
            elif choice.lower() in config.validDouble:
                # TODO: double bet
                hit(p1)
                showHands(p1, dealer, True)
                if checkHand(p1, dealer) >= 99:
                    winner = True
                else:
                    showHands(p1, dealer, True)
                    print('Dealer\'s turn')
                    # at this point, dealer cards are shown
                    showHands(p1, dealer)
                    print('Dealer card revealed.')
                    time.sleep(config.wait_time)
                    while checkHand(dealer, p1, False) < 17:
                        print('Dealer hits.')
                        time.sleep(config.wait_time)
                        hit(dealer)
                        showHands(p1, dealer)

                    if checkHand(dealer, p1) >= 99:
                        winner = True
                    else:
                        if(checkHand(p1, dealer, False) > checkHand(dealer, p1, False)):
                            print('Dealer stands.')
                            time.sleep(config.wait_time)
                            winner = True
                            print('Player Wins!')
                        elif(checkHand(p1, dealer, False) == checkHand(dealer, p1, False)):
                            print('Dealer push.')
                            break
                        else:
                            print('Dealer stands.')
                            time.sleep(config.wait_time)
                            winner = True
                            print('Dealer Wins!')
            # player splits
            elif checkSplit(p1) and choice.lower() in config.validSplits:
                #TODO: split
                split(p1)
                hasSplit = True
            # player stands
            else:
                showHands(p1, dealer, True)
                print('Dealer\'s turn')
                time.sleep(config.wait_time)
                # at this point, dealer cards are shown
                showHands(p1, dealer)
                print('Dealer card revealed.')
                time.sleep(config.wait_time)
                while checkHand(dealer, p1, False) < 17:
                    print('Dealer hits.')
                    time.sleep(config.wait_time)
                    hit(dealer)
                    showHands(p1, dealer)

                if checkHand(dealer, p1) >= 99:
                    winner = True
                else:
                    if(checkHand(p1, dealer, False) > checkHand(dealer, p1, False)):
                        print('Dealer stands.')
                        time.sleep(config.wait_time)
                        winner = True
                        print('Player Wins!')
                    elif(checkHand(p1, dealer, False) == checkHand(dealer, p1, False)):
                        print('Dealer push.')
                        break
                    else:
                        print('Dealer stands.')
                        time.sleep(config.wait_time)
                        winner = True
                        print('Dealer Wins!')
        except ValueError:
            print('Invalid input.')
            time.sleep(config.wait_time)
    print('Play again?')
    choice = input('> ')
    if choice.lower() == 'n' or choice.lower() == 'no':
        done = True
    else:
        p1.hand.clear()
        dealer.hand.clear()
        hasSplit = False
