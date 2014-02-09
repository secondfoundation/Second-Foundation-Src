package glassfrog.model;

import glassfrog.players.HandRankComparator;
import glassfrog.players.Player;
import glassfrog.players.PositionComparator;
import glassfrog.players.PotCommitedComparator;
import glassfrog.handevaluator.EvaluateHand;
import glassfrog.handevaluator.HandEvaluator;
import glassfrog.players.AAAIPlayer;
import glassfrog.players.SeatComparator;
import glassfrog.players.SocketPlayer;
import glassfrog.tools.XMLParser;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.net.SocketTimeoutException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.PrintWriter;
import java.io.Serializable;
import java.util.Collections;
import java.util.Date;
import java.util.LinkedList;
import java.util.NoSuchElementException;
import java.util.StringTokenizer;
import javax.xml.parsers.ParserConfigurationException;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;
import org.xml.sax.SAXParseException;

/**
 * The Dealer class will handle all of the methods of dealing cards, evaluating
 * hands, pots, and betting actions. There should be one Dealer per Room, and
 * each dealer is assigned a list of Players and a Gamedef to which they will 
 * use to play.
 * 
 * Dealers may also be assigned a Room in which they can report game outcomes and
 * similar information.  The Room may also be used to handle the player requests
 * and actions, although I am not sure that will be the case
 * @author jdavidso
 */
public class Dealer implements Runnable, Serializable {

    private Gamedef gamedef;
    private Gamestate gamestate;
    private Hand currentHand;
    private LinkedList<Player> players;
    private Deck deck;
    private int currentPlayer;
    private int handsPlayed;
    private int numHands;
    private String lastAction, name;
    private boolean gameOver = false;
    private boolean hasReported = false;
    private boolean error = false;
    private boolean shuffle = true;
    private transient BufferedWriter errorLogWriter, matchLogWriter,  divatLogWriter,  summaryLogWriter;
    private boolean disconnected = false;
    private static String DEFAULT_ACTION = "c";
    private static int PLAYER_ACTION_TIMEOUT = 1000000;
    private static int PLAYER_AVG_TIME_PER_HAND = 0;
    private static int ACTION_DELAY = 0;

    /**
     * 
     * @param name A String to represent the name of the game for the log file
     * @param numHands the number of hands of which the dealer will play
     * @param gamedef The @Gamedef that will be used to play
     * @param seed An integer representing the seed in which to seed the deck RNG
     * @param players A list of Players that will be seated in the game.     
     */
    public Dealer(String name, int numHands, Gamedef gamedef, int seed, LinkedList<Player> players) {
        this.name = name;
        this.numHands = numHands;
        this.gamedef = gamedef;
        deck = new Deck(seed);
        this.players = players;
        handsPlayed = 0;
        for (Player p : players) {
            p.setPosition(p.getSeat());
        }        
    }

    /**
     * Set the players of the game.  Used by the room to set the players up.
     * @param players LinkedList containing player objects for the game
     * @return True for successful reconnect
     */
    public boolean reconnectPlayers(LinkedList<Player> players) {
        for (Player p : this.players) {
            if (p.isSocketPlayer()) {
                for (Player p1 : players) {
                    if (p1.isSocketPlayer()) {
                        if (p.getName().equalsIgnoreCase(p1.getName())) {
                            try {
                                ((SocketPlayer) p).reconnect(((SocketPlayer) p1).getSocket());
                            } catch (IOException ex) {
                                logError(ex);
                                return false;
                            } catch (NullPointerException ex) {
                                logError(ex);
                                return false;
                            }
                        }
                    }
                }
            } else if (p.isAAAIPlayer()) {
                for (Player p1 : players) {
                    if (p1.isAAAIPlayer()) {
                        if (p.getName().equalsIgnoreCase(p1.getName())) {
                            try {
                                ((AAAIPlayer) p).reconnect(((AAAIPlayer) p1).getSocket(), ((AAAIPlayer) p1).getLocation(), ((AAAIPlayer) p1).getScriptPath());
                            } catch (IOException ex) {
                                logError(ex);
                                return false;
                            } catch (NullPointerException ex) {
                                logError(ex);
                                return false;
                            }
                        }
                    }
                }
            }
        }
        return true;
    }

