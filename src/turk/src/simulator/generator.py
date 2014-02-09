# -*-py-*-  
#
# generator.py: functions that generate hands for the player(s)
# 
# shuffle: creates a new deck
#
import random
import math

class Card:
    # lists
    suits = ['hearts', 'diamonds', 'spades', 'clubs']
    values = ['two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
       'jack', 'queen', 'king', 'ace']

    def __init__(self, in_value, in_suit):
        self.value = in_value
        self.suit = in_suit

    def __str__(self):
        return self.get_name()

    def get_name(self):
        return Card.values[self.value] + ' of ' + Card.suits[self.suit]


class Deck:
    def __init__(self):
        self.cards = []

    def shuffle(self):
        # start deck
        size = range(0,52)

        # first step hardcoded
        deck= []
        temp=random.randint(0,51)
        deck.append(temp)
        size.remove(temp)

        # choose cards randomly
        while (len(size) > 0):
            temp=random.randint(0,51)
            if deck.count(temp) == 0:
                deck.append(temp)
                size.remove(temp)

        self.cards = [self.map_card(card_id) for card_id in deck]

    #
    # map_card
    #
    # takes int input (1-52)
    # returns string (card name)
    #
    def map_card(self, card_id):
        # error handling:
        if math.floor(card_id) != math.ceil(card_id):
            print 'turk epic fail:: ma_card was passed a non-integer number of players!!'
            exit(1)

        if card_id < 0:
            print 'turk epic fail:: map_card given non-real card!'
            exit(1)

        if card_id > 51:
            print 'turk epic fail:: map_card given absurd card draw!'
            exit(1)

        # figure out what we are holding
        nsuit=int(card_id%4)
        nvalue=int(math.floor(card_id/4))

        return Card(nvalue, nsuit)

    #
    # deal_hand: gives each player a hand
    #
    # takes as input the deck and number of cards
    # returns hand
    #
    def deal_cards(self, ncards):

        # deal players hand
        hand = []
        for x in range(ncards):
            card = self.cards.pop()
            # __str__ is defined in card so it will print Ace of Spades etc...
            print "Dealt", card
            hand.append(card)

        return hand
