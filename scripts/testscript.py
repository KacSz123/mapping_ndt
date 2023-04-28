
#!/usr/bin/env python


from alg_ell import *
from robot import *
import matplotlib.pyplot as plt
import time
import queue
import copy
def DistBetween2Ell(e1,e2):
  return math.sqrt(((e1._center[0]-e2._center[0])**2)+((e1._center[1]-e2._center[1])**2))


def UpdateMap(q1,old_e):
    q2 = queue.Queue()
    qtmp2 = queue.Queue()
    for i in q1.queue:
      q2.put(i)
    old_ell = old_e
    xx=[]
    while not q2.empty():
      xx=q2.get()
      #xx=sorted(xx , key=lambda k: [k[1], k[0]])
      ellipses = GetEllipsesFromCsv(10, xx)
      check_ell = True
      if len(old_ell)>0:
        for e in ellipses:

          for el in old_ell:
            if DistBetween2Ell(e,el)<0.1:
              check_ell = False
              break
          if check_ell == True:
            if not EllipseOutOfSize(e,0.4):
              old_ell.append(e)
            #input() 
      else:
          return ellipses

    return old_ell
  
def on_close(event):
    print('Closed Figure!')
    return True
    
def main():
  rospy.init_node("MyNodeNDT")
  r1 = MyRobot()
  time.sleep(0.4)
  xy = r1.MakeDataCart()
  plt.ion()
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.set_xlim(-5,6)
  ax.set_ylim(-4,5.5)

  q1 = queue.Queue()
  qtmp=queue.Queue()
  exits = []
  xy=[]
  fig.canvas.draw()
  fig.canvas.flush_events()
  xyput=[]
  input()
  while 1:
        xy = r1.MakeDataCart()
        qtmp.put(xy)
        print(len(exits))
        #print(qtmp.queue)
        print(qtmp.qsize())
        
        # if qtmp.qsize()==2:
        #   xyput.clear()
        #   for i in range(0,2):
        #     xyput+=qtmp.get()
        #   q1.put(xyput)  
        q1.put(xy)
        if q1.qsize()==10:
          exits = UpdateMap(q1,exits)
          for e in exits:
            #print(1)
                e.set_facecolor('red')   
                ax.add_artist(e)
          q1.get()
        fig.canvas.draw()
        fig.canvas.flush_events()
        #time.sleep(0.05)
  
  
if __name__ == "__main__":
  main()