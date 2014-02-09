/*
 * RoomDialog.java
 *
 * Created on November 21, 2008, 12:19 PM
 */
package swordfish.view;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.StringTokenizer;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.TreeSelectionModel;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import org.jdesktop.application.Action;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;
import org.xml.sax.SAXParseException;

/**
 * A dialog used to connect to the server.  Currently obsolete due to auto-connect
 * but may be re-invoked for multiple server use
 * @author  jdavidso
 */
public class SwordfishRoomDialog extends javax.swing.JDialog {

    private DefaultMutableTreeNode root;
    private ArrayList<DefaultMutableTreeNode> serverList;
    private DefaultTreeModel model;
    private PrintWriter pw;
    private BufferedReader br;    
    private SwordfishView view;
    private boolean autoConnect = false;
    private KeyValidationDialog validationDialog;

    /** Creates new form RoomDialog
     * @param parent Parent of the room dialog
     * @param modal True for a modal room dialog
     */
    public SwordfishRoomDialog(java.awt.Frame parent, boolean modal) {
        super(parent, modal);
        populateRoomTree();
        initComponents();
        connectButton.setEnabled(false);
    }

    /**
     * Dialog for selecting a room to play in derrived from active servers in the server list
     * @param parent Parent to the dialog
     * @param view View to connect the room to
     * @param modal True for modal dialogs
     */
    public SwordfishRoomDialog(java.awt.Frame parent, SwordfishView view, boolean modal) {
        super(parent, modal);
        this.view = view;
        initComponents();
        populateRoomTree();
        connectButton.setEnabled(false);
    }

    /**
     * Populate the Rooms for a Server
     */
    private void populateRoomTree() {
        initializeServerList();
        root = new DefaultMutableTreeNode("Servers");
        for (DefaultMutableTreeNode server : serverList) {
            root.add(server);
        }
        model = new DefaultTreeModel(root);
        roomTree.setModel(model);
    }

    /**
     * Populate the server list
     */
    private void initializeServerList() {
        serverList = getServerList();
        for (int i = 0; i < serverList.size(); i++) {
            DefaultMutableTreeNode server = serverList.get(i);
            if(!populateServer(server)) {
                serverList.remove(server);
                i--;
            }
        }
    }

    /**
     * Initialize the serverlist from the serverList.xml file
     * @return an ArrayList of possible servers
     */
    private ArrayList<DefaultMutableTreeNode> getServerList() {
        ArrayList<DefaultMutableTreeNode> defaultServers = new ArrayList<DefaultMutableTreeNode>();
        defaultServers.add(new DefaultMutableTreeNode("127.0.0.1:9000"));
        boolean isLoaded = false;
        ArrayList<DefaultMutableTreeNode> servers = new ArrayList<DefaultMutableTreeNode>();
        try {
            DocumentBuilderFactory docBuilderFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder docBuilder = docBuilderFactory.newDocumentBuilder();            
            Document doc = (Document) docBuilder.parse(this.getClass().getResourceAsStream("resources/serverList.xml"));
            doc.getDocumentElement().normalize();

            NodeList xmlServerList = doc.getElementsByTagName("Server");            
            for (int i = 0; i < xmlServerList.getLength(); i++) {
                Node serverNode = xmlServerList.item(i);
                if (serverNode.getNodeType() == Node.ELEMENT_NODE) {
                    Element serverElement = (Element) serverNode;
                    String ip = serverElement.getElementsByTagName("IP").item(0).getChildNodes().item(0).getNodeValue().trim();
                    String port = serverElement.getElementsByTagName("Port").item(0).getChildNodes().item(0).getNodeValue().trim();
                    servers.add(new DefaultMutableTreeNode(ip+":"+port));
                    isLoaded = true;
                }
            }
        } catch (ParserConfigurationException ex) {
            view.logError(ex);
            isLoaded = false;
        } catch (IOException ex) {
            view.logError(ex);
            isLoaded = false;
        } catch (SAXParseException ex) {
            view.logError(ex);
            isLoaded = false;
        } catch (SAXException ex) {
            view.logError(ex);
            isLoaded = false;
        }
        if (isLoaded) {
            return servers;
        }
        return defaultServers;
    }

