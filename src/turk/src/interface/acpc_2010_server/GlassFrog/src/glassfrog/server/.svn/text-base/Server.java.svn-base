package glassfrog.server;

import glassfrog.model.Gamedef;
import glassfrog.tools.XMLParser;
import glassfrog.tools.XMLValidator;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.BindException;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.net.SocketTimeoutException;
import java.util.ArrayList;
import java.util.Date;
import java.util.Random;
import java.util.StringTokenizer;
import java.util.concurrent.CopyOnWriteArrayList;
import javax.xml.parsers.ParserConfigurationException;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;
import org.xml.sax.SAXParseException;

/**
 * The Server class is a persistant java server that has a {@link ServerSocket}
 * serving on port 9000.  This ServerSocket handles incoming connections and 
 * sends back information depending on the request made.  The Server is capable 
 * of creating a {@link Room}, querying information about a Room or general 
 * status
 *  
 * Each connection to the server is forked into a separate thread to allow 
 * multiple conncurent connections to the Server.  Each thread only stays alive 
 * for the duration of the request connection and then is terminated.
 * 
 * @author jdavidso
 */
public class Server implements Runnable {

    // TODO: I don't know if CopyOnWriteArrayLists are the best way to ensure
    // thread safety.  This might require actual synchronization.
    private static CopyOnWriteArrayList<Room> rooms = new CopyOnWriteArrayList<Room>();
    private static CopyOnWriteArrayList<Integer> portList = new CopyOnWriteArrayList<Integer>();
    private static CopyOnWriteArrayList<String> keyList = new CopyOnWriteArrayList<String>();
    private static CopyOnWriteArrayList<Thread> liveThreads = new CopyOnWriteArrayList<Thread>();
    private static CopyOnWriteArrayList<String> finishedList = new CopyOnWriteArrayList<String>();
    private static CopyOnWriteArrayList<String> errorList = new CopyOnWriteArrayList<String>();
    private static ServerSocket ss;
    private BufferedWriter errorLogWriter, serverLogWriter;
    private static boolean alive = true;
    private static int PORT = 9000;
    private static int TIMEOUT = 10000;    
    private static String DUPLICATE_POLICY = "NEVER";
    private static final int CONNECTION_MAX = 64;

    /**
     * The constructor for the server starts up a server on port 9000 and 
     * opens a ServerSocket to handle server requests
     * @param timeout A timeout used for server connections
     * @param port a port to start the server on
     * @throws java.net.BindException
     * @throws java.io.IOException
     */
    public Server(int timeout, int port) throws BindException, IOException {
        ss = new ServerSocket(PORT);
        ss.setSoTimeout(TIMEOUT);
        System.out.println("Server started at "+(new Date().toString()));
        System.out.println("PORT = " + PORT);
        System.out.println("TIMEOUT = " + TIMEOUT);
        System.out.println("DUPLICATE_POLICY = " + DUPLICATE_POLICY);
        initLogging();
    }

    /**
     * Initialize the logs for the game.    
     */
    private void initLogging() {        
        String logPath = "logs/";
        try {
            errorLogWriter = new BufferedWriter(new FileWriter(logPath + "server.err", true));
            serverLogWriter = new BufferedWriter(new FileWriter(logPath + "server.log", true));
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
            System.err.println("Server Logging Error: ");
            ex1.printStackTrace();
        }
    }

    /**
     * Specify and extra message to the error logger
     * @param ex 
     * @param message
     */
    public void logError(Exception ex, String message) {
        try {
            errorLogWriter.write(new Date().toString() + " : " + message);
            errorLogWriter.newLine();
        }catch (IOException ex1) {
            System.err.println("Logging Error: ");
            ex1.printStackTrace();
        }
        logError(ex);
    }

    /**
     * Utility for logging a warning message to the errorLogger
     * @param warningMessage A message to log to the error log
     */
    private void logWarning(String warningMessage) {
        try {
            errorLogWriter.write(new Date().toString() + " : ");
            errorLogWriter.write("WARNING: "+warningMessage);
            errorLogWriter.newLine();
        } catch (IOException ex) {
            logError(ex);
        }
    }

    /**
     * Log a info to the serverLogger
     * @param info the message to log to the room log 
     */
    private void logInfo(String info) {
        try {
            serverLogWriter.write(new Date().toString() + " : " + info);
            serverLogWriter.newLine();
        } catch (IOException ex) {
            logError(ex);
        }
    }

