import java.io.*;

/**
 * If a program called by Process sends data to stdout
 * which is not read, it blocks.
 * This class allows you to connect stdout of a process
 * to an inputstream
 */
public class StreamConnect implements Runnable{
  InputStream is;
  OutputStream os;
  PrintStream debug;
  public StreamConnect(InputStream is, OutputStream os, PrintStream debug){
    this.is = is;
    this.os = os;
    this.debug = debug;
  }

  public void run(){
    while(true){
      try{
        /*int i=is.read();
        if (i==-1){
          debug.println("Found EOF");
          break;
        }
        os.write(i);*/
        //debug.println("Read byte");
        int bytesAvailable = is.available();
       
        if (bytesAvailable>0){
          byte[] buffer = new byte[bytesAvailable];
          is.read(buffer);
          os.write(buffer);
          os.flush();
        }
      } catch (Exception e){
      }
      try{
        Thread.currentThread().sleep(20);
        } catch(Exception e){
      }
    }
  }
}