    /**
     * Initialize the logs for the game.
     * The logname will be of the form roomname_timestamp.(log || .err) where 
     * roomname is the name passed from the server to the room and the timestamp      
     */
    private void initLogging() {
        String logPath = "logs/";
        if (name == null) {
            name = "";
            for (Player p : players) {
                name += p.getName() + ":";
            }
            name = name.substring(0, name.length() - 1);
        } try{
            errorLogWriter = new BufferedWriter( new FileWriter(logPath + name + ".dealer.err", true) );
            matchLogWriter = new BufferedWriter( new FileWriter(logPath + name + ".dealer.log", true) );
            divatLogWriter = new BufferedWriter( new FileWriter(logPath + name + ".dealer.divat", true) );
            summaryLogWriter = new BufferedWriter( new FileWriter(logPath + name + ".dealer.summary", true) );
        } catch (IOException ex) {
            System.err.println("Could not initialize dealer logs for " + name + ", exit with IO Error " + ex.toString());
        } catch (SecurityException ex) {
            System.err.println("Could not initialize dealer logs for " + name + ", exit with Security Error " + ex.toString());
        }
    }

    /**
     * Utility for logging an error message to the errorLogger
     * @param ex An exception to log
     */
    public void logError(Exception ex) {
        try {
            errorLogWriter.write(new Date().toString() + " : ");
            ex.printStackTrace(new PrintWriter(errorLogWriter));
        } catch (IOException ex1) {
            System.err.println("Dealer Logging Error: ");
            ex1.printStackTrace();
        }
    }

    /**
     * Utility for logging a warning message to the errorLogger
     * @param warningMessage A message to log to the error log
     */
    public void logWarning(String warningMessage) {
        try {
            errorLogWriter.write(new Date().toString() + " : ");
            errorLogWriter.write("WARNING: "+warningMessage);
            errorLogWriter.newLine();
        } catch (IOException ex) {
            logError(ex);
        }
    }

    /**
     * Log a gamesate to the matchlogger
     * @param matchstate the gamestate message to log to the match log 
     */
    public void logState(String matchstate) {
        try {
            //matchLogWriter.write(new Date().toString());
            //matchLogWriter.flush();
            matchLogWriter.write(matchstate);
            matchLogWriter.newLine();
        } catch (IOException ex) {
            logError(ex);
        }
    }

    /**
     * Log the game stats
     */
    private void logStats() {
        String stats = "";
        stats += "STATS:Current Player:" + currentPlayer + ":Hands Played:" + handsPlayed + "\n";
        for (Player p : players) {
            stats += p.toString() + "\n";
        }
        logState(stats);
    }

    /** 
     * Log a divat readable gamestate into a divat log.  Note: Only implemented for 
     * heads up 2 player.
     * 
     * @param value The value of the game for the first player
     */
    private void logDivat() {
        String divatLine = handsPlayed + ":";
        for (Player p : players) {
            divatLine += p.getName() + ",";
        }
        divatLine = divatLine.substring(0, divatLine.length() - 1);
        divatLine += ":" + 0;
        divatLine += gamestate.getActionString() + ":";
        for (int r = 0; r <= gamestate.getRound(); r++) {
            String privateCards = "";
            for (Player p : players) {
                privateCards = currentHand.getPrivateCardsString(p.getPosition(), r);
                if (privateCards.length() != 0) {
                    divatLine += privateCards + ",";
                }
            }
            if (privateCards.length() != 0) {
                divatLine = divatLine.substring(0, divatLine.length() - 1);
                divatLine += "|";
            }
            String publicCards = currentHand.getPublicCardsString(r);
            if (publicCards.length() != 0) {
                divatLine += "/" + publicCards;
            }
        }
        divatLine += ":";
        for (Player p : players) {
            divatLine += p.getStack() - p.getBuyIn() + ",";
        }
        divatLine = divatLine.substring(0, divatLine.length() - 1);
        try {
            divatLogWriter.write(divatLine);
            divatLogWriter.newLine();
        } catch (IOException ex) {
            logError(ex);
        }
    }

    private void logSummary() {
        String summary = "";
        for (Player p : players) {
            summary += p.getName() + "|";
        }
        summary = summary.substring(0, summary.length() - 1) + ":";
        summary += handsPlayed + ":";
        summary += gamestate.getActionString() + ":";
        for (int r = 0; r <= gamestate.getRound(); r++) {
            String privateCards = "";
            for (Player p : players) {
                privateCards = currentHand.getPrivateCardsString(p.getPosition(), r);
                if (privateCards.length() != 0) {
                    summary += privateCards + "|";
                }
            }
            if (privateCards.length() != 0) {
                summary = summary.substring(0, summary.length() - 1);
            }
            String publicCards = currentHand.getPublicCardsString(r);
            if (publicCards.length() != 0) {
                summary += "/" + publicCards;
            }
        }
        summary += ":";
        for (Player p : players) {
            summary += p.getStack() - p.getBuyIn() + "|";
        }
        summary = summary.substring(0, summary.length() - 1);
        try {
            summaryLogWriter.write(summary);
            summaryLogWriter.newLine();
        } catch (IOException ex) {
            logError(ex);
        }
    }