    /**
     * Populate a given server
     * @param server A node representing the srver to populate
     * @return True for a successful population
     */
    private boolean populateServer(DefaultMutableTreeNode server) {
        try {
            StringTokenizer st = new StringTokenizer(server.toString(),":");
            Socket serverConnection = new Socket(st.nextToken(), new Integer(st.nextToken()).intValue());
            br = new BufferedReader(new InputStreamReader(serverConnection.getInputStream()));
            pw = new PrintWriter(serverConnection.getOutputStream(), true);
            pw.println("LIST");
            pw.flush();
            //Do something multiline here
            String response = "", line;
            while((line = br.readLine()) != null) {
                response += line+"||";
            }            
            if(response.equalsIgnoreCase("||")) {
                server.add(new DefaultMutableTreeNode("No active rooms"));
            } else {                
                StringTokenizer responseST = new StringTokenizer(response,"||");                
                while(responseST.hasMoreTokens()) {
                    String room = responseST.nextToken();
                    StringTokenizer roomST = new StringTokenizer(room,":");
                    if(roomST.countTokens() > 2) {
                        roomST.nextToken();
                        roomST.nextToken();
                        if(roomST.nextToken().equalsIgnoreCase("STARTING")) {
                            server.add(new DefaultMutableTreeNode(room));                    
                        }
                    }
                }
                if(server.getChildCount() == 0) {
                    server.add(new DefaultMutableTreeNode("No active rooms"));
                }
            }
        } catch (UnknownHostException ex) {
            view.logError(ex);
            return false;
        } catch (IOException ex) {
            view.logError(ex);
            return false;
        }
        return true;
    }
    
    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {
        java.awt.GridBagConstraints gridBagConstraints;

        treePanel = new javax.swing.JPanel();
        treeScrollPane = new javax.swing.JScrollPane();
        roomTree = new javax.swing.JTree(root);
        buttonPanel = new javax.swing.JPanel();
        connectButton = new javax.swing.JButton();
        refreshButton = new javax.swing.JButton();

        setDefaultCloseOperation(javax.swing.WindowConstants.DISPOSE_ON_CLOSE);
        setName("Form"); // NOI18N
        getContentPane().setLayout(new java.awt.GridBagLayout());

        treePanel.setBorder(javax.swing.BorderFactory.createEtchedBorder());
        treePanel.setName("treePanel"); // NOI18N
        treePanel.setLayout(new java.awt.GridLayout(1, 0));

        treeScrollPane.setName("treeScrollPane"); // NOI18N

        roomTree.setModel(null);
        roomTree.setName("roomTree"); // NOI18N
        roomTree.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mousePressed(java.awt.event.MouseEvent evt) {
                roomTreeMousePressed(evt);
            }
        });
        roomTree.addTreeSelectionListener(new javax.swing.event.TreeSelectionListener() {
            public void valueChanged(javax.swing.event.TreeSelectionEvent evt) {
                roomTreeValueChanged(evt);
            }
        });
        treeScrollPane.setViewportView(roomTree);
        roomTree.getSelectionModel().setSelectionMode(TreeSelectionModel.SINGLE_TREE_SELECTION);

        treePanel.add(treeScrollPane);

        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.fill = java.awt.GridBagConstraints.BOTH;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 9.0;
        getContentPane().add(treePanel, gridBagConstraints);

        buttonPanel.setBorder(javax.swing.BorderFactory.createBevelBorder(javax.swing.border.BevelBorder.RAISED));
        buttonPanel.setName("buttonPanel"); // NOI18N
        buttonPanel.setLayout(new java.awt.BorderLayout());

        javax.swing.ActionMap actionMap = org.jdesktop.application.Application.getInstance(swordfish.view.SwordfishApp.class).getContext().getActionMap(SwordfishRoomDialog.class, this);
        connectButton.setAction(actionMap.get("connect")); // NOI18N
        org.jdesktop.application.ResourceMap resourceMap = org.jdesktop.application.Application.getInstance(swordfish.view.SwordfishApp.class).getContext().getResourceMap(SwordfishRoomDialog.class);
        connectButton.setText(resourceMap.getString("connectButton.text")); // NOI18N
        connectButton.setName("connectButton"); // NOI18N
        buttonPanel.add(connectButton, java.awt.BorderLayout.CENTER);

        refreshButton.setAction(actionMap.get("refresh")); // NOI18N
        refreshButton.setText(resourceMap.getString("refreshButton.text")); // NOI18N
        refreshButton.setName("refreshButton"); // NOI18N
        buttonPanel.add(refreshButton, java.awt.BorderLayout.PAGE_START);

        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 0;
        gridBagConstraints.gridy = 1;
        gridBagConstraints.fill = java.awt.GridBagConstraints.BOTH;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        getContentPane().add(buttonPanel, gridBagConstraints);

        pack();
    }// </editor-fold>//GEN-END:initComponents

    /**
     * Disable and enable connect buttons based on user selection in the list
     * @param evt TreeSelectionEvent
     */
