/*
 * TCPPlugin.java
 *
 * Created on April 27, 2006, 4:46 PM
 */
import java.awt.event.*;

import com.biotools.meerkat.*;
import com.biotools.meerkat.util.*;
import java.io.*;
import java.net.*;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;

import ca.ualberta.cs.poker.free.server.*;
import java.awt.*;
import javax.swing.*;
/**
 *
 * @author Martin Zinkevich
 */
public class TCPPlugin implements Player, ActionListener{
    String ALWAYS_CALL_MODE = "ALWAYS_CALL_MODE";
    Card holeCard1;
    Card holeCard2;
    Card oppCard1;
    Card oppCard2;
    int uofagameIndex;
    String bettingSequence;
    PrintStream out;
    PrintStream botout;
    int paseat;
    GameInfo info;
    Preferences prefs;
    String executable="";
    String outputFile="BotOutputFile.log";
    String directory;
    String interactionType;
    boolean handBegun;
    /**
     * The socket clients connect to.
     */
    public ServerSocket socket;
    
    
    /**
     * The server-side agent for the player
     */
    PlayerAgent agent;
    
    /** Creates a new instance of TCPPlugin */
    public TCPPlugin(){
    	setupOut();
    }
    
    public void setupOut(){
        try{
        out = new PrintStream(new FileOutputStream("TCPPlugin.log"));
        } catch (FileNotFoundException fnf){
            out = System.out;
        }
        prefs=new Preferences();
        uofagameIndex = -1;
        handBegun = false;
    }
    
    JTextField outFileField;
    JTextField executableField;
    JButton saveButton;
    JButton cancelButton;
	JButton browseExecutableButton;
    JButton browseOutFileButton;
	JPanel settingsPanel;

    public void loadFromPrefs(){
    	if (prefs!=null){
    	executable = prefs.get("EXECUTABLE", "");
    	outputFile = prefs.get("OUTPUT", "BotOutputFile.log");
    	interactionType = prefs.get("INTERACTIONTYPE", "Classic");
        if (settingsPanel!=null){
    	executableField.setText(executable);
    	outFileField.setText(outputFile);
        }
    	}
    }
    
    JRadioButton jLoadLater;
    JRadioButton jLoadNow;
    JRadioButton jInternet;
    
   /**
    * If you implement the getSettingsPanel() method, your bot will display
    * the panel in the Opponent Settings Dialog.
    * @return a GUI for configuring your bot (optional)
    */
   public JPanel getSettingsPanel() {
      settingsPanel = new JPanel(new GridLayout(0,1));
    	  // new JPanel(new GridLayout(3,3));
      /*final JCheckBox acMode = new JCheckBox("Always Call Mode", prefs.getBooleanPreference(ALWAYS_CALL_MODE));
      acMode.addItemListener(new ItemListener() {
         public void itemStateChanged(ItemEvent e) {
            prefs.setPreference(ALWAYS_CALL_MODE, acMode.isSelected());
         }        
      });
      jp.add(acMode);*/
      jLoadLater = new JRadioButton("Classic");
      jLoadNow = new JRadioButton("Start Local Bot");
      jInternet = new JRadioButton("Open port only");
      
      jLoadLater.addActionListener(this);
      jLoadNow.addActionListener(this);
      jInternet.addActionListener(this);
      
      settingsPanel.add(jLoadLater);
      settingsPanel.add(jLoadNow);
      settingsPanel.add(jInternet);
      
      ButtonGroup bg = new ButtonGroup();
      bg.add(jLoadLater);
      bg.add(jLoadNow);
      bg.add(jInternet);
      if (interactionType.equals("Classic")){
        jLoadLater.setSelected(true);
      } else if (interactionType.equals("Local")){
    	jLoadNow.setSelected(true);
      } else if (interactionType.equals("Port")){
    	  jInternet.setSelected(true);
      } else {
    	  interactionType = "Classic";
    	  jLoadLater.setSelected(true);
      }
      
      JPanel executablePanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
      
      executablePanel.add(new JLabel("Executable"));
      executableField = new JTextField(20);
      executableField.addActionListener(this);
      executablePanel.add(executableField);
      browseExecutableButton = new JButton("Browse");
      browseExecutableButton.addActionListener(this);
      executablePanel.add(browseExecutableButton);
      settingsPanel.add(executablePanel);
      
      JPanel outFilePanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
      outFilePanel.add(new JLabel("Output File"));
      outFileField = new JTextField(20);
      outFileField.addActionListener(this);
      outFilePanel.add(outFileField);
      browseOutFileButton = new JButton("Browse");
      browseOutFileButton.addActionListener(this);
      outFilePanel.add(browseOutFileButton);
      settingsPanel.add(outFilePanel);
      
      if (!interactionType.equals("Local")){
    	  disableSettings();
      }
      
      
      JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
      cancelButton = new JButton("Cancel");
      cancelButton.addActionListener(this);
      buttonPanel.add(cancelButton);
      settingsPanel.add(new Label());
      saveButton = new JButton("Save");
      saveButton.addActionListener(this);
      buttonPanel.add(saveButton);
      settingsPanel.add(buttonPanel);
      
      loadFromPrefs();
      return settingsPanel;
   }
   
  
   public void setEnabledSettings(boolean enabled){
   	executableField.setEnabled(enabled);
	browseExecutableButton.setEnabled(enabled);
	outFileField.setEnabled(enabled);
	browseOutFileButton.setEnabled(enabled);
   }
    public void disableSettings() {
    	setEnabledSettings(false);
    }

