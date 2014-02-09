package glassfrog.players;

import java.io.Serializable;
import java.net.SocketTimeoutException;

/**
 * The Player class represents the players in the game.  They are given attribures
 * such as thier current bet, score, how much they have commited to the pot, thier
 * seat, hand rank, stack size.  They also keep track of the actions of the player, 
 * such as if the player has acted in a particular round or if they have folded in
 * a hand
 * 
 * The Player class is also responsible for keeping track of the socket to which 
 * each player connects (The Buffered reader and the Print Writer of each as well)
 * @author jdavidso
 */
public abstract class Player implements Comparable<Player>, Serializable{

    private String name, handString, cardString;    
    private int stack,  buyIn,  currentBet,  score,  
            totalCommitedToPot,  seat, handRank, position;
    private long timeUsed;
    private boolean acted,  folded;    

    /**
     * Default Player constructor
     */
    public Player() {
        this.name = "Default";
        this.buyIn = 0;        
        initializePlayer();
    }

    /**
     * A constructor for a Player object that only takes a name, buyIn
     * 
     * @param name A String representing the name
     * @param buyIn An int representing the buyin value for the player     
     */
    public Player(String name, int buyIn) {
        assert (buyIn > 0);
        this.name = name;
        this.buyIn = buyIn;        
        initializePlayer();
    }
    
    /**
     * Get the amount the player bought in for
     * @return an int representing the buyin amount
     */
    public int getBuyIn() {
        return buyIn;
    }
    
    /**
     * Set the buying amount for the player
     * @param buyIn an int representing the amount the player bought in for
     */
    public void setBuyIn(int buyIn) {
        this.buyIn = buyIn;
    }

    /**
     * Get the current score of the player
     * @return an int representing the player's score
     */
    public int getScore() {
        return score;
    }

    /**
     * Set the current score for the player
     * @param score an int representing the player's score
     */
    public void setScore(int score) {
        this.score = score;
    }
    
    /**
     * Add a value to the player's score
     * @param score an int representing the amount to increment the score by
     */
    public void addToScore(int score) {
        this.score += score;
    }
    
    /**
     * Check whether or not the player has acted in this round
     * @return True if the player has acted, False otherwise
     */
    public boolean isActed() {
        return acted;
    }

    /**
     * Check to see if the player has folded
     * @return True if the player has folded, False otherwise
     */
    public boolean isFolded() {
        return folded;
    }
    
    /**
     * Check to see if the player is a GUIPlayer.
     * @return False for all players other than those that override this method
     */
    public boolean isGuiPlayer() {
        return false;
    }
    
    /**
     * Check to see if this player is a SocketPlayer
     * @return False for all players other than those who override this method
     */
    public boolean isSocketPlayer() {
        return false;
    }
    
    /**
     * Check to see if this player is a AAAIPlayer
     * @return False for all players other than those who override this method
     */    
    public boolean isAAAIPlayer() {
        return false;
    }
    
    /**
     * Get the player's current betsize
     * @return an int representing the betsize of the player
     */
    public int getCurrentBet() {
        return currentBet;
    }
    
    /**
     * Get the total amount the player has committed to the pot
     * @return an int representing the amount the player has committed to the pot
     */
    public int getTotalCommitedToPot(){
        return totalCommitedToPot;
    }
    
    /**
     * Get the name of the player
     * @return a @String representing the player's name
     */
    public String getName(){
        return name;
    }
    
    /**
     * Set the player's name
     * @param name a @String representing the player's name
     */
    public void setName(String name) {
        this.name = name;
    }
    
    /**
     * Get the current stack size of the player
     * @return an int representing the current stack size
     */
    public int getStack(){
        return stack;
    }
    
    /**
     * Set the current stack size for the player
     * @param stack an int representing the stack size to set
     */
    public void setStack(int stack){
        this.stack = stack;
    }
    
    /**
     * Get the player's seat
     * @return an int representing which seat the player is currently sitting in
     */
    public int getSeat() {
        return seat;
    }
    