private void roomTreeValueChanged(javax.swing.event.TreeSelectionEvent evt) {//GEN-FIRST:event_roomTreeValueChanged
    if (roomTree.getSelectionCount() > 0) {
        DefaultMutableTreeNode node = (DefaultMutableTreeNode) roomTree.getLastSelectedPathComponent();
        if (node.getChildCount() == 0 && !node.toString().equalsIgnoreCase("No active rooms") && !node.toString().equalsIgnoreCase("Servers")) {
            connectButton.setText("Connect");
            connectButton.setEnabled(true);
            autoConnect = false;
        } else if(node.getChildCount() != 0 && !node.toString().equalsIgnoreCase("Servers")){
            connectButton.setText("AutoConnect");
            connectButton.setEnabled(true);
            autoConnect = true;
        } else {
            connectButton.setEnabled(false);
        }
    } else {
        connectButton.setEnabled(false);
    }
}//GEN-LAST:event_roomTreeValueChanged

/**
 * Handle double click by running connect method
 * @param evt MouseEvent
 */
private void roomTreeMousePressed(java.awt.event.MouseEvent evt) {//GEN-FIRST:event_roomTreeMousePressed
    if (evt.getClickCount() > 1) {
        connect();        
    }
}//GEN-LAST:event_roomTreeMousePressed

    /**
     * Useless main function from the IDE generation
     * @param args the command line arguments
     */
    public static void main(String args[]) {
        java.awt.EventQueue.invokeLater(new Runnable() {

            public void run() {
                SwordfishRoomDialog dialog = new SwordfishRoomDialog(new javax.swing.JFrame(), true);
                dialog.addWindowListener(new java.awt.event.WindowAdapter() {

                    @Override
                    public void windowClosing(java.awt.event.WindowEvent e) {
                        System.exit(0);
                    }
                });
                dialog.setVisible(true);
            }
        });
    }

    /**
     * Refresh the rooms in the tree
     */
    @Action
    public void refresh() {
        populateRoomTree();       
    }

    /**
     * Connect to the selected room
     */
    @Action
    public void connect() {
        DefaultMutableTreeNode node = (DefaultMutableTreeNode) roomTree.getLastSelectedPathComponent();
        if (node.getChildCount() == 0 && !node.toString().equalsIgnoreCase("No Rooms Found")) {            
            String[] roomSpecs = node.toString().split(":");
            String[] serverSpecs = node.getParent().toString().split(":");
            String ip = serverSpecs[0];
            int roomPort = new Integer(roomSpecs[1]);
            this.setVisible(false);
            view.connectToRoom(ip, roomPort);                        
        } else {
            String[] serverSpecs = node.toString().split(":");
            String ip = serverSpecs[0];
            int port = new Integer(serverSpecs[1]).intValue();
            validationDialog = new KeyValidationDialog((java.awt.Frame)this.getParent(), view, true, ip, port);
            this.setVisible(false);
            validationDialog.setVisible(true);            
        }
    }
    
    /**
     * Reset the validation dialog on uncessessful connect
     */
    public void reset() {
        validationDialog.reset();
    }
    
    /**
     * Hide the key validation window
     */
    public void hideKeyValidation() {
        validationDialog.setVisible(false);
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JPanel buttonPanel;
    private javax.swing.JButton connectButton;
    private javax.swing.JButton refreshButton;
    private javax.swing.JTree roomTree;
    private javax.swing.JPanel treePanel;
    private javax.swing.JScrollPane treeScrollPane;
    // End of variables declaration//GEN-END:variables
}
