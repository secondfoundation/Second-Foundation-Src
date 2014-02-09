#
# python nose regression testing framework
#

from simulator import generator
import string

def test_sim():    
    d = generator.Deck()
    test = str(d.map_card(3))
    correct = "two of clubs"
    assert correct == test
        
def test_deck():
    deck = generator.Deck()
    deck.shuffle()
    check = len(deck.cards)
    assert check == 52

def test_deal():
    deck = generator.Deck()
    deck.shuffle()
    hand = deck.deal_cards(2)
    check = len(hand)
    assert check == 2
