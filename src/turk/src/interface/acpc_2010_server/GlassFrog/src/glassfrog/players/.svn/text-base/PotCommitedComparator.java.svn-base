package glassfrog.players;

import java.util.Comparator;

/**
 * The PotCommitedComparator is used to get the least amout a player in a showdown
 * commited to the pot.  This allows us to calculate sidepots and pay winners in
 * an iterative fashion.
 * @author jdavidso
 */
public class PotCommitedComparator implements Comparator<Player>{

    /**
     * Used to sort players by thier total commited to pot, lowest to highest
     * @param o1 Player 1
     * @param o2 Player 2
     * @return 0 if Player 1 equals Player 2, Positive if Player 1 commited more
     * than player 2 and Negative if Player 1 commited less
     */    
    public int compare(Player o1, Player o2) {
        return o1.getTotalCommitedToPot() - o2.getTotalCommitedToPot();
    }

}
