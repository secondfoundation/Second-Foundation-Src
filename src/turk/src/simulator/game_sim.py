# -*-py-*-  
#
# this holds the core data objects we need
#
import random
import math
from engine import console
from engine import heuristic
from util import helpers
from generator import Deck

class Poker:
    """a game of poker"""
    def __init__(self):
        self.players = []
        self.deck = Deck()

    def start(self,nplayers,nhuman_players):
        
        # error handler for float, double
        if math.floor(nplayers) != math.ceil(nplayers):
            print 'turk epic fail:: gen_hand was passed a non-integer number of players!!'
            exit(1)

        # error handler for float, double (nhuman_players)
        if math.floor(nhuman_players) != math.ceil(nhuman_players):
            print 'turk epic fail:: gen_hand was passed a non-integer number of human players!!'
            exit(1)
            
        # error handler for strings
        try: 
            nplayers=int(nplayers)
        except:
            print 'turk epic fail:: gen_hand was passed a non-integer number of players!!'
            exit(1)
        
        # error handler -- sanity checks
        if nplayers > 10:
            print 'turk epic fail:: gen_hand only supports up to ten players!'
            exit(1)

        # error handler -- sanity checks
        if nhuman_players > nplayers:
            print 'turk epic fail:: poker.start method called with more human players than players!!'
            exit(1)

        # error handler -- sanity checks
        #if nhuman_players > 1:
        #    print 'turk epic fail:: more than one human player selected (we do not support at this time!'
        #    exit(1)

        if nplayers < 2:
            print 'turk epic fail:: gen_hand needs two players!'
            exit(1)
         
        starting_chips = 2000
        player_list = ["jay","nick","sam","julian","marcus","ethan","frank","david","emily","sarah"]

        # can pick a player to be interactive        
        # nick hacking to allow dynamic allocation of:
        # number of human players
        # ACHTUNG! only one (or zero) can be selected!
        console_player = []
        if(nhuman_players > 0 ):
            for x in range(nhuman_players):
                console_player.append(player_list[x])
        else: 
            console_player.append('nobody')        
 
        for x in range(nplayers):
            # default is computer
            player_engine = heuristic.HeuristicDecider()
                       
            # if name on list, make human
            for y in range(len(console_player)):
                if player_list[x] == console_player[y]:
                    player_engine = console.ConsoleDecider()
            
            self.players.append(Player(player_list[x],x,starting_chips, player_engine))

        self.small_blind = 25

        # assign dealer position to random player
        self.dealer_position = random.randint(0,len(self.players) - 1)

        self.hand_history = []

        # this main loop just plays hands until it determines the game is over
        while self.players_have_chips():
            self.deck.shuffle()
            for player in self.players:
                print "*-----------------------------------------*"
                print "player: ",player.name
                print player.name, ' has: ', player.chips, ' chips'
                player.hand = self.deck.deal_cards(2)

            print 'Playing next hand, dealer pos:', self.dealer_position, ' : ', self.players[self.dealer_position].name
            hand = Hand(self.players, self.dealer_position, self.small_blind, self.deck, self.hand_history)
            hand.play()

            # make next player the dealer
            self.dealer_position = (self.dealer_position + 1) % len(self.players)
            while self.players[self.dealer_position].chips <= 0:
                self.dealer_position = (self.dealer_position + 1) % len(self.players)

            self.hand_history.append(hand)

    def players_have_chips(self):
        players_with_chips = [p for p in self.players if p.chips > 0]
        return len(players_with_chips) > 1

#
# jay: trying to rework bets so that it's easier to get useful bet history

