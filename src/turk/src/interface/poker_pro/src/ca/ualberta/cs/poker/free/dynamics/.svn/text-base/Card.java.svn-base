/*
 * Card.java
 * 
 * This is an implementation of a card in a standard
 * deck, adapted from the basic Java example for enumeration.
 * In the future, reverting to a more standard representation
 * might be helpful.
 *
 * Created on April 18, 2006, 11:31 AM
 */

package ca.ualberta.cs.poker.free.dynamics;
import java.security.SecureRandom;

/**
 *
 * @author Martin Zinkevich
 */
public class Card {
    
    /**
     * An enumeration class for Rank.
     * It is unclear if there is a significant gain from this, and it may be deprecated in future versions.
     */
    public enum Rank{
        TWO ('2',0), THREE ('3',1), FOUR ('4',2), FIVE ('5',3), SIX ('6',4), SEVEN ('7',5), EIGHT ('8',6), NINE ('9',7), TEN ('T',8), JACK ('J',9), QUEEN ('Q',10), KING ('K',11), ACE ('A',12);
        public char representation;
        public int index;
        Rank(char representation, int index){
            this.representation = representation;
            this.index = index;
        }
        
        /**
         * A one character string representation.
         * 2-9,T,J,Q,K
         */
        public String toString(){
          return ""+representation;
        }
        
        /**
         * toRank is implemented in a slow fashion: could be optimized.
         * returns 0-12
         */
        public static Rank toRank(char c){
            for(Rank r:values()){
                if (r.representation==c){
                    return r;
                }
            }
            throw new RuntimeException("Did not find rank of card.");
        }
    }
    
    /**
     * An enumeration class for Suit.
     * It is unclear if there is a significant gain from this, and it may be deprecated in future versions.
     */
    public enum Suit{
        CLUBS('c',0), DIAMONDS('d',1), HEARTS('h',2), SPADES('s',3);
        public char representation;
        public int index;
        Suit(char representation, int index){
            this.representation = representation;
            this.index = index;
        }
        public String toString(){
          return ""+representation;
        }
        public static Suit toSuit(char c){
            for(Suit s:values()){
                if (s.representation==c){
                    return s;
                }
            }
            throw new RuntimeException("Did not find suit of card.");
        }
    }
    public Rank rank;
    public Suit suit;
    /** Creates a new instance of Card */
    public Card(Rank rank, Suit suit) {
        this.rank = rank;
        this.suit = suit;
    }
    
    /**
     * Initializes a card from a rank/suit card string.
     */
    public Card(String cardString){
        rank = Rank.toRank(cardString.charAt(0));
        suit = Suit.toSuit(cardString.charAt(1));
    }
    
    /**
     * Converts a string of cards to a card array
     */
    public static Card[] toCardArray(String cards){
        Card[] result = new Card[cards.length()/2];
        int index=0;
        for(int i=0;i<cards.length();i+=2,index++){
            result[index]=new Card(cards.substring(i,i+2));
        }
        return result;
    }
    
    public static Card[] getAllCards(){
        Card[] deck = new Card[52];
        int index = 0;
        for(Rank currentRank: Rank.values()){
            for(Suit currentSuit: Suit.values()){
              deck[index++]=new Card(currentRank,currentSuit);
            }
        }
        return deck;
    }
    /** Deals a certain number of cards into an array. */
    public static Card[] dealNewArray(SecureRandom random, int numCardsToDeal){
        Card[] deck = getAllCards();
        
        for(int i=0;i<numCardsToDeal;i++){
            int toSwap = random.nextInt(52-i)+i;
            Card temp = deck[i];
            deck[i] = deck[toSwap];
            deck[toSwap] = temp;
        }
        Card[] result = new Card[numCardsToDeal];
        for(int i=0;i<numCardsToDeal;i++){
            result[i]=deck[i];
        }
        return result;
    }
    
    /**
     * Returns a string with the rank and suit.
     */
    public String toString(){
        return "" + rank + suit;
    }
    
    public boolean equals(Object other){
    	if (other instanceof Card){
    		Card otherCard = (Card)other;
    		return otherCard.rank==rank && otherCard.suit==suit;
    	}
    	return false;
    }
}
