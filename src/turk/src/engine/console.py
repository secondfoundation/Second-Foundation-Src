# -*-py-*-
#
# Class that prompts for a bet
#
class ConsoleDecider:
    def getDecision(self, hand_context):
        while True:
            try:
                raw_bet = raw_input("place your bet>")
                bet_total = int(raw_bet)
            except ValueError:
                print raw_bet, 'is not a valid bet, please bet again'
                continue

            # check the bet is valid in the round
            # if not, loop back to prompt
            if hand_context.check_bet_sanity(bet_total):
                continue

            return bet_total
