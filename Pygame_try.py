import pygame
import game_classes as gc

#Probably should make all of this a class as well that is initialized when we go from menu screen to game
G = gc.Game(4)
pygame.init()
pygame.display.set_caption("Dominion")
WIDTH = 1550
HEIGHT = 800
FPS = 30

screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
screen.fill((255, 255, 255)) #This should be the background


copper = gc.Card("Copper")

all_sprites = pygame.sprite.Group()
all_sprites.add(copper)

running = True
while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

    for i,card_sprite in enumerate(G.players[1].hand.cards):
        screen.blit(card_sprite.image,(100*i+100,50))

    pygame.display.flip()

pygame.quit()