package ca.ualberta.cs.poker.free.tournament;

/* interface for handling the nodes in the tournament tree
 * implementors include Competitors and Series
 */

import java.security.SecureRandom;
import java.util.Vector;

public interface Node {

        /** Test if all of the matches for this node have been
	 * completed.
	 */
	boolean isComplete();

	/**
	 * Load any new matches into the forge.
	 */
	void load (Forge w);

	/**
	 * Get the winner of this node.
	 */
	Vector<BotInterface> getWinners();

	/**
	 * Generate the card files for this node.
	 */
	void generateCardFiles(SecureRandom random);

	/**
	 * Show the statistics from the tournament
	 */
        void showStatistics();
}