	public void initClient() throws IOException{
        int port = socket.getLocalPort();
        out.println("Before loading:");
        out.println("Executable:"+executable);
        out.println("Output File:"+outputFile);
        
        if (executable.equals("")||interactionType.equals("Classic")){
          Frame f = new Frame("CrazyBot!!!");
          FileDialog fd = new FileDialog(f,"AAAI Bot Startme",FileDialog.LOAD);
          fd.setVisible(true);
          executable = fd.getDirectory()+fd.getFile();
        }
        if (interactionType.equals("Port")){
        	JOptionPane.showMessageDialog(null, "Port "+port+" opened on this machine. Please connect to it via the AAAI protocol, and then press OK.", "Port Opened",JOptionPane.OK_OPTION);
        } else {
        File executableFile = new File(executable);
        directory = executableFile.getParent();
        //Time t = new Time();
        Calendar c = new GregorianCalendar();
        out.println("Time:"+c.get(Calendar.HOUR)+":"+c.get(Calendar.MINUTE));
        out.println("DIRECTORY:"+directory);
        out.println("Executable:"+executable);
        out.println("Output File:"+outputFile);
        out.println("Using ProcessBuilder");
        boolean isMac = System.getProperty("os.name").toLowerCase().startsWith("mac");
        out.println("Running on a Mac? "+isMac);
        ProcessBuilder pb;
        if (isMac){
          pb = new ProcessBuilder(executable,"127.0.0.1",""+port);
        } else {
          pb = new ProcessBuilder("cmd","/C",executable,"127.0.0.1",""+port);
        	
        }
        pb.directory(new File(directory));
        Process p = pb.start();
        InputStream is = p.getInputStream();
        InputStream iserr = p.getErrorStream();
        try{
            botout = new PrintStream(new FileOutputStream("TCPPluginBot.log"));
        } catch (FileNotFoundException fnf){
            botout = System.out;
        }

        StreamConnect sc = new StreamConnect(is,botout,out);
        Thread t = new Thread(sc);
        t.start();
        StreamConnect scerr = new StreamConnect(iserr,botout,out);
        Thread terr = new Thread(scerr);
        terr.start();
        }
        //String[] args = new String[]{"sh", "-c", commandLine};
        //Runtime.getRuntime().exec(commandLine);
        // new File("examples\\randomclient")
        //Runtime.getRuntime().exec(commandLine,null,new File(directory));
        out.println("Client initialized");
    }
    
