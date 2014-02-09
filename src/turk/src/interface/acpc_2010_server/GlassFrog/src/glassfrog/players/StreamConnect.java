package glassfrog.players;

/**
 * Taken form the old AAAI server, this allows the AAAI bots to print thier I/O
 * to file
 * @author martyzinkevich
 */
import java.io.*;

/**
 * If a program called by Process sends data to stdout
 * which is not read, it blocks.
 * This class allows you to connect stdout of a process
 * to an inputstream
 */
public class StreamConnect implements Runnable{
  /** 
   * The stream to be read from.
   * Usually, the stream from the process.
   */
  InputStream is;

  /**
   * The stream to be written to.
   * Usually a file or stdout or stderr.
   */
  OutputStream os;

  /**
   * Generate a new StreamConnect object.
   * @param is Input stream 
   * @param os Output stream
   */
  public StreamConnect(InputStream is, OutputStream os){
    this.is = is;
    this.os = os;
  }

  /**
   * A thread which takes bytes from the input stream
   * to the output stream.
   */
  public void run(){
    byte[] buffer = new byte[4000];
    while(true){
      try{
        int bytesAvailable = is.available();
       
        if (bytesAvailable > 0){
          int bytesRead = is.read(buffer);
          os.write(buffer, 0, bytesRead);
        }
      } catch (Exception e){
      }
      try{
        Thread.sleep(20);
      } catch(InterruptedException e){
        return;
      }
    }
  }
}
