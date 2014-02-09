package glassfrog.players;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.util.Date;
import java.net.SocketTimeoutException;

/**
 * The SocketPlayer class allows for players to connect to the game via socket.
 * A Socket must be passed in to the constructor, which then sets up the PrintWriter
 * and BufferedReader from which the actions are sent and recieved from agents
 * 
 * @author jdavidso
 */
public class SocketPlayer extends Player{
    /**
     * The server socket on which the player is to connect
     */
    protected transient ServerSocket ss;
    /**
     * The socket returned after a successfull connection
     */
    protected transient Socket socket;
    /**
     * The buffered reader for the socket.
     */
    protected transient BufferedReader br;
    /**
     * The print writer for the socket
     */
    protected transient PrintWriter pw;
    /**
     * The maximum time a socket player can take to perform an action
     */
    protected transient long actionTimeout;
    /**
     * The maximum time a socket player can take to perform all their actions
     * in a given match
     */
    protected long matchTimeout;

    private transient final long DEFAULT_ACTION_TIMEOUT = 60000;
    private transient final long DEFAULT_MATCH_TIMEOUT = 0;
    
    /**
     * Empty default contructor for extendability
     */
    public SocketPlayer() {        
    }
    
    /**
     * A contructor for Socket Player that takes a name, buyIn, a seat request and
     * a port for connection
     * @param name a @String representing the name of the player
     * @param buyIn an int representing the requested buyIn amount
     * @param port an int representing a port to establish a connection on
     */
    public SocketPlayer(String name, int buyIn, int port) {
        super(name,buyIn);
        try {
            actionTimeout = DEFAULT_ACTION_TIMEOUT;
            matchTimeout = DEFAULT_MATCH_TIMEOUT;
            ss = new ServerSocket(port);
            socket = ss.accept();
            // Disable Nagle's algorithm, improving latency at a cost of
            // bandwidth
            socket.setTcpNoDelay(true);
            System.out.println("Socket Player connected on port: "+port);
            br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            pw = new PrintWriter(socket.getOutputStream());        
            if(!br.readLine().equalsIgnoreCase("Version:1.0.0")){
                throw new IOException("Invalid version");
            }                
        } catch (IOException ex) {
            System.err.println("Socket Player "+getName()+" hit IOException:"+ex.toString());
        }
    }
            
    /**
     * The SocketPlayer constructor that takes a port and opens a socket connection
     * to handle action requests and updates to the player over a socket
     * 
     * @param name A string representing the player's name
     * @param buyIn an int representing the player's buyIn
     * @param socket a socket to which the player is connected to an agent
     * @throws IOException
     */
    public SocketPlayer(String name, int buyIn, Socket socket) throws IOException {
        super(name,buyIn);
        this.socket = socket;
        this.actionTimeout = DEFAULT_ACTION_TIMEOUT;
        this.matchTimeout = DEFAULT_MATCH_TIMEOUT;
        // Disable Nagle's algorithm, improving latency at a cost of bandwidth
        this.socket.setTcpNoDelay(true);
        initPlayer();
    }

    /**
     * A contructror for SocketPlayer that takes a @BufferedReader and a @PrintWriter
     * and established the player based on the pre-establised in and out.
     * @param name a @String representing the name of the player
     * @param buyIn an int representing the requested buyIn amount
     * @param br A @BufferedReader the player will recieve gamestate information on
     * @param pw A @APrintWriter the player will print action to
     * @throws java.io.IOException
     */
    public SocketPlayer(String name, int buyIn, BufferedReader br, PrintWriter pw) 
            throws IOException {
        super(name,buyIn);
        this.actionTimeout = DEFAULT_ACTION_TIMEOUT;
        this.matchTimeout = DEFAULT_MATCH_TIMEOUT;
        this.br = br;
        this.pw = pw;
        if(br.readLine().equalsIgnoreCase("Version:1.0.0")) {
            return;
        } else {
            throw new IOException("Player has wrong version");
        }
        
    }
    
    /**
     * Returns the port the agent is connected to the player on
     * @return an int representing the port number the agent is connected on
     */
    public int getPort() {
        return socket.getPort();
    }
    
    /**
     * Gets the action of the player through the BufferedReader
     * @return the action sent or throw a NullPointerException on disconnect
     */
    @Override
    public String getAction() throws SocketTimeoutException {
        // Compute which of the timeouts will kill the agent first
        long maxActionTime = actionTimeout;
        String timeoutType = "action Timeout";
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
            System.err.println("SocketPlayer " + getName() + " hit " + timeoutType + " during read, folding hand"); 
            throw new SocketTimeoutException("SocketPlayer" + getName() + ": " + timeoutType);            
        } catch (IOException ex) {
            System.err.println("SocketPlayer "+getName()+" hit IOException during read, folding hand");  
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
        pw.println(gamestate);
        pw.flush();
    }

    /**
     * Set up the Players reader and writer.
     * @throws java.io.IOException
     */
    private void initPlayer() throws IOException{               
        br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        pw = new PrintWriter(socket.getOutputStream());        
         if(br.readLine().equalsIgnoreCase("Version:1.0.0")) {
            return;
        } else {
            throw new IOException("Player has wrong version");
        }         
    }
    
    /**
     * Overrides the @Player implementation of isSocketPlayer and returns True
     * @return True
     */ 
    @Override
    public boolean isSocketPlayer() {
        return true;
    }
    
    /**
     * The reconnect method allows for a player to be reconnected on @Dealer load
     * @param s The @Socket for the player to be reconnected on
     * @throws java.io.IOException
     */
    public void reconnect(Socket s) throws IOException {
        this.socket = s;
        br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        pw = new PrintWriter(socket.getOutputStream());
    }
    
    /**
     * Return the @Socket the player is using
     * @return the @Socket the player is currently using
     */
    public Socket getSocket() {
        return socket;
    }

    /**
     * Closes down all sockets and I/O on shutdown
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
     * Set timeout, used for socket players.  If the socket player takes more
     * time to respond with an action than the specified timeout, then the
     * player's socket will timeout and an exception will be thrown.
     * @param timeout Timeout for the player's actions
     */
    // TODO: The constructor should take timeout parameters
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
