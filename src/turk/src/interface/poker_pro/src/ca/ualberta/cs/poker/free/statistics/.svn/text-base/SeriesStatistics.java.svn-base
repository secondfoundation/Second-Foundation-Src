package ca.ualberta.cs.poker.free.statistics;

import java.util.Hashtable;
import java.util.Vector;

public class SeriesStatistics {
	Vector<Vector<MatchStatistics> > matches;
	public SeriesStatistics(){
		matches = new Vector<Vector<MatchStatistics> >();
	}
	
	public SeriesStatistics(MatchStatistics match){
		add(match);
	}
	
	/**
	 * Add a match to this series.
	 * TODO assert that the added match fits with this set
	 * @param match the match to add
	 */
	public void add(MatchStatistics match){
		for(Vector<MatchStatistics> matchSet:matches){
			MatchStatistics matchHere = matchSet.firstElement();
			if (matchHere.isDuplicate(match)){
				matchSet.add(match);
				return;
			}
		}
		Vector<MatchStatistics> newMatchSet = new Vector<MatchStatistics>();
		newMatchSet.add(match);
		matches.add(newMatchSet);
	}
	
	public Vector<String> getPlayers(){
		MatchStatistics match = matches.firstElement().firstElement();
		return match.getPlayers();
	}
	
	public Vector<MatchStatistics> getAllMatches(){
		Vector<MatchStatistics> result=new Vector<MatchStatistics>();
		for(Vector<MatchStatistics> matchSet:matches){
			result.addAll(matchSet);
		}
		return result;
	}
	public Hashtable<String,Integer> getUtilities(int firstHand, int lastHand){
		Vector<MatchStatistics> allMatches=getAllMatches();
		Hashtable<String,Integer> result=allMatches.firstElement().getUtilityMapInSmallBlinds(firstHand, lastHand);
		for(int i=1;i<allMatches.size();i++){
			allMatches.get(i).addUtility(result,firstHand,lastHand);
		}
		return result;
	}
	
	
}