    /**
     * The run method for the server.  A server will busy wait and listen for 
     * incoming connections on it's ServerSocket and then fork a ServerConnectionHandler
     * thread to deal with the connections while the server is still alive
     */
    public void run() {
        while (alive) {
            try {
                if (liveThreads.size() < CONNECTION_MAX) {
                    Socket s = ss.accept();
                    Thread t = new Thread(new ServerConnectionHandler(s), "ServerConnectionHandler:" + s.toString() );
                    t.start();
                    liveThreads.add(t);
                } else {
                    logWarning("Max connections reached.  Try again in 5s");
                    Thread.sleep(4000);
                }
                houseKeeping();
            } catch (SocketTimeoutException ex) {
                houseKeeping();
            } catch (IOException ex) {
                logError(ex);
                System.exit(-1);
            } catch (InterruptedException ex) {
                logError(ex);
            }
        }
        try {
            ss.close();
        } catch (IOException ex) {
            logError(ex);
            System.exit(-1);
        }
    }

    /**
     * Do some housekeeping whenever a new connection is started or every 30 seconds
     * on the socket timeout
     */
    private void houseKeeping() {
        //Some housekeeping every 10s
        for (Room r : rooms) {
            if (!r.isAlive()) {
                if (keyList.contains(r.getName())) {
                    System.out.println("Freeing Key: " + r.getName());
                    logInfo("Freeing Key: " + r.getName());
                    keyList.remove(r.getName());
                }
                r.shutdown();
                String status = r.getStatus();
                if (status.startsWith(r.getName() + ":"+r.getPort()+":ERROR") || status.startsWith(r.getName() + ":"+r.getPort()+":DISCONNECTED")) {
                    errorList.add(status);
                } else if (status.startsWith(r.getName() + ":"+r.getPort()+":FINISHED")) {
                    finishedList.add(status);
                }
                System.out.println("Removing Room: " + r.getName() + " from active list");
                logInfo("Removing Room: " + r.getName() + " from active list");
                rooms.remove(r);
            }
        }
        for (Thread t : liveThreads) {
            if (!t.isAlive()) {
                liveThreads.remove(t);
            }
        }
    }

    /**
     * A class used to handle incoming connections to the server.  This class is 
     * used to parse the request arguments to the server such as the requests to add 
     * and kill rooms, info requests from rooms and other information regarding the 
     * state of the server
     * @author jdavidso
     */
    public class ServerConnectionHandler implements Runnable {

        private PrintWriter pw;
        private BufferedReader br;
        private Socket socket;
        private final int TIMEOUT = 10000;
        private final Object lock = new Object();

        /**
         * The ServerConnectionHandler takes the socket that the ServerSocket 
         * gets from an accepted connection.  A PrintWriter and BufferedReader
         * are then set up to get the incoming request and possibly return any
         * information to the sender.
         * 
         * After 10s of inactivity from a socket, the socket will timeout
         * 
         * @param socket A Socket passed in from the server
         * @throws java.io.IOException Any exceptions from the socket handleing
         */
        public ServerConnectionHandler(Socket socket) throws IOException {
            this.socket = socket;
            this.socket.setSoTimeout(TIMEOUT);
            this.br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            this.pw = new PrintWriter(socket.getOutputStream());
        }

        /**
         * A wrapper to handle the requests from the server so that this can be
         * invoked in a thread
         */
        public void run() {
            while (socket.isConnected()) {
                try {
                    handleRequest();
                } catch (InterruptedException ex) {
                    logError(ex);
                } catch (SocketTimeoutException ex) {
                    try {
                        logError(ex);
                        br.close();
                        pw.close();
                        socket.close();
                        return;
                    } catch (IOException ex1) {
                        logError(ex);
                    }
                } catch (SocketException ex) {
                    return;
                } catch (IOException ex) {
                    try {
                        logError(ex);
                        br.close();
                        pw.close();
                        socket.close();
                        return;
                    } catch (IOException ex1) {
                        logError(ex);
                    }
                }
            }
        }

