package ca.ualberta.cs.poker.free.statistics;

import java.util.Vector;

import ca.ualberta.cs.poker.free.dynamics.Card;

public class HandStatistics {
    /** The betting sequence (all rbf, no blind info) */
	public String bettingSequence;
	
	/** The net small blinds won in seat order */
	public Vector<Integer> smallBlinds;
	/** The names of the bots in seat order */
	public Vector<String> names;
	
	/** The cards in the format rsrs|rsrs/rsrsrs/rs/rs */
	public String cards;
	/** The hand number */
	int handNumber;
	
	
	
	public HandStatistics(String bettingSequence, Vector<Integer> smallBlinds, 
			Vector<String> names, String cards, int handNumber) {
		this.bettingSequence = bettingSequence;
		this.smallBlinds = smallBlinds;
		this.names = names;
		this.cards = cards;
		this.handNumber = handNumber;
	}


	/**
	 * Test if this hand is a possible duplicate of another hand.
	 * True iff the cards are the same and the players are permuted.
	 * @param other the hand to be compared.
	 * @return if it is possible that this hand is a duplicate of other 
	 */
	public boolean isDuplicate(HandStatistics other){
		if (!other.names.containsAll(names)){
			return false;
		}
		if (!names.containsAll(other.names)){
			return false;
		}
		return cards.startsWith(other.cards)||other.cards.startsWith(cards);
	}
	
	/**
	 * Useful only for unbounded stack games.
	 * @return
	 */
	public String getRawCardsBuffered(){
		String result = remove(cards,'/');
		result = remove(result,'|');
		//System.err.println(result);
		return bufferCards(result,5+(names.size()*2));
	}

	public String getRawActions(){
		return remove(bettingSequence,'/');
	}
	/**
	 * Buffers observed cards with cards from the deck.
	 * @param original the original string of cards
	 * @param numCards the total number of cards at the end.
	 * @return a string of cards (no spaces)
	 */
	public String bufferCards(String original, int numCards){
		Card[] array=Card.toCardArray(original);
		Vector<Card> result = new Vector<Card>();
		for(Card c:array){
			result.add(c);
			//System.err.println("Card:"+c);
		}
		//System.err.println("result.size()=="+result.size());
		if (result.size()<numCards){
			Card[] other=Card.getAllCards();
			for(Card c:other){
				if (!result.contains(c)){
					result.add(c);
					if (result.size()==numCards){
						String strResult="";
						for(Card c2:result){
							strResult += c2;
						}
						return strResult;
					}
				}
			}
		}
		return original;
		//throw new RuntimeException("Internal error in bufferCards: original="+original+", numCards="+numCards);
	}
	public static HandStatistics getUofAHandStatistics(String line){
		Vector<String> splitLine = split(line,':');
		int handNumber = Integer.parseInt(splitLine.get(0));
		Vector<String> names = split(splitLine.get(1),',');
		String weirdBetting = splitLine.get(2);
		weirdBetting=weirdBetting.replace('k', 'c');
		weirdBetting=weirdBetting.replace('b', 'r');
		weirdBetting=remove(weirdBetting,'0');
		String weirdCards = splitLine.get(3);
		weirdCards = remove(weirdCards,'|');
		weirdCards = weirdCards.replace(',','|');
		// Five dollars is a small blind
		Vector<String> dollars = split(splitLine.get(4),',');
		Vector<Integer> smallBlinds = new Vector<Integer>();
		for(String dollar:dollars){
			smallBlinds.add(Integer.parseInt(dollar)/5);
		}
		return new HandStatistics(weirdBetting,smallBlinds, 
				names, weirdCards, handNumber);
	}
	