    /**
     * Deal will deal a game until the Gamedef.gameOver is true.  This allows
     * for any number of options to be specified to the Gamedef to allow for 
     * different game ending situations (bankroll, handscount, forever).
     * 
     * The deal function follows the following algorithm:
     * While not gameover:
     *   generate a new hand for the players
     *   generate a new gamestate
     *   play hand
     * 
     * The gamestate here refers to the game properties such as potsize, folded
     * players, etc.
     * 
     */
    public void deal() {
        initLogging();
        try {
            loadSettings();
        } catch (ParserConfigurationException ex) {
            logError(ex);
        } catch (SAXParseException ex) {
            logError(ex);
        } catch (SAXException ex) {
            logError(ex);
        } catch (IOException ex) {
            logError(ex);
        } catch (InterruptedException ex) {
            logError(ex);
        }
        sendPlayerInfos();
        for (Player p : players) {
            if (p.isAAAIPlayer() || p.isGuiPlayer() || p.isSocketPlayer()) {
                p.setActionTimeout(PLAYER_ACTION_TIMEOUT);
                p.setMatchTimeout(PLAYER_AVG_TIME_PER_HAND * numHands);
            }
        }
        while (!gameOver && !disconnected) {
            //Initialize the winners, gamestate, and get a new hand
            gamestate = new Gamestate(gamedef);
            gamestate.setButton(players.size() - 1);
            for (Player p : players) {
                p.resetPlayer(gamedef.isDoylesGame());
            }
            Collections.sort(players, new PositionComparator());
            //Used to check specific hands that can be pre set
            if (shuffle) {
                currentHand = deck.dealHand(players.size(), gamedef.getNumRounds(),
                        gamedef.getNumPrivateCards(), gamedef.getNumPublicCards());
            } else {
                shuffle = true;
            }
            logState(currentHand.toString());
            playHand();
            if (shuffle) {
                logStats();
            }
            if (handsPlayed >= numHands) {
                gameOver = true;
            }
        }
        if (gameOver) {
            String gameOverString = "#GAMEOVER";
            for (Player p : players) {
                p.resetPlayer(gamedef.isDoylesGame());
                p.update(gameOverString);
            }
        }
        while (!hasReported) {
            try {
                Thread.sleep(5000);
            } catch (InterruptedException ex) {
                logError(ex);
            }
        }
        shutdownLogging();
    }

    /**
     * Close the log files
     */
    private void shutdownLogging() {
        try {
            errorLogWriter.close();
            matchLogWriter.close();
            summaryLogWriter.close();
            divatLogWriter.close();
        } catch (IOException ex) {
            System.err.println("Error closing logfiles: "+ex.toString());
        }
    }

    /**
     * Send the gui players the player info for correct display.
     */
    private void sendPlayerInfos() {
        String playerInfos = "#PLAYERS";
        LinkedList<Player> seatSorted = players;
        Collections.sort(seatSorted, new SeatComparator());
        for (Player p : seatSorted) {
            playerInfos += "||" + p.toShortString();
        }

        for (Player p : players) {
            if (p.isGuiPlayer()) {
                p.update(playerInfos);
            }
        }
    }

    /**
     * Only used for test purposed, this is a method to create a specific hand
     * @param testHand
     */
    public void setCurrentHand(Hand testHand) {
        shuffle = false;
        currentHand = testHand;
    }

    /**
     * Plays a single hand of poker.
     */
    private void playHand() {
        do {
            playRound();
            if (gamestate.getRound() >= gamedef.getNumRounds() - 1) {
                gamestate.setHandOver(true);
            } else if (!isHandOver()) {
                nextRound();
            }
        } while (!gamestate.isHandOver());
        //updatePlayers();
        if (shuffle) {
            evaluateHand();
            handsPlayed++;
            for (Player p : players) {
                p.setPosition((p.getPosition() + 1) % players.size());
            }
        }
    }