# A round is a round of bets
# I think this is cleaner than a 2D array in Hand and it also has utilities to
# set the bet type and amount
class Round:
    def __init__(self, name):
        self.name = name
        self.bets = []

    def __str__(self):
        return self.name

    # underscore indicates private
    # this and _set_bet_amount are private because they break if called before some bet attributes are set
    def _set_bet_type(self, bet):
        if bet.total == -1:
            bet.type = Bet.Type.fold
            return

        if len(self.bets) != 0:
            prev_total = self.bets[-1].total
        else:
            prev_total = 0

        if prev_total == 0:
            bet.type = Bet.Type.bet
        elif prev_total < bet.total:
            bet.type = Bet.Type.inc
        elif prev_total == bet.total:
            bet.type = Bet.Type.call

    # underscore indicates private
    # this and _set_bet_type are private because they break if called before some bet attributes are set
    def _set_bet_amount(self, bet):
        # the bet amount is the amount the player had to add to the pot from their previous bet total
        bet.amount = bet.total - bet.player.round_pot

    # this will create a Bet given a player and a bet total, and fill in the type (call, raise etc)
    # it will also track the difference from the player's previous bet total compared to the new total
    # this function is really a utility for setting up all this information based on only the bet total
    # it does not add the bet to the bets for the round
    def make_round_bet(self, bet_total, player, blind = False):
        bet = Bet()
        bet.total = bet_total
        bet.player = player
        if bet.total != -1:
            self._set_bet_amount(bet)
        if blind:
            bet.type = Bet.Type.blind
        else:
            self._set_bet_type(bet)
        return bet

    # same as make_round_bet, except the bet is added to the current round and the player's round_pot is updated
    def add_round_bet(self, bet_total, player, blind = False):
        bet = self.make_round_bet(bet_total, player, blind)
        self.bets.append(bet)
        bet.player.round_pot = bet.total
        return bet


# class for Bets to make it easier to track their player, type etc
class Bet:
    fold = -1

    # constants for bet types to prevent typos
    class Type:
        # raise is a keyword, use 'inc'
        fold, call, inc, bet, blind = "fold", "call", "raise", "bet", "blind"

    def __init__(self):
        # player who made the bet
        self.player = None
        # the total chips the player has in the pot for this round
        # this is the total bet that they matched
        self.total = None
        # this is the incremental amount of this particular call/raise
        # if this is an initial bet (previous player checked) total and amount will be equal
        self.amount = None
        # keep track of whether the bet was a bet/call/raise as we go so it's easy to analyze betting patterns later
        self.type = None

    def __str__(self):
        return self.player.name + " " + self.get_action()

    def get_action(self):
        str_amount = str(self.amount)
        str_total = str(self.total)
        if self.type == self.Type.fold:
            return "folds"
        if self.type == self.Type.call:
            call_str = "calls " + str_amount
            if str_amount !=  str_total:
                call_str += " more for " + str_total + " total"
            return call_str
        if self.type == self.Type.inc:
            return "raises to " + str_total + " total"
        if self.type == self.Type.bet:
            if self.total == 0:
                return "checks"
            else:
                return "bets " + str_amount
        if self.type == self.Type.blind:
            return "puts in " + str_total + " blind"

class Pot:
    def __init__(self, name, base_chips):
        self.name = name
        self.net_chips = base_chips
        self.base_chips = base_chips

    def __str__(self):
        return self.name

