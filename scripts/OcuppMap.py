import numpy as np

class mapa:
    def __init__(self, size, resolution, pHit, pMiss, pose):
        self._resolution = resolution
        self._cells = int(size*2 / resolution)
        self._l0 = np.log(1)
        self._map = np.zeros((self._cells, self._cells)) + self._l0
        self._mapToPlot = np.zeros((self._cells, self._cells)) + 0.5
        self._lHit = np.log(pHit/(1-pHit))
        self._lMiss = np.log(pMiss/(1-pMiss))
        self._point0x = self._cells/2 + pose[0]# - 0.18
        self._point0y = self._cells/2 + pose[1]


    def getMap(self):
        return self._map, self._mapToPlot

    def updateMap(self, X, Y, pose):
        for i in range(0, len(X)):
            self.MissBoxes(pose, [X[i], Y[i]])
            self.updateCell(X[i], Y[i])


    def updateCell(self, x, y):

        _x = int(x / self._resolution + self._point0x)
        _y = int(y / self._resolution + self._point0y)

        lt = self._map[_y][_x]
        # lt = lt + self.inverse_sensor_model(lt) - self._l0
        lt = lt + self._lHit - self._l0

        self._map[_y][_x] = lt
        self._mapToPlot[_y][_x] = self.LogToP(lt)
    
    def LogToP(self, lt):
        p = 1 - 1/(1+np.exp(lt))
        return p
    
    def GlobalCoord(self,x,y):
        position = np.array([0, 0], dtype=np.float)
        x = x
        x = y
        position[0]= x * self._resolution
        position[1]= y * self._resolution
        return position
    def distancePointToLine(self, A, B, C, xPoint, yPoint):
        return np.absolute(A * xPoint + B * yPoint + C) / np.sqrt(A * A + B * B)
    def MissBoxes(self,startPoint, endPoint):
        
        A = endPoint[1] - startPoint[1]
        B = startPoint[0] - endPoint[0]
        C = endPoint[0] * startPoint[1] - startPoint[0] * endPoint[1]
        startPointInt=[0,0]
        endPointInt=[0,0]
        startPointInt[0]= int(startPoint[0] / self._resolution + self._point0x)
        startPointInt[1] = int(startPoint[1] / self._resolution + self._point0y)
        endPointInt[0]= int(endPoint[0] / self._resolution + self._point0x)
        endPointInt[1] = int(endPoint[1] / self._resolution + self._point0y)
        rangeForX = 0
        if startPointInt[0] < endPointInt[0]:
            rangeForX = range(startPointInt[0], endPointInt[0])
        elif startPointInt[0] > endPointInt[0]:
            rangeForX = range(startPointInt[0], endPointInt[0], -1)
        else:
            rangeForX = [startPointInt[0]]
        rangeForY = 0
        if startPointInt[1] < endPointInt[1]:
            rangeForY = range(startPointInt[1], endPointInt[1])
        elif startPointInt[1] > endPointInt[1]:
            rangeForY = range(startPointInt[1], endPointInt[1], -1)
        else:
            rangeForY = [startPointInt[1]]

        for x in rangeForX:
            for y in rangeForY:
                # glob = self.GlobalCoord(x,y)
                # if self.distancePointToLine(A,B,C,glob[0],glob[1]) < 2*self._resolution:
                        lt = self._map[y][x]
                        lt = lt + self._lMiss - self._l0
                        self._map[y][x] = lt
                        self._mapToPlot[y][x] = self.LogToP(lt)