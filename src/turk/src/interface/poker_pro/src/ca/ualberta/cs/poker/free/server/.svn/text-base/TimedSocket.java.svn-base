package ca.ualberta.cs.poker.free.server;
import java.net.*;
import java.io.*;
import java.util.*;


/**
 * TimedSocket.java
 * The alien's "agent" on the server side. 
 * Sends messages to the alien and
 * receives messages from the alien.
 * Messages sent:<BR>
 * MATCHSTARTED:&lt;IP&gt;:&lt;port&gt;:&lt;alienbot&gt;<BR>
 * ERROR:&lt;message&gt;<BR>
 * LOGINSUCCESS
 * Messages received:<BR>
 * LOGIN:&lt;username&gt;:&lt;password&gt;<BR>
 * MATCHREQUEST:&lt;clientIP&gt;:&lt;alienbot&gt;:&lt;opponent&gt;:&lt;gametype&gt;<BR>
 * MATCHTERMINATE:&lt;matchname&gt;<BR>
 * LOGOUT<BR>
 *
 */
public class TimedSocket {
    /**
     * The current message terminator is CR LF (13 10).
     */
    public static final String messageTerminator = "" + ((char)13)+((char)10);
    
    /**
     * The time remaining to use (in milliseconds)
     */
    long timeRemaining;
    
    /**
     * The total (match) elapsed sending time.
     */
    public long elapsedSendingTime;
    
    /**
     * The client socket (for sending and receiving messages)
     */
    public Socket socket;
    

    /**
     * The stream for sending messages to a client.
     */
    OutputStream os;
    
    /**
     * The stream for receiving messages from a client.
     */
    InputStream is;
    
    /**
     * The partial response received from the client.
     */
    String response;

    /**
     * The player index
     */
    int playerIndex;

    public void setSocket(Socket socket){
    	this.socket = socket;
    }
    
    /** 
     * Creates a new instance of TimedSocket
     */
    public TimedSocket(Socket socket, int playerIndex)
      throws SocketException, IOException{
        this.socket = socket;
	this.playerIndex = playerIndex;
    }
    
    /** 
     * Creates a new instance of TimedSocket
     */
    public TimedSocket(Socket socket)
      throws SocketException, IOException{
        this.socket = socket;
	    this.playerIndex = -1;
    }

    /** 
     * Creates a new instance of TimedSocket
     */
    public TimedSocket(){
        this.socket = null;
	this.playerIndex = 0;
    }

    public static Vector<String> parseByColons(String str){
      Vector<String> result = new Vector<String>();
      int lastIndex=-1;
      while(true){
        int currentIndex = 0;
	currentIndex = str.indexOf(':',lastIndex+1);
	if (currentIndex==-1){
		result.add(str.substring(lastIndex+1));
	  return result;
	}
	result.add(str.substring(lastIndex+1,currentIndex));
	lastIndex=currentIndex;
      }
    }
	


    /**
     * Reset the time at the beginning of the hand.
     */
    public void setTimeRemaining(long timeRemaining){
        this.timeRemaining = timeRemaining;
    }
    
    /**
     * Send a message to the client. Appends a message terminator.
     */
    public void sendMessage(String message) throws TimeoutException{
        //System.out.println("MessageTerminator:"+((int)(messageTerminator.charAt(0))));
        //System.out.println("MessageTerminator:"+((int)(messageTerminator.charAt(1))));
        try{
            //System.out.println("Message Length:"+message.length());
            
            message = message + messageTerminator;
            //System.out.println("Message Length:"+message.length());
            
            byte[] messageData = message.getBytes();
            long initialTime = new Date().getTime();
            long timeUsed,currentTime;
            socket.setSoTimeout(120000);
            os.write(messageData);
            currentTime = new Date().getTime();
            timeUsed = currentTime - initialTime;
            if (timeUsed>=100000){
                throw new TimeoutException(playerIndex,true,"Real timeout");
            }
            elapsedSendingTime += timeUsed;
        } catch (SocketException to){
            throw new TimeoutException(playerIndex,true,"Socket error:"+to.getMessage());
        } catch (IOException io){
            throw new TimeoutException(playerIndex,true,"I/O error:"+io.getMessage());
        }
    }
    
    /**
     * Receives a message from the client. Removes the message terminator.
     * TODO: Handle an interruption
     */
    public String receiveMessage() throws TimeoutException{
    	//System.err.println("Time remaining:"+timeRemaining);
        try{
        long initialTime = new Date().getTime();
        long timeUsed=0;
        long currentTime=initialTime;
        
        do{
        	//System.err.println("receiveMessage:A");
        	socket.setSoTimeout((int)(timeRemaining-timeUsed));
            
            response = response + (char)(is.read());
            currentTime = new Date().getTime();
            timeUsed = currentTime - initialTime;
            if (timeUsed>=timeRemaining){
            	//System.err.println("receiveMessage:B");
                throw new TimeoutException(playerIndex,false,"Real timeout");
            }
        	//System.err.println("receiveMessage:C");
        } while(!isComplete(response));
        timeRemaining-=timeUsed;
        String result = response.substring(0,response.length()-messageTerminator.length());
        response = "";
        return result;
        } catch (SocketException to){
            throw new TimeoutException(playerIndex,false,"Socket error:"+to.getMessage());
        } catch (IOException io){
            throw new TimeoutException(playerIndex,false,"I/O error:"+io.getMessage());
        }
    }
    
    /**
     * A message is complete if it ends with the message terminator.
     */
    public boolean isComplete(String result){
        return result.endsWith(messageTerminator);
    }
    
    /**
     * Close the connection to the client.
     */
    public void close() throws IOException{
        if (os!=null){
        	os.close();
        	os=null;
        }
        if (is!=null){
        	is.close();
        	is=null;
        }
        if (socket!=null){
        	socket.close();
        }
    }

    /**
     * Open the outputstream and inputstream from the socket.
     */
    public void open() throws IOException{
      socket.setTcpNoDelay(true);
      os = socket.getOutputStream();
      is = socket.getInputStream();
      response = "";
    }
}