	/**
	 * Gets small blinds in player order
	 * @param line
	 * @return
	 */
	public static Vector<Integer> getGameStateSmallBlinds(String line){
		Vector<String> splitLine = split(line,':');
		Vector<Integer> result = new Vector<Integer>();
		for(int i=0;i<2;i++){
			double dollars = Double.parseDouble(splitLine.get(i+5));
			int smallBlinds = (int)(dollars/5.0);
			result.add(smallBlinds);
		}
		return result;
	}
	/**
	 * 
	 * @param line a GAMESTATE entry as output by the 2006 AAAI server
	 * @param names names in game order
	 * @return A HandStatistics object representing the hand
	 */
	public static HandStatistics getGameStateHandStatistics(String line,Vector<String> names,Vector<Integer> previousSmallBlinds){
		//throw new RuntimeException("Not implemented");
		Vector<String> splitLine = split(line,':');
		int handNumber = Integer.parseInt(splitLine.get(2));
		String bettingSequence = splitLine.get(3);
		String cards = splitLine.get(4);
		boolean flipped = (handNumber % 2)==1;
		Vector<Integer> currentSmallBlinds = getGameStateSmallBlinds(line);
		Vector<Integer> bankrollChange = new Vector<Integer>();
		Vector<String> seatNames = new Vector<String>();
		if (flipped){
			bankrollChange.add(currentSmallBlinds.get(1)-previousSmallBlinds.get(1));
			bankrollChange.add(currentSmallBlinds.get(0)-previousSmallBlinds.get(0));
			seatNames.add(names.get(1));
			seatNames.add(names.get(0));
		} else {
			bankrollChange.add(currentSmallBlinds.get(0)-previousSmallBlinds.get(0));
			bankrollChange.add(currentSmallBlinds.get(1)-previousSmallBlinds.get(1));
			seatNames.add(names.get(0));
			seatNames.add(names.get(1));
		}
		
		return new HandStatistics(bettingSequence,bankrollChange, 
				seatNames, cards, handNumber);
	}
	
	public static HandStatistics getGameStateVersion2HandStatistics(String line){
		Vector<String> splitLine = split(line,':');
		Vector<String> names = split(splitLine.get(0),'|');
		int handNumber = Integer.parseInt(splitLine.get(1));
		String bettingSequence = splitLine.get(2);
		String cards = splitLine.get(3);
		Vector<String> smallBlindStrings = split(splitLine.get(4),'|');
		Vector<Integer> smallBlinds = new Vector<Integer>();
		for(String str:smallBlindStrings){
			smallBlinds.add(Integer.parseInt(str));
		}
		return new HandStatistics(bettingSequence,smallBlinds, 
				names, cards, handNumber);
	}
	
	/**
	 * Splits a string based upon a character.
	 * @see ca.ualberta.cs.poker.free.server.TimedSocket#parseByColons(String)
	 * TODO put this in a standard place (perhaps a util package?)
	 * @param str The string to split
	 * @param splitter a character upon which to split
	 * @return a vector of split strings, some possibly empty.
	 */
    public static Vector<String> split(String str, char splitter){
      Vector<String> result = new Vector<String>();
      int lastIndex=-1;
      while(true){
        int currentIndex = 0;
	currentIndex = str.indexOf(splitter,lastIndex+1);
	if (currentIndex==-1){
		result.add(str.substring(lastIndex+1));
	  return result;
	}
	result.add(str.substring(lastIndex+1,currentIndex));
	lastIndex=currentIndex;
      }
    }
    
    public static String remove(String str, char removed){
    	Vector<String> pieces = split(str,removed);
    	String result = "";
    	for(String piece:pieces){
    		result += piece;
    	}
    	return result;
    }
    
    public String toString(){
    	String result = "";
    	for(int i=0;i<names.size()-1;i++){
    		result+=names.get(i)+"|";
    	}
    	result+=names.lastElement();
    	result += (":" + handNumber + ":"+bettingSequence +":"+cards);
    	result += ":"+smallBlinds.firstElement();
    	for(int i=1;i<smallBlinds.size();i++){
    		result+=("|"+smallBlinds.get(i));
    	}
    	return result;
    }
}