    /**
     * This function follows the following algorithm:
     *  while(!roundOver):
     *    get next player to act
     *    send gamestate to player
     *    wait for action from player or timeout
     *    update gamestate
     * 
     * This essentially plays one round of poker, gets the actions from all
     * the players and keeps an up to date gamestate information.
     */
    private void playRound() {
        currentPlayer = gamestate.getButton();

        //Post blind in round 0
        if (gamestate.getRound() == 0) {
            postBlinds();
        }
        while (!isRoundOver()) {
            updatePlayers();
            Player p = getNextPlayer();
            String response = "";
            try {
                do{
                  response = p.getAction();
                  lastAction = parseAction(response);
                } while( lastAction == null );
            } catch (SocketTimeoutException ste) {
                logError(ste);
                gamestate.setHandOver(true);
                lastAction = "f";
                handleDisconnect();
            } catch (NoSuchElementException ex) {
                logWarning("Player "+p.getName()+"  sent invalid response [" +
                           response + "] to server on hand " + handsPlayed + 
                           ", using default action:" + DEFAULT_ACTION);
                lastAction = DEFAULT_ACTION;
            } catch (NullPointerException ex) {
                gamestate.setHandOver(true);
                lastAction = "f";
                handleDisconnect();
            }
            updateGamestate();
            if (gamestate.isHandOver()) {
                return;
            }
        }
    }

    /**
     * On a disconnect, for now we are going to do a few things.
     * First we are going to end the hand in a fold for the disconnected player
     * Second, we are going to stop the match and set a flag for the Room to pickup.
     * This will allow the room to serialize the dealer object to file, and when 
     * we reload, we will grab the dealer object, load it in and continue from the
     * very next hand.
     */
    private void handleDisconnect() {
        disconnected = true;
        int idlePlayers = players.size();
        for (Player p : players) {
            if (p.isActed()) {
                idlePlayers--;
            }
        }
        if (idlePlayers > 0 && gamestate.getRound() == 0) {
            shuffle = false;
        }
    }

    /**
     * Update the game to the next round.  Reset players current bets and action
     * flags
     */
    private void nextRound() {
        for (Player p : players) {
            p.resetRound();
        }
        gamestate.nextRound();
    }

    /**
     * This posts the "antes" or blinds for the game.  Assumes that after the
     * blinds are posted, the action falls to the next player at the table.
     */
    // XXX: No test to see if blinds put you all-in.  This is a problem for
    // non-Doyle's games
    private void postBlinds() {
        if (gamedef.isReverseBlinds() && players.size() == 2) {
            currentPlayer = 0;
        }
        for (int i = 0; i < gamedef.getBlindStructure().length; i++) {
            Player p = getNextPlayer();
            int betValue = gamedef.getBlind(i);
            p.postBlind(betValue);
            gamestate.makeBet(betValue, 0);
            //No Limit Betting
            if (gamedef.isNoLimit()) {
                gamestate.addToActionString("b" + betValue);
            }
        }
        // XXX: Terrible hack to get the minimum bet after blinds set correctly for
        // heads-up no-limit.  The minBet (as it is currently used) should be
        // set to the minimum raise plus the next player to act's amount to
        // call.  This is hardcoded to assume the player who posted the 0th
        // blind above is the next to act.  This will not work with more than 2
        // players.  Furthermore, since postBlind doesn't check if the player
        // has enough chips for the blind, the amount to call could be wrong.
        gamestate.setMinBet( (gamedef.getBlind(1) - gamedef.getBlind(0)) + gamedef.getMinBet() );
        gamestate.setNumBets(0);
    }

    /**
     * Increments the currentPlayer index to the next player and returns that 
     * index.
     * @return An integer index to the next player in the list of players % size
     */
    private int nextPlayer() {
        currentPlayer = (currentPlayer + 1) % players.size();
        return currentPlayer;
    }

    /**
     * This function returns the next active player.  That is, the next player
     * that hasn't folded or isn't all in or the player we started at (That player
     * must have went all in and everybody else folded) Probably shouldn't be 
     * able to occur.
     * @return The next active player
     */
    private Player getNextPlayer() {
        Player p;
        int count = 0;
        do {
            p = players.get(nextPlayer());
            count++;
        } while (p.isFolded() || p.isAllIn() || count >= players.size());
        return p;
    }

    /**
     * Check to see if the round is over according to the rules of the game
     * For this to be satisfied, all the players must now be unable to act.
     * We are going to refactor these checks out and see if a player "can act"
     *  
     * @return Whether or not the round is over.
     */
    private boolean isRoundOver() {
        int activePlayers = players.size();
        for (Player p : players) {
            if (p.isFolded()) {
                //Remove folded players from active players                           
                activePlayers--;
            } else if (p.isAllIn()) {
                //Remove all in players from active players            
                activePlayers--;
            } else if (p.getCurrentBet() >= gamestate.getCurrentBet() && p.isActed()) {
                //Remove calls or raises            
                activePlayers--;
            }
        }
        return (activePlayers <= 0);
    }