        /**
         * Handles any request made from a connection to the server
         * @throws java.io.IOException
         * @throws java.socket.SocketTimeoutException
         */
        private void handleRequest() throws IOException, SocketTimeoutException,
                InterruptedException {
            String request = br.readLine();
            StringTokenizer st;
            try {
                st = new StringTokenizer(request, ":");
            } catch (NullPointerException ex) {
                logWarning("Server request " + request + "empty or missing parameters");
                pw.println("Invalid request, use HELP to see list of valid request");
                pw.flush();
                br.close();
                pw.close();
                socket.close();
                return;
            }
            if (st.countTokens() < 1) {
                logWarning("Server request " + request + "empty or missing parameters");
                pw.println("Invalid request, use HELP to see list of valid request");
                pw.flush();
                return;
            }
            String requestType = st.nextToken();

            if (requestType.equalsIgnoreCase("LIST")) {
                //List the active rooms
                pw.println(list());
                pw.flush();
            } else if (requestType.equalsIgnoreCase("CLEAR")) {
                errorList.clear();
                finishedList.clear();
                if (st.countTokens() > 0 && st.nextToken().equalsIgnoreCase("ALL")) {
                    keyList.clear();
                    portList.clear();
                }
            } else if (requestType.equalsIgnoreCase("STATUS")) {
                //Handle Status Request
                if (st.countTokens() > 0) {
                    while (st.hasMoreTokens()) {
                        pw.println(getStatus(st.nextToken()));
                        pw.flush();
                    }
                } else {
                    pw.println("Invalid use\n" + getUsage("STATUS"));
                    pw.flush();
                    return;
                }
            } else if (requestType.equalsIgnoreCase("KILL")) {
                //Handle Kill Request
                if (st.countTokens() > 0) {
                    while (st.hasMoreTokens()) {
                        kill(st.nextToken());
                    }
                } else {
                    pw.println("Invalid use\n" + getUsage("KILL"));
                    pw.flush();
                }
            } else if (requestType.equalsIgnoreCase("NEW")) {
                //Handle New Room from Command Line                
                if (st.countTokens() < 4) {
                    pw.println("Invalid use\n" + getUsage("NEW"));
                    pw.flush();
                    return;
                }
                String name = st.nextToken();
                int hands = new Integer(st.nextToken()).intValue();
                String gamedefPath = st.nextToken();
                int seed = new Integer(st.nextToken()).intValue();
                String botlist = "";
                if (st.countTokens() > 0) {
                    botlist = st.nextToken();
                    botlist = botlist.replace(" ", ":");
                }
                int port = startRoom(name, hands, gamedefPath, seed);
                if (port != -1) {
                    pw.println("New room added successfully on port:" + port);
                    pw.flush();
                    if (botlist.length() != 0) {
                        BotManager bm = new BotManager(port);
                        StringTokenizer botST = new StringTokenizer(botlist, "|");
                        while (botST.hasMoreTokens()) {
                            bm.addBot(botST.nextToken());
                        }
                        bm.startBots();
                    }
                } else {
                    logWarning("Room " + name + "could not start");
                    pw.println("ERROR:Could not start a new room, check the logfile for more information");
                    pw.flush();
                }
            } else if (requestType.equalsIgnoreCase("CONFIG")) {
                //Handle new room from config file
                if (st.countTokens() < 1) {
                    pw.println("Invalid use\n" + getUsage("CONFIG"));
                    pw.flush();
                    return;
                }
                try {
                    parseConfigFile("config/" + st.nextToken(), "", -1);
                } catch (ParserConfigurationException ex) {
                    logError(ex);
                } catch (SAXParseException ex) {
                    logError(ex);
                } catch (SAXException ex) {
                    logError(ex);
                }
            } else if (requestType.equalsIgnoreCase("AUTOCONNECT")) {
                /* Auto create game using the key given.  First check the key, 
                 * if it is valid, create the game, if not, return invalid key message
                 */
                if (st.countTokens() < 1) {
                    pw.println("ERROR:Key not specified");
                    pw.flush();
                    return;
                }
                String key = st.nextToken().toUpperCase();
                if (keyList.contains(key)) {
                    pw.println("ERROR:Key already in use, Please try another key or " +
                            "logout where the first key is in use");
                    pw.flush();
                } else {
                    try {
                        autoConnect(key);
                    } catch (NullPointerException ex) {
                        logWarning("Invalid seed from key" + key);
                        pw.println("ERROR:Invalid key, Please check the key for " +
                                "errors and try again");
                        pw.flush();
                    } catch (ParserConfigurationException ex) {
                        logError(ex);
                        pw.println("ERROR:Validation server down, please try again later");
                        pw.flush();
                    } catch (SAXParseException ex) {
                        logError(ex);
                        pw.println("ERROR:Validation server down, please try again later");
                        pw.flush();
                    } catch (SAXException ex) {
                        logError(ex);
                        pw.println("ERROR:Validation server down, please try again later");
                        pw.flush();
                    }
                }
            } else if (requestType.equalsIgnoreCase("GETINFO")) {
                /* Monitor Script, return some stats to the python monitor */
                pw.println("Rooms in Use: " + rooms.size() + ": Keys In Use: " + keyList.size());
                pw.flush();
            } else if (requestType.equalsIgnoreCase("HELP")) {
                String helpRequest = "";
                if (st.countTokens() > 0) {
                    helpRequest = st.nextToken();
                }
                pw.println(getUsage(helpRequest));
                pw.flush();
            } else {
                pw.println("Invalid request, use HELP to see list of valid request");
                pw.flush();
            }
            socket.close();
        }

