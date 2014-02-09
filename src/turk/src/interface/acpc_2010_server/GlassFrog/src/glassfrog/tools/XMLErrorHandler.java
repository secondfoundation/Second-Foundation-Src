package glassfrog.tools;

/**
 * An error handler for the XML Validator.  Dumps all output to stderr
 * @author jdavidso
 */
import org.xml.sax.ErrorHandler;
import org.xml.sax.SAXParseException;

/**
 * Dump all errors to stderr for XML
 * @author josh
 */
public class XMLErrorHandler implements ErrorHandler {

    private String logPath = "logs/";
    private static final String ERROR_LOG = "errorLog.log";
    private static final String ERROR_LOGGER = "glassfrog.errorlogger";

    /**
     * Dump all errors to stderr for XML
     * @param exception
     */
    public void error(SAXParseException exception) {
        System.err.println("error: " + exception.getMessage());
    }

    /**
     * Dump all errors to stderr for XML
     * @param exception
     */
    public void fatalError(SAXParseException exception) {
        System.err.println("fatalError: " + exception.getMessage());
    }

    /**
     * Dump all errors to stderr for XML
     * @param exception
     */
    public void warning(SAXParseException exception) {
        System.err.println("warning: " + exception.getMessage());
    }
}

