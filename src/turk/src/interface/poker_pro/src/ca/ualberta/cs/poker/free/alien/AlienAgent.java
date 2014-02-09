package ca.ualberta.cs.poker.free.alien;
import ca.ualberta.cs.poker.free.dynamics.MatchType;
import ca.ualberta.cs.poker.free.dynamics.LimitType;
import ca.ualberta.cs.poker.free.server.*;
import ca.ualberta.cs.poker.free.tournament.*;

import java.net.*;
import java.io.*;
import java.util.*;


/**
 * AlienAgent.java
 * The alien's "agent" on the server side. 
 * Sends messages to the alien and
 * receives messages from the alien.
 * Messages sent:<BR>
 * CLEANMACHINE:&lt;description&gt;<BR>
 * ASSIGNMACHINE:&lt;description&gt; (always sent before ASSIGNBOT)<BR>
 * ASSIGNBOT:&lt;name&gt;:&lt;serverIP&gt;:&lt;port&gt;(always sent after ASSIGNMACHINE)<BR>
 * MATCHSTARTED:&lt;matchname&gt;<BR>
 * MATCHTERMINATE:&lt;matchname&gt;<BR>
 * MATCHCOMPLETE:&lt;matchname&gt;<BR>
 * ERROR:&lt;message&gt;<BR>
 * SUCCESS<BR>
 * Messages received:<BR>
 * LOGIN:&lt;username&gt;:&lt;password&gt;<BR>
 * CREATEMACHINE:&lt;description&gt;<BR>
 * CREATEBOT:&lt;description&gt;<BR>
 * MATCHREQUEST:&lt;gametype&gt;:&lt;alienBotName&gt;:&lt;opponentBotName&gt;<BR>
 * MATCHTERMINATE:&lt;matchname&gt;<BR>
 * CHANGEPASSWORD:&lt;username&gt;:&lt;newpassword&gt;<BR>
 * LOGOUT<BR>
 * SHUTDOWN<BR>
 * ADDUSER:&lt;teamname&gt;:&lt;username&gt;:&lt;newpassword&gt;:&lt;email&gt;:&lt;accountType&gt;<BR>
 *
 * TODO Make sure the match queue is synchronized. Perhaps add a synchronized
 * method for adding matches?
 */
public class AlienAgent extends TimedSocket implements Runnable{

	static String tempRoot = "data/temp/";
    /**
     * Unique agent name, used to append to file names.
     */
    String agentName;

    /**
     * Initialized to false
     * When true, AlienAgent will be destroyed.
     */
    boolean complete;

    /**
     * Bots that have been introduced (in AlienBot form)
     */
    Hashtable<String,AlienBot> bots;

    PrintStream out;
    
    /**
     * Matches which have been completed.
     */
    Vector<MatchInterface> completedMatches;

    /**
     * Matches which have been queued.
     */
    Vector<MatchInterface> queuedMatches;


    /**
     * Machines which have been added.
     */
    Vector<MachineInterface> queuedMachines;
    
    /**
     * The user account associated with this agent.
     * An account can have more than one agent associated with it.
     */
    AlienAccount account;

    /**
     * The parent node.
     */
    AlienNode parent;
    
    /**
	 * Creates a new instance of AlienAgent;
	 */
	public AlienAgent(Socket socket, AlienNode parent) throws SocketException,
			IOException {
		super(socket);
		System.err.println("A new AlienAgent has been created.");
		this.parent = parent;
		this.account = null;
		this.complete = false;
		this.agentName = parent.getNewAgentName();
		completedMatches = new Vector<MatchInterface>();
		queuedMatches = new Vector<MatchInterface>();
		queuedMachines = new Vector<MachineInterface>();
		bots = new Hashtable<String, AlienBot>();
		out = new PrintStream(new FileOutputStream(agentName+".in.txt"));
		Thread t = new Thread(this);
		t.start();
	}
    

    /**
	 * Sends an error message, then close the connection.
	 */
    public void sendError(String error){
      try{
    	System.err.println("Sent error "+error);
    	out.println("ERROR OBSERVED:"+error);
        sendMessage("ERROR:"+error);
      } catch(TimeoutException to){
      }
      
      suicide();
    }

