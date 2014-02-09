package ca.ualberta.cs.poker.free.tournament;

import java.io.*;
import java.net.*;
import java.util.Vector;


/*
 * This class contains the code to start a process on a remote machine
 * and clean up afterwards.
 * 
 * @author Martin Zinkevich
 * 
 */
public class RemoteMachine implements MachineInterface {
        /**
	 * Track the loose threads from this machine.
	 */
        Vector<Thread> looseThreads;

        /**
	 * The address of the remote machine.
	 */
	private InetAddress address;

	/**
	 * The username for ssh on the remote machine.
	 */
	private String username;

	/**
	 * The location which can be used by the bot.
	 */
	private String expansionLocation;

	/**
	 * Is true if the remote machine is Windows.
	 */
	public boolean isWindows;

	/**
	 * True if an aggressive clean should be made.
	 */
	private boolean shouldClean;
	
	
	/**
	 * Construct a new RemoteMachine.
	 */
	public RemoteMachine(InetAddress address, String username,
	String expansionLocation, boolean isWindows) {
		this.address=address;
		this.username=username;
		this.expansionLocation=expansionLocation;
		if (expansionLocation.equals("")){
		  throw new RuntimeException("Empty expansionLocation");
		}
		this.isWindows = isWindows;
		this.shouldClean = false;
		this.looseThreads = new Vector<Thread>();
	}
	
	
	/**
	 * get the IP address of the RemoteMachine.
	 */
	public InetAddress getIP(){
	  return address;
	}
	
	/** 
	 * Tests if the address to check is exactly equal to the address of
	 * the remote machine. Hopefully, the remote machine has only one
	 * IP address.
	 */
    public boolean isThisMachine(InetAddress addr) {
    	return address.equals(addr);
	}


		/**
	 * This copies the bot from the server to the remote
	 * machine.
	 * 
	 * Note that the current implementation does not
	 * send the bot's tar file to an agreed upon location.
	 * This can be fixed in the future.
	 */
        public void copyFromServer(BotTarFile bot){
	  String scpCommand = "scp -r " + bot.getLocation()+".tar" + 
	  " " + username+ "@" + address.getHostAddress() + ":~";
	  try{
  	  Runtime.getRuntime().exec(scpCommand).waitFor();
	  } catch (InterruptedException e){
	  } catch (IOException io){
	  }
	}


        /**
	 * This extracts the bot and connects to the server.
	 * However, it does this in a separate thread.
	 */
	public void extractAndPlay(BotTarFile bot, InetAddress server,
	int port){
	        String tarFile = bot.getLocation();
		String internalLocation = expansionLocation +
		bot.getInternalLocation();
		String executable = internalLocation+"startme.bat";
		String serverIP = server.getHostAddress();

		String redirOutErr = " > "+expansionLocation+"out.txt 2> " +expansionLocation+"err.txt ";

		String tarCommand = 
		 "tar -xf " + tarFile + " -C "+
		expansionLocation;// + redirOutErr;
		String cdCommand = "cd " +  internalLocation;
		String exCommand = executable +" "+ serverIP + " "+port+redirOutErr;

	        executeRemoteCommandAndWait(tarCommand);
		String jointCommand =
		cdCommand+";"+exCommand;
		// Note that this does NOT wait for the command
		// to complete.
	        executeRemoteCommand(jointCommand);
	}

        /**
	 * Execute a remote command and wait for it to terminate.
	 */
        public void executeRemoteCommandAndWait(String command){
	  try{
	    executeRemoteCommand(command).waitFor();
	  } catch (InterruptedException e){
	  }
	}

	/**
	 * Begin execution of a remote command.
	 */
	public Process executeRemoteCommand(String command){
	  String login = username + "@" + address.getHostAddress();
	  String prefix = "ssh";
	  String fullCommand = prefix + " "+login+" "+command;
	  System.out.println("Executing "+command);
	  System.out.println("Full command:"+fullCommand);

	  try{
  	  Process p =  Runtime.getRuntime().exec(fullCommand);
	  // @TODO: add these to loose threads for cleanup
	  Thread scout = new Thread(new
	  StreamConnect(p.getInputStream(),System.out));
	  scout.start();
	  looseThreads.add(scout);
	  
	  Thread scerr = new Thread(new
	  StreamConnect(p.getErrorStream(),System.err));
	  scerr.start();
	  looseThreads.add(scerr);

	  return p;
	  } catch (IOException io){
	    System.err.println("I/O Exception executing a remote command");
	    return null;
	  }
	}

        /**
	 * Aggressively kill a Linux bot.
	 * UNTESTED
	 */
        public void remoteKillLinux(){
	  throw new RuntimeException("RemoteMachine.remoteKillLinux() not implemented");
	}

	/**
	 * Remotely kill a Windows bot.
	 * UNTESTED
	 */
        public void remoteKillWindows(){
	  String command = "cmd.exe /C taskkill.exe /F /FI \"USERNAME eq " 
	  + username + "\"";
	  executeRemoteCommandAndWait(command);
	}
	
	/**
	 * Clean files from the remote machine.
	 * UNTESTED
	 */
	public void cleanFiles(){
	  String command = "'rm -rf " + expansionLocation + "/*'";
	  executeRemoteCommandAndWait(command);
	}

        /**
	 * Restart the machine.
	 * UNTESTED
	 */
	public void restartMachine(){
	  throw new RuntimeException("Not implemented");
	}

        /**
	 * Start a bot.
	 */
	public void start(BotInterface bot, InetAddress server, int port) {
	  System.out.println("Starting machine "+address);
	  extractAndPlay((BotTarFile)bot,server,port);
	}

	public void clean(){
	  for(Thread t:looseThreads){
	    t.interrupt();
	  }
	  if (shouldClean){
	    cleanFiles();
	    if (isWindows){
	      remoteKillWindows();
	    } else {
	      remoteKillLinux();
	    }
	  }
	}

        /**
	 * Output the IP as a string.
	 */
	public String toString(){
	  return address.toString();
	}
}
