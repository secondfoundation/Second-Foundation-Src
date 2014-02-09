package glassfrog.players;

import java.io.BufferedReader;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.io.File;
import java.net.BindException;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.net.SocketTimeoutException;
import java.net.UnknownHostException;
import java.lang.ProcessBuilder;
import java.util.Date;
import java.util.Vector;


/**
 * A player used to connect the AAAI bots to the server.  
 * This class acts as an interface for the bots to connect into the code.
 * They are invoked by a BotManager and thier parameters are specified in a 
 * config file that the server parses.  This is to get around setting things like
 * the name, seat and buyin from the bot's perspective, but rather the config file
 * handles all of that information and simple adds the AAAIPlayer to the room and
 * the AAAIPlayer opens a port to the bot through which the Room is able to send
 * and recieve messages
 * 
 * @author jdavidso
 */
public class AAAIPlayer extends Player implements Runnable{
    private transient ServerSocket ss;
    private transient Socket socket;
    private transient PrintWriter pw;
    private transient BufferedReader br;
    private transient int port;
    private transient String location, logPrefix;
    private transient File script;
    /**
     * The maximum time a socket player can take to perform an action
     */
    private transient long actionTimeout;
    /**
     * The maximum time a socket player can take to perform all their actions
     * in a given match
     */
    private long matchTimeout;

    private transient final long DEFAULT_ACTION_TIMEOUT = 60000;
    private transient final long DEFAULT_MATCH_TIMEOUT = 0;
    
    /**
     * Invoke the super constructor, set up the server socket, get the port, and
     * then run the script associated with the bot
     * @param name The players name
     * @param buyIn The buyIn amount to play the game
     * @param location
     * @param portBase The portBase used by the server
     * @param scriptPath A path to the shell script
     * @param logPrefix A string telling the bot what to append to the out and error logs
     * @throws IOException 
     */
    public AAAIPlayer(String name, int buyIn, String location, String scriptPath, int portBase, String logPrefix) throws IOException {
        super(name, buyIn);
        actionTimeout = DEFAULT_ACTION_TIMEOUT;
        matchTimeout = DEFAULT_MATCH_TIMEOUT;
        this.location = location;
        this.script = new File( scriptPath );
        this.logPrefix = logPrefix;
        int i = 0;
        do {            
            try {
                ss = new ServerSocket(portBase+i);
                port = ss.getLocalPort();
            } catch (BindException ex) {
                i++;
                continue;
            }           
            if(i >= 1000) {
                throw new BindException("Could not bind to an open port in the port range"+portBase+"to "+(portBase+i));                                
            }
        }while(ss == null || !ss.isBound());        
        Thread t = new Thread(this, "AAAIPlayer:" + getName() + ":" + port);
        t.start();
        try {
            /*
             * Players have 10 minutes to connect to the server.  They must
             * setup thier socket in the first 30s of being executed to avoid
             * dead script errors
             */
            ss.setSoTimeout(600000);
            socket = ss.accept();
            // Disable Nagle's algorithm, improving latency at a cost of
            // bandwidth
            socket.setTcpNoDelay(true);
            pw = new PrintWriter(socket.getOutputStream());
            br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            if(!br.readLine().equalsIgnoreCase("Version:1.0.0")) {
                throw new IOException("Incorrect protocol version");
            }
        } catch (SocketTimeoutException ex) {
            System.err.println("AAAIPPlayer "+getName()+" hit startup timeout");
            throw new NullPointerException("Socket Timeout");
        }
    }

    /**
     * Gets the action of the player through the BufferedReader
     * @return the action sent or "f" on error
     */
    @Override
    public String getAction() throws SocketTimeoutException {
        // Compute which of the timeouts will kill the agent first
        long maxActionTime = actionTimeout;
        String timeoutType = "action timeout";
        if( matchTimeout > 0 && (matchTimeout - getTimeUsed()) < actionTimeout ) {
          maxActionTime = matchTimeout - getTimeUsed();
          timeoutType = "match timeout";
        }

        try {
            long initialTime = new Date().getTime();
            this.socket.setSoTimeout((int) maxActionTime);
            String response = br.readLine();
            long currentTime = new Date().getTime();
            setTimeUsed( getTimeUsed() + (currentTime - initialTime) );
            return response;
        } catch (SocketTimeoutException ste) {
            System.err.println("AAAIPlayer " + getName() + " hit " + timeoutType + " during read, folding hand"); 
            throw new SocketTimeoutException("AAAIPlayer " + getName() + ": " + timeoutType);            
        } catch (IOException ex) {
            System.err.println("AAAIPlayer "+getName()+" hit IOException during read, folding hand"); 
            //System.err.println( ex.toString() );
            ex.printStackTrace();
            throw new NullPointerException("Player Disconnected");            
        }
    }

    /**
     * Send the gamestate to the player through the PrintWriter
     * @param gamestate The gamestate to send
     */
    @Override
    public void update(String gamestate) {
       /* NOTE: competition protocol dictates that all messages are followed by
        * a carraige return and a line feed.  PrintWriter println() should not
        * be used as it outputs different line separators depending on the
        * platform */
        pw.print(gamestate + "\r\n");
        pw.flush();
    }
    
    /**
     * Get the port the player is associated with
     * @return the port
     */
    public int getPort() {
        return port;
    }
    
    /**
     * Return the machine location of the player
     * @return a String representing the machine location of the bot
     */
    public String getLocation() {
        return location;
    }
    
    /**
     * Get the path the bot is running on
     * @return A String representing the executeable path of the bot
     */
    public String getScriptPath() {
        return script.getPath();
    }