        private String getUsage(String helpRequest) {
            String usageString = "";
            if (helpRequest.length() == 0) {
                usageString = "Usage: Valid commands are\nLIST\nCLEAR\nSTATUS\nKILL\nNEW\nCONFIG\nAUTONCONNECT\nGETINFO\nHELP\n" +
                        "For specific help on each command, type HELP:COMMAND\r\r\n";
            } else {
                if (helpRequest.equalsIgnoreCase("LIST")) {
                    usageString = "Sends a list of the active rooms";
                } else if (helpRequest.equalsIgnoreCase("CLEAR")) {
                    usageString = "Clears the errorList, finishedList\nUse CLEAR:ALL to clear keyList and portList as well";
                } else if (helpRequest.equalsIgnoreCase("STATUS")) {
                    usageString = "Query the status of a particular room.\nSTATUS:ROOMNAME to use";
                } else if (helpRequest.equalsIgnoreCase("KILL")) {
                    usageString = "Kill a room or all of the rooms or the whole server.\nKILL:ROOMNAME|ALL|SERVER";
                } else if (helpRequest.equalsIgnoreCase("NEW")) {
                    usageString = "Start a new room on the server.\nNEW:NAME:NUMHANDS:GAMEDEF:SEED:";
                } else if (helpRequest.equalsIgnoreCase("CONFIG")) {
                    usageString = "Start a new room on the server with a config file.\nAll config paths are relative to the config directory on the server\n" +
                            "CONFIG:CONFIGPATH";
                } else if (helpRequest.equalsIgnoreCase("AUTOCONNECT")) {
                    usageString = "Autoconnect starts a room using a key.\nThis is for setting up matches where an administrator can supply users with keys and those" +
                            "keys then supply room information from the keys.xml file.\nAUTOCONNECT:KEY";
                } else if (helpRequest.equalsIgnoreCase("GETINFO")) {
                    usageString = "Supplies general server information.  Can be used in conjunction with the monitorServer.py script to test if the server is alive\n";
                } else if (helpRequest.equalsIgnoreCase("HELP")) {
                    usageString = "Displays this help";
                } else {
                    usageString = "Invalid request type\nUsage: Valid commands are\nLIST\nSTATUS\nKILL\nNEW\nCONFIG\nCOMMANDLINE\nAUTONCONNECT\nGETINFO\nHELP\n" +
                            "For specific help on each command, type HELP:COMMAND";
                }
            }
            return usageString;
        }

        /**
         * The auto connect routine for a key value and the online client
         * @param key
         */
        private void autoConnect(String key) throws NullPointerException,
                ParserConfigurationException, SAXParseException, SAXException,
                IOException,
                InterruptedException {
            int seed;
            String response, config;
            response = validateKey(key);
            StringTokenizer st = new StringTokenizer(response, ":");
            pw.println("Username:" + st.nextToken());
            pw.flush();
            seed = new Integer(st.nextToken()).intValue();
            config = st.nextToken();
            keyList.add(key);
            parseConfigFile("config/" + config, key, seed);
        }

        /**
         * Lookup a seed and username from a specific key value.  
         * Used for matching users to logs and seeds to recreate play
         * @param key a String used for the key value pair of the seed
         */
        private String validateKey(String key) throws NullPointerException,
                ParserConfigurationException, SAXParseException,
                SAXException, IOException {
            int seed = -1;
            String userName = "", config = "";
            XMLParser parser = parser = new XMLParser("keys/keys.xml");
            NodeList nl = parser.parseElements("Key");
            for (int i = 0; i < nl.getLength(); i++) {
                Node keyNode = nl.item(i);
                if (keyNode.getNodeType() == Node.ELEMENT_NODE && parser.getStringFromNode(keyNode, "KeyValue").equalsIgnoreCase(key)) {
                    userName = parser.getStringFromNode(keyNode, "UserName");
                    seed = parser.getIntFromNode(keyNode, "Seed");
                    config = parser.getStringFromNode(keyNode, "Config");
                }
            }
            if (seed == -1) {
                throw new NullPointerException("Key not found");
            }
            return userName + ":" + seed + ":" + config;
        }

