# -*- coding: utf-8 -*-

from intervaltree import IntervalTree
from Location import Location
import numpy as np
import math as math

class Supermarket(Location):
    
  def initLocations(self):
    self.aisles=self.constantsAndRandom.getRandomNumberOfAislesInSupermarket_1()
    self.aisleLength=self.constantsAndRandom.Supermarket_aisleLength
    self.aisleWidth=self.constantsAndRandom.Supermarket_aisleWidth
    self.yRange=self.aisles*self.aisleLength
    self.xRange=self.aisleWidth
        
  def assignPhysicsNewVisitor(self, person, timeToday):
    duration = self.constantsAndRandom.randomIntUniform(self.constantsAndRandom.SupermarketVisit_minimumDuration,self.constantsAndRandom.SupermarketVisit_maximumDuration)
    if(timeToday+duration > self.constantsAndRandom.SupermarketVisit_closingTime):
        duration = self.constantsAndRandom.SupermarketVisit_closingTime - timeToday

    person.YbaseSpeed=self.yRange/duration # meters per millisecond
    maximumSpeedDelta = self.constantsAndRandom.Supermarket_MaximumWalkingSpeedMetersPerMilliSecond - person.YbaseSpeed
    maximumSpeedDelta = maximumSpeedDelta / self.constantsAndRandom.randomIntUniform(1,10)
    person.Ycycle_intensity = maximumSpeedDelta / 2 / person.Ycycle_duration # sine integral from 0 to pi is 2, unit meters per millisecond**2

    person.position=(self.constantsAndRandom.randomFloatBetweenZeroAndNumber(self.xRange),0) # meters
    person.Yspeed=person.YbaseSpeed # meters per millisecond
    person.Xspeed=0 # meters per millisecond
    person.Yacceleration=0 # meters per millisecond^2
    person.Xacceleration=0 # meters per millisecond^2
    person.visitStart=timeToday
        
  def assignPhysicsUpdate(self, person, timeToday):
    person.Xacceleration = self.constantsAndRandom.getRandomXaccelerationPerson_mms2()

    speedTotal = math.sqrt(person.Xspeed**2+person.Yspeed**2)
    
    if(speedTotal > self.constantsAndRandom.Supermarket_MaximumWalkingSpeedMetersPerMilliSecond):
        person.Xspeed = np.sign(person.Xspeed) * math.sqrt(self.constantsAndRandom.Supermarket_MaximumWalkingSpeedMetersPerMilliSecond**2 - person.Yspeed**2)
                
    if(person.Xspeed > self.constantsAndRandom.Supermarket_MaximumWalkingSpeedMetersPerMilliSecond and person.Xacceleration > 0):
        person.Xacceleration = - person.Xacceleration
    if(person.Xspeed < - self.constantsAndRandom.Supermarket_MaximumWalkingSpeedMetersPerMilliSecond and person.Xacceleration < 0):
        person.Xacceleration = - person.Xacceleration
    
    person.Yacceleration = person.Ycycle_intensity * math.sin(math.pi*(timeToday - person.visitStart)/person.Ycycle_duration)

    if(person.position[0] > self.xRange):
        person.position = (self.xRange,person.position[1])
    if(person.position[0] < 0):
        person.position = (0,person.position[1])
    if(person.position[1]<0):
        person.position = (person.position[0],0)
    if(person.position[1]>self.yRange):
        person.standardSupermarket.visitorsNowList.remove(person)
    
  def initDayCustom(self):
    pass
    
  def noteVisitFromPersonCustom(self,person):
    person.daysInSupermarket.append(self.constantsAndRandom.time_day)