  
import numpy as np
import math
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from mymath import *

import rospy
class MyRobot():
  _scan = []
  _mapx = []
  _mapxy = []
  _mapy = []
  _mapy_ang = list(range(0,360))
  _scan_ang_rad =  [math.radians(i) for i in _mapy_ang ]
  _path = []
  
  _theta= 0.0
  _position = [0,0,0]
  _orientation = [0,0,0,0]
  # sub=rospy.Subscriber('/_scan',LaserScan, callback)
  
  def __init__(self):
    rospy.Subscriber('/scan',LaserScan, self.callback)
    rospy.Subscriber('/odom',Odometry, self.callback_pose)
    # for i in self._mapy_ang:
    #   self._scan_ang_rad.append(math.radians(i))
  def callback(self,msg):
    self._scan=msg.ranges
  def callback_pose(self,msg):
        self._position[0] = msg.pose.pose.position.x
        self._position[1] = msg.pose.pose.position.y
        self._position[2] = msg.pose.pose.position.z
        self._orientation[0] = msg.pose.pose.orientation.x
        self._orientation[1] = msg.pose.pose.orientation.y
        self._orientation[2] = msg.pose.pose.orientation.z
        self._orientation[3] = msg.pose.pose.orientation.w 
        self.theta=self.GetOrientation()
    # print(self._scan)
  def MakeDataCart(self):
    # print(len(self._scan))
    self._mapx.clear()
    self._mapy.clear()
    self._mapxy.clear()
    for i in range(0, len(self._scan)):
        if (
            not math.isnan(self._scan[i])
            and not math.isinf(self._scan[i])
            #and not math.isnan(_mapy)
            #and not math.isinf(_mapy)
            and self._scan[i]<=3
        ): 
            Xp = self._scan[i] * np.cos(self._scan_ang_rad[i] + self.theta)+self._position[0]
            Yp = self._scan[i] * np.sin(self._scan_ang_rad[i] + self.theta)+self._position[1]
            # Xp0=Xp
            # Yp0=Yp
            # Xp= Xp0*math.cos(-self.theta)-Yp0*math.sin(-self.theta)
            # Yp=Xp0*math.sin(-self.theta)+Yp0*math.cos(-self.theta)
            self._mapx.append(Xp)
            self._mapxy.append((Xp,Yp))
            self._mapy.append(Yp)
    # print(len(self._mapx))
    return  self._mapxy

  def GetOrientation(self):
      a = get_yaw_z_radians(self._orientation[0],self._orientation[1],self._orientation[2],self._orientation[3])
      if a < 0:
        return (math.pi-abs(a))+math.pi
      else:
        return a
  def GetPose(self):
      return self._position[0], self._position[1]
      
  def MakeDataPol(self):
    return self._scan_ang_rad


  def WriteDataToFile(self,filename):
    file = open(filename,"w")
    file.write("x;y \n")
    for i in range(len(self._mapx)):
      file.write("%f;%f \n" % (self._mapx[i],self._mapy[i]))
    file.close()
    
    
#     def ConvertData(_scan):
#   kat = np.arange(0,360)
#   # global _mapy_ang
#   # _mapy_ang=[]
#   # global _mapx
#   # global _mapy
#   # # print(len(kat))
#   # for i in kat:
#   #   _mapy_ang.append(math.radians(i))
#   # # print(_mapy_ang)
#   # for i in range(0, len(_scan)):
#   #       if (
#   #           not math.isnan(_scan[i])
#   #           and not math.isinf(_scan[i])
#   #           #and not math.isnan(_mapy)
#   #           #and not math.isinf(_mapy)
#   #           and _scan[i]< 2
#   #       ): 
#   #           _mapx.append(_scan[i] * np.cos(_mapy_ang[i]))
#   #           _mapy.append(_scan[i] * np.sin(_mapy_ang[i]))
#    # print(len(_mapx))