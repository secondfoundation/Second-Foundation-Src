package glassfrog.model;

import java.io.Serializable;
import java.util.ArrayList;

/**
 * The Hand class is used to represent a set of cards for the players and the 
 * board.  More specifically, a Hand is the set of all the private cards for 
 * all of the players over all of the rounds and the set of public cards for 
 * all of the rounds.
 * Use: To store hands dealt from the deck and give string representations of
 * those hands for evaluation.
 * @author jdavidso
 */
public class Hand implements Serializable{

    private int numRounds;
    private int numPlayers;    
    private int[] numPrivateCards;
    private int[] numPublicCards;
    private ArrayList<Card>[] publicCards; //[round]
    private ArrayList<Card>[][] privateCards; //[player][round]    
   
    /**
     * Return the public cards for a given round
     * @param round an int representing the round to return the public cards for
     * @return an @ArrayList of @Cards for the given round
     */
    public ArrayList<Card> getPublicCards(int round) {
        return publicCards[round];
    }
    
    /**
     * Set the public card array for the hand
     * @param publicCards an @ArrayList of @Cards that represents the public cards
     * for the hand
     */
    public void setPublicCards(ArrayList<Card>[] publicCards){
        this.publicCards = publicCards;
    }

    /**
     * Return the private cards for a player for the given hand in a given round
     * @param player an int representing the seat of the player to return the cards
     * to
     * @param round an int representing the round the private cards came from
     * @return an @ArrayList of @Cards for the player and round specified
     */
    public ArrayList<Card> getPrivateCards(int player, int round) {
        return privateCards[player][round];
    }
    
    /**
     * Set the private cards for a specific player
     * @param privateCards an @ArrayList of @Cards representing the players private cards
     */
    public void setPrivateCards(ArrayList<Card>[][] privateCards){
        this.privateCards = privateCards;
    }
    
    /**
     * Default constructor. Not really intened for use.
     */
    public Hand() {
        numRounds = 0;
        numPrivateCards = null;
        numPublicCards = null;
        numPlayers = 0;
        initializeCardArrays();
    }

    /**
     * Good constructor.  Takes in the number of players, rounds, private and
     * public cards and initializes the arrays and numbers for holding and 
     * displaying the Hand information.
     * 
     * @param numPlayers
     * @param numRounds
     * @param numPrivateCards
     * @param numPublicCards
     */
    public Hand(int numPlayers, int numRounds, int[] numPrivateCards,
            int[] numPublicCards) {
        this.numRounds = numRounds;
        this.numPlayers = numPlayers;
        this.numPrivateCards = numPrivateCards;        
        this.numPublicCards = numPublicCards;
        initializeCardArrays();        
    }
    
    /**
     * Used to preset a hand with given cards
     * @param numPlayers
     * @param numRounds
     * @param publicCards
     * @param privateCards
     */
    public Hand(int numPlayers, int numRounds, ArrayList<Card>[] publicCards, 
            ArrayList<Card>[][] privateCards) {
        this.numRounds = numRounds;
        this.numPlayers = numPlayers;
        this.publicCards = publicCards;
        this.privateCards = privateCards;
    }

    /**
     * Initializes the public and private card arrays with to the proper sizes
     */
    private void initializeCardArrays() {
        publicCards = new ArrayList[numRounds];
        privateCards = new ArrayList[numPlayers][numRounds];        
    }    

    /**
     * Override of the toString method for easy to read hand representation.
     * 
     * @return an easy to read representation of the hand
     */
    @Override
    public String toString() {
        String retString = "";
        for (int player = 0; player < numPlayers; player++) {
            retString += "Position " + player + ": [ ";
            for (int round = 0; round < numRounds; round++) {                                
                for (Card c : privateCards[player][round]) {
                    retString += c.toString() + " ";
                }                
                retString += "| ";
            }
            retString += "]\n";
        }
        
        retString += "Board Cards: [ ";
        for (int round = 0; round < numRounds; round++) {            
            for (Card c : publicCards[round]) {
                retString += c.toString() + " ";
            }
            retString += "| ";            
        }
        retString += "]";        
        return retString;
    }
    
    /**
     * Return the hand for the given player (only thier private cards) and all
     * public cards. This is used to be passed to the hand evaluation class.
     * 
     * @param player An integer representing the index of the player for the hand
     * @return A string formatted for the hand evaluation class
     */
    public String getEvaluationString(int player) {
        String retString = "";
        for (int round = 0; round < numRounds; round++) {
            for (Card c : privateCards[player][round]) {
                retString += c.toString() + " ";
            }            
        }        
        retString += boardToString();
        return retString;
    }

    /**
     * Returns the board cards for a given hand, space delimited.
     * @return A string representing the board cards
     */
    public String boardToString() {
        String retString = "";
        for (int roundIndex = 0; roundIndex < numRounds; roundIndex++) {
            for (Card c : publicCards[roundIndex]) {
                retString += c.toString() + " ";
            }
        }
        return retString;
    }

    /**
     * Return the cards for a player for a given round
     * @param player An integer representation of the player for the index
     * @param round An integer representation of the round for the index
     * @return A string representing the private cards for a given player/round
     */
    public String getPrivateCardsString(int player, int round) {
        String retString = "";
        for (Card c : privateCards[player][round]) {
            retString += c.toString();
        }
        return retString;
    }

    /**
     * Return the public cards for a given round
     * @param round An integer representation of a round for the index
     * @return A string representing the public cards for a specified round
     */
    public String getPublicCardsString(int round) {
        String retString = "";
        for (Card c : publicCards[round]) {
            retString += c.toString();
        }
        return retString;
    }
}
