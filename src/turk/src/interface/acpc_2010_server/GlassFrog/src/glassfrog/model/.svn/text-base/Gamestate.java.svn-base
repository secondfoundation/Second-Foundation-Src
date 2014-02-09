package glassfrog.model;

import java.io.Serializable;

/**
 * The Gamestate class handles all of the state information for a particular
 * game at any given time.  This class is constantly updated and accessed.
 * It holds information pertinant to the actual game, not the individual players
 * such as potsize, current bet, num bets, round number
 * 
 * @author jdavidso
 */
public class Gamestate implements Serializable{
    
    private int potsize;
    private int minBet;
    private int maxBet;
    private int currentBet;
    private int round;
    private int numBets;
    private int button;
    private boolean handOver;      
    private String actionString;
    private Gamedef gamedef;
    
    /**
     *  Get the current position of the button
     * @return an int representing position of the button
     */
    public int getButton() {
        return button;
    }

    /**
     * Set the position of the button
     * @param button an int representing the position of the button
     */
    public void setButton(int button) {
        this.button = button;
    }
    
    /**
     * Get the current bet size
     * @return an int representing the current bet size
     */
    public int getCurrentBet() {
        return currentBet;
    }

    /**
     * Set the current betsize
     * @param currentBet an int representing the current betsize
     */
    public void setCurrentBet(int currentBet) {
        this.currentBet = currentBet;
    }

    /**
     * Return whether or not the hand is over
     * @return True if the hand is over, false otherwise
     */
    public boolean isHandOver() {
        return handOver;
    }

    /**
     * Sets whether the hand is over or not
     * @param handOver a boolean representing whether or not the hand is over
     */
    public void setHandOver(boolean handOver) {
        this.handOver = handOver;
    }

    /**
     * Get the maximum bet of the game
     * @return an int representing the game's maximum bet
     */
    public int getMaxBet() {
        return maxBet;
    }

    /**
     * Set the maximum bet of the game
     * @param maxBet an int representing the games max bet
     */
    public void setMaxBet(int maxBet) {
        this.maxBet = maxBet;
    }

    /**
     * Get the minimum bet for the game
     * @return an int representing the minimum bet for the game
     */
    public int getMinBet() {
        return minBet;
    }

    /**
     * Set the minimum bet for the game
     * @param minBet an int representing the game's minimum bet
     */
    public void setMinBet(int minBet) {
        this.minBet = minBet;
    }

    /**
     * Get the number of bets made so far in the game for the round
     * @return an int representing the number of bets made in the game for the round
     */
    public int getNumBets() {
        return numBets;
    }

    /**
     * Set the number of bets made so far in the game in this round
     * @param numBets an int representing the number of bets made in the round
     */
    public void setNumBets(int numBets) {
        this.numBets = numBets;
    }

    /**
     * Get the current potsize
     * @return an int representing the current potsize of the game
     */
    public int getPotsize() {
        return potsize;
    }

    /**
     * Set the potsize
     * @param potsize an int representing the potsize of the game
     */
    public void setPotsize(int potsize) {
        this.potsize = potsize;
    }

    /**
     * Get the current round
     * @return an int representing the current round of the game
     */
    public int getRound() {
        return round;
    }

    /**
     * Set the current round
     * @param round and int representing the current round of the game
     */
    public void setRound(int round) {
        this.round = round;
    }    
    
    /**
     * Get the the string representation of the betting sequence
     * @return A string representing the betting sequence
     */
    public String getActionString() {
        return actionString;
    }
    
    /**
     * Default constructor.
     */
    public Gamestate( Gamedef gamedef ) {
        button = 0;
        round = 0;
        potsize = 0;
        numBets = 0;
        maxBet = 0;
        minBet = 0;
        currentBet = 0;
        handOver = false;   
        actionString = "";
        this.gamedef = gamedef;
    }

    /**
     * Increment the round by one.  Reset the current bet to 0 and the num bets;
     * Append a "/" to the action string
     */
    public void nextRound() {
        round++;        
        // XXX: This is a slightly hacky way to get the minimum bet and that
        // wasn't the intended use for this gamedef parameter.
        minBet = gamedef.getMinBet();
        actionString += "/";
        numBets = 0;        
    }
    
    /**
     * Have the game commit a bet of size betSize.  The current bet will then
     * be the max of the current bet and the betSize.
     * @param betSize an int representing the size of the bet to make
     * @param lastCommited an int to make sure the current bet is how much the last
     *        player had in the pot
     */
    public void makeBet(int betSize, int lastCommited) {
        // XXX: minBet is not being updated correctly if betSize+lastCommited <
        // currentBet since it will become negative.  This doesn't come up if
        // stacks are equal in size, but if stacks are unequal then this can
        // come up.
        // XXX: minBet is also not updated correctly if we were in a 3 player
        // no-limit game.  This should really just directly implement the rule
        // where a raise must be at least as big as the previous raise.
        int totalCommitted = betSize + lastCommited;

        addToPot(betSize);   
        if(totalCommitted > currentBet) {
            numBets++;
            minBet = 2*(totalCommitted - currentBet);
        }
        currentBet = (totalCommitted < currentBet ? currentBet : totalCommitted); 
        //minBet = 2*betSize;        
    }
    
    /**
     * Add to the pot the amount given.
     * @param amount An int amount to add to the pot
     */
    public void addToPot(int amount) {
        potsize += amount;
    }
    
    /**
     * Subtract from the pot the amount given.  Used for hand evaluation and payout
     * @param amount The amount to subtract from the potsize
     */
    public void subtractFromPot(int amount) {
        potsize -= amount;
    }
    
    /**
     * Add an action to the action string.
     * @param action a string representing what actions to add to the action string
     */
    public void addToActionString(String action) {
        actionString += action;
    }
    
    /**
     * A String representation of the gamestate... This is the human readable
     * one for debugging, a player friendly one will have to be generated
     * @return A Human readable gamestate represented as a String
     */
    @Override
    public String toString() {
        String gsString = "";
        gsString+="Round: "+round+"\n";
        gsString+="Button: "+button+"\n";
        gsString+="Potsize: "+potsize+"\n";
        gsString+="Min Bet: "+minBet+"\n";
        gsString+="Max Bet: "+maxBet+"\n";
        gsString+="Current Bet: "+currentBet+"\n";
        gsString+="Num Bets this round: "+numBets+"\n";        
        return gsString;
    }
}