    /**
     * Sends a message to assign a bot.<BR>
     * ASSIGNBOT:&lt;name&gt;:&lt;serverIP&gt;:&lt;port&gt;(always sent after ASSIGNMACHINE)<BR>
     * @see AlienClient#processAssignBotMessage(String)
     * @param name name of the bot
     * @param serverIP the IP of the poker server for the match
     * @param port the port of the poker server
     */
    public void sendAssignBot(String name, InetAddress serverIP, int port){
    	try{
    		sendMessage("ASSIGNBOT:"+name+":"+serverIP.getHostAddress()+":"+port);
    	} catch (TimeoutException to){
			out.println("SUICIDE:sendAssignBot");
    		suicide();
    	}
    }
    
    /**
     * Sends a message to assign a machine.<BR>
     * ASSIGNMACHINE:&lt;description&gt;<BR>
     * Always followed by ASSIGNBOT.<BR>
     * @see AlienClient#processAssignMachineMessage(String)
     * @param description a description of the machine
     */
    public void sendAssignMachine(String description){
    	try {
			sendMessage("ASSIGNMACHINE:"+description);
		} catch (TimeoutException e) {
			out.println("SUICIDE:sendAssignMachine");
			suicide();
		}
    }
    /**
     * NOTE: at present this function is not called.
     * Send a message of the form:<BR>
     * MATCHSTARTED:&lt;matchname&gt;<BR>
     * @see AlienClient#processMatchStartMessage(String)
     * @param matchName the name of the match
     */
    public void sendMatchStarted(String matchName){
      try{
      sendMessage("MATCHSTARTED:"+matchName);
      } catch (TimeoutException te){
			out.println("SUICIDE:sendMatchStarted:"+te);
        suicide();
      }
    }

    /**
     * Adds a queued match. However, if the Agent has been terminated,
     * silently fails.
     * @param match the match to add.
     */
    public synchronized void addQueuedMatch(MatchInterface match) {
    	//System.out.println("AlienAgent.addQueuedMatch()");
		if (!complete) {
			parent.generateCardFile(match);

			queuedMatches.add(match);
			parent.pushBack(match);
		}
	}
    
    /**
	 * Complete the match
	 * 
	 * @param match
	 *            the match that is completed
	 * 
	 */
    public synchronized void handleCompleteMatch(MatchInterface match){
      if (!completedMatches.contains(match)){
    	  completedMatches.add(match);
    	  sendMatchComplete(match.getName());
      }
    }

    /**
     * Sends a message that the match is complete.<BR>
     * MATCHCOMPLETE:matchname<BR>
     * @see AlienClient#processMatchComplete(String)
     * @param matchname the name of the match
     */ 
    public void sendMatchComplete(String matchname){
      try{
        sendMessage("MATCHCOMPLETE:"+matchname);
      } catch (TimeoutException te){
			out.println("SUICIDE:sendMatchComplete:"+te);
        suicide();
      }
    }

    /**
     * Initialize account.
     * If the message received is not a login message,
     * or the login info is incorrect, then logout.
     * LOGIN:&lt;username&gt;:&lt;password&gt;<BR>
     * @throws TimeoutException 
     */
    public boolean login() throws TimeoutException{
      for(int i=0;i<3;i++){
        String str = receiveMessage();
        Vector<String> data = parseByColons(str);
        /*System.out.println("data.size()="+data.size());
        for(int j=0;j<data.size();j++){
        	System.out.println(data.get(j));
        }*/
        if (data.size()!=3){
            sendError("Expected login:<username>:<password>, received "+str);
            return false;
        }
        if (!data.get(0).equals("LOGIN")){
          sendError("Expected login:<username>:<password>, received "+str);
	      return false;
        }
        String username = data.get(1);
        String password = data.get(2);
        account = parent.testLogin(username,password);
        if (account!=null){
	  sendMessage("SUCCESS");
	  return true;
	}
	try{
		System.err.println("Failed login:"+str);
        sendMessage("ERROR:Login incorrect:please try again");
	} catch (TimeoutException te){
		out.println("Timeout error(login):"+te);
	  suicide();
	  return false;
	}
      }
      sendError("Too many attempts at a login");
      return false;
    }

    
    public boolean isLegalAlienBotName(String alienBotName){
      if (alienBotName.contains(".")){
	    sendError("No periods allowed in bot names");
	    return false;
	  } else if (parent.getOpponent(alienBotName)!=null){
	    sendError("Alien bots cannot have the same names as opponents");
	    return false;
	  }
      return true;
    }
    
