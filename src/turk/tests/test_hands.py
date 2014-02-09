#
# test that gen_score method correctly sets 
#

from simulator import generator
from simulator import game_sim

#
# test for four of a kind
#
def test_4kind():

    # initalize everything
    nick = game_sim.Player('nick',0,100,'nada')
    d = generator.Deck()
    community_cards = []

    # give nick community cards
    community_cards.append(d.map_card(0))
    community_cards.append(d.map_card(1))
    community_cards.append(d.map_card(2))
    # turn and river cards
    community_cards.append(d.map_card(3))
    community_cards.append(d.map_card(4))
    
    # personal hand
    nick.hand.append(d.map_card(5))
    nick.hand.append(d.map_card(10))    

    nick.gen_score(community_cards)

    # check hand is correct
    assert nick.strflush  == 0
    assert nick.fourkind  == 1
    assert nick.fullhouse == 0
    assert nick.flush     == 0
    assert nick.straight  == 0
    assert nick.threekind == 0
    assert nick.pair      == 0

    assert nick.besthand == 7
    # check it thinks we have two's (lowest possible)
    assert nick.highcard == 0

#
# test for three of a kind
#
def test_3kind():

    # initalize everything
    nick = game_sim.Player('nick',0,100,'nada')
    d = generator.Deck()
    community_cards = []

    # give nick community cards
    community_cards.append(d.map_card(4))
    community_cards.append(d.map_card(5))
    community_cards.append(d.map_card(6))
    # turn and river cards
    community_cards.append(d.map_card(30))
    community_cards.append(d.map_card(40))
    
    # personal hand
    nick.hand.append(d.map_card(17))
    nick.hand.append(d.map_card(10))    

    nick.gen_score(community_cards)

    # check hand is correct
    assert nick.strflush  == 0
    assert nick.fourkind  == 0
    assert nick.fullhouse == 0
    assert nick.flush     == 0
    assert nick.straight  == 0
    assert nick.threekind == 1
    assert nick.pair      == 0

    assert nick.besthand == 3
    # check it thinks we have three's 
    assert nick.highcard == 1

#
# test for nothing
#
def test_nothing():

    # initalize everything
    nick = game_sim.Player('nick',0,100,'nada')
    d = generator.Deck()
    community_cards = []

    # give nick community cards
    community_cards.append(d.map_card(0))
    community_cards.append(d.map_card(51))
    community_cards.append(d.map_card(17))
    # turn and river cards
    community_cards.append(d.map_card(30))
    community_cards.append(d.map_card(40))
    
    # personal hand
    nick.hand.append(d.map_card(5))
    nick.hand.append(d.map_card(10))    
            
    nick.gen_score(community_cards)

    # check hand is correct
    assert nick.strflush  == 0
    assert nick.fourkind  == 0
    assert nick.fullhouse == 0
    assert nick.flush     == 0
    assert nick.straight  == 0
    assert nick.threekind == 0
    assert nick.pair      == 0

    assert nick.besthand == 0
    #assert nick.highcard == 1

#
# test for pair
#
def test_pair():

    # initalize everything
    nick = game_sim.Player('nick',0,100,'nada')
    d = generator.Deck()
    community_cards = []

    # give nick community cards
    community_cards.append(d.map_card(0))
    community_cards.append(d.map_card(51))
    community_cards.append(d.map_card(49))
    # turn and river cards
    community_cards.append(d.map_card(30))
    community_cards.append(d.map_card(40))
    
    # personal hand
    nick.hand.append(d.map_card(5))
    nick.hand.append(d.map_card(10))    

    nick.gen_score(community_cards)

    # check hand is correct
    assert nick.strflush  == 0
    assert nick.fourkind  == 0
    assert nick.fullhouse == 0
    assert nick.flush     == 0
    assert nick.straight  == 0
    assert nick.threekind == 0
    assert nick.pair      == 1

    assert nick.besthand == 1
    # check it thinks we have aces
    assert nick.highcard == 12

#
# test for two pair
#
def test_two_pair():

    # initalize everything
    nick = game_sim.Player('nick',0,100,'nada')
    d = generator.Deck()
    community_cards = []

    # give nick community cards
    community_cards.append(d.map_card(0))
    community_cards.append(d.map_card(51))
    community_cards.append(d.map_card(49))
    # turn and river cards
    community_cards.append(d.map_card(30))
    community_cards.append(d.map_card(17))
    
    # personal hand
    nick.hand.append(d.map_card(16))
    nick.hand.append(d.map_card(10))    

    nick.gen_score(community_cards)

    # check hand is correct
    assert nick.strflush  == 0
    assert nick.fourkind  == 0
    assert nick.fullhouse == 0
    assert nick.flush     == 0
    assert nick.straight  == 0
    assert nick.threekind == 0
    assert nick.pair      == 2

    assert nick.besthand == 2
    # check it thinks we have aces
    assert nick.highcard == 12
    assert nick.sechighcard == 4

