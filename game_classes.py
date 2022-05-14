#Tips from: https://www.youtube.com/watch?v=t8YkjDH86Y4&t=1s

import random as rand
import numpy as np
import pygame
import os

#The game class contains the game, it sets up the players and keeps track of the turns and who is playing and such.
class Game(object):
    #Maybe rewrite init so that it creates the player selection menu instead and make this init what happens after
    def __init__(self,players_nr,**kwargs): #Card set should also be an input
        self.garbage = Garbage()#This is easy, just empty from the start
        self.field = Field()#This should need some input, basically the cards we play with
        self.turn_nr = 1
        #Setting up players
        self.players = {}
        self.nr_players = players_nr
        for nr in range(players_nr):
            self.players[nr] = Player(self,nr,**kwargs)

        self.game_start()

    def game_start(self): #Setting round and selecting starting player, also starting their tur
        self.round = 1
        self.first_player = rand.randint(1,self.nr_players)
        self.p_turn = self.first_player
        self.start_turn()
    
    def start_turn(self): #unfinished, this should basically run the method that allows interaction with the hand
        print(f'Turn {self.round} for player {self.p_turn}')
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
    def __init__(self,game,nr,**kwargs): #Might need the game later on for certain functions
        self.number = nr
        self.deck = Deck()
        self.hand = Hand("line")
        self.hand.fill_hand(self)
        screen = kwargs.get("Screen")
        self.hand.set_hand_position(screen)
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
        dir_path = os.path.dirname(os.path.realpath(__file__))  #probably define somewhere else, but for now here is fine
        Card_Path = "Assets/Cards/"
        self.type = type
        self.path = os.path.abspath(f"{dir_path}/{Card_Path}{type}.jpg")
        self.image = pygame.image.load(self.path)
        self.rect = self.image.get_rect()

    def __str__(self):
        return f"{self.type}"

    def play(self,player):
        print(self.type)
        #Should be something that happens when you play the card
        player.in_play.cards.append(self)


#the deck class should be a storage of a collection of cards and should be able to shuffle and draw 
class Deck(object):
    def __init__(self):
        self.build()
    
    def __str__(self):
        card_string = ""
        for c in self.cards:
            card_string += f"{c}, "
        return card_string[:-2]

    def build(self): #Could add set keyword for different starting sets
        start_conditions = {"Copper":7,"Estate":3}
        starting_deck = []
        for name,amount in start_conditions.items():
            for i in range(amount):
                starting_deck.append(Card(name))
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


#The Discard_pile class should just be a storage of the cards in the discard pile and should be able to destroy itself 
class Discard_pile(object):
    def __init__(self):
        self.cards = []

    def __str__(self):
        card_string = ""
        for c in self.cards:
            card_string += f"{c}, "
        return card_string[:-2]
    
    def destroy(self):
        self.cards = []        


#Hand class should be a storage of the cards in hands and should be able to fill and be discarded into discard pile
class Hand(object):
    def __init__(self,position = "line"):#position in which the cards are visualized (line or arch)
        self.cards = []
        self.position = position

    def __str__(self):
        card_string = ""
        for c in self.cards:
            card_string += f"{c}, "
        return card_string[:-2]

    def hand_size(self):
        return len(self.cards)

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

    #3 below need fixing
    def arch_position(self,screen, scaled_W = 200, N = 7, outer_angle = 45):
        tot_cards = self.hand_size() 
        arch_N = sum([np.cos(np.pi*self.angle_for_card_arch(tot_cards,j,outer_angle)/180) for j in range(N)])  
        im = self.cards[0].image.convert_alpha() #Rather have something else

        W = scaled_W
        H = W*im.get_height()/im.get_width()  #Probably make these fixed and globally accesible

        first_angle = self.angle_for_card_arch(tot_cards,0,outer_angle)
        N_W_outer = W*np.cos(np.pi*first_angle/180)+H*np.sin(abs(np.pi*first_angle/180))
        R = abs((arch_N*W/2 - N_W_outer/2)/np.sin(np.pi*first_angle/180))
        Scale_height = (R*np.cos(np.pi*first_angle/180)-(H*np.cos(np.pi*first_angle/180)+W*np.sin(abs(np.pi*first_angle/180)))/2)
        
        WIDTH = screen.get_width()
        HEIGHT = screen.get_height()

        for i,card_sprite in enumerate(self.cards):
            im = card_sprite.image.convert_alpha()

            angle = self.angle_for_card_arch(tot_cards,i,outer_angle)
            N_W = W*np.cos(np.pi*angle/180)+H*np.sin(abs(np.pi*angle/180))
            N_D = H*np.cos(np.pi*angle/180)+W*np.sin(abs(np.pi*angle/180))
            DW = R*np.sin(np.pi*angle/180)-N_W/2
            DH = R*np.cos(np.pi*angle/180)+N_D/2-Scale_height

            rotated_card = pygame.transform.rotate(pygame.transform.scale(im,(W,H)),-angle)

            screen.blit(rotated_card,(WIDTH/2+DW,HEIGHT-DH))

            card_sprite.rect = rotated_card.get_rect()
            card_sprite.rect.center = (WIDTH/2+DW,HEIGHT-DH)

    def line_position(self,screen, scaled_W = 200, N = 5):
        tot_cards = self.hand_size()   
        im = self.cards[0].image.convert_alpha()

        W = scaled_W
        H = W*im.get_height()/im.get_width()  

        WIDTH = screen.get_width()
        HEIGHT = screen.get_height()

        for i,card_sprite in enumerate(self.cards):
            im = card_sprite.image.convert_alpha()

            scaled_card = pygame.transform.scale(im,(W,H))

            screen.blit(scaled_card,(W*(N-1)/(tot_cards+1)*(i+1)+WIDTH/2-W*N/2,HEIGHT-H)) 

            card_sprite.rect = scaled_card.get_rect()
            card_sprite.rect.center = (W*(N-1)/(tot_cards+1)*(i+1)+WIDTH/2-W*N/2,HEIGHT-H)

    def angle_for_card_arch(self,tot_cards,card_id,outer_ang): #check if can made less kwargs
        return 2*outer_ang/(tot_cards+1)*(card_id+1)-outer_ang

    def set_hand_position(self,screen):
        position = self.position
        if self.hand_size() != 0:
            if position == "line":
                self.line_position(screen)
            elif position == "arch":
                self.arch_position(screen)
            else:
                raise Exception(f"{position} is not a hand layout") 
    
    def swap_hand_position(self):
        self.position = {"line":"arch","arch":"line"}[self.position]


#In play class represents the cards that are currently in play (can't be shuffled in deck for the time) should be able to discard into discard pile
class In_play(object):
    def __init__(self):
        self.cards = []
    
    def __str__(self):
        card_string = ""
        for c in self.cards:
            card_string += f"{c}, "
        return card_string[:-2]

    #Putting the in play cards into the discard pile
    def discard_play(self,player):
        player.discard_pile.cards.extend(self.cards)
        self.cards = []        


#The cards that have been destroyed, should just be a collection that can do nothing
class Garbage(object):
    def __init__(self):
        self.cards = []

    def __str__(self):
        return [c for c in self.cards]


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
print(P1.deck)
print(P1.hand)
print(P1.discard_pile)
P1.hand.redraw_hand(P1)
print(P1.deck)
print(P1.hand)
print(P1.discard_pile)
P1.hand.redraw_hand(P1)
print(P1.deck)
print(P1.hand)
print(P1.discard_pile)
'''



