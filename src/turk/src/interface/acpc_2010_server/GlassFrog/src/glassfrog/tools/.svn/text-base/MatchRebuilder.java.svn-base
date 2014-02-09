package glassfrog.tools;

import glassfrog.model.Dealer;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.StringTokenizer;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * This class is used to rebuild a match from a log file.  This is in the event
 * that there was a server crash, we need to rebuild a match from a log in order
 * to save a serialized version of the match at the point of the log.
 * @author jdavidso
 */
public class MatchRebuilder {   

    /**
     * Empty constructor
     */
    public MatchRebuilder() {}

    /**
     * Restore a match from the last state found in the log file.  Hopefully you
     * don't loose the ser and log files, or you are sunk
     * @param key The key we wish to recreate the serial file for.
     * @return True on sucessfully resoring the dealer.ser file for the game
     * @throws FileNotFoundException
     * @throws IOException
     * @throws ClassNotFoundException
     */
    public static Dealer restore(String key) throws FileNotFoundException, IOException, ClassNotFoundException {
        BufferedReader br;
        int handNumber;
        String name;
        int stack;
        int seat;
        int position;
        int score;
        //Get the last saved file.  If one doesn't exist we will have to create it.
        String filename = "save/" + key + ".dealer.ser";
        ObjectInputStream in = new ObjectInputStream( new FileInputStream(filename) );
        Dealer dealer = (Dealer) in.readObject();
        in.close();
        //Parse the hand and score info from the 
        String logName = "logs/" + key + ".dealer.rawlog";
        br = new BufferedReader(new FileReader(logName));
        String nextLine;
        while ((nextLine = br.readLine()) != null) {
            if (nextLine.startsWith("STATS")) {
                StringTokenizer st = new StringTokenizer(nextLine, ":");
                st.nextToken();
                st.nextToken();
                st.nextToken();
                st.nextToken();
                try {
                    handNumber = new Integer(st.nextToken()).intValue();
                    //Restore the dealer to the last hand played
                    dealer.restoreToHand(handNumber);
                } catch (NumberFormatException ex) {
                    System.err.println("Could not parse hand number, exiting");
                    throw new ClassNotFoundException();
                }
            } else if (nextLine.startsWith("AAAIPLAYER") || nextLine.startsWith("GUIPLAYER")) {
                //Setup a AAAI Player
                StringTokenizer st = new StringTokenizer(nextLine, ":");
                st.nextToken();
                st.nextToken();
                name = st.nextToken();
                st.nextToken();
                try {
                    stack = new Integer(st.nextToken()).intValue();
                    st.nextToken();
                    seat = new Integer(st.nextToken()).intValue();
                    st.nextToken();
                    position = new Integer(st.nextToken()).intValue();
                    st.nextToken();
                    score = new Integer(st.nextToken()).intValue();
                    if (!dealer.restorePlayer(name, seat, stack, position, score)) {
                        System.err.println("Could not restore player " + name + ", exiting");
                        throw new ClassNotFoundException();
                    } 
                } catch (NumberFormatException ex) {
                    System.err.println("Could not parse player info, exiting");
                    throw new ClassNotFoundException();
                }
            }
        }
        br.close();

        //Write out the new serialized file           
        System.out.println("Restored session: "+key);
        System.out.println("Writing new dealer to file " + filename);
        FileOutputStream fos = new FileOutputStream(filename);
        ObjectOutputStream out = new ObjectOutputStream(fos);
        out.writeObject(dealer);
        out.close();
        return dealer;
    }

    /**
     * Start the server from the command line.  Can also be started via the class
     * @param args Command line args
     */
    public static void main(String[] args) {        
        try {
            MatchRebuilder.restore(args[0]);
        } catch (FileNotFoundException ex) {
            Logger.getLogger(MatchRebuilder.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(MatchRebuilder.class.getName()).log(Level.SEVERE, null, ex);
        } catch (ClassNotFoundException ex) {
            Logger.getLogger(MatchRebuilder.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
}
