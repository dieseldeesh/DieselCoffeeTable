import pyin
import time
import threading
import numpy as np
import sys

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
   glRotatef(0, 0, 0, amp*10.0 )
   gluLookAt (0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
   glScalef (amp*30.0, amp*30.0, amp*30.0)      # modeling transformation 
   glutWireCube (1.0)
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