        /**
         * Get the status for a given room name, or for all the rooms if ALL is
         * specified as the argument.  Rooms are delimited by ||
         * @param roomName A name for the specific status
         * @return The status of a given room or all the rooms
         */
        private String getStatus(String roomName) {
            String status = "";
            //Check for Running, if not running then:
            //Check the finished queue, then the Error queue,
            //if not finished or error, then None

            //Check for running rooms, return the status if active
            for (Room r : rooms) {
                if (r.getName().equalsIgnoreCase(roomName)) {
                    status = r.getStatus();
                }
            }
            if (status.length() != 0) {
                return status;
            } else {
                //Check now the finished and error queues
                for (String message : finishedList) {
                    if (message.startsWith(roomName)) {
                        status = message;
                        return status;
                    }
                }
                for (String message : errorList) {
                    if (message.startsWith(roomName)) {
                        status = message;
                        return status;
                    }
                }
            }
            status = roomName + ":NONE";
            return status;
        }

        /**
         * Get a list of all the Running, Finished, Disconnected and Errored Rooms
         * @return
         */
        private String list() {
            String roomList = "";
            //Get the Running list
            for (Room r : rooms) {
                roomList += r.getStatus() + "\n";
            }
            //Get the Error and Finished lists
            for (String message : finishedList) {
                roomList += message + "\n";
            }
            for (String message : errorList) {
                roomList += message + "\n";
            }
            return roomList;
        }

        /**
         * Parse the given config file.  Config files can have a number of options
         * and requests in them, see the sample CONFIG.SAMPLE for more information
         * on specific config file options
         * 
         * @param path A path to a given XML config file
         * @param name A @String for the name of the room, blank to use name 
         * specified in the config file                  
         * @param seed Specify the seed.  Use -1 to grab from config file
         */
        private void parseConfigFile(String path, String name, int seed) throws ParserConfigurationException,
                SAXParseException, SAXException, IOException,
                InterruptedException {
            int port = -1;
            XMLValidator validator = new XMLValidator("xsd/config.xsd");
            if (!validator.validateXML(path)) {
                logError(new ParserConfigurationException("Check config.xsd to ensure " + path + " fits the schema"));
                return;
            }

            //Get the Room info                       
            XMLParser parser;
            parser = new XMLParser(path);

            NodeList nl = parser.parseElements("Room");
            if (nl.getLength() < 1) {
                //No rooms found in config file.  Should be an error of some sorts
                return;
            }
            Node roomNode = nl.item(0);
            if (roomNode.getNodeType() == Node.ELEMENT_NODE) {
                if (name.equalsIgnoreCase("")) {
                    name = parser.getStringFromNode(roomNode, "Name");
                }
                int hands = parser.getIntFromNode(roomNode, "Hands");
                if(hands < 1) {
                    pw.println("ERROR:No hands in config file.");
                    pw.flush();
                    return;
                }
                String gamedefPath = parser.getStringFromNode(roomNode, "Gamedef");
                if(gamedefPath.equalsIgnoreCase("None")) {
                    pw.println("ERROR:No gamedef in config file.");
                    pw.flush();
                    return;
                }
                if (seed == -1) {
                    seed = parser.getIntFromNode(roomNode, "Seed");
                }
                port = startRoom(name, hands, gamedefPath, seed);
                if (port == -1) {
                    logWarning("Room " + name + "could not start");
                    pw.println("ERROR:Could not start a new Room");
                    pw.flush();
                    return;
                }
                portList.add(port);
                pw.println("New room started on port:" + port);
                pw.flush();
            }
            //Get the BotList info            
            BotManager bm = new BotManager(port);
            nl = parser.parseElements("Bot");
            for (int i = 0; i < nl.getLength(); i++) {
                Node botNode = nl.item(i);
                if (botNode.getNodeType() == Node.ELEMENT_NODE) {
                    String type = parser.getStringFromNode(botNode, "Type");
                    String botName = parser.getStringFromNode(botNode, "Name");
                    int buyIn = parser.getIntFromNode(botNode, "BuyIn");
                    String location = parser.getStringFromNode(botNode, "Location");
                    String executable = parser.getStringFromNode(botNode, "Executable");
                    bm.addBot(type + ":" + botName + ":" + buyIn + ":" + location + ":" + executable);
                }
            }
            bm.startBots();
        }

