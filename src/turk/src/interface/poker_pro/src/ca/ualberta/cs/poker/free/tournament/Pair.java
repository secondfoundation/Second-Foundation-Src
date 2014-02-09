package ca.ualberta.cs.poker.free.tournament;

public class Pair<A,B> {
	A first;
	B second;
	
	
	public Pair(A first, B second){
		this.first = first;
		this.second = second;
	}
	
	public Pair(Pair<A,B> pair){
		this(pair.first,pair.second);
	}
	public Pair(){
		this(null,null);
	}
	
	public boolean equals(Object obj){
		//System.err.println("Pair.equals(Object)");
		return equals((Pair<A,B>)obj);
	}
	
	public boolean equals(Pair<A,B> obj){
		//System.err.println("Pair.equals(Pair)");
		if (this.first!=null){
			if (obj.first==null){
				return false;
			}
			if (!this.first.equals(obj.first)){
				return false;
			}
		} else if (obj.first!=null){
			return false;
		}
		
		if (this.second!=null){
			if (obj.second==null){
				return false;
			}
			if (!this.second.equals(obj.second)){
				return false;
			}
		} else if (obj.second!=null){
			return false;
		}
		return true;
	}
	
	public int hashCode(){
		int firstHashCode = (first==null) ? 0 : first.hashCode();
		int secondHashCode = (second==null) ? 0 : second.hashCode();
		/*System.err.println(first);
		System.err.println("firstHashCode:"+firstHashCode);
		System.err.println(second);
		System.err.println("secondHashCode:"+secondHashCode);*/
		
		return firstHashCode;
	}
}
