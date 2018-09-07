package ui;

import java.awt.*;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

import javax.print.DocFlavor.STRING;
import javax.swing.*;
import org.w3c.dom.Document;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

public class ImagePanel extends JPanel {
private Image img;

public ImagePanel() {
	// TODO Auto-generated constructor stub
	setBorder(BorderFactory.createMatteBorder(5, 5, 5, 5, Color.yellow));
}
public static  int i = 0;
public static String outString;
public static void addI()

{
    i++;
}

public static void deleteI()

{
    i--;
}


public void paint(Graphics g)

{
	 ImageIcon imageIcon = new ImageIcon() ;
    int x =0;
  //  ImageIcon imageIcon ;
    int y = 0;
    ArrayList<String> files = utils.getFiles(mainFrame.filePath);
  
   
    if(!files.isEmpty()&&i>=0&&i<files.size()) {
    
    	int flength =mainFrame.filePath.length();
    	
    	 ArrayList<String> imageInfoFiles = utils.getFiles(mainFrame.filePath.substring(0, flength-10)+"ImageInfo/");
		 imageIcon  = new ImageIcon(files.get(i));
		 File f = new File(imageInfoFiles.get(i));   
		outString ="";
		try {
			 DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();   
			 DocumentBuilder builder = factory.newDocumentBuilder();   
			 Document doc;
			 doc = builder.parse(f);
			 outString ="图像复杂度:"+ doc.getElementsByTagName("complexity").item(0).getFirstChild().getNodeValue()+"\n";   
			 outString +=("分辨率:"+ doc.getElementsByTagName("resolutionRatio").item(0).getFirstChild().getNodeValue()+"\n");
			 outString +=("目标数:"+ doc.getElementsByTagName("boxNum").item(0).getFirstChild().getNodeValue()+"\n"); 
			 outString +=("目标框面积:"+ doc.getElementsByTagName("boxArea").item(0).getFirstChild().getNodeValue()+"\n"); 
			

		} catch (SAXException | IOException | ParserConfigurationException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}   
		   
		       
		 g.drawImage(imageIcon.getImage(),x,y,getSize().width,getSize().height,this);
	    mainFrame.textArea.setText(ImagePanel.outString);
		 
		 
}
   
    else {
    	/*imageIcon = new ImageIcon("F:\\SciencedataSet\\test\\null.jpg") ;
    	 g.drawImage(imageIcon.getImage(),x,y,getSize().width,getSize().height,this);*/
    	 if(i<0)
    		 i = 0;
    	 if(i>=files.size())
    		 i = files.size()-1;
    }

}
}