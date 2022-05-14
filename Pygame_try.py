import this
from turtle import bgcolor
import pygame
import game_classes as gc
import numpy as np

#Probably should make all of this a class as well that is initialized when we go from menu screen to game
WIDTH = 1550
HEIGHT = 801
FPS = 30
BG_Colour = (255, 10, 255)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()

G = gc.Game(4,Screen = screen)
pygame.init()
pygame.display.set_caption("Dominion")

#copper = gc.Card("Copper")

#all_sprites = pygame.sprite.Group()
#all_sprites.add(copper)



this_player = 1

G.players[this_player].deck.draw(G.players[this_player],5)

running = True
I = 0
while running:
    screen.fill(BG_Colour)

    clock.tick(FPS)
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            #if "clicked on card":
                #Play that card
            #else:
            G.players[this_player].hand.swap_hand_position()

            #some buttons in between as well


    G.players[this_player].hand.set_hand_position(screen)
    print([c.rect.center for c in G.players[this_player].hand.cards])

           
    pygame.display.flip()
pygame.quit()

#TO DO:
#ALLOW TO CLICK ON A CARD
#ALLOW A CLICKED CARD TO BE PLAYED