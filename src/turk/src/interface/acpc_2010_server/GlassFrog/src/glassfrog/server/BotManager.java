package glassfrog.server;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;

/**
 * The BotManager class is used to start up bots specified in the config file of
 * the server.  The BotManager uses a ArrayList passed in the constructor to 
 * initiate the execution of the bots to the server to ensure tha the bots are 
 * started on the correct socket
 * 
 * @author jdavidso
 */
public class BotManager {

    private ArrayList<String> botList;
    private int port;
    private Socket socket;
    private PrintWriter pw;
    private BufferedReader br;
    
    /**
     * The constructor takes a port the Room is on to connect the bots.
     * Hardcoded to the localhost for now
     * 
     * @param port an int value representing the Room we are going to connect to's
     * port value
     */
    public BotManager(int port) {
        this.port = port;
        botList = new ArrayList<String>();
        try {
            socket = new Socket("127.0.0.1", port);
            pw = new PrintWriter(socket.getOutputStream());
            br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            System.out.println("BotManager initialized on port:"+port);
        } catch (UnknownHostException ex) {
            System.err.println("BotManager recieved UknownHostException:"+ex.toString());
        } catch (IOException ex) {
            System.err.println("BotManager recieved IOException:"+ex.toString());
        }
    }
    
    /**
     * Add a bot to the botList waiting to be executed
     * @param botString A String representing the bot to be executed
     */
    public void addBot(String botString) {
        botList.add(botString);        
    }
    
    /**
     * For each bot in the bot list, get the port the room is listening on and then
     * exec the bot command on the remote or local machine
     */
    public void startBots() {                
        for(String bot : botList) {            
            pw.println(bot);
            pw.flush();
            System.out.println("Starting bot:"+bot);
        }
    }         
}