    /**
     * Processes a message in the middle.
     * @param message
     */
    public void processMessage(String message){
	      if (message.equals("LOGOUT")){
			out.println("SUICIDE:processMessage");
  	        suicide();
  		    return;
  	      } else if (message.startsWith("MATCHREQUEST:")){
  	    	  processMatchRequestMessage(message);
  	      } else if (message.startsWith("CREATEBOT:")){
  	    	  processCreateBotMessage(message);
  	      } else if (message.startsWith("CREATEMACHINE:")){
  	    	  processCreateMachineMessage(message);
  	      } else if (message.startsWith("MATCHTERMINATE:")){
  	    	  processMatchTerminateMessage(message);
  	      }	else if (message.startsWith("CHANGEPASSWORD:")){
  	    	  processChangePasswordMessage(message);
  	      } else if (message.startsWith("ADDUSER:")){
	    	  processAddUserMessage(message);
	      } else if (message.equals("SHUTDOWN")){
  	    	  processShutdownMessage();
  	      } else {
  	    	  sendError("Unknown message");
  	      }
    }
    
    /**
     * @see AlienClient#sendMatchTerminate(String)
     * Process a request to terminate a match.
     * The name of the match is prepended with the session name.<BR>
     * MATCHTERMINATE:&lt;matchname&gt;<BR>
     * @param message
     */
    public synchronized void processMatchTerminateMessage(String message) {
		Vector<String> fields = parseByColons(message);
		String name = fields.get(1);
		name = account.username + "." + agentName+"."+name; 
		for(int i=0;i<queuedMatches.size();i++){
			MatchInterface match = queuedMatches.get(i);
			if (match.getName().equals(name)){
				parent.killMatch(match);
				queuedMatches.remove(i);
				sendMatchTerminate(name);
				return;
			}
		}	
	}
    
    

    private void sendMatchTerminate(String name) {
        try{
            sendMessage("MATCHTERMINATE:"+name);
            } catch (TimeoutException te){
    			out.println("SUICIDE:sendMatchTerminate:"+te);
              suicide();
            }
	}


	public synchronized void addMachine(AlienMachine machine){
    	if (!complete){
    		queuedMachines.add(machine);
    		parent.add(machine);
    	}
    }

	/**
     * Process a request to create a machine.<BR>
     * CREATEMACHINE:&lt;description&gt;
     * 
     * @param message
     */
    public void processCreateMachineMessage(String message) {
    	Vector<String> fields = parseByColons(message);
		String description = fields.get(1);
		try {
			AlienMachine machine = new AlienMachine(this, description);
			addMachine(machine);
		} catch (IOException io) {
			out.println("SUICIDE:processCreateMachineMessage");
			suicide();
		}
	}
		
	


	/**
     * Process a request to create a bot.<BR>
     * CREATEBOT:&lt;description&gt;
     * 
     * @param message
     */
	public void processCreateBotMessage(String message) {
		Vector<String> fields = parseByColons(message);
		if (fields.size()!=2){
			sendError("Expected CREATEBOT:<description>, received "+message);
			out.println("SUICIDE:processCreateBotMessage:0");
			suicide();
			return;
		}
		String description = fields.get(1);
		try {
			AlienBot bot = new AlienBot(this, description);
			bots.put(bot.getName(), bot);
		} catch (IOException io) {
			out.println("SUICIDE:processCreateBotMessage:1");
			suicide();
		}
	}
	
	public void processShutdownMessage(){
		if (account.superuser){
			try{
				sendMessage("SUCCESS");
			} catch (TimeoutException to){
				
			}
			parent.startShutdown();
		} else {
			sendError("Not superuser: cannot shutdown system");
		} 
	}

	public void processChangePasswordMessage(String message){
		Vector<String> fields = parseByColons(message);
		System.err.println("CHANGEPASSWORD message received:"+message);
		if (fields.size()!=3){
			sendError("Expected CHANGEPASSWORD:<account>:<password>, received "+message);
			out.println("SUICIDE:processChangePasswordMessage:0");
			suicide();
			return;
		}
		String accountName = fields.get(1);
		String password = fields.get(2);
		AlienAccount otherAccount = parent.getAccount(accountName);
		if (otherAccount==null){
			sendError("No such user:"+accountName);
			out.println("SUICIDE:processChangePasswordMessage:1");
			suicide();
			return;
		}
		if (!account.superuser){
			if (!account.teamLeader){
				if (account!=otherAccount){
					sendError("Insufficient permission");
					out.println("SUICIDE:processChangePasswordMessage:2");
					suicide();
					return;
				}
			} else if (account.team.equals(otherAccount.team)){
				sendError("Different team");
				out.println("SUICIDE:processChangePasswordMessage:3");
				suicide();
				return;
			}
		}
		
		
		parent.changePassword(accountName,password);
		try{
		sendMessage("SUCCESS");
		} catch (TimeoutException te){
			out.println("SUICIDE:processChangePasswordMessage:4:"+te);
			suicide();
		}
	}