    /**
     * Update the current gamestate.  This will update the game based on the 
     * action that was taken by the player and set important things like
     * is the hand or round over etc, etc.
     */
    private void updateGamestate() {
        Player p = players.get(currentPlayer);
        int currentBet = gamestate.getCurrentBet();
        int playerBet = p.getCurrentBet();

        switch (lastAction.toLowerCase().charAt(0)) {
            case 'f':
                //fold case
                p.fold();
                gamestate.addToActionString("f");
                break;
            case 'c':
                //call case
                gamestate.makeBet(p.call(currentBet), playerBet);
                gamestate.addToActionString("c");
                if (gamedef.isNoLimit()) {
                    gamestate.addToActionString("" + currentBet);
                }
                break;
            case 'r':
                //raise case
                int raise = 0;
                int playerStack = p.getStack();
                int minimumBet = gamestate.getMinBet();
                if (gamedef.isNoLimit()) {
                    if (!(lastAction.length() > 1)) {
                        logWarning("Player "+p.getName()+"  sent invalid action [" +
                                   lastAction + "] to server on hand " + handsPlayed + 
                                   ". Expected raise quantity, using default action:" + DEFAULT_ACTION);
                        lastAction = DEFAULT_ACTION;
                        updateGamestate();
                        return;
                    }
                    try {
                        raise = new Integer(lastAction.substring(1)).intValue() - playerBet;
                        if ( raise == playerStack || (raise < playerStack && raise >= minimumBet) ) {
                            // Do nothing, valid raise without modification
                        } else if ( raise > playerStack ) {
                            // Player bet more than they had.  Output warning
                            logWarning("Player "+p.getName()+"  sent raise exceeding stack [" +
                                       lastAction + "] to server on hand " + handsPlayed + 
                                       ", using all-in: r" + (playerStack+playerBet) );
                        } else if( minimumBet < playerStack ) {
                            // Player raised less than minimum, not all-in, and can make a minimum bet
                            raise = minimumBet;
                            logWarning("Player "+p.getName()+"  sent insufficient raise amount [" +
                                       lastAction + "] to server on hand " + handsPlayed + 
                                       ", using minimum raise: r" + (raise+playerBet) );
                        } else {
                            // Player raised less than minimum, not all-in, and cannot make a minimum bet
                            raise = minimumBet;
                            logWarning("Player "+p.getName()+"  sent insufficient raise amount [" +
                                       lastAction + "] to server on hand " + handsPlayed + 
                                       " and minimum exceeds stack, using all-in: r" + (playerStack+playerBet) );
                        }

                        // Note: if raise > playerStack, the player bet() will
                        // downsize the bet.  This should be done more clearly.
                        raise = p.bet(raise);
                        gamestate.makeBet(raise, playerBet);
                        gamestate.addToActionString("r" + (raise + playerBet));
                    } catch (NumberFormatException e) {
                        logError(e);
                        logWarning("Player "+p.getName()+"  sent invalid action [" +
                                   lastAction + "] to server on hand " + handsPlayed + 
                                   ", using default action:" + DEFAULT_ACTION);
                        lastAction = DEFAULT_ACTION;
                        updateGamestate();
                        return;
                    }
                } else {
                    if (lastAction.length() > 1) {
                        logWarning("Player "+p.getName()+"  sent invalid action [" +
                                   lastAction + "] to server on hand " + handsPlayed + 
                                   ", using default action:" + DEFAULT_ACTION);
                        lastAction = DEFAULT_ACTION;
                        updateGamestate();
                        return;
                    }
                    if (gamestate.getNumBets() >= gamedef.getBetsPerRound()[gamestate.getRound()]) {
                        lastAction = "c";
                        updateGamestate();
                        return;
                    }
                    raise = gamestate.getCurrentBet() + gamedef.getBet(gamestate.getRound()) - playerBet;
                    gamestate.makeBet(p.bet(raise), playerBet);
                    gamestate.addToActionString("r");
                }
                break;
            default:
                //Something broken, raise excepion
                logWarning("Player "+p.getName()+"  sent invalid action [" +
                                   lastAction + "] to server on hand " + handsPlayed + 
                                   ", using default action:" + DEFAULT_ACTION);
                lastAction = DEFAULT_ACTION;
                updateGamestate();
                return;
        }
        //Check to see if everyone has folded... then we can be hand over!
        gamestate.setHandOver(isHandOver());
    }

