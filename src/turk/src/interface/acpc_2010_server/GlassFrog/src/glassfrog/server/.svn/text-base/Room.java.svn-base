package glassfrog.server;

import glassfrog.players.Player;
import glassfrog.model.Dealer;
import glassfrog.model.Gamedef;
import glassfrog.players.AAAIPlayer;
import glassfrog.players.GUIPlayer;
import glassfrog.tools.MatchRebuilder;
import glassfrog.tools.XMLParser;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.InvalidClassException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.PrintWriter;
import java.net.BindException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Random;
import java.net.SocketTimeoutException;
import java.util.Date;
import java.util.LinkedList;
import java.util.StringTokenizer;
import javax.xml.parsers.ParserConfigurationException;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;
import org.xml.sax.SAXParseException;

/**The Room class is the class that will handle all of the game code.  The rooms
 * consist of Players and a Dealer.  The room is responsible for handleing all 
 * the connections to the Players, The room takes connections until it is "full"
 * then it will start the game with the given specifications.  After the game is 
 * started, the dealer will then handle all of the game logic, and the Room will
 * be responsible for message passing to the players.  Essentially, the Dealer
 * handles the gamestates, and then the room is responsible for sending an action
 * request to the proper player.  The response is then sent back to the Dealer.
 * Once the game is over, the room will be shutdown, or restarted, depending on 
 * specifications of the room.
 *
 * @author jdavidso
 */
public class Room implements Runnable {

    private String name;
    private Gamedef gamedef;
    private Dealer dealer;
    private ServerSocket serverSocket;
    private LinkedList<Player> players = new LinkedList<Player>();
    private int playerCount;
    private int port;
    private int seed;
    private int numHands;
    private boolean runOnce = true;
    private boolean alive = true;
    private BufferedWriter errorLogWriter, roomLogWriter;
    private static final int ROOM_TIMEOUT = 1000;
    private static int TIMEOUT = 60000;
    private static int PORTBASE = 9001;
    private static boolean SAVE_FLAG = true;

    /**
     * Starts up a Room.  A Room is a place where players connect to in order to 
     * get assigned sockets to talk to the dealer.  Here the name, game definition, 
     * number of hands and seed are specified.
     * @param name The name of the match/room
     * @param hands The number of hands to play
     * @param gamedef The game definition used
     * @param seed a seed for the cards in the game
     * @throws IOException
     * @throws InterruptedException
     */
    public Room(String name, int hands, Gamedef gamedef, int seed) throws IOException, InterruptedException {
        this.name = name.toUpperCase();
        this.gamedef = gamedef;
        this.numHands = hands;
        this.seed = seed;
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
        initServerSocket();
    }

    /**
     * Initialize the logs for the game.
     * The logname will be of the form roomname_timestamp.(log || .err) where 
     * roomname is the name passed from the server to the room and the timestamp      
     */
    private void initLogging() {
        String logPath = "logs/";
        try {
            errorLogWriter = new BufferedWriter(new FileWriter(logPath + name + ".room.err", true));
            roomLogWriter = new BufferedWriter(new FileWriter(logPath + name + ".room.log", true));
        } catch (IOException ex) {
            System.err.println("Could not initialize logs, exit with IO Error " + ex.toString());
        } catch (SecurityException ex) {
            System.err.println("Could not initialize logs, exit with Secutirty Error " + ex.toString());
        }
    }