        /**
         * Shudown a specific room or all of the rooms if the ALL argument is 
         * passed in as the roomName
         * @param roomName The name of the room to kill
         */
        private void kill(String roomName) throws IOException {
            for (Room r : rooms) {
                if (roomName.equalsIgnoreCase("ALL") ||
                        r.getName().equalsIgnoreCase(roomName)) {
                    r.shutdown();
                    pw.println("Room " + roomName + " shutting down");
                    pw.flush();
                }
            }
            if (roomName.equalsIgnoreCase("SERVER")) {
                killServer();
            }
        }

        /**
         * Closes the current connection and sets the alive boolean to false 
         * telling the server to stop listening for incoming connections and to 
         * exit
         * 
         * @throws java.io.IOException
         */
        private void killServer() throws IOException {
            pw.println("Server shutting down");
            pw.flush();
            alive = false;
        }

        /**
         * Start up a new room
         * @param name The name of the room to start
         * @param hands number of hands to plat
         * @param gamedefPath the path to the gamedef file
         * @param seed the seed for the cards
         * @return the port the room is on
         */
        private int startRoom(String name, int hands, String gamedefPath, int seed) throws IOException, InterruptedException {
            /* Parse the gamedef */
            Gamedef gamedef;            
            try {
                gamedef = new Gamedef("gamedef/" + gamedefPath);
            } catch (ParserConfigurationException ex) {
                logError(ex);
                return -1;
            } catch (SAXParseException ex) {
                logError(ex);
                return -1;
            } catch (SAXException ex) {
                logError(ex);
                return -1;
            } catch (IOException ex) {
                logError(ex);
                return -1;
            }
            for (Room r : rooms) {
                if (r.getName().equalsIgnoreCase(name)) {
                    if(DUPLICATE_POLICY.equalsIgnoreCase("ALLOW")) {
                        continue;
                    } else if(DUPLICATE_POLICY.equalsIgnoreCase("NEVER")) {
                        logWarning("Tried to start duplicate room "+name+" with NEVER policy");
                        return -1;
                    } else if(DUPLICATE_POLICY.equalsIgnoreCase("AUTO")) {
                        name = name + new Random().nextInt(100);
                        startRoom(name, hands, gamedefPath, seed);
                        break;
                    }
                }
            }
            Room r = new Room(name, hands, gamedef, seed);
            rooms.add(r);
            Thread t = new Thread(r, "Room:" + name);
            t.start();
            return r.getPort();
        }
    }

    /**
     * Start the server from the command line.  Can also be started via the class
     * @param args Command line args
     */
    public static void main(String[] args) {
        try {
            try {
                loadSettings();
            } catch (ParserConfigurationException ex) {
                ex.printStackTrace();
            } catch (SAXParseException ex) {
                ex.printStackTrace();
            } catch (SAXException ex) {
                ex.printStackTrace();
            }
            Server instance = new Server(PORT, TIMEOUT);
            Thread t = new Thread(instance, "Server:" + PORT);
            t.start();
            while (t.isAlive()) {
                Thread.sleep(100000);
            }
        } catch (InterruptedException ex) {
            System.err.println("Server thread caught Interrupted Exception in main");
            ex.printStackTrace();
        } catch (BindException ex) {
            System.err.println("Could not bind server port");
            ex.printStackTrace();
        } catch (IOException ex) {
            System.err.println("Server thread caught IO Exception in main");
            ex.printStackTrace();
        }
    }

    private static void loadSettings() throws ParserConfigurationException,
            SAXParseException, SAXException, IOException,
            InterruptedException {
        //Get the Room info                       
        XMLParser parser;
        try {
            parser = new XMLParser("config/SERVER.config.xml");
        } catch (FileNotFoundException ex) {
            System.err.println("Could not find SERVER.config.xml in config directory, using defaults...");
            return;
        }

        NodeList nl = parser.parseElements("Server");
        if (nl.getLength() < 1) {
            return;
        }
        Node serverNode = nl.item(0);
        if (serverNode.getNodeType() == Node.ELEMENT_NODE) {
            int port = parser.getIntFromNode(serverNode, "Port");
            PORT = (port == 0 ? PORT : port);
            TIMEOUT = parser.getIntFromNode(serverNode, "Timeout");            
            String policy = (parser.getStringFromNode(serverNode, "DuplicatePolicy"));
            DUPLICATE_POLICY = policy.equalsIgnoreCase("None") ? DUPLICATE_POLICY : policy;
        }
    }
}
