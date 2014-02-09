package glassfrog.model;

import java.io.Serializable;

/**
 * The Card class is used to represent cards in the deck.  The cards have a suit
 * and a rank and are initialized as such
 * 
 * @author jdavidso
 */
public class Card implements Serializable{
    private Integer rank;
    private String suit;
   
    /**
     * A default constructor with rank 0 and unsuited.
     */
    public Card() {
        rank = 0;
        suit = "Unsuited";
    }

    /**
     * This is the constructor most often used to create a card with a given 
     * suit and rank.
     * 
     * @param suit The String representation of a playing card suit
     * @param rank The Integer representation of the card suit.
     */
    public Card(String suit, Integer rank){
        this.rank = rank;
        this.suit = suit;
    }
    
    /**
     * This constructor constructs a card out of just a string.
     * Strinks are Rank then Suit, as such As for the Ace of spades, Kh for the
     * king of hearts Qd for the queen of diamonds Jc for the Jack of clubs then
     * Th for the 10 of hearts 9-2 for the other ranks
     * @param cardString A String representation of the card
     */
    public Card(String cardString) {
        switch(cardString.toUpperCase().charAt(0)) {
            case 'A':
                this.rank = 1;
                break;
            case 'K':
                this.rank = 13;
                break;
            case 'Q':
                this.rank = 12;
                break;
            case 'J':
                this.rank = 11;
                break;
            case 'T':
                this.rank = 10;
                break;
            default:
                try {
                    this.rank = new Integer(cardString.substring(0,1));
                } catch (NumberFormatException ex) {
                    this.rank = 0;
                }
        }
        switch(cardString.toLowerCase().charAt(1)) {
            case 's':
                this.suit = "Spades";
                break;
            case 'h':
                this.suit = "Hearts";
                break;
            case 'd':
                this.suit = "Diamonds";
                break;
            case 'c':
                this.suit = "Clubs";
                break;            
            default: this.suit = "Unsuited";
        }
        
    }

    /**
     * Returns the rank of the Card
     * 
     * @return rank
     */
    public Integer getRank() {
        return rank;
    }

    /**
     * Returns the suit of the Card
     * 
     * @return suit
     */
    public String getSuit() {
        return suit;
    }

    /**
     * Returns a human readable String representation of the Card given by the 
     * rank then the first character of the suit.  ie: 7d, Ac
     * 
     * @return a String representing the card (Suit and Rank)
     */
    @Override
    public String toString() {
        return printRank() + printSuit();
    }

    /**
     * Returns the first character of the suit in lower case.
     * 
     * @return substring(0,1) suit
     */
    private String printSuit() {
        return suit.substring(0, 1).toLowerCase();
    }

    /**
     * Returns a human readable rank from the rank integer.
     * 
     * @return rank {(0-9, T, J, Q, K, A }
     */
    private String printRank() {
        if (rank == 1) {
            return "A";
        } else if (rank < 10) {
            return rank.toString();
        } else {
            switch (rank) {
                case 10:
                    return "T";
                case 11:
                    return "J";
                case 12:
                    return "Q";
                case 13:
                    return "K";
            }
        }
        return "";
    }
}
