package swordfish.view;

import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.event.ActionListener;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JPanel;
import javax.swing.JSlider;
import javax.swing.SwingConstants;

/**
 * A Slider class that has some buttons for betsizes and such
 * @author jdavidso
 */
public class NoLimitSlider extends JPanel
{
    
    private JSlider betsizeSlider;
    private JButton potsizeButton, halfpotButton, allinButton;
    private int stacksize = 400;
    private int minBet = 2;    
    
    /**
     *  Create a nolimit slider for bet amounts and standard options
     */
    public NoLimitSlider() {
        super();
        this.setOpaque(false);        
        potsizeButton = new JButton("Pot");
        halfpotButton = new JButton("1/2 Pot");
        allinButton = new JButton("All In");        
        potsizeButton.setActionCommand("potsize");
        halfpotButton.setActionCommand("halfpotsize");
        allinButton.setActionCommand("allin");
        /*
        ActionListener al = new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                if("potsize".equals(e.getActionCommand())) {
                    betsizeSlider.setValue(100);
                } else if ("halfpotsize".equals(e.getActionCommand())) {
                    betsizeSlider.setValue(50);
                } else if ("allin".equals(e.getActionCommand())) {
                    betsizeSlider.setValue(stacksize);
                }
            }
            
        };
        potsizeButton.addActionListener(al);
        halfpotButton.addActionListener(al);
        allinButton.addActionListener(al);*/
        betsizeSlider = new JSlider(SwingConstants.HORIZONTAL,minBet,stacksize,minBet);
        betsizeSlider.setPreferredSize(new Dimension(205, 25));
        betsizeSlider.setMinorTickSpacing((stacksize*5)/100);
        betsizeSlider.setMajorTickSpacing((stacksize*25)/100);                
        betsizeSlider.setPaintTicks(true);            
        
        JPanel buttonGroup = new JPanel() {
            @Override
            public Dimension getMinimumSize() {
                return getPreferredSize();
            }
            @Override
            public Dimension getPreferredSize() {
                return new Dimension(205, 15);
            }
            @Override
            public Dimension getMaximumSize() {
                return getPreferredSize();
            }                        
        };
        
        buttonGroup.setLayout(new BoxLayout(buttonGroup,BoxLayout.LINE_AXIS));
        buttonGroup.add(halfpotButton);
        buttonGroup.add(potsizeButton);
        buttonGroup.add(allinButton);
        buttonGroup.setOpaque(false);
        setLayout(new BoxLayout(this,BoxLayout.PAGE_AXIS));
        add(buttonGroup);
        buttonGroup.setAlignmentY(TOP_ALIGNMENT);          
        add(betsizeSlider);
        betsizeSlider.setOpaque(false);   
    }
    
    /**
     * Override for anti-aliased text
     * @param g The graphics parameter
     */
    @Override
    public void paintComponent(Graphics g) {
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint (RenderingHints.KEY_TEXT_ANTIALIASING,
            RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
        super.paintComponent (g2);
    }
    
    /**
     * Return the value of the slider object
     * @return an int representing the betsize
     */
    public int getValue() {
        return betsizeSlider.getValue();
    }
    
    /**
     * Set the value of the slider object
     * @param value an int to set the slider to.
     */
    public void setValue(int value) {
        betsizeSlider.setValue(value);
    }
    
    /**
     * Set the slider to the min bet allowed
     * @param minBet The min bet value to set the slider to
     */
    public void setMinBet(int minBet) {
        this.minBet = minBet;
    }
    
    /**
     * Return the betsize slider object
     * @return the JSlider
     */
    public JSlider getSlider() {
        return betsizeSlider;
    }
            
    /**
     * Allow the slider to be modified
     * @param enabled True for enableing the slider
     */
    public void enableSlider(Boolean enabled) {
        betsizeSlider.setEnabled(enabled);
        potsizeButton.setEnabled(enabled);
        halfpotButton.setEnabled(enabled);
        allinButton.setEnabled(enabled);
        betsizeSlider.setValue(minBet);
    }

    /**
     * Make the slider invisible
     */
    public void invisible() {
        betsizeSlider.setVisible(false);
        potsizeButton.setVisible(false);
        halfpotButton.setVisible(false);
        allinButton.setVisible(false);
    }        
    
    /**
     * Initialize the slider
     * @param minbet set the min value of the slider
     * @param stacksize set the max value of the slider
     */
    public void initSlider(int minbet, int stacksize) {
        this.minBet = minbet;
        this.stacksize = stacksize;
        betsizeSlider.setMaximum(stacksize);
        betsizeSlider.setMinimum(minbet);
        betsizeSlider.setValue(minbet);
    }
    
    /**
     * Add a listener for the buttons on the slider
     * @param al the action listener for the buttons
     */
    public void addButtonActionListener(ActionListener al) {
        potsizeButton.addActionListener(al);
        halfpotButton.addActionListener(al);
        allinButton.addActionListener(al);
    }
}