    public void initConnection(){
        try{
            socket = new ServerSocket(0);
            initClient();
            out.println("socket port:"+socket.getLocalPort());
            Socket childSocket = socket.accept();
            agent=new PlayerAgent(childSocket,0);
            agent.setTimeRemaining(1000);
            if (!agent.receiveMessage().equals("VERSION:1.0.0")){
                out.println("The first player does not acknowledge the protocol.");
            }
            out.println("Successful connection!");
        } catch(TimeoutException to){
            out.println("The " + ((to.playerIndex==0) ? "first" : "second") + " player does not acknowledge the protocol.");
        } catch (SocketException so){
            out.println(so);
            out.println("The first player's connection appears broken.");
        } catch (IOException io){
            out.println(io);
            out.println("The first player's connection appears broken.");                  
        }
    }

    public void init(Preferences prefs){
    	this.prefs = prefs;
    	loadFromPrefs();
    }
    
    public com.biotools.meerkat.Action getAction(){
        try{
        String response;
        do{
            out.println("Response attempt for state:"+getMatchState());
              response = agent.receiveMessage();
            out.println("Response received:"+response);
        } while(!isAppropriate(response));
        out.println("Response accepted:"+response);
        char c = getActionFromResponse(response);
        //out.println("Action parsed:"+c);
        //char c = 'c';
        switch(c){
            case 'r':
                return com.biotools.meerkat.Action.raiseAction(info);
            case 'c':
                return com.biotools.meerkat.Action.callAction(info);
            case 'f':
            default:
                return com.biotools.meerkat.Action.foldAction(info);
        }
        } catch (TimeoutException to){
            out.println("Timeout exception in response attempt for state:"+getMatchState());
            return com.biotools.meerkat.Action.foldAction(info);
        }
        //return Action.foldAction(info);
    }
    
    public void gameStartEvent(GameInfo info){
        if (socket==null){
            initConnection();
        }
        agent.setTimeRemaining(7000);
        uofagameIndex++;
        bettingSequence = "";
        this.holeCard1=null;
        this.holeCard2=null;
        this.oppCard1=null;
        this.oppCard2=null;
        this.info = info;
    }
    
    public void gameStateChanged(){
        
    }
    
    
    public void holeCards(Card h1, Card h2, int seat){
        holeCard1 = h1;
        holeCard2 = h2;
        paseat = seat;
        if (handBegun == true){
        	JOptionPane.showMessageDialog(null, "Warning: the AAAI protocol specifies \"no mucking\" whereas mucking"+
        			" appears to be turned on. Please verify that \"Options->Muck Losing Hands\" is turned off before continuing.");
        }
        handBegun = true;
        sendMatchState();
    }

    public void dealHoleCardsEvent(){
        
    }
    
    public void winEvent(int seat, double amount, String cards){
        
    }
    
    public void gameOverEvent(){
    }
    
    public void showdownEvent(int seat, Card c1, Card c2){
        if (seat!=paseat){
            oppCard1 = c1;
            oppCard2 = c2;
            //out.println("Showdown event state:"+getMatchState());
            handBegun = false;
            sendMatchState();
        }
    }
    
    public void stageEvent(int stage){
        if (stage!=Holdem.PREFLOP){
            bettingSequence += "/";
            //out.println("Sending for stage event "+stage+" state:"+getMatchState());

            sendMatchState();
        }
    }
    public void actionEvent(int pos, com.biotools.meerkat.Action action){
        if (action.isFold()){
            bettingSequence += "f";
            handBegun = false;
            //out.println("Sending for actionEvent(fold):"+getMatchState());
            sendMatchState();
        } else if (action.isCheckOrCall()){
            bettingSequence += "c";
            boolean roundOver = bettingSequence.endsWith("cc")||bettingSequence.endsWith("rc");
            if (!roundOver){
                //out.println("Sending for actionEvent(call):"+getMatchState());
            
                sendMatchState();
            }
        } else if (action.isBetOrRaise()){
            bettingSequence += "r";
            //out.println("Sending for actionEvent(raise):"+getMatchState());
            sendMatchState();
        }
    }
    
    
    /**
     * Tests if a response is actually a response to the CURRENT state.
     */
    public boolean isAppropriate(String response){
        if (response.length()<2){
            return false;
        }
        if (info.getCurrentPlayerSeat()!=paseat){
            return false;
        }
        String responseFront = response.substring(0,response.length()-2);
        //out.println("FRONT OF RESPONSE:"+responseFront);
        //out.println("STATE TO MATCH:"+getMatchState());
        return (getMatchState().equals(responseFront));
    }
    
