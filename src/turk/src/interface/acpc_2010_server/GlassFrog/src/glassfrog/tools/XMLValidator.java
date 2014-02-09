package glassfrog.tools;

import java.io.IOException;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import org.xml.sax.SAXException;


/**
 * A class to validate a given XML file with a specified XML Schema.  This will 
 * help eliminate any errors the user has when putting together the config files 
 * associated with the server by catching them and returning the message to the
 * user before any execution
 * 
 * @author jdavidso
 */
public class XMLValidator {
    private String xsdFile;
    private DocumentBuilderFactory factory;
    private DocumentBuilder builder;
    
    /**
     * The constructor for the validator.  This will set up the DocumentBuilder 
     * and the associated XML Schema file for this validator.
     * 
     * @param xsdFile A path to the XML Schema to use
     */
    public XMLValidator(String xsdFile){
        this.xsdFile =xsdFile;
        factory = DocumentBuilderFactory.newInstance();        
        factory.setNamespaceAware(true);
        factory.setValidating(true);
        factory.setAttribute("http://java.sun.com/xml/jaxp/properties/schemaLanguage",
                "http://www.w3.org/2001/XMLSchema");
        factory.setAttribute("http://java.sun.com/xml/jaxp/properties/schemaSource", 
                "file:./"+xsdFile);                     
    }
    
    /**
     * Set the schema for the xml to validate against
     * @param xsdFile a path to the xsd to validate against
     */
    public void setSchema(String xsdFile) {
        factory.setAttribute("http://java.sun.com/xml/jaxp/properties/schemaSource", 
                "file:./"+xsdFile);        
    }

    /**
     * Run the xml validator on the fgiven file
     * @param xmlFile The file to validate
     * @return True for a valid XML file, False otherwise
     * @throws ParserConfigurationException
     * @throws SAXException
     * @throws IOException
     */
    public boolean validateXML(String xmlFile) throws ParserConfigurationException,
    SAXException, IOException{
        boolean isValid = true;
        builder = factory.newDocumentBuilder();
        builder.setErrorHandler( new XMLErrorHandler() );
        builder.parse(xmlFile);
        return isValid;
    }
}

