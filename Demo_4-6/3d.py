import pyin
import time
import threading
import numpy as np
import sys
import random
import math

try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print '''
ERROR: PyOpenGL not installed properly.  
        '''
shape = 0
N=25
RADIUS=1
tt = pyin.TapTester()
amp = 10
fft_block = []
r,g,b = 0.0,0.0,0.0
rT, gT, bT = True, False, False
def listen():
  global amp, fft_block
  while(True):
      amp, fft_block = tt.listen()


thr = threading.Thread(target=listen, args=(), kwargs={})
thr.start()

def animate():
  glutPostRedisplay()

def init(): 
   glClearColor (0.0, 0.0, 0.0, 0.0)
   glShadeModel (GL_FLAT)
 
def changeColor():
   global rT,gT,bT,r,g,b, fft_block
   if not len(fft_block):
     fftMag = 1.0
   else:
     fftMag = abs(random.choice(fft_block))%2.5
   if (rT):
     r+=fftMag
     if (b>0): 
       b-=5
     if (b<0): 
       b=0
     if (r>255):
       r-=100
       gT=True
       rT=False
  
   elif (gT):
     g += fftMag
     if (r>0): 
       r-=5
     if (r<0):
      r=0
     if (g>255):
       g-=100
       bT=True
       gT=False 

   elif (bT) :
     b += fftMag
     if (g>0):
       g-=5
     if (g<0):
       g=0
     if (b>255):
       b-=100
       rT=True
       bT=False
  
def shape0():
   #glutWireCube (1.0)
   glutWireSphere(1.0, 10,10)

def shape1():
   glutSolidCube (1.0)

def shape2():
   #glutWireSphere(1.0, 10,10)
   glColor3f(r*1.0,g*1.0,b*1.0)


   xpts=[]
   ypts=[]
   for i in range(0,N):
       xpts.append(RADIUS*math.sin(N*i/(math.pi)))
       ypts.append(RADIUS*math.cos(N*i/(math.pi))) 

   glBegin(GL_LINES)
   for i in range(0,N):
       for j in range(i,N):
        for k in range(i,j):
           glVertex2f(xpts[i],ypts[i])
           glVertex2f(xpts[j],ypts[j])
           glVertex2f(xpts[k],ypts[k])
   glEnd()

def shape3():
   glutSolidSphere(1.0, 10,10)

def display():
   global amp, shape
   
  
   changeColor();
   # print "amp: ",amp
   glClear (GL_COLOR_BUFFER_BIT)
   glLoadIdentity ()             # clear the matrix 
   # viewing transformation 
  # glRotatef(3.0, 1.0,1.0,1.0)

   gluLookAt (0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
   scale = amp*10.0
   glScalef (scale,scale,scale)      # modeling transformation 
   glColor3f(r*1.0,g*1.0,b*1.0)
   #glutWireSphere(1.0, 10,10)

   # glLineWidth(2.5); 
   # glBegin(GL_LINES);
   # glVertex3f(0.0, 0.0, 0.0);
   # glVertex3f(15, 0, 0);

   # glVertex3f(0.0, 0.0, 0.0);
   # glVertex3f(0,3,15);
   # glEnd();
   

   shape2()
   glFlush ()



def reshape (w, h):
   global amp, idx
   glViewport (0, 0, w, h)
   glMatrixMode (GL_PROJECTION)
   glLoadIdentity ()
   glFrustum (-1.0, 1.0, -1.0, 1.0, 1.5, 20.0)
   glMatrixMode (GL_MODELVIEW)

def keyboard(key, x, y):
   if key == chr(27):
      import sys
      sys.exit(0)

def init_cube():
  glutInit(sys.argv)
  glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB)
  glutInitWindowSize (500, 500)
  glutInitWindowPosition (100, 100)
  glutCreateWindow ('cube')
  init ()
  glutDisplayFunc(display)
  glutReshapeFunc(reshape)
  glutKeyboardFunc(keyboard)
  glutIdleFunc(animate)
  glutMainLoop()




init_cube()

