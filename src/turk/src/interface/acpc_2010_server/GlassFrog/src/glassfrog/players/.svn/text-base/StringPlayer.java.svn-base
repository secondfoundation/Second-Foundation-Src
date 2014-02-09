package glassfrog.players;

import java.util.StringTokenizer;

/**
 * A Player used for testing purposes that takes an action string "|" delimited 
 * and will play those actions until the string has run out, then it will play 
 * the default action of call
 * 
 * @author jdavidso
 */
public class StringPlayer extends Player{
    transient private String actionString;
    transient private StringTokenizer actionTok;
    transient private boolean repeatAction = false;
    transient private String action;
   
    /**
     * Constructor for a StringPlayer.  The constructor takes a name, a buyIn amount
     * a seat and an actionString. The action string is a series of actions that
     * the player will take delimited by "|" .  A special case of this is the single
     * character string, which can be used to creat an "always X" player where X is 
     * one of {f,c,r, rN}.  Once a player runs out of actions and if it is on the 
     * special case, action c will be returned
     * 
     * @param name String representing the player name
     * @param buyIn int representing the buyIn amount
     * @param seat int representing the seat the player is in.
     * @param actionString A "|" delimited string that represents players action    
     * 
     */
    public StringPlayer(String name, int buyIn, int seat, String actionString) {
        super(name,buyIn);
        this.actionString = actionString;
        if(actionString.length() == 1) {
            repeatAction = true;
            action = actionString;
        }
        actionTok = new StringTokenizer(actionString,"|");
    }
    
    /**
     * Returns the next action in the string given by the tokenizer, default action c
     * @return The next action for the player to take
     *
     */
    @Override
    public String getAction() {
        if(!repeatAction) {                    
            if(actionTok.hasMoreTokens()) {
                action = actionTok.nextToken();
            } else {
                action = "c";
            }
        }
        return action;
    }

    /**
     * Do nothing
     * @param gamestate a String reprenting the gamestate
     */
    @Override
    public void update(String gamestate) {       
    }

    /**
     * Do nothing
     */
    @Override
    public void shutdown() {        
    }
    
    /**
     * Appends String to the @Player toString method
     * @return "String" appended to the toString method of @Player
     */
    @Override
    public String toString() {
        return "String"+super.toString();
    }
    

}
