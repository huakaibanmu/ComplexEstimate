package ui;

import java.awt.List;
import java.io.File;
import java.util.ArrayList;

public class utils {

	static ArrayList<String> getFiles(String directoryPath){
		  ArrayList<String> list = new ArrayList<String>();
		  if(directoryPath != null) {
	        File baseFile = new File(directoryPath);
	        if (baseFile.isFile() || !baseFile.exists()) {
	            return list;
	        }
	        File[] files = baseFile.listFiles();
	        for (File file : files) 
	            list.add(file.getAbsolutePath());
			return list;
			}
		return list;
}
}
