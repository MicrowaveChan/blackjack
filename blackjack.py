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


def main():
    # start of game
    decks = deck.Deck(config.numDecks)

    p1 = player.Player('Player')
    dealer = player.Player('Dealer')

    done = False
    # game loop
    while not done:
        winner = False
        decks.dealCard(p1, 2)
        decks.dealCard(dealer, 2)
        while not winner:
            showHands(p1, dealer, True)
            if(p1.checkHand(dealer) == 100):
                winner = True
                break
            try:
                print('Player\'s turn')
                #TODO: Check for split
                if(p1.checkSplit()):
                    print('Hit, Stand, Double Down or split?')
                else:
                    print('Hit, Stand or Double Down?')

                choice = input('> ')
                # will catch invalid inputs
                if choice.lower() not in config.validHits and choice.lower() not in config.validStands and choice.lower() not in config.validDouble and choice.lower() not in config.validSplits:
                    raise ValueError
                
                # player hits
                elif choice.lower() in config.validHits:
                    p1.hit(decks)
                    showHands(p1, dealer, True)
                    if p1.checkHand(dealer) >= 99:
                        winner = True
                # player double downs
                elif choice.lower() in config.validDouble:
                    # TODO: double bet
                    p1.hit(decks)
                    showHands(p1, dealer, True)
                    if p1.checkHand(dealer) >= 99:
                        winner = True
                    else:
                        showHands(p1, dealer, True)
                        print('Dealer\'s turn')
                        # at this point, dealer cards are shown
                        showHands(p1, dealer)
                        print('Dealer card revealed.')
                        time.sleep(config.waitTime)
                        while dealer.checkHand(p1, False) < 17:
                            print('Dealer hits.')
                            time.sleep(config.waitTime)
                            dealer.hit(decks)
                            showHands(p1, dealer)

                        if dealer.checkHand(p1) >= 99:
                            winner = True
                        else:
                            if(p1.checkHand(dealer, False) > dealer.checkHand(p1, False)):
                                print('Dealer stands.')
                                time.sleep(config.waitTime)
                                winner = True
                                print('Player Wins!')
                            elif(p1.checkHand(dealer, False) == dealer.checkHand(p1, False)):
                                print('Dealer push.')
                                break
                            else:
                                print('Dealer stands.')
                                time.sleep(config.waitTime)
                                winner = True
                                print('Dealer Wins!')
                # player splits
                elif p1.checkSplit() and choice.lower() in config.validSplits:
                    #TODO: split
                    p1.split()
                    hasSplit = True
                # player stands
                else:
                    showHands(p1, dealer, True)
                    print('Dealer\'s turn')
                    time.sleep(config.waitTime)
                    # at this point, dealer cards are shown
                    showHands(p1, dealer)
                    print('Dealer card revealed.')
                    time.sleep(config.waitTime)
                    while dealer.checkHand(p1, False) < 17:
                        print('Dealer hits.')
                        time.sleep(config.waitTime)
                        dealer.hit(decks)
                        showHands(p1, dealer)

                    if dealer.checkHand(p1) >= 99:
                        winner = True
                    else:
                        if(p1.checkHand(dealer, False) > dealer.checkHand(p1, False)):
                            print('Dealer stands.')
                            time.sleep(config.waitTime)
                            winner = True
                            print('Player Wins!')
                        elif(p1.checkHand(dealer, False) == dealer.checkHand(p1, False)):
                            print('Dealer push.')
                            break
                        else:
                            print('Dealer stands.')
                            time.sleep(config.waitTime)
                            winner = True
                            print('Dealer Wins!')
            except ValueError:
                print('Invalid input.')
                time.sleep(config.waitTime)
        print('Play again?')
        choice = input('> ')
        if choice.lower() == 'n' or choice.lower() == 'no':
            done = True
        else:
            p1.hand.clear()
            dealer.hand.clear()
            hasSplit = False


if __name__ == '__main__':
    main()