	/**
     * Receive a message in the normal loop.
     * Could be MATCHREQUEST, CREATEBOT, CREATEMACHINE,
     * MATCHTERMINATE, or LOGOUT.
     *
     */
    public void receiveNormalMessage(){
    	try{
    	      String str = receiveMessage();
    	      processMessage(str);
        } catch (TimeoutException te){
			out.println("SUICIDE:receiveNormalMessage:"+te);
            suicide();
    	    return;
          }
    	      
    }
    
    
    /**
	 * Receive a match, and then send it to the AlienNode. using
	 * AlienNode.pushBack(). Note that the REVERSE of the match is also added.
	 */
	public void processMatchRequestMessage(String str){
	  // System.err.println("AlienNode.processMatchRequestMessage("+str+")");
      // MATCHREQUEST:<gametype>:<matchname>:<alienbotname>:<opponentname>
      Vector<String> mess = parseByColons(str);
      if (!mess.get(0).equals("MATCHREQUEST")){
        sendError("Expected match request and received "+str);
	    return;
      }
      if (mess.size()<2){
    	  sendError("Wrong number of parameters in " + str);
    	  return;    	  
      }
      String gameType = mess.get(1);
      if (gameType.equals("HEADSUPLIMIT")){
    	if (mess.size()!=5){
    	  sendError("Wrong number of parameters in " + str);
    	  return;
    	}
    	String matchName = mess.get(2);
    	String alienBotName = mess.get(3);
        AlienBot alienBot = bots.get(alienBotName);
        if (alienBot==null){
        	sendError("Unknown alien bot request:"+alienBotName);
        	return;
        }
        String opponentName = mess.get(4);
        BotInterface opponentBot = parent.getOpponent(opponentName);
        if (opponentBot==null){
        	sendError("Unknown opponent bot:"+opponentName);
        	return;
        }
        
        InetAddress serverIP = parent.getServerIP();
        
        Vector<BotInterface> forwardBots = new Vector<BotInterface>();
        forwardBots.add(alienBot);
        forwardBots.add(opponentBot);
        String baseName = account.username +"." + agentName + "." + matchName;
        String cardFileName = matchName + ".crd";
        String forwardMatchName = baseName + "."
        +alienBotName+"."+opponentName;
        
        MatchType info = new MatchType(LimitType.LIMIT,false,0,1000);
        info.timePerHand = 60000;
        info.chessClock = false;
        HeadsUpMatch forwardMatch = new
	    HeadsUpMatch(forwardBots,
	    cardFileName,serverIP,
	    forwardMatchName,info);
        //System.out.println("About to queue match");
        addQueuedMatch(forwardMatch);
        
        String reverseMatchName = baseName + "."
        +opponentName + "." + alienBotName;
	    Vector<BotInterface> reverseBots = new Vector<BotInterface>();
	    reverseBots.add(opponentBot);
	    reverseBots.add(alienBot);
        HeadsUpMatch reverseMatch = new
	    HeadsUpMatch(reverseBots,
	    cardFileName,serverIP,reverseMatchName,info);
        addQueuedMatch(reverseMatch);
      } else {
        sendError("ERROR:Only supports heads-up for now");
	return;
      }
	}
	
	public synchronized void testCompletedMatches(){
		for(MatchInterface m:queuedMatches){
			if (m.isComplete()){
				handleCompleteMatch(m);
			}
		}
	}
	
