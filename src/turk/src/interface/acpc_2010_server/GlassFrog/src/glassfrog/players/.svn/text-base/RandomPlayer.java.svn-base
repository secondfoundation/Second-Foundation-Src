package glassfrog.players;

import java.security.SecureRandom;
import java.util.Random;
import java.util.StringTokenizer;

/**
 * An Abstract class used to define some specific properties about Random Players
 * such as thier RNG and thier fold call and raise weights.
 * 
 * This class is extended from the Player class
 * @author jdavidso
 */
public abstract class RandomPlayer extends Player{

    transient private int seed;   
    /**
     * A Random to generate actions
     */
    transient protected Random rng;
    /**
     * Wieght of the fold action in the random distribution
     */
    transient protected int foldWeight = 1;
    /**
     * Wieght of the call action in the random distribution
     */
    transient protected int callWeight = 1;
    /**
     * Wieght of the raise action in the random distribution
     */
    transient protected int raiseWeight = 1;
    
    /**
     * A constructor for Random Player that takes a seed to seed the action RNG with
     * 
     * @param name String representing the player name
     * @param buyIn int representing the buy in amount
     * @param seed an int to seed the rng
     */
    public RandomPlayer(String name, int buyIn, int seed) {
        super(name,buyIn);
        this.seed = seed;
        rng = new Random(seed);
    }
    
    /**
     * A constructor for Random Plauer that takes a string for the action weights
     * 
     * @param name String representing the player name
     * @param buyIn int representing the buy in amount
     * @param weights A String representing the f,c,r weights ("1,1,1") being uniform
     */
    public RandomPlayer(String name, int buyIn, String weights) {
        super(name,buyIn);
        seed = new SecureRandom().nextInt();
        rng = new Random(seed);
        calculateWeights(weights);
    }
    
    /**
     * A generic Random Player that has a random seed and uniform action weights
     * 
     * @param name String representing the player name
     * @param buyIn int representing the buy in amount
     */
    public RandomPlayer(String name, int buyIn) {
        super(name,buyIn);
        seed = new SecureRandom().nextInt();
        rng = new Random(seed);
    }        

    /**
     * This method assumes the weightString is correct with 3 weights, each comma
     * delimited and corrisponding to f,c,r actions
     * 
     * @param weightString A comma delimited string representing action weights
     */
    private void calculateWeights(String weightString) {
        StringTokenizer st = new StringTokenizer(weightString, ",");
        foldWeight = new Integer(st.nextToken()).intValue();
        callWeight = new Integer(st.nextToken()).intValue();
        raiseWeight = new Integer(st.nextToken()).intValue();
    }
    
    /**
     * Do nothing on update
     * @param gamestate the gamestate string
     */
    @Override
    public void update(String gamestate) {
        
    }
    
    /**
     * Do nothing on shutdown.
     */
    @Override
    public void shutdown() {
    }
}
