package ui;
import java.awt.Font;
import java.awt.Image;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;

import java.awt.event.ActionListener;

import javax.swing.ImageIcon;

import javax.swing.JButton;

import javax.swing.JFrame;

import javax.swing.JLabel;

import javax.swing.JPasswordField;

import javax.swing.JTextField;

import ui.mainFrame;

public class HelloLabel extends JFrame{


	private static JLabel jl_1;//��¼�İ���

	private static JFrame jf_1;//��½�Ŀ��


   private static JLabel jl_admin;

   
   public HelloLabel (){//��ʼ����½����
   	    int w = 700;int h= 400;
	    jf_1=new JFrame("ͼ����������ϵͳ");
	    jf_1.setResizable(false);
	   
	    int x = (Toolkit.getDefaultToolkit().getScreenSize().width - w) / 2;
		int  y= (Toolkit.getDefaultToolkit().getScreenSize().height - h) / 2;
		jf_1.setBounds(x, y, 700, 400);
		ImageIcon bgim1 = new ImageIcon(System.getProperty("user.dir")+"\\image\\shouye2.jpg") ;//����ͼ��
		jf_1.setIconImage(bgim1.getImage());
		
		ImageIcon bgim = new ImageIcon(System.getProperty("user.dir")+"\\image\\shouye2.jpg") ;//����ͼ��

		bgim.setImage(bgim.getImage().getScaledInstance(bgim.getIconWidth(),

												       bgim.getIconHeight(), 

												       Image.SCALE_DEFAULT));  

		jl_1=new JLabel();
		
		jl_1.setBounds(x, y, 700, 400);
		jl_1.setIcon(bgim);

		jf_1.add(jl_1);

		jf_1.setVisible(true);

		jf_1.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		jf_1.setLocation(x,y);

	}

	public static void main(String[] args) {
		HelloLabel hl =new HelloLabel();
		//��½����¼�
		 long startMili=System.currentTimeMillis();
		 long endMili;
		 while((endMili=System.currentTimeMillis()-startMili)<3000)
		 { 
			 Math.random();
		 }
		 hl.jf_1.dispose();//���ٵ�ǰ����
	     mainFrame frame = new mainFrame();//Ϊ��ת�Ľ���
	   
	     frame.setVisible(true);
					

			
			}
}


