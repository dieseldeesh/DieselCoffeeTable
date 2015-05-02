import pyin
import time
import threading
import numpy as np
import sys
N=25
RADIUS=95

try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print '''
ERROR: PyOpenGL not installed properly.  
        '''

tt = pyin.TapTester()
amp = 10
fft_block = []
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

def display():
   global amp
   # print "amp: ",amp
   glClear (GL_COLOR_BUFFER_BIT)
   glColor3f (1.0, 1.0, 1.0)
   glLoadIdentity ()             # clear the matrix 
   # viewing transformation 
   glRotatef(0, 0, 0, amp*100.0 )
   gluLookAt (0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
   scale = amp*50.0
   glScalef (scale,scale,scale)      # modeling transformation 
   glColor3ub(255,255,0)
   #glutWireCube (1.0)
   #glutWireSphere(1.0, 10,10)

   xpts=[]
   ypts=[]
   for i in range(0,N):
       xpts.append(RADIUS*math.sin(2.0*math.pi*i/N))
       ypts.append(RADIUS*math.cos(2.0*math.pi*i/N))   

   glBegin(GL_LINE_STRIP)
   for i in range(0,N):
       for j in range(i,N):
           glVertex2f(xpts[i],ypts[i])
           glVertex2f(xpts[j],ypts[j])
   glEnd()

   glFlush ()

def reshape (w, h):
   global amp, idx
   glViewport (0, 0, w, h)
   glMatrixMode (GL_PROJECTION)
   glLoadIdentity ()
   if w>h:
     glViewport((w-h)/2,0,h,h)
   else:
     glViewport(0,(h-w)/2,w,w)

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

