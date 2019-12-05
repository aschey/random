import random
import copy

# Simulation:
#   Define bluff strategy
#   Each player has risk tolerance, bluff percentage
#   Players learn each others' strategies

class Card(object):

    def __init__(self, number, suit):
        # convert to int because of input method in Game's init
        self.number = int(number)
        self.suit = suit


    def __str__(self):
        return str(self.number) + ' of ' + self.suit

    def getSuit(self):
        """
        returns the suit of the card as a string
        """
        return self.suit


    def getNumber(self):
        """
        returns the number of the card as an int
        """
        return self.number
    

    def __eq__(self, other):
        return self.getSuit() == other.getSuit() and self.getNumber() == \
               other.getNumber()
    

    def __ne__(self, other):
        return not self.__eq__(other)


    def getAttribute(self, check):
        """
        check- string (either "suit", "number", or "both")
        returns an attribute as a string, depending on the
        value of check
        """
        if check == 'number':
            return self.number
        elif check == 'suit':
            return self.suit
        elif check == 'both':
            return self.__str__()


class Deck(object):

    def __init__(self):
        suits = ('spades', 'clubs', 'hearts', 'diamonds')
        self.deck = []
        # numbers 2 to 14 represent cards from 2 to ace
        for num in range(2, 15):
            # nested loop adds every card in every suit to deck
            for suit in suits:
                self.deck.append(Card(num, suit))
                

    def getDeck(self):
        """
        returns all the cards in the deck as as Card objects
        """
        return self.deck
    
        
    def draw(self, removeCard):
        """
        removeCard- string
        removes the specified card from the deck
        """
        for card in self.deck:
            if card == removeCard:
                # remove card from deck so it can't be drawn again
                self.deck.remove(card)
                break
        else:
            raise NameError("cannot have two of the same cards")
        

    def deal(self, numCards = 2):
        """
        numCards- int
        creates a new hand, removes the drawn cards from the deck,
        and returns the updated hand
        """
        hand = []
        # draw two (by default) random cards
        for card in range(numCards):
            hand.append(random.choice(self.deck))
            self.draw(hand[-1])

        return hand
    

    def __str__(self):
        cards = ''
        for card in self.deck:
            cards += (str(card) + ', ')
        return cards

    
