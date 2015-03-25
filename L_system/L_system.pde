import toxi.geom.*;
import peasy.*;
import ddf.minim.analysis.*;
import ddf.minim.*;
import sound.*;

PeasyCam cam;
Minim minim;  
AudioPlayer jingle;
FFT fft;
/*
  dVals[0]
 color
 angle2
 angle3
 rotate x
 rotate y
 rotate z
 */
ArrayList <Stick> sticks;
float ANGLE2 = 69.9004, ANGLE3 = 0, r=100, g=0, b=0;
float[] dVals = new float[7];
boolean rT=true, gT=false, bT=false;

void setup() {
  size(1300, 750, P3D);
  smooth();

  cam = new PeasyCam(this, 100);

  minim = new Minim(this);
  jingle = minim.loadFile("trapstorm.mp3", 1024);
  jingle.loop();
  fft = new FFT( jingle.bufferSize(), jingle.sampleRate() );
  fft.linAverages( 12 );

  sticks = new ArrayList <Stick> ();
}

void draw() {
  background(0);
  fft.forward( jingle.mix );


  sticks.clear();
  int w = 10;
  for (int i = 0; i < 7; i++)
  {
    dVals[i]=fft.getAvg(i);
    if (i==0) {
      dVals[0]=dVals[0]/5;
      if (dVals[0]>4) dVals[0]=4;
      if (dVals[0]<1.5) dVals[0]=1.5;
    }
    else if (i==2) {
      ANGLE2+=dVals[2];
    }
    else if (i==3) {
      ANGLE3+=dVals[3];
    }
    else if (i<7 && i>3) {
      dVals[i]=dVals[i]*PI/120;
    }
  }

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

  Vec3D initLoc = new Vec3D(0, 0, 0);
  Vec3D initVel = new Vec3D(dVals[0], 0, 0);
  Vec3D initColor = new Vec3D(r, g, b);
  Stick s = new Stick(initLoc, initVel, 20, 1, initColor);

  sticks.add(s);

  for (Stick elem : sticks) {
    elem.run();
  }
  cam.rotateX(dVals[4]);
  cam.rotateY(dVals[5]);
  cam.rotateZ(dVals[6]);
  //c++;
}

class Stick {

  Vec3D loc, vel, oriLoc, c;

  int gen;
  int type;

  Stick(Vec3D _loc, Vec3D _vel, int _gen, int _type, Vec3D _c) {
    loc = _loc;
    vel = _vel;
    oriLoc = _loc.copy();
    gen = _gen;
    type = _type;
    c = _c;

    //stack of functions that get executed only once
    updateDir();
    updateLoc();
    spawn();
  }

  void run() {
    display();
  }

  void spawn() {
    if (gen > 0) {
      if (type == 1) {
        Vec3D initLoc1 = loc.copy(), initVel1 = vel.copy(), c1 = c.copy();
        Vec3D initLoc2 = loc.copy(), initVel2 = vel.copy(), c2 = c.copy();

        Stick newS1 = new Stick(initLoc1, initVel1, gen - 1, 1, c1);
        Stick newS2 = new Stick(initLoc2, initVel2, gen - 1, 2, c2);

        sticks.add(newS1);
        sticks.add(newS2);
      }
      else if (type == 2) {
        Vec3D initLoc = loc.copy(), initVel = vel.copy(), c1 = c.copy();

        Stick newS = new Stick(initLoc, initVel, gen - 1, 3, c1);

        sticks.add(newS);
      }
      else {
        Vec3D initLoc = loc.copy(), initVel = vel.copy(), c1 = c.copy();

        Stick newS = new Stick(initLoc, initVel, gen - 1, 1, c1);

        sticks.add(newS);
      }
    }
  }

  void updateDir() {
    float aX, aY, aZ;
    switch (type) {
    case 1: 
      aX = radians(0);
      aY = radians(3.1240345);
      aZ = radians(0);
      break;

    case 2: 
      aX = radians(0);
      aY = radians(0);
      aZ = radians(ANGLE2);

      break;

    default:
      aX = radians(ANGLE3);
      aY = radians(0);
      aZ = radians(0);
      break;
    }
    vel.rotateX(aX);
    vel.rotateY(aY);
    vel.rotateZ(aZ);
  }

  void updateLoc() {
    loc.addSelf(vel);
  }

  void display() {
    stroke(c.x,c.y,c.z);
    strokeWeight(4);
    pt(loc);

    stroke(255);
    strokeWeight(1);
    ln(loc, oriLoc);
  }

  void ln(Vec3D p1, Vec3D p2) {
    line(p1.x, p1.y, p1.z, p2.x, p2.y, p2.z);
  }

  void pt(Vec3D p) {
    point(p.x, p.y, p.z);
  }
}
