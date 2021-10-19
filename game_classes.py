#Tips from: https://www.youtube.com/watch?v=t8YkjDH86Y4&t=1s

import random as rand
import pygame
import os

#The game class contains the game, it sets up the players and keeps track of the turns and who is playing and such.
class Game(object):
    #Maybe rewrite init so that it creates the player selection menu instead and make this init what happens after
    def __init__(self,players_nr): #Card set should also be an input
        self.garbage = Garbage()#This is easy, just empty from the start
        self.field = Field()#This should need some input, basically the cards we play with

        #Setting up players
        self.players = {}
        self.nr_players = players_nr
        for nr in range(players_nr):
            self.players[nr] = Player(self,nr)

        self.game_start()

    def game_start(self): #Setting round and selecting starting player, also starting their tur
        self.round = 1
        self.first_player = rand.randint(1,self.nr_players)
        self.p_turn = self.first_player
        self.start_turn()
    
    def start_turn(self): #unfinished, this should basically run the method that allows interaction with the hand
        print('hi')
        #if turn has been ended (need to add interactivity for that) maybe in different function
        #self.end_turn()

    def end_turn(self): #Turn end sequence, updating round number if needed and player turn
        self.next_player()
        if self.p_turn == self.first_player:
            self.next_round()
        self.start_turn()        

    def next_player(self):
        self.p_turn = self.p_turn % self.nr_players + 1

    def next_round(self):
        self.round += 1
    


#The player class keeps track of which hand, deck and discard pile belongs to an individual, maybe add actions to here as well?
class Player(object):
    def __init__(self,game,nr): #Might need the game later on for certain functions
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


#The card class should just be a storage of the cards maybe also what happens when you play it? (Maybe use switch statement for that in newest python version)
class Card(pygame.sprite.Sprite):
    def __init__(self,type):
        pygame.sprite.Sprite.__init__(self)
        Card_Path = "Assets/Cards/"
        self.type = type
        self.path = os.path.abspath(f"{Card_Path}{type}.jpg")
        self.image = pygame.image.load(self.path)
        self.rect = self.image.get_rect()

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
        start_cards = [Card("Estate"),Card("Copper")]
        number_cards = [3,7]
        starting_deck = []
        for i,n in enumerate(start_cards):
            starting_deck.extend([n]*number_cards[i])
        self.cards = starting_deck
        self.shuffle()
    
    def shuffle(self): #shuffling the deck, no seeding has been implemented, might do that later
        for i in range(len(self.cards)-1,0,-1):
            r = rand.randint(0,i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def draw(self, player, amount = 1): #Drawing a card, will also rebuild the deck if you try to draw when the deck is empty
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
        
    def rebuild(self, player): #Rebuilding the deck, putting the deck into the discard pile taking that discard pile, making it empty in the process, and making that into the deck by shuffling
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

    #Drawing the 5 cards to fill the hand
    def fill_hand(self,player):
        player.deck.draw(player,5)
    
    #Throwing the hand away at the end of the turn
    def discard_hand(self,player):
        player.discard_pile.cards.extend(self.cards)
        self.cards = []

    #Refilling your hand after your turn has ended
    def redraw_hand(self,player):
        self.discard_hand(player)
        self.fill_hand(player)

    def show(self):
        return [c.show() for c in self.cards]


#In play class represents the cards that are currently in play (can't be shuffled in deck for the time) should be able to discard into discard pile
class In_play(object):
    def __init__(self):
        self.cards = []

    #Putting the in play cards into the discard pile
    def discard_play(self,player):
        player.discard_pile.cards.extend(self.cards)
        self.cards = []

    def show(self):
        return [c.show() for c in self.cards]


#The cards that have been destroyed, should just be a collection that can do nothing
class Garbage(object):
    def __init__(self):
        self.cards = []

    def show(self):
        return [c.show() for c in self.cards]


#Collection of piles of cards that can be bought, can be selected from and update the amount of cards in those piles
class Field(object):
    def __init__(self):
        self.piles = []
        #Fill the field with card piles that are chosen and the default ones


#Just a list of cards in a pile on the field should just be an amount and card object
class Field_pile(object):
    def __init__(self,type):
        self.amount = 0
        self.card = Card(type)

'''
G = Game(4)
print(G.p_turn,G.round)
for _ in range(10):
    G.end_turn()
    print(G.p_turn,G.round)


P1 = G.players[1]
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
'''