    /**
     * Check to see if everyone is all in or has folded (basically nobody can 
     * act anymore)
     * @return True if the hand is over and we should evaluate
     */
    private boolean isHandOver() {
        int foldCount = 0;
        int allInCount = 0;
        int callCount = 0;
        for (Player p : players) {
            if (p.isFolded()) {
                //First check the fold cases            
                foldCount++;
                if (foldCount == players.size() - 1) {
                    return true;
                }
            } else if (p.isAllIn()) {
                //All Ins            
                allInCount++;
            } else if (p.getCurrentBet() == gamestate.getCurrentBet()) {
                //One caller, everone else all in
                callCount++;
                if (callCount > 1) {
                    return false;
                }
            }
            if ((allInCount + callCount + foldCount) == players.size()) {
                // Everyone has either folded, went all in (except one caller)
                return true;
            }
        }
        return false;
    }

    /**
     * The evaluateHand function runs the routine for determining which players
     * won and how much each of them won.  First it will determine the rank of 
     * the players, rank 0 being the winner(s) followed by rank 1, rank 2, etc.
     * This is done for each sidepot, and we pay the money out of the potsize.
     * 
     */
    private void evaluateHand() {
        String cardString;
        LinkedList<Player> rankedPlayers = new LinkedList<Player>();
        LinkedList<Player> foldedPlayers = new LinkedList<Player>();
        HandEvaluator h = new HandEvaluator();

        //Assign Hand Ranks
        for (Player p : players) {
            cardString = currentHand.getEvaluationString(players.indexOf(p));
            if (!p.isFolded()) {
                p.setHandRank(HandEvaluator.rankHand(new EvaluateHand(cardString)));
                p.setHandString(HandEvaluator.nameHand(new EvaluateHand(cardString)));
                p.setCardString(h.getBest5CardHand(new EvaluateHand(cardString)).toString());
                rankedPlayers.add(p);
            } else {
                p.setHandRank(-1);
                foldedPlayers.add(p);
            }
        }

        int i = 0;
        while (gamestate.getPotsize() > 0) {
            i++;
            Collections.sort(rankedPlayers, new PotCommitedComparator());
            int minTotalCommited = rankedPlayers.get(0).getTotalCommitedToPot();
            Collections.sort(rankedPlayers, new HandRankComparator());

            LinkedList<Player> potWinners = new LinkedList<Player>();

            int maxRank = -1;
            for (Player p : rankedPlayers) {
                if (p.getHandRank() >= maxRank) {
                    maxRank = p.getHandRank();
                    potWinners.add(p);
                }
            }

            int payout = 0, remainder = 0;
            for (int j = 0; j < foldedPlayers.size(); j++) {
                Player p = foldedPlayers.get(j);
                if (p.getTotalCommitedToPot() > 0) {
                    if (p.getTotalCommitedToPot() <= minTotalCommited) {
                        payout += p.getTotalCommitedToPot();
                        foldedPlayers.remove(p);
                        j--;
                    } else {
                        payout += minTotalCommited;
                        p.subtractTotalCommitedToPot(minTotalCommited);
                    }
                }
            }

            //Still need to adjust what happens to the remainder chips in odd
            //pot sizes
            payout += rankedPlayers.size() * minTotalCommited;
            remainder = payout % potWinners.size();
            payout /= potWinners.size();

            gamestate.subtractFromPot(remainder);

            String showdownString = "";
            for (Player p : potWinners) {
                p.payout(payout);
                showdownString += p.getName() + " won " + payout;
                if (rankedPlayers.size() > 1) {
                    showdownString += " with hand " + p.getHandString() + "/" +
                            p.getCardString() + ":";
                }
                gamestate.subtractFromPot(payout);
            }

            //Let the players see the hand if there was a showdown
            if (rankedPlayers.size() > 1) {
                for (Player p : players) {
                    p.update(getShowdownGameState(p));
                    logState(getShowdownGameState(p));
                }
            } else {
              updatePlayers();
            }

            //Send the showdown message to the GUI players
            for (Player p : players) {
                if (p.isGuiPlayer()) {
                    p.update("#SHOWDOWN||" + showdownString);
                }
            }

            for (int j = 0; j < rankedPlayers.size(); j++) {
                Player p = rankedPlayers.get(j);
                if (p.getTotalCommitedToPot() == minTotalCommited) {
                    rankedPlayers.remove(p);
                    j--;
                } else {
                    rankedPlayers.get(rankedPlayers.indexOf(p)).subtractTotalCommitedToPot(minTotalCommited);
                }
            }
            for (Player p : players) {
                int score = p.getStack() - p.getBuyIn();
                p.addToScore(score);
            }
            logDivat();
            logSummary();
        }
    }

