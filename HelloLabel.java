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


	private static JLabel jl_1;//登录的版面

	private static JFrame jf_1;//登陆的框架


   private static JLabel jl_admin;

   
   public HelloLabel (){//初始化登陆界面
   	    int w = 700;int h= 400;
	    jf_1=new JFrame("图像质量评测系统");
	    jf_1.setResizable(false);
	   
	    int x = (Toolkit.getDefaultToolkit().getScreenSize().width - w) / 2;
		int  y= (Toolkit.getDefaultToolkit().getScreenSize().height - h) / 2;
		jf_1.setBounds(x, y, 700, 400);
		ImageIcon bgim1 = new ImageIcon(System.getProperty("user.dir")+"\\image\\shouye2.jpg") ;//背景图案
		jf_1.setIconImage(bgim1.getImage());
		
		ImageIcon bgim = new ImageIcon(System.getProperty("user.dir")+"\\image\\shouye2.jpg") ;//背景图案

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
		//登陆点击事件
		 long startMili=System.currentTimeMillis();
		 long endMili;
		 while((endMili=System.currentTimeMillis()-startMili)<3000)
		 { 
			 Math.random();
		 }
		 hl.jf_1.dispose();//销毁当前界面
	     mainFrame frame = new mainFrame();//为跳转的界面
	   
	     frame.setVisible(true);
					

			
			}
}


