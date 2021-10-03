#Tips from: https://www.youtube.com/watch?v=t8YkjDH86Y4&t=1s
import random as rand

#The player class keeps track of which hand, deck and discard pile belongs to an individual, maybe add actions to here as well?
class Player(object):
    def __init__(self,nr):
        self.number = nr
        self.deck = Deck()
        self.hand = Hand(self)
        self.discard_pile = Discard_pile()


#The card class should just be a storage of the cards maybe also what happens when you play it?
class Card(object):
    def __init__(self,type):
        self.type = type

    def play(self):
        print(self.type)
        #Should be something that happens when you play the card
    
    def show(self):
        return self.type


#the deck class should be a storage of a collection of cards and should be able to shuffle and draw 
class Deck(object):
    def __init__(self):
        self.build()

    def build(self): #Could add set keyword for different starting sets
        card_names = ["Estate","copper"]
        number_cards = [3,7]
        starting_cards = []
        for i,n in enumerate(card_names):
            starting_cards.extend([n]*number_cards[i])
        self.cards = starting_cards
        self.shuffle()
    
    def shuffle(self):
        for i in range(len(self.cards)-1,0,-1):
            r = rand.randint(0,i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def draw(self, hand, amount):
        for i in range(amount):
            drawn = self.cards.pop()
            hand.append(drawn)
        #Unfinished, need to add a check to make sure that the deck is filled, otherwise the discarded cards class needs to be shuffled into the


    def show(self):
        return self.cards

#The Discard_pile class should just be a storage of the cards in the discard pile
class Discard_pile(object):
    def __init__(self):
        self.cards = []

    def show(self):
        return self.cards


class Hand(object):
    def __init__(self,Player):
        self.cards = []
        self.fill_hand(Player)
        #Maybe only fill hand when the game starts

    def fill_hand(self,Player):
        Player.deck.draw(self.cards,5)
    
    def discard_hand(self,Player):
        Player.discard_pile.cards.extend(self.cards)
        self.cards = []


    def show(self):
        return self.cards












class Field(object):
    def __init__(self):
        self.piles = []
        #Fill the field with card piles that are chosen and the default ones

class Field_pile(object):
    def __init__(self):
        self.amount = 0
        self.type = ''

P1 = Player(1)
print(P1.deck.show())
print(P1.hand.show())
P1.hand.discard_hand(P1)
print(P1.hand.show())
print(P1.discard_pile.show())
