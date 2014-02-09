package ca.ualberta.cs.poker.free.statistics;

import java.awt.FileDialog;
import java.awt.Frame;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PipedReader;
import java.io.PipedWriter;
import java.util.StringTokenizer;
import java.util.Vector;

import java.util.Hashtable;

import ca.ualberta.cs.poker.free.dynamics.MatchType;
import ca.ualberta.cs.poker.free.dynamics.LimitType;
import ca.ualberta.cs.poker.free.dynamics.RingDynamics;
import ca.ualberta.cs.poker.free.tournament.Profile;
//import ca.ualberta.cs.poker.free.tournament.StreamConnect;

public class MatchStatistics {
	Vector<HandStatistics> hands;
	boolean hasHeader;
	String formatType;
	LimitType limitType;
	boolean stackBound;
	int initialStack;
	
	MatchStatistics(String logfile) throws FileNotFoundException, IOException{
		System.err.println("Reading "+logfile);
		BufferedReader reader = new BufferedReader(new FileReader(new File(logfile)));
		hands = new Vector<HandStatistics>();
		read(reader);
	}
	

	/**
	 * Confirms that particular files were generated according to the game
	 * specification in RingDynamics.
	 * 
	 */
	public boolean confirm(){
		String []names = hands.firstElement().names.toArray(new String[2]);
		MatchType info = new MatchType(limitType,stackBound,initialStack,hands.size());
			RingDynamics game = new RingDynamics(
				names.length,// numPlayers, 
				info,
				names//botNames
			);
		return confirm(game);
	}

	/**
	 * Confirms that particular files were generated according to the game
	 * specification in RingDynamics.
	 * 
	 */
	public boolean confirm(RingDynamics game) {
		// Pipe p = new Pipe();
		try {
			PipedWriter pw = new PipedWriter();
			PipedReader pr = new PipedReader(pw);
			BufferedReader br = new BufferedReader(pr);
			for (HandStatistics hand : hands) {
				// If we ever want no-limit ring games, we have to change this
				// here.
				System.err.println("hand.getRawCardsBuffered()="+hand.getRawCardsBuffered());
				pw.write(hand.getRawCardsBuffered() + "\n");
				game.nextHand(br);
				String rawBetting = hand.getRawActions();
				String currentAction = "";
				System.err.println("rawBetting:"+rawBetting);
				String verboseBetting = "";
				for (int i = 0; i < rawBetting.length(); i++) {
					char lastLetter = rawBetting.charAt(i);
					if (Character.isDigit(lastLetter)) {
						currentAction += lastLetter;
					} else {
						if (currentAction.length() > 0) {
                            //System.err.println(game.toString());
							//System.err.println("currentAction:"+currentAction+" seat: " + game.seatToAct + " round: "+game.roundIndex+" bettingSoFar: "+rawBetting.substring(0,i));
							int oldSeat = game.seatToAct;
							if (!currentAction.startsWith("b")){
							game.handleAction(currentAction);
							}
							verboseBetting += currentAction + oldSeat+","+game.inPot[oldSeat];
							if (game.isGameOver()){
								verboseBetting += "*";
							} else if (game.firstActionOnRound){
								verboseBetting +="/";
							}
							//System.err.println("State:"+verboseBetting);
						}
						currentAction = "" + lastLetter;
					}
				}
				//System.err.println("currentAction:"+currentAction);
				if (!currentAction.startsWith("b")){
					game.handleAction(currentAction);
				}
				verboseBetting += currentAction + game.seatToAct+","+game.inPot[game.seatToAct];
				if (game.isGameOver()){
					verboseBetting += "*";
				} else if (game.firstActionOnRound){
					verboseBetting +="/";
				}
				System.err.println("State:"+verboseBetting);

				if (!game.isGameOver()) {
					System.err
							.println("Error: actions ended prematurely in hand:"
									+ hand);
					return false;
				} else if (game.amountWon == null) {
					System.err.println("Error 2 in hand:" + hand);
					return false;
				}
				for (int i = 0; i < hand.smallBlinds.size(); i++) {
					if (hand.smallBlinds.get(i) != game.amountWon[i]) {
						System.err.println("Error in the amount won in hand:"
								+ hand);
						System.err.println("Should have been "
								+ game.getGlobalState());
						return false;
					}

				}

			}
			return true;
		} catch (IOException io) {
			return false;
		}

	}
	
