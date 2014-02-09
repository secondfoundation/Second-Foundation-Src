package glassfrog.model;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Random;

/**
 * A Class given to represent a standard 52 card, 4 suit deck of playing cards.
 * @author jdavidso
 */
public class Deck implements Serializable{

    private static final int DECK_SHUFFLE = 52;
    private static final int NUM_SUITS = 4;
    private static final int NUM_RANKS = 13;
    private static final String[] suits = {"Spades", "Hearts", "Clubs", "Diamonds"};
    private static final Integer[] ranks = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13};
    private Random rng;
    private int numUsedCards;
    private int usedIndex;
    private ArrayList<Card> deck;
    
    /**
     * Return a card at a given index in the deck
     * @param cardIndex The index from which to draw the card
     * @return The Card in the current deck
     */
    public Card getCard(int cardIndex) {
        return deck.get(cardIndex % deck.size());
    }

    /**
     * Get the next unused Card in the deck. Incrementing the used index by 1.
     * Used for the deal function
     * @return The next card in the deck
     */
    public Card getNextCard() {
        return deck.get(usedIndex++);
    }

    /**
     * Construtor specifying a seed to set our RNG with.
     * The deck is then sonstructed as an array of 52 cards in order of suit/rank
     * @param seed An int used to seed the deck to create repeatable deals
     */
    public Deck(int seed) {
        usedIndex = 0;
        numUsedCards = 0;
        rng = new Random(seed);
        deck = new ArrayList<Card>();
        for (String suit : suits) {
            for (Integer rank : ranks) {
                deck.add(new Card(suit, rank));
            }
        }
    }

    /**
     * Shuffles the top N cards where N is the amount of cards that are needed
     * in order to draw a hand based on the information specified by the dealer.
     * Reset the usedIndex to 0 for drawing off the top.
     */
    public void shuffle() {
        usedIndex = 0;
        for (int i = 0; i < numUsedCards; i++) {
            int index = (rng.nextInt(NUM_SUITS * NUM_RANKS) + i) % (DECK_SHUFFLE - i);
            Card swap = deck.get(index);
            deck.remove(swap);
            deck.add(i, swap);
        }
    }

    /**
     * Returns the deck, in array indexed order.
     * @return A string representing the cards in the deck, newline delimited.
     */
    @Override
    public String toString() {
        String retString = "";
        for (Card c : deck) {
            retString += c.toString() + "\n";
        }
        return retString;
    }

    /**
     * Deals a new hand from the deck.  This method takes in the parameters needed
     * to create a new hand from a shuffled deck.  It deals the cards using the 
     * following algorithm:
     * 
     * calculate number of cards needed to shuffle
     * shuffle
     * For each round:
     *   For each player:
     *     add to privateCards[player][round] number of private cards for this round
     *   add to publicCards[round] number of public cards for this round
     * 
     * Essentially for each round, deal each player the cards they need then deal 
     * the board cards
     * 
     * @param numPlayers An integer representing the number of players
     * @param numRounds An integer representing the number of rounds
     * @param numPrivateCards An array of integers where the index is the round 
     * and the value is the number of private cards for each player for that round
     * @param numPublicCards An array of integers where the index is the round 
     * and the value is the number of public cards for that round
     * @return A Hand object representing all of the card information to play a 
     * hand of poker
     */
    public Hand dealHand(int numPlayers, int numRounds, int[] numPrivateCards,
            int[] numPublicCards) {

        Hand newHand = new Hand(numPlayers, numRounds, numPrivateCards, numPublicCards);
        ArrayList<Card>[][] privateCards = new ArrayList[numPlayers][numRounds];
        ArrayList<Card>[] publicCards = new ArrayList[numRounds];
        numUsedCards = 0;

        for (int i = 0; i < numRounds; i++) {
            numUsedCards += numPlayers * numPrivateCards[i] + numPublicCards[i];
        }

        shuffle();
        for (int round = 0; round < numRounds; round++) {
            for (int player = 0; player < numPlayers; player++) {
                privateCards[player][round] = new ArrayList<Card>();
                for (int cardIndex = 0; cardIndex < numPrivateCards[round]; cardIndex++) {
                    privateCards[player][round].add(getNextCard());
                }
            }
            publicCards[round] = new ArrayList<Card>();
            for (int cardIndex = 0; cardIndex < numPublicCards[round]; cardIndex++) {
                publicCards[round].add(getNextCard());
            }
        }

        newHand.setPrivateCards(privateCards);
        newHand.setPublicCards(publicCards);

        return newHand;
    }
}