    /**
     * Set the player's seat
     * @param seat an int representing which seat the player is to be assigned
     */
    public void setSeat(int seat) {
        this.seat = seat;
    }
    
    /**
     * Get the hand rank of the player's current hand
     * @return an int representing the hand rank of the player.  Note: this is not
     * calculated by the player, but rather assigned on showdown by the @Dealer
     */
    public int getHandRank() {
        return handRank;
    }
    
    /**
     * Set the hand rank for the player
     * @param handRank an int representing the hand rank as calculated by the @Dealer
     */
    public void setHandRank(int handRank) {
        this.handRank = handRank;
    }
    
    /**
     * Get the @String representation of the player's cards.  This is calculated by 
     * the @HandEvaluator from teh @Dealer class
     * @return a @String representing the best 5-Card hand the player has made
     */
    public String getHandString() {
        return handString;
    }
    
    /**
     * Set the string value of the player's current hand.  This is used for 
     * showdowns on the gui
     * 
     * @param handString The string that represents the players hand
     */
    public void setHandString(String handString) {
        this.handString = handString;
    }
    
    /**
     * Get a string representation of thier best 5 card hand
     * @return a String representation of the player's best 5 card hand
     */
    public String getCardString() {
        return cardString;
    }

    /**
     * Set a string representing the players best 5 card poker hand
     * @param cardString A string that represents the players 5 best cards
     */
    public void setCardString(String cardString) {
        this.cardString = cardString;
    }
    
    /**
     * Get the players position relative to the button
     * @return The player's position, 0 being the 
     */
    public int getPosition() {
        return position;
    }    
    
    /**
     * Set the players position relative to the button
     * @param position The position the player is in.  0 is the button.
     */
    public void setPosition(int position) {
        this.position = position;
    }        

    /**
     * All players must implement a shutdown routine
     */
    public abstract void shutdown();
    
    /**
     * Subtract the amount from the Player's totalCommitedToPot value
     * 
     * @param amount Amount to subtract
     */
    public void subtractTotalCommitedToPot(int amount) {
        totalCommitedToPot -= amount;
    }

    /**
     * Set up all the defaults for the player, such as the acted and folded flags 
     * to false, the bets and scores to 0 and set the stack to the buyin value
     */
    private void initializePlayer() {
        acted = false;
        folded = false;
        currentBet = 0;
        score = 0;
        totalCommitedToPot = 0;
        stack = buyIn;
        position = seat;
        timeUsed = 0;
    }

    /**
     * Make a bet of the passed in size.  This will decrement the Player's stack,
     * increase thier current bet and total commited to the pot, as well as set
     * thier acted flag for the round to true.
     * @param betSize
     * @return The size of the bet that is made
     */
    public int bet(int betSize) {
        if(betSize > stack) {
            betSize = stack;
        }
        stack -= betSize;
        currentBet += betSize;
        totalCommitedToPot += betSize;
        acted = true;
        return betSize;
    }

    /**
     * A special type of bet where the player is considered not to have acted
     * for the round
     * @param blindSize The size of bet that the player makes
     * @return The players current bet
     */
    // XXX: Doesn't test if the blind is bigger than your stack
    public int postBlind(int blindSize) {
        currentBet = bet(blindSize);
        acted = false;
        return currentBet;
    }

    /**
     * Set the player's fold flag to true
     */
    public void fold() {
        folded = true;
    }
    
    /**
     * GetAction is the method that all the inherited classes of the bot 
     * must implement.  This is called by the dealer to get the bot's actions
     * 
     * @return one of {f,c,r,rX} where X is a raise amount
     * 
     */
    public abstract String getAction() throws SocketTimeoutException;
    
    /**
     * update is called by dealer to transmit the current gamestate in String 
     * representation to the player.  This tells the player what the current
     * gamestate is.
     * 
     * @param gamestate The AAAI competition formated string representation of the
     * gamestate
     */
    public abstract void update(String gamestate);
            
