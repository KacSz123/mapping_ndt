  
import numpy as np
import math

import rospy
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry

from mymath import *
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


  def __init__(self):
    rospy.Subscriber('/scan',LaserScan, self.callback)
    rospy.Subscriber('/odom',Odometry, self.callback_pose)
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

  def MakeDataCart(self):
    self._mapx.clear()
    self._mapy.clear()
    self._mapxy.clear()
    for i in range(0, len(self._scan)):
        if (
            not math.isnan(self._scan[i])
            and not math.isinf(self._scan[i])
            and self._scan[i]<=3
        ): 
            Xp = self._scan[i] * np.cos(self._scan_ang_rad[i] + self.theta)+self._position[0]
            Yp = self._scan[i] * np.sin(self._scan_ang_rad[i] + self.theta)+self._position[1]
            self._mapx.append(Xp)
            self._mapxy.append((Xp,Yp))
            self._mapy.append(Yp)
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
    