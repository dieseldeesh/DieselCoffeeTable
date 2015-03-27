import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.awt.image.*;

import javax.imageio.ImageIO;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.CvType;
import org.opencv.core.Scalar;
import org.opencv.highgui.VideoCapture;

public class ImageProcessing implements Runnable{
	
	final int INTERVAL=2000;///you may use interval
   // CanvasFrame canvas = new CanvasFrame("Web Cam");
    public ImageProcessing() {
       // canvas.setDefaultCloseOperation(javax.swing.JFrame.EXIT_ON_CLOSE);
    }
    @Override
    public void run() {
        VideoCapture grabber = new VideoCapture();
        int i=0;
        try {
            grabber.open(7);
            while (true) {
                Mat newIm = new Mat();
                try {
                    // retrieve image
                    grabber.retrieve(newIm);
                    
                    Image imagenb = toImage(newIm);
                    BufferedImage finIm = toBufferedImage(imagenb);
                    
                    File outputfile = new File(""+(i++)+"saved.jpg");
                    ImageIO.write(finIm, "jpg", outputfile);
                }
                catch (IOException e) {
                    System.out.println("Image not rendered");
                }
                // show image on window
                //canvas.showImage(finIm);
                Thread.sleep(INTERVAL);
                if (i==5)
                    break;
            }
        }
        catch (Exception e) {
        	e.printStackTrace();
        }
    }
    
    public static void main(String[] args)
    {
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
    	ImageProcessing test = new ImageProcessing();
    	test.run();
    }
    
    public Image toImage(Mat m){
        int type = BufferedImage.TYPE_BYTE_GRAY;
        if ( m.channels() > 1 ) {
            type = BufferedImage.TYPE_3BYTE_BGR;
        }
        int bufferSize = m.channels()*m.cols()*m.rows();
        byte [] b = new byte[bufferSize];
        m.get(0,0,b); // get all the pixels
        BufferedImage image = new BufferedImage(m.cols(),m.rows(), type);
        final byte[] targetPixels = ((DataBufferByte) image.getRaster().getDataBuffer()).getData();
        System.arraycopy(b, 0, targetPixels, 0, b.length);  
        return image;

    }
    
    /**
     * Converts a given Image into a BufferedImage
     *
     * @param img The Image to be converted
     * @return The converted BufferedImage
     */
    public static BufferedImage toBufferedImage(Image img)
    {
        if (img instanceof BufferedImage)
        {
            return (BufferedImage) img;
        }
        
        // Create a buffered image with transparency
        BufferedImage bimage = new BufferedImage(img.getWidth(null), img.getHeight(null), BufferedImage.TYPE_INT_ARGB);
        
        // Draw the image on to the buffered image
        Graphics2D bGr = bimage.createGraphics();
        bGr.drawImage(img, 0, 0, null);
        bGr.dispose();
        
        // Return the buffered image
        return bimage;
    }

}