    /**
     * Utility for logging an error message to the errorLogger
     * @param ex
     */
    public void logError(Exception ex) {
        try {
            errorLogWriter.write(new Date().toString() + " : ");
            ex.printStackTrace(new PrintWriter(errorLogWriter));
        } catch (IOException ex1) {
            System.err.println("Room Logging Error: ");
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
     * Log a gamesate to the roomLogger
     * @param info the message to log to the room log 
     * @param toOut True to print to stdout
     */
    public void logInfo(String info, boolean toOut) {
        try {
            roomLogWriter.write(new Date().toString() + " : ");
            roomLogWriter.write(info);
            roomLogWriter.newLine();
        } catch (IOException ex) {
            logError(ex);
        }
        if (toOut) {
            System.out.println(new Date().toString());
            System.out.println(info);
        }
    }

    /**
     * Set up the server socket. Try 999 ports starting from the PORTBASE.  If unable,
     * throw BindException
     * @throws java.io.BindException
     * @throws java.InterruptedException
     * @throws java.io.IOException
     */
    private void initServerSocket() throws BindException, InterruptedException, IOException {
        int i = 0;
        serverSocket = null;
        do {
            try {
                serverSocket = new ServerSocket(PORTBASE + i);
                port = serverSocket.getLocalPort();
                return;
            } catch (BindException ex) {
                i++;
                continue;
            }
        } while (i < 1000);
        throw new BindException("Could not bind to an open port in the port range" + PORTBASE + "to " + (PORTBASE + i));
    }

    /**
     * Listen for incoming connections.  Create a thread to handle the connection
     * which will figure out if the connection request is a the dealer, server or 
     * player then do the appropriate operations.
     * When handling connections, if we are waiting to start the game, then 
     * this method will create and execute a dealer thread to be run in the game
     * This thread will check for new connections every 1s
     * 
     */
    private void listen() throws IOException {
        logInfo("Room " + name + " listening for incoming connections on port: " + port, true);
        serverSocket.setSoTimeout(ROOM_TIMEOUT);
        Thread dealerThread = null;
        while (alive) {
            try {
                Socket socket = serverSocket.accept();
                Thread t = new Thread(new RoomConnectionHandler(socket), "RoomConnectionHandler:" + socket.toString() );
                t.start();
            } catch (SocketTimeoutException ex) {
                if (playerCount == gamedef.getMinPlayers() && dealerThread == null) {
                    if (SAVE_FLAG) {
                        try {
                            String filename = "save/" + name + ".dealer.ser";
                            ObjectInputStream in = new ObjectInputStream(new FileInputStream(filename));
                            logInfo("Loading a dealer for Room:" + name, true);
                            dealer = (Dealer) in.readObject();
                            in.close();
                            if (!dealer.reconnectPlayers(players)) {
                                logInfo("Could not reconnect players, shutting down room", true);
                                return;
                            }
                        } catch (ClassNotFoundException ex1) {
                            logError(ex1);
                            logInfo("Room:" + name + " could not load dealer from save, attempting logfile restore...", true);
                            startNewDealer();
                        } catch (InvalidClassException ex1) {
                            logError(ex1);
                            logInfo("Room:" + name + " could not load dealer from save, attempting logfile restore...", true);
                            startNewDealer();
                        } catch (FileNotFoundException ex1) {                            
                            try {
                                logInfo("Room:" + name + " checking for restore point", true);
                                dealer = MatchRebuilder.restore(name);
                                if (!dealer.reconnectPlayers(players)) {
                                    logInfo("Could not reconnect players, shutting down room", true);
                                    return;
                                }
                            } catch (FileNotFoundException ex2) {
                                //Could not restore a dealer, default to new.                                
                                logInfo("Room:" + name + " could not find restore point", true);
                                logInfo("Room:" + name + " starting a new dealer", true);
                                startNewDealer();
                            } catch (ClassNotFoundException ex2) {                                
                                logInfo("Room:" + name + " error restoring dealer", true);
                                logInfo("Room:" + name + " starting a new dealer", true);
                                startNewDealer();
                            }
                        }
                    } else {
                        startNewDealer();
                    }
                    dealerThread = new Thread(dealer, "Dealer:" + name);
                    dealerThread.start();
                }
                if (dealerThread != null) {
                    if (dealer.isDisconnected() || dealer.isGameOver() || dealer.isError()) {
                        if(SAVE_FLAG) {
                            saveDealer();
                        }
                        String gameStatus = getStatus();
                        logInfo(gameStatus, true);
                        if (runOnce) {
                            shutdown();
                        }
                    }
                }
            }
        }
    }

    /**
     * Load up a new dealer and save it for the first time.
     */
    private void startNewDealer() {
        dealer = new Dealer(name, numHands, gamedef, seed, players);
        if (SAVE_FLAG) {
            saveDealer();
        }
    }

    /**
     * Save the instance of the dealer to file for reloading of the game
     */
    private void saveDealer() {
        try {
            String filename = "save/" + name + ".dealer.ser";
            ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(filename));
            out.writeObject(dealer);
            out.close();
        } catch (IOException ex) {
            logError(ex);
        }
    }

    /**
     * Calls the listen method to wait for connections.  Listen will only end
     * in one of two situations.
     * 1) The server tells the room to shutdown
     * 2) The room has finished playing a game and the constructor or server set
     * the runOnce flag for the room.  The runOnce flag tells the room to only 
     * execute one run of the dealer, and once that ends (either in a disconnect
     * or a gameOver) then the room will shut down
     */
    public void run() {
        try {
            listen();
        } catch (IOException ex) {
            logError(ex);
            alive = false;
        }
    }

    /**
     * Return the current status of the room.  The current hand, players, stats, 
     * and some vague information about the game
     * 
     * @return The room's current status
     */
    public String getStatus() {
        String status = name + ":" + port + ":";
        try {
            status += dealer.getStats();
        } catch (NullPointerException ex) {
            status += "STARTING";
        }
        return status;
    }

    /**
     * Getter for the room's name
     * @return The room name
     */
    public String getName() {
        return name;
    }

    /**
     * Check to see if the room is still alive.  This is for shutting down the
     * rooms from the server
     * @return The alive status of the room
     */
    public boolean isAlive() {
        return alive;
    }

    /**
     * Return the port the room is running on
     * @return an int representing the port
     */
    public int getPort() {
        return port;
    }

    /**
     * Shutdown a room via request from the server or game is over
     */
    public void shutdown() {
        alive = false;
        try {
            serverSocket.close();            
            roomLogWriter.close();
            errorLogWriter.close();
            for (Player p : players) {
                p.shutdown();
            }
        } catch (IOException ex) {
            System.err.println("Error in shutdown of room "+name);
        }
    }

    /**
     * Return a human readable, parser friendly : delimited representation of the
     * Room's info
     * @return A String containing all the info relevant to the Room
     */
    @Override
    public String toString() {
        String roomString = "ROOM:Name:" + name + ":PORT:" + port + ":PLAYERS:" +
                playerCount + "/" + gamedef.getMaxPlayers();
        return roomString;
    }

    /**
     * An Inner Class used to handle incoming connections to the room.
     * These connections should be player connections, and each type of player
     * will have thier own way to connect depending on the type of player.
     * 
     */
    private class RoomConnectionHandler implements Runnable {

        private String connectionArgs;
        private Socket socket;
        private PrintWriter pw;
        private BufferedReader br;

        /**
         * The constructor for the ConnectionHandler inner class.  The connection
         * handler takes a socket passed in from the room, opens a print writer 
         * and buffered reader on the socket and then parses the first argument
         * sent by the connection.  The connections should be players connections
         * or commands send by the server
         * 
         * @param socket A socket passed in to handle the connection in and outputs
         * 
         */
        public RoomConnectionHandler(Socket socket) throws IOException {
            this.socket = socket;
            this.socket.setSoTimeout(TIMEOUT);
            br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            pw = new PrintWriter(socket.getOutputStream());
        }

        /**
         * This method handles the request sent in on the socket.  
         * If the request is of the player type, then handlePlayerRequest is called.  
         * If the request is of the server type, then the handleServerRequest is
         * called.
         * 
         */
        public void run() {
            try {
                while ( (connectionArgs = br.readLine()) != null ) {
                    StringTokenizer st = new StringTokenizer(connectionArgs, ":");
                    if (st.hasMoreTokens()) {
                        String type = st.nextToken();
                        if (type.equalsIgnoreCase("GUIPlayer")) {
                            GUIPlayer p;
                            ObjectOutputStream oos = new ObjectOutputStream(socket.getOutputStream());
                            oos.writeObject(gamedef);
                            oos.flush();
                            int playerPort;
                            ServerSocket ss;
                            Socket playerSocket;
                            for (int i = 0; i < 3; i++) {
                                playerPort = new Random().nextInt(1000) + port;
                                try {
                                    ss = new ServerSocket(playerPort);
                                    pw.println("Listening on port:" + playerPort);
                                    pw.flush();
                                    playerSocket = ss.accept();
                                    String playerName = st.nextToken();
                                    int buyIn = new Integer(st.nextToken()).intValue();
                                    p = new GUIPlayer(playerName, buyIn, playerSocket);
                                    addPlayer(p);
                                    logInfo("Room " + name + " added new player " + p.toString(), true);
                                    return;
                                } catch (BindException ex) {
                                    continue;
                                }
                            }
                            pw.println("ERROR:Could not connect to the server, the server may be full\n.Please try again later.");
                            pw.flush();
                            logError(new BindException("Could not bind a player port"));
                            socket.close();
                            alive = false;
                        } else if (type.equalsIgnoreCase("AAAIPlayer")) {
                            AAAIPlayer p;
                            String playerName = st.nextToken();
                            int buyIn = new Integer(st.nextToken()).intValue();
                            String location = st.nextToken();
                            String execPath = st.nextToken();
                            p = new AAAIPlayer(playerName, buyIn, location, execPath, port, name);
                            addPlayer(p);
                            logInfo("Room " + name + " added new player " + p.toString(), true);
                        } else if (type.equalsIgnoreCase("STATUS")) {
                            getStatus();
                        } else {
                            logWarning("Unknown request: " + type);
                        }
                    }
                }
            } catch (SocketTimeoutException ex) {
                cleanup(true);
            } catch (IOException ex) {
                logError(ex);
                cleanup(false);
            } catch (NullPointerException ex) {
                logError(ex);
                cleanup(false);
            } finally {
                cleanup(true);
            }
        }

        /**
         * Check to see if the name and the seat are already assigned to a player
         * if so, use the next open seat or assign a random int between 1 and 10
         * to the player name
         * 
         * @param newPlayer The player to ba added to the players list
         */
        private void addPlayer(Player newPlayer) {
            for (Player p : players) {
                if (p.getName().equalsIgnoreCase(newPlayer.getName())) {
                    newPlayer.setName(newPlayer.getName() + new Random().nextInt(100));
                    addPlayer(newPlayer);
                    return;
                }

                if (p.getSeat() == newPlayer.getSeat()) {
                    newPlayer.setSeat(p.getSeat() + 1);
                    addPlayer(newPlayer);
                    return;
                }
            }
            //If we are using Doyles Game, ignore the buyin
            if (gamedef.isDoylesGame()) {
                newPlayer.setBuyIn(gamedef.getStackSize());
            }
            players.add(newPlayer);
            playerCount++;
        }

        private void cleanup(boolean stillAlive) {
            try {
                br.close();
                pw.close();
                socket.close();
                alive = stillAlive;
            } catch (IOException ex) {
                logError(ex);
                return;
            }

        }
    }

    private static void loadSettings() throws ParserConfigurationException,
            SAXParseException, SAXException, IOException,
            InterruptedException {
        //Get the Room info                       
        XMLParser parser;
        try {
            parser = new XMLParser("config/ROOM.config.xml");
        } catch (FileNotFoundException ex) {
            System.err.println("Could not find ROOM.config.xml in config directory, using defaults...");
            return;
        }

        NodeList nl = parser.parseElements("Room");
        if (nl.getLength() < 1) {
            return;
        }
        Node roomNode = nl.item(0);
        if (roomNode.getNodeType() == Node.ELEMENT_NODE) {
            TIMEOUT = parser.getIntFromNode(roomNode, "Timeout");
            int configport = parser.getIntFromNode(roomNode, "Portbase");
            PORTBASE = (configport == 0 ? PORTBASE : configport);
            SAVE_FLAG = parser.getBooleanFromNode(roomNode, "Save");            
        }
    }
}