#
# test for full house
#
def test_full_house():

    # initalize everything
    nick = game_sim.Player('nick',0,100,'nada')
    d = generator.Deck()
    community_cards = []

    # give nick community cards
    community_cards.append(d.map_card(45))
    community_cards.append(d.map_card(46))
    community_cards.append(d.map_card(47))
    # turn and river cards
    community_cards.append(d.map_card(30))
    community_cards.append(d.map_card(38))
    
    # personal hand
    nick.hand.append(d.map_card(5))
    nick.hand.append(d.map_card(39))    

    nick.gen_score(community_cards)

    # check hand is correct
    assert nick.strflush  == 0
    assert nick.fourkind  == 0
    assert nick.fullhouse == 1
    assert nick.flush     == 0
    assert nick.straight  == 0
    assert nick.threekind == 0
    assert nick.pair      == 0

    assert nick.besthand == 6
    # check it thinks we have kings over jacks
    assert nick.highcard == 11
    assert nick.sechighcard == 9

#
# test for flush
#
def test_flush():

    # initalize everything
    nick = game_sim.Player('nick',0,100,'nada')
    d = generator.Deck()
    community_cards = []

    # give nick community cards
    community_cards.append(d.map_card(8))
    community_cards.append(d.map_card(12))
    community_cards.append(d.map_card(1))
    # turn and river cards
    community_cards.append(d.map_card(20))
    community_cards.append(d.map_card(40))
    
    # personal hand
    nick.hand.append(d.map_card(24))
    nick.hand.append(d.map_card(51))    

    nick.gen_score(community_cards)

    # check hand is correct
    assert nick.strflush  == 0
    assert nick.fourkind  == 0
    assert nick.fullhouse == 0
    assert nick.flush     == 1
    assert nick.straight  == 0
    assert nick.threekind == 0
    assert nick.pair      == 0

    assert nick.besthand == 5
    assert nick.highcard == 10

#
# test for straight
#
def test_straight():

    # initalize everything
    nick = game_sim.Player('nick',0,100,'nada')
    d = generator.Deck()
    community_cards = []

    # give nick community cards
    community_cards.append(d.map_card(8))
    community_cards.append(d.map_card(41))
    community_cards.append(d.map_card(16))
    # turn and river cards
    community_cards.append(d.map_card(21))
    community_cards.append(d.map_card(38))
    
    # personal hand
    nick.hand.append(d.map_card(24))
    nick.hand.append(d.map_card(13))    
            
    nick.gen_score(community_cards)

    # check hand is correct
    assert nick.strflush  == 0
    assert nick.fourkind  == 0
    assert nick.fullhouse == 0
    assert nick.flush     == 0
    assert nick.straight  == 1
    assert nick.threekind == 0
    assert nick.pair      == 0

    assert nick.besthand == 4
    assert nick.highcard == 6

#
# test for straight flush
#
def test_straight_flush():

    # initalize everything
    nick = game_sim.Player('nick',0,100,'nada')
    d = generator.Deck()
    community_cards = []

    # give nick community cards
    community_cards.append(d.map_card(8))
    community_cards.append(d.map_card(41))
    community_cards.append(d.map_card(16))
    # turn and river cards
    community_cards.append(d.map_card(21))
    community_cards.append(d.map_card(38))
    
    # personal hand
    nick.hand.append(d.map_card(24))
    nick.hand.append(d.map_card(13))    
            
     # for debugging
    print 'community cards: '
    for i in range(0,len(community_cards)):
        print 'name ', community_cards[i].get_name()
    print 'player hand: '
    for i in range(0,len(nick.hand)):
        print 'name ', nick.hand[i].get_name()
            
    nick.gen_score(community_cards)

    # check hand is correct
    assert nick.strflush  == 0
    assert nick.fourkind  == 0
    assert nick.fullhouse == 0
    assert nick.flush     == 0
    assert nick.straight  == 1
    assert nick.threekind == 0
    assert nick.pair      == 0

    assert nick.besthand == 4
    #assert nick.highcard == 
