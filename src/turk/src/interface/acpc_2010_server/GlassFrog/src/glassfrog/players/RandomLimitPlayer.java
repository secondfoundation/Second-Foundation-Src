package glassfrog.players;

/**
 * The RandomLimitPlayer is an extention on the RandomPlayer.  It will choose
 * random actions {f,c,r} based on uniform distribution or a wieghted one.  A 
 * seed can also be specified to get repeatable performance from the rng
 * 
 * @author jdavidso
 */
public class RandomLimitPlayer extends RandomPlayer{            
    /**
     * Constructor for a Random Limit Player with a seed
     * @param name String representing the player name
     * @param buyIn int representing the buy in amount
     * @param seed an int to seed the rng
     */
    public RandomLimitPlayer(String name, int buyIn, int seed) {
        super(name,buyIn,seed);
    }
    
    /**
     * Constructor for a Random Limit Player with weighted values for the actions
     * @param name String representing the player name
     * @param buyIn int representing the buy in amount
     * @param weights A String representing the f,c,r weights ("1,1,1") being uniform
     */
    public RandomLimitPlayer(String name, int buyIn, String weights) {
        super(name,buyIn,weights);
    }
    
    /**
     * Constructor for a general purpose Random Limit player (random seed, uniform actions)
     * @param name String representing the player name
     * @param buyIn int representing the buy in amount
     */
    public RandomLimitPlayer(String name, int buyIn) {
        super(name,buyIn);
    }

    
    /**
     * Return a Random action from either Fold Call or Raise based on the wieghting
     * array given
     * @return An action of Fold Call or Raise {f,c,r}
     */
    @Override
    public String getAction() {
        int weightSum = foldWeight + callWeight + raiseWeight;
        int sample = rng.nextInt(weightSum) + 1;
        if(sample <= foldWeight) {
            return "f";                
        } else if (sample > foldWeight && sample <= foldWeight+callWeight) {
            return "c";                
        } else {            
            return "r";
        }
    }    
    
    /**
     * Append RandomLimit identifier to the @Player toString method
     * @return "RandomLimit"+the @Player toString method
     */
    @Override
    public String toString() {
        return "RandomLimit"+super.toString();
    }

}