class Hand:
    # set up all the data for the hand, this should be everything the decision engine needs to make a bet
    def __init__(self, players, dealer_position, small_blind, deck, hand_history):
        self.players = players
        self.dealer_position = dealer_position
        self.small_blind = small_blind
        self.deck = deck
        self.hand_history = hand_history

        self.round_iterator = None
        self.players_remaining = len(players)
        self.active_player = None
        self.round = None
        self.pots = [Pot("main", 0)]
        self.community_cards = []

        # obviously these rounds are specific to Hold-em so this Hand class is really a HoldemHand
        pre_flop = Round("pre_flop")
        # before each round begins, the setup() function for that round is called
        # each round is assigned a pointer to the function that will serve as its setup function
        # this should allow us to re-use the main round loop for other games besides hold em,
        # since they can define their own rounds
        pre_flop.setup = self.do_blinds

        flop = Round("flop")
        flop.setup = self.deal_flop

        turn = Round("turn")
        river = Round("river")
        turn.setup = river.setup = self.deal_post_flop

        self.all_rounds = [pre_flop, flop, turn, river]

    def play(self):
        for p in self.players:
            p.in_play = True

        for self.round in self.all_rounds:
            print "*-----------------------------------------*"
            print " Next round:", self.round
            print "*-----------------------------------------*"

            # reset state in the hand
            self.reset_round()
            # run the specific setup function for this round
            self.round.setup()

            while not self.all_round_bets_called():
                self.active_player = self.round_iterator.next()
                # get the next action from the player's decision engine
                # This Hand object has everything the engine needs (including the hand history)
                # bet will be -1 (fold), 0 (check) or a total amount representing a bet, call or raise
                bet_total = self.active_player.decision_engine.getDecision(self)
                # add_round_bet will take care of keeping track of other bet attributes besides the total amount
                # this frees the decision engine from having to correctly construct the Bet object
                bet = self.round.add_round_bet(bet_total, self.active_player)
                # __str__ is defined in bet so that this prints 'jay calls 200', 'jay raises 100 to 150 total', etc
                print bet

                if bet.type == Bet.Type.fold:
                    self.active_player.fold()
                    self.players_remaining = self.players_remaining - 1
                else:
                    self.active_player.chips -= bet.amount
                    self.pot += bet.amount

            # all players except one fold, we have a winner
            # nick: bug in here, trying fix
            if self.players_remaining == 1:
                self.active_player = self.round_iterator.next()
                self.active_player.chips += self.active_player.best_pot.net_chips
                print self.active_player.name, 'won', self.pot, 'chips'
                return

            # this is the end of the last round, and more than one player remains, rank their hands and determine winner
            if self.round == self.all_rounds[-1]:
                self.show_hand()

          #  self.update_pots()

    def reset_round(self):
        self.round_iterator = self.make_round_iterator()
        for p in self.players:
            p.round_pot = 0

    # this is called at the end of every round to consolidate player's round-pots into pots for the hand
    # it will create a side pot for each player who is all-in
    def update_pots(self):
        def pot_compare(p1, p2):
            return p1.round_pot - p2.round_pot

        players_all_in = [p for p in self.players if p.in_play]
        players_all_in.sort(pot_compare)
        for i, player in enumerate(players_all_in):
            self.pots[-1].net_chips += player.round_pot * (self.players_remaining - i)
            player.best_pot = self.pots[-1]
            self.add_side_pot()

    def add_side_pot(self):
        new_pot = Pot("side pot " + str(len(self.pots) - 1), self.pots[-1].net_chips)
        self.pots.append(new_pot)

    # setup function for pre_flop round
    def do_blinds(self):
        # small blind
        self.active_player = self.round_iterator.next()
        self.round.add_round_bet(self.small_blind, self.active_player, blind = True)
        self.active_player.chips -= self.small_blind

        # big blind
        big_blind = self.small_blind * 2
        self.active_player = self.round_iterator.next()
        self.round.add_round_bet(big_blind, self.active_player, blind = True)
        self.active_player.chips -= big_blind

        self.pot = self.small_blind + big_blind

    # setup function for flop round
    def deal_flop(self):
        self.community_cards.append(self.deck.deal_cards(3))

    # setup function for turn and river rounds
    def deal_post_flop(self):
        self.community_cards.append(self.deck.deal_cards(1))

    #
    # check bet sanity: checks if a bet is valid
    #
    # return: 0 --> valid bet
    #         1 --> invalid
    def check_bet_sanity(self,bet_total):
        bet = self.round.make_round_bet(bet_total, self.active_player)

        if(bet.amount>self.active_player.chips):
            print 'you do not have enough chips!'
            exit(1)

        stuff = self.round.bets
        last = len(stuff)-1

        # no previous bets this round -- allow for check
        # OR, player is folding, also allow that
        if(last==-1 or bet.type == Bet.Type.fold):
            return 0
        # already bet: check this bet is equal or greater
        else:
            old_bet = stuff[last]
            if(bet.total>=old_bet.total):
                # bet must also be big blind or greater
                if(bet.total>0 and bet.total< 2*self.small_blind):
                    print 'bet is too small-- min bet is: ', 2*self.small_blind
                    return 1
                if(bet.total%self.small_blind != 0):
                    print 'bet must be a multiple of the small blind, i.e. X*', self.small_blind
                    return 1
                #else, good to go
                return 0
            else:
                print 'invalid bet-- minimum to call is:', old_bet.total
                return 1

    #
    # show_hand: if the round is the river and betting is over
    # all players show hands and a winner is selected
    #
    def show_hand(self):
        print "*-----------------------------------------*"
        print " Betting is over--show your cards gentlemen"
        print '',self.players_remaining, " players show their hands."
        print "*------------------------------------------"
        winner = self.active_player
        winner.gen_score(list(self.community_cards))

        contender = self.round_iterator.next()
        contender.gen_score(list(self.community_cards))

        # we have an active player, check his cards against each other set
        # we do this (players_remaining -1 ) times
        for p in range(self.players_remaining-1):
            
            # in the event of a tie, go to high card compare
            if(winner.besthand == contender.besthand):
                print 'both players have the same hand! checking for high card'
                # todo 
                winner = self.tiebreaker(winner,contender)
                print winner.name, 'wins the hand'                

            if(winner.besthand > contender.besthand):
                print winner.name, 'currently has the best hand:'
            else: 
                print contender.name, 'currently has the best hand:'
                winner = contender

            # need a new contender
            contender = self.round_iterator.next()

        # to the winner goes the spoils
        winner.chips += self.pot
        print winner.name, 'won with: '
        print winner.hand_names[winner.besthand]
        print 'pot was: ',self.pot, 'chips'
        return

    # TODO handle all-in
    # TODO handle side pots
    def all_round_bets_called(self):
        if len(self.round.bets) < len(self.players):
            return False

        # get latest bets for each player (last players_remaining elements in the list)
        last_bets = self.round.bets[-self.players_remaining:]
        bet_to_match = last_bets[0].total

        for bet in last_bets[1:]:
            if bet.total != bet_to_match:
                print 'Not all bets in', self.round, 'have been called:', [str(b) for b in self.round.bets]
                return False

        print 'All bets in', self.round, 'have been called:', [str(b) for b in self.round.bets]
        return True

    #
    # tiebreaker: if players both have same hand (say, a flush)
    #             determine which hand is higher
    # 
    def tiebreaker(self,winner,contender):
        # for now, just making winner win, even if unrealistic
        return winner


    # trying out a 'generator' to iterate through the active players in a round
    # http://docs.python.org/py3k/tutorial/classes.html#generators
    def make_round_iterator(self):
        active_index = self.dealer_position
        while self.players_remaining > 0:
            active_index = (active_index + 1) % len(self.players)
            while not self.players[active_index].in_play:
                active_index = (active_index + 1) % len(self.players)
            print "Next Player:", self.players[active_index]
            yield self.players[active_index]

        print 'turk epic fail:: StopIteration error : the round iterator cannot return a valid player-- all players are folded.  Check your win conditions.'
        exit(1)