    /**
	 * tar and e-mail completed matches to competitor. <BR>
	 * function.
	 */
    public void emailCompletedMatches(){
    	Vector<String> files=new Vector<String>();
    	for(MatchInterface m:completedMatches){
    		HeadsUpMatch m2 = (HeadsUpMatch)m;
    		files.add(m2.resultFile);
    		files.add(m2.logFile);
    	}
    	if (files.isEmpty()){
    		return;
    	}
    	String tempDirectory = agentName;
    	String tarFile = agentName +".tar";

    	// DEPRECATED since we're using TarAndWeb
    	//String destinationAddress = account.email;
    	//String subject = "Poker Server "+agentName+" Results";
    	//String body  = "The following tar file has the results of "+completedMatches.size()+" matches.\n";
    	//body += "The units is small blinds (one small bet is two small blinds).\n";
    	//body += "- Martin Zinkevich and Christian Smith\n";
    	//TarAndEmail tae = new TarAndEmail(subject, body, destinationAddress, 
	//tempDirectory, tarFile, files);
    	
    	TarAndWeb taw = new TarAndWeb( account.username, tempDirectory, tarFile, files);
    	
	try{
    		taw.execute();
    	} catch (IOException io){
    		System.err.println("Error sending e-mail");
    		io.printStackTrace(System.err);
    	}
	
    }
   /**
     * Remove pointer from parent.
     */
    public synchronized void suicide(){
      emailCompletedMatches();
      parent.removeAgent(this);
      complete = true;
      try{
    	  out.println("SUICIDE");
    	  out.close();
    	  close();
      } catch (IOException io){
      }
    }

    public void run() {
		try {
			open();

			if (login() == false) {
				return;
			}
		} catch (IOException io) {
			return;
		} catch (TimeoutException te) {
			return;
		}

		while (true) {
			if (complete){
				return;
			}
			receiveNormalMessage();
			if (complete) {
				return;
			}
			try {
				Thread.sleep(5000);
			} catch (InterruptedException ie) {
				out.println("SUICIDE:run");
				suicide();
				return;
			}
		}
	}
    
    /**
	 * Recieves a message: waits a day for a response.
	 */
    public String receiveMessage() throws TimeoutException{
      if (!complete){
    	  setTimeRemaining(24*60*60*1000);
    	  String result = super.receiveMessage();
    	  out.println("message received:"+result);
    	  out.flush();
          return result;
      }
      return "LOGOUT";
    }

    /**
     * Sends a message.
     * Waits 30 seconds for reception.
     */
    public void sendMessage(String message) throws TimeoutException{
      if (!complete){
    	//setTimeRemaining(30000);
    	out.println("server reply:"+message);
        super.sendMessage(message);
      }
    }


    /**
     * Sends a message to clean a particular machine.<BR>
     * CLEANMACHINE:&lt;description&gt;
     * @see AlienClient#processCleanMachineMessage(String)
     * @param description
     */
	public void sendCleanMachine(String description) {
		try{
		  sendMessage("CLEANMACHINE:"+description);
		} catch (TimeoutException te){
			out.println("SUICIDE:sendCleanMachine:"+te);
			suicide();
		}
	}
	/**
	 * Add a user. Tests for permission.
	 * ADDUSER:&lt;teamname&gt;:&lt;username&gt;:&lt;newpassword&gt;:&lt;email&gt;:&lt;accountType&gt;<BR>
	 */
	public void processAddUserMessage(String message){
		Vector<String> fields = parseByColons(message);
		if (fields.size()!=6){
			sendError("Wrong format");
			out.println("SUICIDE:processAddUserMessage");
			// Why is this here? A second suicide?
			suicide();
		}
		String teamname = fields.get(1);
		String username = fields.get(2);
		String password = fields.get(3);
		String email = fields.get(4);
		String accountType = fields.get(5);
		
		boolean superuser = accountType.equalsIgnoreCase("superuser");
		boolean teamLeader = accountType.equalsIgnoreCase("teamleader");
		if (!account.superuser){
			if (!account.teamLeader){
				sendError("Cannot add user unless team leader or superuser");
				return;
			}
			if (!teamname.equals(account.team)){
				sendError("Cannot add user for other team");
				return;
			}
			if (superuser){
				sendError("Only superusers can create superuser accounts");
				return;
			}
			AlienAccount existing = parent.getAccount(username);
			if (existing!=null){
				if (!existing.team.equals(account.team)){
					sendError("User exists for other team");
					//suicide();
					return;
				}
			}
		}
		AlienAccount result = new AlienAccount(username,password,teamname,email,teamLeader,superuser);
		parent.addAccount(result);
		try{
		sendMessage("SUCCESS");
		} catch (TimeoutException to){
		}
	}
}
