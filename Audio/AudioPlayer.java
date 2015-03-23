import java.io.File;

import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;
import javax.sound.sampled.DataLine;
import javax.sound.sampled.FloatControl;

public class AudioPlayer {
	
	public static void playAudio(boolean cup, boolean cup1, boolean cup2, boolean cup3,
						float volume, float volume1, float volume2, float volume3){
		
		try{
		
			AudioInputStream audioInputStream =
		        AudioSystem.getAudioInputStream( new File("test.wav"));
			AudioFormat format = audioInputStream.getFormat();
	        DataLine.Info info = new DataLine.Info(Clip.class, format);
	        Clip clip = (Clip)AudioSystem.getLine(info);
		    clip.open(audioInputStream);
		    long sec = clip.getMicrosecondLength();
		    long millisec = sec/1000;
		    
		    AudioInputStream audioInputStream1 =
			        AudioSystem.getAudioInputStream( new File("test1.wav"));
		    AudioFormat format1 = audioInputStream1.getFormat();
	        DataLine.Info info1 = new DataLine.Info(Clip.class, format1);
	        Clip clip1 = (Clip)AudioSystem.getLine(info1);
			clip1.open(audioInputStream1);
			long sec1 = clip1.getMicrosecondLength();
			long millisec1 = sec1/1000;
			
			AudioInputStream audioInputStream2 =
				    AudioSystem.getAudioInputStream( new File("test2.wav"));
			AudioFormat format2 = audioInputStream2.getFormat();
	        DataLine.Info info2 = new DataLine.Info(Clip.class, format2);
	        Clip clip2 = (Clip)AudioSystem.getLine(info2);
			clip2.open(audioInputStream2);
			long sec2 = clip2.getMicrosecondLength();
			long millisec2 = sec2/1000;
				    
			AudioInputStream audioInputStream3 =
				AudioSystem.getAudioInputStream( new File("test3.wav"));
			AudioFormat format3 = audioInputStream3.getFormat();
	        DataLine.Info info3 = new DataLine.Info(Clip.class, format3);
	        Clip clip3 = (Clip)AudioSystem.getLine(info3);
			clip3.open(audioInputStream3);
			long sec3 = clip3.getMicrosecondLength();
			long millisec3 = sec3/1000;
			
			if (cup){
	    		FloatControl gainControl = 
		    		    (FloatControl) clip.getControl(FloatControl.Type.VOLUME);
		    		gainControl.setValue(gainControl.getValue()+volume);
			}
			
			if (cup1){
	    		FloatControl gainControl1 = 
		    		    (FloatControl) clip1.getControl(FloatControl.Type.VOLUME);
		    		gainControl1.setValue(gainControl1.getValue()+volume1);
			}
			
			if (cup2){
	    		FloatControl gainControl2 = 
		    		    (FloatControl) clip2.getControl(FloatControl.Type.VOLUME);
		    		gainControl2.setValue(gainControl2.getValue()+volume2);
			}
			
			if (cup3){
	    		FloatControl gainControl3 = 
		    		    (FloatControl) clip3.getControl(FloatControl.Type.VOLUME);
		    		gainControl3.setValue(gainControl3.getValue()+volume3);
			}
			
			while (true){
				
		    	if (cup){
		    		clip.start();
		    	}
		    	if (cup1){
		    		clip1.start();
		    	}
		    	if (cup2){
		    		clip2.start();
		    	}
		    	if (cup3){
		    		clip3.start();
		    	}
		    	
		    	Thread.sleep(Math.min(millisec, Math.min(millisec1, Math.min(millisec2, millisec3))));
		    
		    	if (cup){
		    		clip.stop();
		    		clip.setFramePosition(0);
		    	}
		    	if (cup1){
		    		clip1.stop();
		    		clip1.setFramePosition(0);
		    	}
		    	if (cup2){
		    		clip2.stop();
		    		clip2.setFramePosition(0);
		    	}
		    	if (cup3){
		    		clip3.stop();
		    		clip3.setFramePosition(0);
		    	}
		    }
		}
		catch (Exception e){
			e.printStackTrace();
		}
		
	}
	
	
	public static void main (String[] args){
		
		playAudio(true, false, true, true, -50.0f, -10.0f, 0.0f, -5.0f);
		
		
	}

}