    /**
     * Get the gamestate for the specified player in the AAAI competition format
     * This is a string representation of the betting, and the private and public
     * cards
     * @param p The player for whom to show the gamestate
     * @return A string representing the current state of the game
     */
    private String getGameState(Player p) {
        String delimiter = ":";
        String currentGameState = "MATCHSTATE" + delimiter;
        currentGameState += p.getPosition() + delimiter;
        currentGameState += handsPlayed + delimiter;
        currentGameState += gamestate.getActionString() + delimiter;

        for (Player player : players) {
            if (player.equals(p)) {
                for (int round = 0; round <= gamestate.getRound(); round++) {
                    String privateCardString = currentHand.getPrivateCardsString(
                            p.getPosition(), round);
                    currentGameState += (round > 0 &&
                            !privateCardString.equalsIgnoreCase("") ? "/" : "");
                    currentGameState += privateCardString;
                }
            }
            if (player.getPosition() < (players.size() - 1)) {
                currentGameState += "|";
            }
        }

        for (int round = 0; round <= gamestate.getRound(); round++) {
            String publicCardString = currentHand.getPublicCardsString(round);
            currentGameState += (round > 0 &&
                    !publicCardString.equalsIgnoreCase("") ? "/" : "");
            currentGameState += publicCardString;
        }

        return currentGameState;
    }

    /**
     * Get the Full Showdown Gamestate to send to the players at HandOver
     * @param position The position of the player to send this too.
     * @return A string representation of the Full Showdown Gamestate
     */
    private String getShowdownGameState(Player p) {
        String delimiter = ":";
        String fullGameState = "MATCHSTATE" + delimiter;
        fullGameState += p.getPosition() + delimiter;
        fullGameState += handsPlayed + delimiter;
        fullGameState += gamestate.getActionString() + delimiter;

        for (Player player : players) {
            if ( player.equals(p) || !player.isFolded() ) {
              for (int round = 0; round < gamedef.getNumRounds(); round++) {
                  String privateCardString = currentHand.getPrivateCardsString(
                          player.getPosition(), round);
                  fullGameState += (round > 0 &&
                          !privateCardString.equalsIgnoreCase("") ? "/" : "");
                  fullGameState += privateCardString;
              }
            }
            if (player.getPosition() < players.size() - 1) {
                fullGameState += "|";
            }
        }

        for (int round = 0; round < gamedef.getNumRounds(); round++) {
            String publicCardString = currentHand.getPublicCardsString(round);
            fullGameState += (round > 0 &&
                    !publicCardString.equalsIgnoreCase("") ? "/" : "");
            fullGameState += publicCardString;
        }

        return fullGameState;
    }

    /**
     * Send the players thier new gamestates
     */
    private void updatePlayers() {
        if (ACTION_DELAY > 0) {
            try {
                Thread.sleep(ACTION_DELAY);
            } catch (InterruptedException ex) {
                logError(ex);
            }
        }
        for (Player p : players) {
            p.update(getGameState(p));
            logState(getGameState(p));
        }
    }

    /**
     * Parse out the last token of the response string and return it as the action
     * the player took
     * 
     * @param playerResponse
     * @return the action from the response string
     */
    // TODO: Modify parseAction to use the string split and test the response
    // for validity rather than throwing a NoSuchElement exception
    private String parseAction(String response) {
        StringTokenizer st = new StringTokenizer(response, ":");
        String action = "";
        st.nextToken();
        st.nextToken();
        int handCheck = new Integer(st.nextToken()).intValue();
        if (handCheck != handsPlayed) {
            Player p = players.get(currentPlayer);
            logWarning("Dealer recieved response [" + response + 
                       "] from player " + p.getName() + 
                       " with action for hand number " + handCheck + 
                       " waiting for hand number " + handsPlayed);
            return null;
        }
        logState(response);
        while (st.hasMoreTokens()) {
            action = st.nextToken();
        }
        return action;
    }

    /**
     * Run the dealer in a thread
     */
    public void run() {
        deal();
    }

