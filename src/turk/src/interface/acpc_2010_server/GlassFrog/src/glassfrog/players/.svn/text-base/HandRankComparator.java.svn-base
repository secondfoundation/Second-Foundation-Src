package glassfrog.players;

import java.util.Comparator;

/**
 * The HandRankComparator is used to rank the players based on their current hand
 * rank, set by the dealer evaluation of thier hands at showdown. The higher the 
 * hand rank, the better the hand.  Folds are given a rank of -1
 * @author jdavidso
 */
public class HandRankComparator implements Comparator<Player>{

    /**
     * Used to sort players by hand rank, The higher the rank, the better the hand
     * @param o1 Player 1
     * @param o2 Player 2
     * @return 0 for a tie, Positive if Player 2 has a higher rank and Negative
     * if Player 1 has a higher rank.
     */    
    public int compare(Player o1, Player o2) {
        return o2.getHandRank() - o1.getHandRank();
    }   

}