class Player:
    """a player"""
    def __init__(self, name, position, starting_chips, decision_engine):
        self.name = name
        self.position = position
        self.in_play = True
        self.chips = starting_chips
        self.decision_engine = decision_engine
        self.hand = []
        self.round_pot = 0
        self.pots = []

        self.strflush  = 0
        self.fourkind  = 0
        self.fullhouse = 0
        self.flush     = 0
        self.straight  = 0
        self.threekind = 0        
        self.pair      = 0
        
        # int corresponding to best hand
        self.besthand  = 0 

        # this is a list of high cards after winning hand
        self.highcard = [] 

        # list of each possible hand (ORDER MATTERS HERE)
        self.hand_names = ['high card','pair','two pair', 'three of a kind', 'straight', 'flush', 'full house', 'four of a kind', 'straight flush']


    def __str__(self):
        return self.name

    def fold(self):
        self.in_play = False

    #
    # compare hand: looks at the cards
    # returns a 'score' 
    # obviously has to be a long int
    # 
    # score will be:
    #
    # 0 -- high card       (x)
    # 1 -- pair            (x)
    # 2 -- two pair        ( )
    # 3 -- 3 of a kind     (x)
    # 4 -- straight        ( )
    # 5 -- flush           (x)
    # 6 -- full house      (x)
    # 7 -- 4 of a kind     (x)
    # 8 -- straight flush  (x)
    #
    # after that, we take the high card
    # this is encoded as: highcard [0-13]

    def gen_score(self,community_cards):

        # set all card status to zero
        self.strflush  = 0
        self.fourkind  = 0
        self.fullhouse = 0
        self.flush     = 0
        self.straight  = 0
        self.threekind = 0        
        self.pair      = 0

        # reset best hand
        self.besthand = 0
        self.highcard = 0

        # first, assemble all the cards into a single list
        # flatten turns [[1,2,3],4,5] into [1,2,3,4,5]
        flattened_cards = helpers.flatten(community_cards)
        full_hand = self.hand
        full_hand.extend(flattened_cards)

        print [str(c) for c in full_hand]

        # now, with the full hand, lets determine what hand they have

        # check for straight
        # this is horribly hacked together but it works so oh well
        val_list = []
        for i in range(0,len(full_hand)):
            val_list.append(full_hand[i].value)
            
        # make list big to small
        val_list.sort()
        val_list.reverse()
        
        flg = 0
        # start with largest remaining card
        for i in range(0,7):           
            if(flg==0):
                start = val_list[i]
                hstart = val_list[i]
                cnt = 1
                
                # find cards one smaller than previous card
                for j in range(i,6):                    
                    if((start-1)  == val_list[j+1]):
                        cnt=cnt+1
                        start = val_list[j+1]
                    else:
                        break
                    
                    if(cnt == 4):
                        flg=1
                        print 'you have a straight!'                
                        self.highcard = hstart
                        self.straight = 1
                        self.besthand = 4
                
        # check for flush
        # should have used COUNT list method       
        best = []
        for i in range(0,3):
            outlist = [x for x in full_hand if x.suit == i]
            if(len(outlist) >= 5 ):
                print 'you have a flush!'
                self.flush = 1
                self.besthand = 5

                # find highcard
                for j in range(0,len(outlist)):
                    if(outlist[j].value > self.highcard):
                        self.highcard = outlist[j].value

        # straight flush check
        if(self.straight == 1 and self.flush == 1):
            self.straighflush = 1                        
            self.besthand     = 8
            # todo: check highcard is both part of straight and flush
 
        # check for pairs
        best = []
        for i in range(0,13):
            outlist = [x for x in full_hand if x.value == i]
            if(len(outlist) > len(best)):
                best = outlist

        # find longest string of cards that are identical in value
        count = len(best)
                
        if(count==4):
            print 'you have four of a kind!'
            self.fourkind = 1
            self.besthand = 7
            self.highcard = best[0].value
            return #do NOT check for lesser hands!

        # check for 3 of a kind
        if(count==3):                
            # if three of a kind, lets check for the full house
            secbest = []
            for i in range(0,13):
                # check its not the same hand
                if(i != best[0].value):                               
                    secoutlist = [x for x in full_hand if x.value == i]
                    if(len(secoutlist) > len(secbest)):
                        secbest = secoutlist
            
            seccount = len(secbest)
            if(seccount==2):
                print 'you have a full house!'
                self.fullhouse  = 1
                self.besthand   = 6
                self.highcard = best[0].value
                self.sechighcard = secbest[0].value
                return # do NOT check for lesser hands!
            
            # otherwise, you 'just' had three of a kind
            print 'you have a three of a kind!'
            self.threekind = 1
            self.besthand = 3
            self.highcard = best[0].value
            return

        # check for a pair (or two)            
        if(count==2):
            # if pair, lets check for two pair
            secbest = []
            for i in range(0,13):
                # check its not the same hand
                if(i != best[0].value):                               
                    secoutlist = [x for x in full_hand if x.value == i]
                    if(len(secoutlist) > len(secbest)):
                        secbest = secoutlist
            
            seccount = len(secbest)
            if(seccount==2):
                print 'you have two pair!'
                self.pair  = 2
                self.besthand   = 2
                
                if(best[0].value > secbest[0].value):
                    self.highcard    =    best[0].value
                    self.sechighcard = secbest[0].value
                else:
                    self.highcard    = secbest[0].value
                    self.sechighcard =    best[0].value

                return # do NOT check for lesser hands!
            
            # else, just a single pair
            print 'you have a pair!'
            self.pair += 1
            self.besthand = 1
            self.highcard = best[0].value
            return # do NOT check for lesser hands!

        # nada -- set up list of high cards

        for x in range(len(full_hand)-1):
            #highcard.append(int(math.floor(full_hand[x]/4)))
            
            # highcard.sort()
            return # done here