	void read(BufferedReader reader) throws IOException{
		String firstLine = reader.readLine();
		System.err.println("First line:\n");
		System.err.println(firstLine);
		if (firstLine.startsWith("## GAMESTATE Version 2.0")){
			formatType = "GAMESTATE VERSION 2.0";
			hasHeader = true;
			String secondLine = reader.readLine();
			StringTokenizer st = new StringTokenizer(secondLine);
			st.nextToken(); // Burn the comment characters ("##")
			st.nextToken(); // Burn the first word ("type")
			String limitTypeString = st.nextToken();
			String stackBoundString = st.nextToken();
			limitType = LimitType.parse(limitTypeString);
			stackBound = (stackBoundString.equals("STACKBOUND"));
			if (stackBound){
				String thirdLine = reader.readLine();
				st = new StringTokenizer(thirdLine);
				st.nextToken(); // ##
				st.nextToken(); // "stacksize:"
				initialStack = Integer.parseInt(st.nextToken());
			} else {
				initialStack = 0;
			}
			String nextLine = Profile.nextLine(reader);
			while(nextLine!=null){
				hands.add(HandStatistics.getGameStateVersion2HandStatistics(nextLine));
				nextLine = Profile.nextLine(reader);
			}
		} else if (firstLine.startsWith("MATCHSTATE:")){
			formatType = "GAMESTATE VERSION 1.0";
			hasHeader = false;
			limitType = LimitType.LIMIT;
			stackBound = false;
			initialStack = 0;
			
			
			String nextLine = firstLine;
			Vector<Integer> previousSmallBlinds = new Vector<Integer>();
			previousSmallBlinds.add(0);
			previousSmallBlinds.add(0);
			do{
			  Vector<String> names = new Vector<String>();
			  names.add("Player0");
			  names.add("Player1");
			  
			  hands.add(HandStatistics.getGameStateHandStatistics(nextLine, names,previousSmallBlinds));
			  previousSmallBlinds = HandStatistics.getGameStateSmallBlinds(nextLine);
			  nextLine = reader.readLine();
			} while(nextLine!=null);
		} else {
			formatType = "U OF A VERSION 1.0";
			hasHeader = false;
			limitType = LimitType.LIMIT;
			stackBound = false;
			initialStack = 0;
			
			String nextLine = firstLine;
			do{
				// If a line does not begin "<integer>:" then it is not a valid U of
				// Alberta hand outcome
				try{
					Integer.parseInt(HandStatistics.split(nextLine,':').get(0));	
				} catch (NumberFormatException nfe){
					continue;
				}
				hands.add(HandStatistics.getUofAHandStatistics(nextLine));
				nextLine=reader.readLine();
			} while(nextLine!=null);
		}
	}
	
	public Vector<String> getPlayers(){
		return hands.firstElement().names;
	}
	

	public void addUtility(Hashtable<String,Integer> utilities, int firstHand, int lastHand){
		Vector<String> players = getPlayers();
		Vector<Integer> newUtils = getUtilitiesInSmallBlinds(firstHand,lastHand);
		for(int i=0;i<players.size();i++){
			String player = players.get(i);
			int oldTally = utilities.get(player);
			int currentUtility = newUtils.get(i);
			utilities.put(player, oldTally+currentUtility);
		}
	}

	public Hashtable<String,Integer> getUtilityMapInSmallBlinds(int firstHand, int lastHand){
		Vector<String> players = getPlayers();
		Hashtable<String,Integer> utilities = new Hashtable<String,Integer>();
		
		for(String player:players){
			utilities.put(player,0);
		}
		for(HandStatistics hand:hands){
			if (hand.handNumber>=firstHand&&hand.handNumber<=lastHand){
			for(int i=0;i<hand.names.size();i++){
				String player = hand.names.get(i);
				int currentUtility = hand.smallBlinds.get(i);
				int oldTally = utilities.get(player);
				utilities.put(player,oldTally+currentUtility);	
			}
			}
		}
		return utilities;
	}
	
	public Vector<Integer> getUtilitiesInSmallBlinds(int firstHand, int lastHand){
		Vector<String> players = getPlayers();
		Hashtable<String,Integer> utilities = getUtilityMapInSmallBlinds(firstHand, lastHand);
		Vector<Integer> result = new Vector<Integer>();
		for(String player:players){
			result.add(utilities.get(player));
		}
		return result;
	}
	
	public void normalizeHandNumbers(){
		for(int i=0;i<hands.size();i++){
			hands.get(i).handNumber=i;
		}
	}
	
	/**
	 * Tests if two matches could be duplicate based upon 
	 * the players and the cards.
	 * @param other the match to compare to
	 * @return whether it is possible if the matches could be duplicate
	 */
	public boolean isDuplicate(MatchStatistics other){
		if (hands.size()!=other.hands.size()){
			return false;
		}
		for(int i=0;i<hands.size();i++){
			if (!hands.get(i).isDuplicate(other.hands.get(i))){
				return false;
			}
		}
		return true;
	}
	
	public int getFirstHandNumber(){
		int minSoFar = Integer.MAX_VALUE;
		for(HandStatistics hand:hands){
			if (hand.handNumber<minSoFar){
				minSoFar = hand.handNumber;
			}
		}
		return minSoFar;
	}
	
	int getLastHandNumber(){
		int maxSoFar = Integer.MIN_VALUE;
		for(HandStatistics hand:hands){
			if (hand.handNumber>maxSoFar){
				maxSoFar = hand.handNumber;
			}
		}
		return maxSoFar;
	}
	
	public static void handleFile(String file) throws IOException{
			File f = new File(file);
			if (!(f.exists())){
				System.err.println("File not found:"+file);
			} else if (f.isDirectory()){
				System.err.println("Descending into directory "+file);
				String[] files = f.list();
				if (!file.endsWith(File.separator)){
					file+=File.separator;
				}
				
				for(String subFile:files){
					handleFile(file+subFile);
				}
			} else if (file.endsWith(".res")){
				System.err.println("Result file "+file+" passed over.");
			} else {
			  System.err.println("Loading match "+file+"...");
			  MatchStatistics m = new MatchStatistics(file);
			  System.err.println("Loaded match:"+file);
			  if (!m.confirm()){
				System.err.println("Match does not agree with ring policy:"+file);
				System.exit(0);
			  } else {
				System.err.println("Match appears good:"+file);
			  }
			}
	}
			
	public static void main(String[] args) throws IOException{
		if (args.length!=0){
			for(String file:args){
				
				handleFile(HandStatistics.remove(file,'"'));
			}
		} else {
			Frame f = new Frame();
			FileDialog fd = new FileDialog(f,"Load match statistics",FileDialog.LOAD);
			fd.setVisible(true);
			String dir = fd.getDirectory();
			String file = fd.getFile();
			handleFile(dir+file);
			System.exit(0);
		}
	}
}