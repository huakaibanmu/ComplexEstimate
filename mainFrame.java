package ui;

import java.awt.BorderLayout;
import java.awt.EventQueue;
import java.awt.Toolkit;

import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JProgressBar;
import javax.swing.border.EmptyBorder;
import javax.swing.border.LineBorder;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.xml.sax.SAXException;

import javax.swing.JSplitPane;
import javax.swing.BorderFactory;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFileChooser;

import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.awt.event.ActionEvent;
import javax.swing.JTextArea;
import java.awt.Color;
import java.awt.Dimension;

import javax.swing.JTextPane;

public class mainFrame extends JFrame {

	private JPanel contentPane;
	public static String filePath;
	public static	JTextArea textArea = new JTextArea();

	/**
	 * Create the frame.
	 */
	public mainFrame() {
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		  int w = 700;int h= 400;
		  int x = (Toolkit.getDefaultToolkit().getScreenSize().width - w) / 2;
	     int  y= (Toolkit.getDefaultToolkit().getScreenSize().height - h) / 2;
		setBounds(x, y, 700, 400);
		setTitle("图像质量评测软件");
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		System.out.println(System.getProperty("user.dir"));
		ImageIcon background= new ImageIcon(System.getProperty("user.dir")+"\\image\\shouye.jpg");
		setIconImage(background.getImage());
		JLabel label = new JLabel(background);//把背景图片显示在一个标签里面
		//把标签的大小位置设置为图片刚好填充整个面板
		label.setBounds(0,0,background.getIconWidth(),background.getIconHeight());//把内容窗格转化为JPanel，否则不能用方法setOpaque（）来使内容窗格透明
		setContentPane(contentPane);
		contentPane.setLayout(null);
		ImagePanel panel_1 = new ImagePanel();
		JButton bLastImage = new JButton("上一张 图片");
		JButton bNextImage = new JButton("下一张 图片");
		JButton bshowFileInfo = new JButton("查看文件图像平均信息");
		JButton btnSelectFiles = new JButton("选择文件");
		JProgressBar pbar= new JProgressBar();
		pbar.setBounds(20, 30,30,30);
		contentPane.add(pbar);
		pbar.setVisible(false);
		  JLabel statusLabel = new JLabel("Reading data, please wait..."); 
//			statusLabel.setIcon(new ImageIcon("F:\\workspace\\ImageComplexShow\\loading.gif"));
//			statusLabel.setHorizontalAlignment(JLabel.CENTER); 
		  //statusLabel.setVisible(true);
	
//			statusLabel.setOpaque(false);
//			
		btnSelectFiles.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				// TODO Auto-generated method stub
				bNextImage.setEnabled(false);
				bLastImage.setEnabled(false);
				JFileChooser fileChooser = new JFileChooser("C:\\");
				fileChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
				int returnVal = fileChooser.showOpenDialog(fileChooser);
				if(returnVal == JFileChooser.APPROVE_OPTION){ 
				filePath= fileChooser.getSelectedFile().getAbsolutePath();//这个就是你选择的文件夹的路径
				String[] args1 = new String[] { "python",System.getProperty("user.dir")+ "\\complexEstimate.py", filePath}; 
		    try {
					Process pr=Runtime.getRuntime().exec(args1);
				
					 JFrame frame = new JFrame();
				        // ...
				        LoadingPanel glasspane = new LoadingPanel();
				        Dimension dimension = Toolkit.getDefaultToolkit().getScreenSize();
				        glasspane.setBounds(100, 100, 700,400);
				        frame.setGlassPane(glasspane);
				        glasspane.setText("Loading data, Please wait ...");
				        glasspane.start();//开始动画加载效果
				        frame.setVisible(true);
					pr.waitFor();
					glasspane.stop();
					bNextImage.setEnabled(true);
					bshowFileInfo.setEnabled(true);
					panel_1.setVisible(true);
				} catch (IOException | InterruptedException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}

				} 
			}
		});
		btnSelectFiles.setBounds(15, 25, 130, 30);
		contentPane.add(btnSelectFiles);
		
		panel_1.setBounds(5, 65, 360, 241);
		panel_1.setVisible(false);
		contentPane.add(panel_1);
		
		
		bLastImage.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				
				ArrayList<String> files = utils.getFiles(filePath);
				ImagePanel.deleteI();
				panel_1.repaint();
				if(!files.isEmpty()&&ImagePanel.i>0&&ImagePanel.i<files.size()) {
					bNextImage.setEnabled(true);
					textArea.setText(ImagePanel.outString);
				}
				else if(ImagePanel.i <= 0) {
					bLastImage.setEnabled(false);
				}

			}
		});
		bLastImage.setBounds(165, 25, 130, 30);
		bLastImage.setEnabled(false);
		contentPane.add(bLastImage);
	
		
		bNextImage.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				ArrayList<String> files = utils.getFiles(filePath);
				ImagePanel.addI();
				panel_1.repaint();
				
				if(!files.isEmpty()&&ImagePanel.i<files.size()-1&&ImagePanel.i>=0) {
					bLastImage.setEnabled(true);
					
				}
				else if(ImagePanel.i >= files.size()-1){
					bNextImage.setEnabled(false);
				}
			}
		});
		bNextImage.setBounds(325, 25, 130, 30);
		contentPane.add(bNextImage);
		bNextImage.setEnabled(false);
		
		
		bshowFileInfo.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				if(filePath != null) {
					int flength =filePath.length();
					 File f = new File(filePath.substring(0, flength-10)+"ImagesInfo.xml");   
						String fileInfo ="";
						try {
							 DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();   
							 DocumentBuilder builder = factory.newDocumentBuilder();   
							 Document doc;
							 doc = builder.parse(f);
							 fileInfo ="图像张数:"+ doc.getElementsByTagName("imageNum").item(0).getFirstChild().getNodeValue()+"\n";   
							 fileInfo +=("平均复杂度:"+ doc.getElementsByTagName("complexMean").item(0).getFirstChild().getNodeValue()+"\n");
							 fileInfo +=("最大复杂度:"+ doc.getElementsByTagName("complexMax").item(0).getFirstChild().getNodeValue()+"\n"); 
							 fileInfo +=("最小复杂度:"+ doc.getElementsByTagName("complexMin").item(0).getFirstChild().getNodeValue()+"\n"); 
							 textArea.setText(fileInfo);

						} catch (SAXException | IOException | ParserConfigurationException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}   
				}
				
				} 
			
		});
		bshowFileInfo.setBounds(470, 25, 170, 30);
		contentPane.add(bshowFileInfo);
		bshowFileInfo.setEnabled(false);
		textArea.setBounds(400, 65, 180, 200);
		textArea.setForeground(Color.magenta);
		contentPane.add(textArea);
		textArea.setOpaque(false);
		contentPane.add(statusLabel);
		contentPane.add(label);
		label.setOpaque(false);
	}
}
