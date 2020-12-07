# -*- coding: utf-8 -*-

from Location import Location
from intervaltree import IntervalTree
import math
import numpy as np

class WorkplaceOrSchool(Location):
    
  def initLocations(self):
    self.rowCapacity = self.constantsAndRandom.getRandomNumberRowCapacityOfWorkplace_1()
    self.capacity = self.rowCapacity**2
    self.distanceBetweenSeats = self.constantsAndRandom.getRandomDistanceBetweenWorkplaceOrSchoolSeats()
    
  def initDayCustom(self):
    self.availableSeats = np.arange(1, self.capacity+1)
    np.random.shuffle(self.availableSeats)
    self.availableSeats = list(self.availableSeats)
    
  def noteVisitFromPersonCustom(self,person):
    person.daysInWorkplaceOrSchool.append(self.constantsAndRandom.time_day)
        
  def assignPhysicsNewVisitor(self, person, timeToday):
    indexOfSeat = self.availableSeats.pop(0)

    seatXindex = indexOfSeat % self.rowCapacity
    seatYindex = int((indexOfSeat - seatXindex) / self.rowCapacity)

    person.workOrSchool_PositionSeat = (self.distanceBetweenSeats*(seatXindex+1),self.distanceBetweenSeats*(seatYindex+1))
    person.workOrSchool_XcoordinateAisle = self.distanceBetweenSeats*(seatXindex+0.5)
    person.position = (person.workOrSchool_XcoordinateAisle,0)
    person.Xspeed = 0 # meters per millisecond
    person.Yspeed = self.constantsAndRandom.WorklocationManager_WalkingSpeedMetersPerMilliSecond # meters per millisecond
    person.Yacceleration = 0 # meters per millisecond^2
    person.Xacceleration = 0 # meters per millisecond^2
        
  def assignPhysicsUpdate(self, person, timeToday):
    if(timeToday <= self.constantsAndRandom.WorklocationVisit_openingTime+self.constantsAndRandom.WorklocationVisit_duration/2): # arriving
        if(person.Yspeed > 0 and person.position[1] >= person.workOrSchool_PositionSeat[1]): # walked to far in y direction
            if(person.position[1] > person.workOrSchool_PositionSeat[1]):
                person.position = (person.position[0],person.workOrSchool_PositionSeat[1])
            person.Yspeed = 0
            person.Xspeed = self.constantsAndRandom.WorklocationManager_WalkingSpeedMetersPerMilliSecond
        if(person.Xspeed > 0 and person.position[0] >= person.workOrSchool_PositionSeat[0]): # walked to far in x direction
            if(person.position[0] > person.workOrSchool_PositionSeat[0]):
                person.position = (person.workOrSchool_PositionSeat[0],person.position[1])
            person.Xspeed = 0
    else: # leaving
        if(timeToday == person.timeTodayWorkplaceOrSchoolVisit + self.constantsAndRandom.WorklocationVisit_duration):
            person.Xspeed = - self.constantsAndRandom.WorklocationManager_WalkingSpeedMetersPerMilliSecond
        if(person.Xspeed < 0 and person.position[0] <= person.workOrSchool_XcoordinateAisle): # walked to far in x direction
            if(person.position[0] < person.workOrSchool_XcoordinateAisle):
                person.position = (person.workOrSchool_XcoordinateAisle,person.position[1])
            person.Xspeed = 0
            person.Yspeed = - self.constantsAndRandom.WorklocationManager_WalkingSpeedMetersPerMilliSecond
        if(person.position[1] <= 0):
            self.visitorsNowList.remove(person)