    /**
     * Have the player call the current bet  This will take the player's current 
     * bet and figure out how much more the player has to bet to call, make that
     * bet then return the amount it cost to make the bet since there will be some
     * cases where a call will be more that the player's stack and the player will
     * then be all in for less than the amount needed to call
     * 
     * @param currentBet The size of the bet that the player needs to call
     * @return The amount that the player bet to call the current bet passed in
     */
    public int call(int currentBet) {        
        int betSize = currentBet - this.currentBet;
        if(betSize >= 0) {
            //Call
            return bet(betSize);
        }
        return betSize;
    }

    /**
     * Check to see if the player is all in.  This is whether or not they have 
     * any chips left in thier stack
     * @return True if stack &lt;= 0
     */
    public boolean isAllIn() {
        return stack <= 0;
    }

    /**
     * Payout the player.  That is, increase thier stack by the value passed in.
     * @param pay The amount to increase the player's stack by
     */
    public void payout(int pay) {
        stack += pay;
    }

    /**
     * Reset the per/round attributes such as the acted flag and currentBet for 
     * the player.
     */
    public void resetRound() {
        acted = false;
        //currentBet = 0;
    }

    /**
     * Reset all of the per/hand values for the player, such as the acted and 
     * folded flags, the current bet, and the amount the player has commited to 
     * the pot so far
     */
    public void resetHand() {
        acted = false;
        folded = false;
        currentBet = 0;
        totalCommitedToPot = 0;
    }

    /**
     * Set the Player's stack back to the starting size.  Used for Doyle's game
     */
    public void resetStack() {
        stack = buyIn;
    }
    
    /**
     * Reset the Player.
     * 
     * This will reset the player's current stack to the starting value, all of
     * the per/hand attribures and the score to 0
     * 
     * @param doylesGame
     */
    public void resetPlayer(boolean doylesGame) {
        resetHand();        
        if(doylesGame) {
            resetStack();
        }
        
    }

    /**
     * A string representation of a Player object
     * @return A String representation of this player.
     */
    @Override
    public String toString() {
        return "PLAYER:Name:"+ name + ":Stack:" + stack + ":Seat:" + seat + 
                ":Position:" + position + ":Score:" + score;
    }
    
    /**
     * A compact string representation of a Player object (name:stack:score:seat)
     * @return A compact String representation of this player.
     */    
    public String toShortString() {
        return "PLAYER:"+ name + ":" + stack + ":" + score + ":" + seat;                
    }

    /**
     * Compare the stack size of one player to another.  Used to sort the 
     * players by stacksize in the game
     * @param o The player to compare this player to.
     * @return 0 if the stacks are equal, Positive if the other player has a 
     * stack larger than this player, Negative if this player has a stack larger
     * than the player being compared to.
     */
    public int compareTo(Player o) {
        return o.stack - this.stack;
    }
    
    /**
     * Set timeout, used for socket players.  If the socket player takes more
     * time to respond with an action than the specified timeout, then the
     * player's socket will timeout and an exception will be thrown.
     * @param timeout Timeout for the player's actions
     */
    public void setActionTimeout(long timeout) {};

    /**
     * Set timeout, used for socket players.  If the socket player takes more
     * time than the specified timeout over the course of the entire match,
     * then the player's socket will timeout and an exception will be thrown.
     * @param timeout Timeout for the player's actions
     */
    public void setMatchTimeout(long timeout) {};

    /**
     * Set the amount of time used by this player to take actions
     * @param used int representing the number of milliseconds used by the
     * player to act
     */
    public void setTimeUsed(long used) {
        this.timeUsed = used;
    }

    /**
     * Get the value of the per action timeout.  Currently used for socket
     * players. 
     * @return an int representing the number of milliseconds allowed for per
     * action.
     */
    public long getActionTimeout() {
        return 0;
    };

    /**
     * Get the value of the per match timeout.  Currently used for socket
     * players. 
     * @return an int representing the number of milliseconds allowed over the
     * entire match
     */
    public long getMatchTimeout() {
        return 0;
    };

    /**
     * Get the amount of time used by this player to take actions
     * @return an int representing the number of milliseconds used by the
     * player to act
     */
    public long getTimeUsed() {
        return timeUsed;
    }
}