class Game(object):

    def __init__(self, card1, card2, numOpps):
        self.deck = Deck()
        # split called in order to index card names
        if card1 == None:
            self.card1 = str(self.drawRandomCard()).split()
        else:
            self.card1 = card1.split()
        if card2 == None:
            self.card2 = str(self.drawRandomCard()).split()
        else:
            self.card2 = card2.split()
        
        for card in [self.card1, self.card2]:
            if card[0] == 'jack':
                card[0] = '11'
            elif card[0] == 'queen':
                card[0] = '12'
            elif card[0] == 'king':
                card[0] = '13'
            elif card[0] == 'ace':
                card[0] = '14'
                
        self.table = []
        
        # index 0 and 2 refer to card name and suit
        self.hand = [Card(self.card1[0], self.card1[2]), Card(self.card2[0], \
                                                              self.card2[2])]
        if card1 != None:
            self.deck.draw(self.hand[0])
        if card2 != None:
            self.deck.draw(self.hand[1])
            
        self.drawOppHands(numOpps)


    def getTable(self):
        """
        returns all cards on the table
        """
        table = 'table = '
        oppHands = 'opponent cards = '
        for card in self.table:
            table += (str(card) + ', ')
        return table
    
    def getOppHands(self):
        """
        returns all cards in the opponents' hands
        """
        oppHands = 'opp hands = '
        for card in self.oppHands:
            oppHands += (str(card) + ', ')
        return oppHands
        

    def flop(self):
        """
        adds three cards to the table (the flop)
        """
        self.table = self.deck.deal(3)

    def addOne(self):
        """
        adds another card to the table (the turn/river)
        """
        self.table += self.deck.deal(1)


    def tableCards(self, check):
        """
        check- a string (either "suit", "number", or "both")
        returns a dictionary of all cards on the table
        """
        cards = {}
        for card in self.table:
            cards[card.getAttribute(check)] = 0

        for card in self.table:
            cards[card.getAttribute(check)] += 1

        return cards


    def tableOneCard(self, index, check):
        """
        index- an int
        check- a string (either "suit", "number", or "both")
        returns a dictionary of all cards on the table plus
        one from your hand at the specified index
        """
        cards = self.tableCards(check)
        # get the card at the specified index (1 or 2)
        if self.hand[index].getAttribute(check) in cards.keys():
            cards[self.hand[index].getAttribute(check)] += 1
        else:
            cards[self.hand[index].getAttribute(check)] = 1

        return cards
    

    def tableBothCards(self, check):
        """
        check- a string (either "suit", "number", or "both")
        returns a dictionary of all cards on the table plus both from your
        hand
        """
        cards = self.tableCards(check)
        
        for card in self.hand:
            if not card.getAttribute(check) in cards.keys():
                cards[card.getAttribute(check)] = 0
        
        for card in self.hand:
            cards[card.getAttribute(check)] += 1
                
        return cards


    def isTwoOfAKind(self):
        """
        returns true if the hand is two of a kind
        """
        if self.card1[0] == self.card2[0]:
            return True
        cards = self.tableCards('number')
        for card in cards.keys():
            if card == int(self.card1[0]) or card == int(self.card2[0]):
                return True
        return False


    def drawOppHands(self, numOpps):
        """
        numOpps- an int
        draws cards from the deck and places them in the
        opponents' hands
        """
        self.oppHands = []
        for player in range(numOpps * 2):
            # draw two cards for each opponent to simulate a real game
            self.oppHands.append(random.choice(self.deck.getDeck()))
            self.deck.draw(self.oppHands[-1])
            #print(self.deck.getDeck())
            #print()
            
    def drawRandomCard(self):
        """
        draws a random card from the deck
        """
        card = random.choice(self.deck.getDeck())
        self.deck.draw(card)
        return card


    def isMultipleOfAKind(self, num):
        """
        num- an int
        returns true if the hand is 3 or 4 of a kind
        depending on the input for num
        """
        if num < 3 or num > 4:
            raise ValueError("num must be either 3 or 4")
            
        cards = self.tableBothCards('number')
        for card in cards.keys():
            for i in [self.card1, self.card2]:
                if card == int(i[0]) and cards[card] >= num:
                    return True
        return False


    def isTwoPair(self):
        cards = self.tableBothCards('number')
        numPairs = 0
        for num in cards.values():
            if num > 1:
              numPairs += 1
            if numPairs == 2:
                return True
        return False


    def isStraight(self, cards = None):
        """
        cards- a dict
        returns true if the hand is a straight
        """
        num_in_order = 1
        if cards == None:
            cards = self.tableBothCards('number')
            
        cards = sorted(cards)
        
        for card in range(len(cards) - 1):
            if cards[card + 1] == cards[card] + 1:
                num_in_order += 1
                if num_in_order == 5:
                    return True
            else:
                num_in_order = 1
                
        return False


    def isFlush(self):
        """
        returns true if the hand is a flush
        """
        cards = self.tableBothCards('suit')
        for card in cards.values():
            if card >= 5:
                return True
        return False


    def isStraightFlush(self):
        """
        returns true if the hand is a straight flush
        """
        if not self.isFlush() or not self.isStraight():
            return False
        
        check = self.tableBothCards('suit')
        for i in check.keys():
            if check[i] >= 5:
                suit = i
                
        check = self.tableBothCards('both')
        checkCopy = copy.deepcopy(check)
        for i in check.keys():
            if i.split()[-1] != suit:
                checkCopy.pop(i)
        check = checkCopy
                
        straightCheck = []
        for i in check.keys():
            straightCheck.append(int(i.split()[0]))
        return self.isStraight(straightCheck)

    def isFullHouse(self):
        """
        returns true if the hand is a full house
        """
        cards = self.tableBothCards('number')
        two = False
        three = False
        for number in cards.values():
            if number >= 3:
                three = True
            elif number >= 2:
                two = True
        return two and three


def runSimulation(card1 = None, card2 = None, numOpps = 2, numTrials = 10000):
    """
    runs simulations of games and returns probabilities of drawing certain hands
    """
    # order for stats: two of a kind, three of a kind, four of a kind, straight,
    # flush, straight flush, full house
    flopStats = [0.0] * 8
    turnStats = [0.0] * 8
    riverStats = [0.0] * 8
    for test in range(numTrials):
        game = Game(card1, card2, numOpps)
        game.flop()
        flopStats = getStats(game, flopStats)
        game.addOne()
        turnStats = getStats(game, turnStats)
        game.addOne()
        riverStats = getStats(game, riverStats)
        
    print("probablilities")
    print()
    print("after the flop...")
    printStats(flopStats, numTrials)
    print()
    print("after the turn...")
    printStats(turnStats, numTrials)
    print()
    print("after the river...")
    printStats(riverStats, numTrials)

def getStats(game, stats):
    """
    stats- a list
    checks which conditions the hand satisfies and returns the
    updated stats
    """
    if game.isTwoOfAKind():
        stats[0] += 1
    if game.isMultipleOfAKind(3):
        stats[1] += 1
    if game.isMultipleOfAKind(4):
        stats[2] += 1
    if game.isTwoPair():
        stats[3] += 1
    if game.isStraight():
        stats[4] += 1
    if game.isFlush():
        stats[5] += 1
    if game.isStraightFlush():
        stats[6] += 1
    if game.isFullHouse():
        stats[7] += 1
    return stats
    
def printStats(stats, numTrials):
    """
    prints all stats once the simulation has finished
    """
    for s in range(len(stats)):
        stats[s] = stats[s] / numTrials * 100
    print("two of a kind:", stats[0], "%")
    print("three of a kind:", stats[1], "%")
    print("four of a kind:", stats[2], "%")
    print("two pair:", stats[3], "%")
    print("straight:", stats[4], "%")
    print("flush:", stats[5], "%")
    print("straight-flush:", stats[6], "%")
    print("full house:", stats[7], "%")

    
runSimulation(numOpps = 0, numTrials = 1000)
    




    
        
                        
                        
                        

                            
