import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import ddf.minim.analysis.*; 
import ddf.minim.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class AudioVisualizer2 extends PApplet {




AudioInput in;
Minim minim;  
AudioPlayer jingle;
FFT fft;


int cuantos = 16000;
Pelo[] lista;
float radio = 200, prev = -1, diffMax = 0.2f;
float ANGLE2 = 69.9004f, ANGLE3 = 0;
int r=100, g=0, b=0;
float[] dVals = new float[7];
boolean rT=true, gT=false, bT=false;

public void setup() {
  size(1024, 768, P3D);

  radio = height/3.5f;

  lista = new Pelo[cuantos];
  for (int i = 0; i < lista.length; i++) {
    lista[i] = new Pelo();
  }
  noiseDetail(3);
  minim = new Minim(this);
  in = minim.getLineIn();
  fft = new FFT( in.left.size(), 441000);
  fft.linAverages(8);
}

public void draw() {
  background(0);
  fft.forward(in.left);

  for (int i = 0; i < 7; i++)
  {
    dVals[i]=fft.getAvg(i)/20;
  }
  
  // if (dVals[0]>1.5) dVals[0]=1.5;
  // if (dVals[0]<1.05) dVals[0]=1.05;

  if (rT) {
    r += fft.getAvg(1);
    if (b>0) b-=5;
    if (b<0) b=0;
    if (r>255) {
      r-=10;
      g=30;
      gT=true;
      rT=false;
    }
  }
  else if (gT) {
    g += fft.getAvg(1);
    if (r>0) r-=5;
    if (r<0) r=0;
    if (g>255) {
      g-=10;
      b=30;
      bT=true;
      gT=false;
    }
  }
  else if (bT) {
    b += fft.getAvg(1);
    if (g>0) g-=5;
    if (g<0) g=0;
    if (b>255) {
      b-=10;
      r=30;
      rT=true;
      bT=false;
    }
  }

  translate(width/2, height/2);
  rotateY(dVals[1]);
  rotateX(dVals[2]);
  rotateX(dVals[3]);
  fill(0);
  noStroke();
  sphere(radio);

  for (int i = 0; i < lista.length; i++) {
    lista[i].dibujar(r,g,b,dVals[0]*2);
  }

}


class Pelo
{
  float z = random(-radio, radio);
  float phi = random(TWO_PI);
  float largo = random(1.15f, 1.2f);
  float theta = asin(z/radio);

  Pelo() { // what's wrong with a constructor here
    z = random(-radio, radio);
    phi = random(TWO_PI);
    largo = random(1.15f, 1.2f);
    theta = asin(z/radio);
  }

  public void dibujar(int r, int g, int b, float multi) {

    float off = (noise(millis() * 0.0005f, sin(phi))-0.5f) * 0.3f;
    float offb = (noise(millis() * 0.0007f, sin(z) * 0.01f)-0.5f) * 0.3f;
    
    if(multi<1) multi=1;
    
    multi = largo*multi;
    
    if(multi>3) multi=3;
    
    float thetaff = theta+off;
    float phff = phi+offb;
    float x = radio * cos(theta) * cos(phi);
    float y = radio * cos(theta) * sin(phi);
    float z = radio * sin(theta);

    float xo = radio * cos(thetaff) * cos(phff);
    float yo = radio * cos(thetaff) * sin(phff);
    float zo = radio * sin(thetaff);

    float xb = xo * multi;
    float yb = yo * multi;
    float zb = zo * multi;

    strokeWeight(1);
    beginShape(LINES);
    stroke(0);
    vertex(x, y, z);
    stroke(r,g,b);
    vertex(xb, yb, zb);
    endShape();
  }
}
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "AudioVisualizer2" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
