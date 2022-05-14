import pygame
import game_classes as gc
import numpy as np

def angle_for_card_arch(tot_cards,card_id,outer_ang):
    return 2*outer_ang/(tot_cards+1)*(card_id+1)-outer_ang

def arch_position(cards, scaled_W = 200, N = 7, outer_angle = 45):
    tot_cards = len(cards)  #Maybe make part of hand object
    arch_N = sum([np.cos(np.pi*angle_for_card_arch(tot_cards,j,outer_angle)/180) for j in range(N)])  
    im = cards[0].image.convert_alpha()

    W = scaled_W
    H = W*im.get_height()/im.get_width()  #Probably make these fixed and globally accesible

    first_angle = angle_for_card_arch(tot_cards,0,outer_angle)
    N_W_outer = W*np.cos(np.pi*first_angle/180)+H*np.sin(abs(np.pi*first_angle/180))
    R = abs((arch_N*W/2 - N_W_outer/2)/np.sin(np.pi*first_angle/180))
    Scale_height = (R*np.cos(np.pi*first_angle/180)-(H*np.cos(np.pi*first_angle/180)+W*np.sin(abs(np.pi*first_angle/180)))/2)

    for i,card_sprite in enumerate(G.players[this_player].hand.cards):
        im = card_sprite.image.convert_alpha()

        angle = angle_for_card_arch(tot_cards,i,outer_angle)
        N_W = W*np.cos(np.pi*angle/180)+H*np.sin(abs(np.pi*angle/180))
        N_D = H*np.cos(np.pi*angle/180)+W*np.sin(abs(np.pi*angle/180))
        DW = R*np.sin(np.pi*angle/180)-N_W/2
        DH = R*np.cos(np.pi*angle/180)+N_D/2-Scale_height

        screen.blit(pygame.transform.rotate(pygame.transform.scale(im,(W,H)),-angle),(WIDTH/2+DW,HEIGHT-DH))

def line_position(cards, scaled_W = 200, N = 5):
    tot_cards = len(cards)  #Maybe make part of hand object
    im = cards[0].image.convert_alpha()

    W = scaled_W
    H = W*im.get_height()/im.get_width()  #Probably make these fixed and globally accesible

    for i,card_sprite in enumerate(G.players[this_player].hand.cards):
        im = card_sprite.image.convert_alpha()

        screen.blit(pygame.transform.scale(im,(W,H)),(W*(N-1)/(tot_cards+1)*(i+1)+WIDTH/2-W*N/2,HEIGHT-H)) #move somewhere else

#Probably should make all of this a class as well that is initialized when we go from menu screen to game
G = gc.Game(4)
pygame.init()
pygame.display.set_caption("Dominion")
WIDTH = 1550
HEIGHT = 801
FPS = 30

screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
screen.fill((255, 255, 255)) #This should be the background


#copper = gc.Card("Copper")

#all_sprites = pygame.sprite.Group()
#all_sprites.add(copper)



this_player = 1

G.players[this_player].deck.draw(G.players[this_player],5)

running = True
while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

    W = 150

    line_position(G.players[this_player].hand.cards, scaled_W = W)
    arch_position(G.players[this_player].hand.cards, scaled_W = W)
        
        
    pygame.display.flip()

pygame.quit()