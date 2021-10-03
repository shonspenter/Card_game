#Tips from: https://www.youtube.com/watch?v=t8YkjDH86Y4&t=1s

class Card(object):
    def __init__(self,type):
        self.type = type

    def play(self):
        print(self.type)

class Deck(object):
    def __init__(self):
        self.cards = []
        Deck.build()

    def build(self): #Could add set keyword for different starting sets
        self.cards.append()


class Hand(object):
    def __init__(self):
        self.cards = []

class Field(object):
    def __init__(self):
        self.piles = []
        #Fill the field with card piles that are chosen and the default ones

class Pile(object):
    def __init__(self):
        self.amount = 0
        self.type = ''

card = Card('gold')
card.play()