    /**
     * Gets the last character of a response, which should be 'c', 'r', or 'f'
     */
    public char getActionFromResponse(String response){
        return response.charAt(response.length()-1);
    }
    
    public void sendMatchState(){
        out.println("SENDING:"+getMatchState());
        try{
            agent.sendMessage(getMatchState());
        } catch (TimeoutException to){
        }
    }
    
    public String getMatchState(){
        int uofaserverseat = (info.getButtonSeat()==paseat) ? 1 : 0;
        String result = "MATCHSTATE:" + uofaserverseat + ":" + uofagameIndex + ":"+bettingSequence +":";
        String oppCards = (oppCard1==null) ? "" : ("" + oppCard1 + oppCard2);
        String holeCards = (holeCard1==null) ? "" : ("" + holeCard1 + holeCard2);
        String nonButtonCards = (uofaserverseat==0) ? holeCards : oppCards;
        String buttonCards = (uofaserverseat==1) ? holeCards : oppCards;
        result = result + nonButtonCards + "|" + buttonCards;
        Hand board = info.getBoard();
        if (board.size()>=3){
            String flop = "/"+ board.getCard(1) + board.getCard(2) + board.getCard(3);
            result = result + flop;
        }
        if (board.size()>=4){
            String turn = "/" + board.getCard(4);
            result = result + turn;
        }
        if (board.size()>=5){
            String river = "/" + board.getCard(5);
            result = result + river;
        }
        
        return result;
    }
    
    public static void main(String[] args){
    	System.out.println(System.getProperty("os.name").toLowerCase().startsWith("mac"));
        //TCPPlugin plugin = new TCPPlugin();
        //plugin.initConnection();
    }

    public void saveFromSettingsPanel(){
		executable = executableField.getText();
		outputFile = outFileField.getText();
		prefs.setPreference("EXECUTABLE", executable);
		prefs.setPreference("OUTPUT", outputFile);
		prefs.setPreference("INTERACTIONTYPE",interactionType);
    }
	public void actionPerformed(ActionEvent e) {
		if (e.getSource()==saveButton){
            saveFromSettingsPanel();
		} else if (e.getSource()==cancelButton){
			loadFromPrefs(); 
		} else if (e.getSource()==browseExecutableButton){
			  Frame f = new Frame("CrazyBot!!!");
	          //f.show();
	          FileDialog fd = new FileDialog(f,"AAAI Bot Startme",FileDialog.LOAD);
	          fd.setVisible(true);
	          
	          //executable = fd.getDirectory() + File.pathSeparator + fd.getFile();
	          executableField.setText(fd.getDirectory() + fd.getFile());
	          saveFromSettingsPanel();
		} else if (e.getSource()==browseOutFileButton){
			  Frame f = new Frame("CrazyBot!!!");
	          //f.show();
	          FileDialog fd = new FileDialog(f,"Output file for AAAI Bot",FileDialog.SAVE);
	          fd.setVisible(true);
	          
	          //executable = fd.getDirectory() + File.pathSeparator + fd.getFile();
	          outFileField.setText(fd.getDirectory() + fd.getFile());
	          saveFromSettingsPanel();
		} else if (e.getSource().equals(jLoadLater)){
			disableSettings();
			interactionType = "Classic";
		} else if (e.getSource().equals(jLoadNow)){
			setEnabledSettings(true);
			interactionType = "Local";
		} else if (e.getSource().equals(jInternet)){
			disableSettings();
			interactionType = "Port";
		}
		
		
	}
}