    /**
     * Runs the script associated with this player.  It will wait 5s to allow
     * time for the ServerSocket to start accepting connections
     */
    public void run() {
        Vector<Thread> looseThreads = new Vector<Thread>();
        String command = "";

        try {
            Thread.sleep(5000);
        } catch (InterruptedException ex) {
            System.err.println("AAAIPlayer "+getName()+" thread interuppted\n");
        }

        try {
            String agentCommand = script.getAbsolutePath() + " " + InetAddress.getLocalHost().getHostAddress() + " " + port;
            String agentWorkingDir = script.getParentFile().getAbsolutePath();
            command = "{ cd " + agentWorkingDir + "; " + agentCommand + "; }";

            ProcessBuilder proc;
            if(location.equalsIgnoreCase("127.0.0.1") || location.equalsIgnoreCase("localhost")) {
              proc = new ProcessBuilder( script.getAbsolutePath(), InetAddress.getLocalHost().getHostAddress(), Integer.toString(port) );
              proc.directory( script.getParentFile() );
              System.out.println("Executing bot command: \""+ agentCommand + "\" from " + agentWorkingDir);
            } else {
              proc = new ProcessBuilder("ssh", location, command);
              System.out.println("Executing bot command: ssh " + location + " " + command);
            }

            Process p = proc.start();
            FileOutputStream normalOut = new FileOutputStream("output/"+logPrefix+":"+getName()+".out");
            FileOutputStream errOut = new FileOutputStream("output/"+logPrefix+":"+getName()+".err");

            StreamConnect sc = new StreamConnect(p.getInputStream(), normalOut);
            Thread tsc = new Thread(sc, "StreamConnect:stdout:AAAIPlayer:" + getName() + ":" + port);
            tsc.start();
            looseThreads.add(tsc);

            StreamConnect scerr = new StreamConnect(p.getErrorStream(), errOut);
            Thread tscerr = new Thread(scerr, "StreamConnect:stderr:AAAIPlayer:" + getName() + ":" + port);
            tscerr.start();
            looseThreads.add(tscerr);

            p.waitFor();
            normalOut.close();
            errOut.close();
        } catch (UnknownHostException ex) {
            System.err.println("AAAIPlayer "+getName()+" could not reach host:"+ex.toString());
        } catch (InterruptedException e){
          // TODO: Do something more intelligent here
        } catch (IOException io) {
            System.err.println("AAAIPlayer "+getName()+" I/O Exception executing a local command: " + command);
            //System.err.println( io.toString() );
            io.printStackTrace();
        } finally {
            // Shut down all of the threads transferring output from the agent to a file once the process is finished
            for(Thread t:looseThreads){
              t.interrupt();
            }
        }
    }

    /**
     * Overrides the @Player call to this method and returns True
     * @return True
     */
    @Override
    public boolean isAAAIPlayer() {
        return true;
    }
    
    /**
     * Used to reconnect a player upon dealer reloads.  This takes a socket
     * connection and re-initializes the @PrintWriter and @BufferedReader
     * @param s a socket to reconnect to
     * @param location a location to reconnect to
     * @param scriptPath a path where the bot executeable is located
     * @throws java.io.IOException
     */
    public void reconnect(Socket s, String location, String scriptPath) throws IOException {
        this.socket = s;        
        br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        pw = new PrintWriter(socket.getOutputStream());
        this.location = location;
        this.script = new File( scriptPath );
    }
    
    /**
     * Get the @Socket the player is connected on
     * @return the @Socket the player is connected on
     */
    public Socket getSocket() {
        return socket;
    }

    /**
     * Override's the @Player implementation of this method and closes the @Socket
     * the @PrintWriter and the @BufferedReader down
     */
    @Override    
    public void shutdown() {
        try {
            br.close();
            pw.close();
            socket.close();
        } catch (IOException ex) {
            System.err.println("Error while trying to close the socket for the player "+getName());
        }
    }
    
    /**
     * Returns AAAI appended to the @Player representation of the object
     * @return AAAI appended to the front of the @Player toString method
     */
    @Override
    public String toString() {
        return "AAAIPLAYER " + getName() + " " + getBuyIn() + " " + location +
             " " + script.getPath() + " " + getTimeUsed() + "ms " + getScore();
    }
    
    /**
     * Set timeout, used for socket players.  If the socket player takes more
     * time to respond with an action than the specified timeout, then the
     * player's socket will timeout and an exception will be thrown.
     * @param timeout Timeout for the player's actions
     */
    // TODO: The constructor should take timeout parameters
    // TODO: Remove these once AAAIPlayer is a subclass of socket player
    public void setActionTimeout(long timeout) {
        this.actionTimeout = timeout;
    }

    /**
     * Set timeout, used for socket players.  If the socket player takes more
     * time than the specified timeout over the course of the entire match,
     * then the player's socket will timeout and an exception will be thrown.
     * @param timeout Timeout for the player's actions
     */
    public void setMatchTimeout(long timeout) {
        this.matchTimeout = timeout;
    }

    /**
     * Get the value of the per action timeout.  Currently used for socket
     * players. 
     * @return an int representing the number of milliseconds allowed for per
     * action.
     */
    @Override
    public long getActionTimeout() {
        return this.actionTimeout;
    }

    /**
     * Get the value of the per match timeout.  Currently used for socket
     * players. 
     * @return an int representing the number of milliseconds allowed over the
     * entire match
     */
    @Override
    public long getMatchTimeout(){
        return this.matchTimeout;
    }
}