    /**
     * Return stats about the game.
     * @return A string representing the room stats
     */
    public String getStats() {
        String stats = "";
        if (gameOver) {
            stats += "FINISHED:";
        } else if (disconnected) {
            stats += "ERROR:DISCONNECTED:";
        } else if (error) {
            stats += "ERROR:";
        } else {
            stats += "RUNNING:";
        }
        stats += handsPlayed + ":";
        for (Player p : players) {
            stats += p.toString() + ":";
        }
        stats = stats.substring(0, stats.length() - 1);
        if (gameOver || disconnected || error) {
            hasReported = true;
        }
        return stats;
    }

    /**
     * Check to see whether or not the games is over
     * @return True for gameOver, False otherwise
     */
    public boolean isGameOver() {
        return gameOver;
    }

    /**
     * Check to see if one of the players has disconnected
     * @return True is there has been a disconect, False otherwise
     */
    public boolean isDisconnected() {
        return disconnected;
    }

    /**
     * Check to see if the game error'd out
     * @return True if there was an error
     */
    public boolean isError() {
        return error;
    }

    /**
     * Set the disconnected flag
     * @param disconnected a boolean to set the disconnected flag
     */
    public void setDisconnected(boolean disconnected) {
        this.disconnected = disconnected;
    }

    /**
     * An overriden function used to change the default serialization behavior
     * on a write
     * @param out the output stream to write the object to
     * @throws java.io.IOException
     */
    private void writeObject(ObjectOutputStream out) throws IOException {
        out.defaultWriteObject();
    }

    /**
     * An overriden function used when loading the object.  The default behavior 
     * is used and the disconnect flag is reset
     * @param in The input stream to load the object from
     * @throws java.io.IOException
     * @throws java.lang.ClassNotFoundException
     */
    private void readObject(ObjectInputStream in) throws IOException, ClassNotFoundException {
        in.defaultReadObject();
        disconnected = false;
    }

    /**
     * Restores a player matching the name.  This resets thier stack score and position
     * @param name The players name to restore
     * @param seat The seat to restore the player to
     * @param stack The stacksize the player needs restoring to
     * @param position The positions to restore the player to
     * @param score The score of the player to be restored
     * @return True on a sucessful restore, false otherwise
     */
    public boolean restorePlayer(String name, int seat, int stack, int position, int score) {
        for (Player p : players) {
            if (p.getName().equalsIgnoreCase(name)) {
                p.setPosition(position);
                p.setSeat(seat);
                p.setStack(stack);
                p.setScore(score);
                return true;
            }
        }
        return false;
    }

    /**
     * Used to restore the game to a specific hand.  The game deals out the 
     * hands from the deck until the hand number is reached
     * @param handNumber The hand to restore to
     */
    public void restoreToHand(int handNumber) {
        while (handsPlayed < handNumber) {
            currentHand = deck.dealHand(players.size(), gamedef.getNumRounds(),
                    gamedef.getNumPrivateCards(), gamedef.getNumPublicCards());
            handsPlayed++;
        }
        if (handsPlayed >= numHands) {
            gameOver = true;
        }
    }

    private static void loadSettings() throws ParserConfigurationException,
            SAXParseException, SAXException, IOException,
            InterruptedException {
        //Get the Room info                       
        XMLParser parser;
        try {
            parser = new XMLParser("config/DEALER.config.xml");
        } catch (FileNotFoundException ex) {
            System.err.println("Could not find DEALER.config.xml in config directory, using defaults...");
            return;
        }

        NodeList nl = parser.parseElements("Dealer");
        if (nl.getLength() < 1) {
            return;
        }
        Node dealerNode = nl.item(0);
        if (dealerNode.getNodeType() == Node.ELEMENT_NODE) {
            PLAYER_ACTION_TIMEOUT = parser.getIntFromNode(dealerNode, "ActionTimeout");
            PLAYER_AVG_TIME_PER_HAND = parser.getIntFromNode(dealerNode, "AverageTimePerHand");
            DEFAULT_ACTION = parser.getStringFromNode(dealerNode, "DefaultAction");
            ACTION_DELAY = parser.getIntFromNode(dealerNode, "ActionDelay");
        }
        if (DEFAULT_ACTION.equalsIgnoreCase("CALL")) {
            DEFAULT_ACTION = "c";
        } else if (DEFAULT_ACTION.equalsIgnoreCase("FOLD")) {
            DEFAULT_ACTION = "f";
        } else {
            DEFAULT_ACTION = "c";
        }
    }
}
