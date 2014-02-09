package glassfrog.players;

import java.util.StringTokenizer;

/**
 * The RandomNoLimit player class is a version of the RandomPlayer for NoLimit
 * Texas Holdem
 * 
 * The Player will perform a random action based on a seed, a random seed or a 
 * string of weights ("1,1,1") being the uniform weighted string for f,c,r.  A
 * raise value will be random number between the players min bet and their stacksize
 * 
 * This extends the RandomPlayer class
 * @author jdavidso
 */
public class RandomNoLimitPlayer extends RandomPlayer{        
    
    private int minBet = 0;    
    
    /**
     * Constructor for a Random No Limit Player with a seed
     * @param name String representing the player name
     * @param buyIn int representing the buy in amount
     * @param seed an int to seed the rng
     */
    public RandomNoLimitPlayer(String name, int buyIn, int seed) {
        super(name,buyIn);
    }
    
    /**
     * Constructor for a Random No Limit Player with weighted values for the actions
     * @param name String representing the player name
     * @param buyIn int representing the buy in amount
     * @param weights A String representing the f,c,r weights ("1,1,1") being uniform
     */
    public RandomNoLimitPlayer(String name, int buyIn, String weights) {
        super(name,buyIn,weights);
    }
    
    /**
     * Constructor for a general purpose Random No Limit player (random seed, uniform actions)
     * @param name String representing the player name
     * @param buyIn int representing the buy in amount
     */
    public RandomNoLimitPlayer(String name, int buyIn) {
        super(name,buyIn);
    }
    
    /**
     * Using a wieghted sum and an random number, generate the next action for the
     * bot to take.  If the action is a raise, then get a random bet amount between
     * the min bet and the stacksize
     * @return The action to send to the dealer
     */
    @Override
    public String getAction() {
        int weightSum = foldWeight + callWeight + raiseWeight;
        int sample = rng.nextInt(weightSum);
        if(sample <= foldWeight) {
            return "f";                
        } else if (sample > foldWeight && sample <= foldWeight+callWeight) {
            return "c";                
        } else {
            int betValue;
            if(this.getStack() <= minBet) {
                betValue = this.getStack();
            } else {
                betValue = minBet + rng.nextInt(this.getStack()-minBet);                    
            }
            return "r"+betValue;
        }                 
    }
    
    /**
     * Update the players information based on the gamestate String.  In this 
     * player, the min bet is calculated from the last raise made, the last 
     * blind made or just return 1;
     * @param gamestate The AAAI formated gamestate String
     */
    @Override
    public void update(String gamestate) {        
        StringTokenizer st = new StringTokenizer(gamestate,":");
        String token;
        //Get the betting string;
        do {
            token = st.nextToken();
        }while(!token.substring(0,1).equalsIgnoreCase("b"));
        
        int lastRaisePos = token.lastIndexOf("r");
        if(lastRaisePos < 0) {
            lastRaisePos = token.lastIndexOf("b");
        }
        
        if(lastRaisePos < 0) {
            minBet = 1;
            return;
        }
        
        int nextCall = token.indexOf("c", lastRaisePos);
        int nextFold = token.indexOf("f", lastRaisePos);
        
        nextCall = (nextCall < 0 ? 0 : nextCall);
        nextFold = (nextFold < 0 ? 0 : nextFold);
        
        int lastRaise = new Integer( (nextCall < nextFold ? 
            token.substring(lastRaisePos, nextCall) : 
            token.substring(lastRaisePos, nextFold))).intValue();
        
        minBet = lastRaise*2;
        
    }    
    
    /**
     * Append RandomNoLimit identifier to the @Player toString method
     * @return "RandomNoLimit"+the @Player toString method
     */
    @Override
    public String toString() {
        return "RandomNoLimit"+super.toString();
    }

}
