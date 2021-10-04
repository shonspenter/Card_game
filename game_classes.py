#Tips from: https://www.youtube.com/watch?v=t8YkjDH86Y4&t=1s
import random as rand

#Need to make class Game
#class Game(object,players_nr):
#    def __init__(self):
#        Plist = []
#        for nr in range(players_nr):
#            Plist.append(Player(nr))


#The player class keeps track of which hand, deck and discard pile belongs to an individual, maybe add actions to here as well?
class Player(object):
    def __init__(self,nr):
        self.number = nr
        self.deck = Deck()
        self.hand = Hand()
        self.hand.fill_hand(self)
        self.discard_pile = Discard_pile()
        self.in_play = In_play()

    def end_turn(self):
        self.hand.discard_hand(self)
        self.hand.fill_hand(self)
        self.in_play.discard_play(self)


#The card class should just be a storage of the cards maybe also what happens when you play it?
class Card(object):
    def __init__(self,type):
        self.type = type

    def play(self,player):
        print(self.type)
        #Should be something that happens when you play the card
        player.in_play.cards.append(self)

    def show(self):
        return self.type


#the deck class should be a storage of a collection of cards and should be able to shuffle and draw 
class Deck(object):
    def __init__(self):
        self.build()

    def build(self): #Could add set keyword for different starting sets
        start_cards = [Card("Estate"),Card("copper")]
        number_cards = [3,7]
        starting_deck = []
        for i,n in enumerate(start_cards):
            starting_deck.extend([n]*number_cards[i])
        self.cards = starting_deck
        self.shuffle()
    
    def shuffle(self):
        for i in range(len(self.cards)-1,0,-1):
            r = rand.randint(0,i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def draw(self, player, amount = 1):
        for i in range(amount):
            if len(self.cards) != 0:
                drawn = self.cards.pop()
                player.hand.cards.append(drawn)
            elif len(player.discard_pile.cards) != 0:
                self.rebuild(player)
                drawn = self.cards.pop()
                player.hand.cards.append(drawn)
            else:
                print("could not draw any more") #Maybe do something else with this later
        
    def rebuild(self, player):
        player.discard_pile.cards.extend(self.cards)
        self.cards = player.discard_pile.cards
        player.discard_pile.destroy()
        self.shuffle()

    def show(self):
        return [c.show() for c in self.cards]


#The Discard_pile class should just be a storage of the cards in the discard pile and should be able to destroy itself 
class Discard_pile(object):
    def __init__(self):
        self.cards = []
    
    def destroy(self):
        self.cards = []

    def show(self):
        return [c.show() for c in self.cards]


#Hand class should be a storage of the cards in hands and should be able to fill and be discarded into discard pile
class Hand(object):
    def __init__(self):
        self.cards = []

    def fill_hand(self,player):
        player.deck.draw(player,5)
    
    def discard_hand(self,player):
        player.discard_pile.cards.extend(self.cards)
        self.cards = []

    def redraw_hand(self,player):
        self.discard_hand(player)
        self.fill_hand(player)

    def show(self):
        return [c.show() for c in self.cards]


#In play class represents the cards that are currently in play (can't be shuffled in dack) should be able to discard into discard pile
class In_play(object):
    def __init__(self):
        self.cards = []

    def discard_play(self,player):
        player.discard_pile.cards.extend(self.cards)
        self.cards = []

    def show(self):
        return [c.show() for c in self.cards]


P1 = Player(1)
print(P1.hand)
print(P1.deck.show())
print(P1.hand.show())
print(P1.discard_pile.show())
P1.hand.redraw_hand(P1)
print(P1.deck.show())
print(P1.hand.show())
print(P1.discard_pile.show())
P1.hand.redraw_hand(P1)
print(P1.deck.show())
print(P1.hand.show())
print(P1.discard_pile.show())



class Garbage(object):
    def __init__(self):
        self.cards = []

    def show(self):
        return [c.show() for c in self.cards]

class Field(object):
    def __init__(self):
        self.piles = []
        #Fill the field with card piles that are chosen and the default ones

class Field_pile(object):
    def __init__(self):
        self.amount = 0
        self.type = ''


