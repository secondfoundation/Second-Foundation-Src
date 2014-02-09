# -*-py-*-  
#
# function that returns a decision, based on the heuristics available

class HeuristicDecider():
    def getDecision(self, hand_context):
        # all bets in the current round, except for folds
        round_bets = [b for b in hand_context.round.bets if b.type != "fold"]

        # an example of the new bets, I think they are easier to make decisions with...
        # if the current round is the flop, and this isn't the first bet...
        if hand_context.round.name == "flop" and len(round_bets) != 0:
            # get all players who have called the latest bet
            all_callers = [b.player for b in hand_context.round.bets if b.total == round_bets[-1].total]
            # the first player in that list is the original raiser
            original_raiser = all_callers[0]
            # look in the pre-flop bets for a raise by that player
            pre_flop_raise = [b for b in hand_context.all_rounds[0].bets if b.type == "raise" and b.player == original_raiser]
            # if that player raised pre-flop, we're scared and fold
            if len(pre_flop_raise) != 0:
                print 'Player', original_raiser, 'was the original raiser and raised pre-flop, strength detected'
                return -1
            else:
                # if not, we call
                print 'Player', original_raiser, 'was the original raiser and did not raise pre-flop, possible bluff'
                return round_bets[-1].total

        # grab last bet
        round_bets = hand_context.round.bets
        # if no last bet (bot going first)--check
        if len(round_bets) == 0:
            bet_total = 0
        # otherwise, call
        # unless other player folded! 
        # Then revel in your sweet, sweet victory
        else:
            if(round_bets[-1].type == "fold"):
                bet_total = 0
            else:
                bet_total = round_bets[-1].total

        if hand_context.check_bet_sanity(bet_total):
            print 'turk epic fail:: Heuristic decider made an invalid bet!', bet_total
            exit(1)

        # decision engine does not need to worry about correctly setting up the Bet object
        # the simulator will take care of that based on the bet total and its position in the round
        return bet_total
