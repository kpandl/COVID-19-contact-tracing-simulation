# -*- coding: utf-8 -*-

from LocationManager import LocationManager
from WorkplaceOrSchool import WorkplaceOrSchool
from intervaltree import Interval, IntervalTree
import math

class WorkplaceOrSchoolManager(LocationManager):
    
  def initLocations(self):
    
    self.listOfPeopleWorking = [p for p in self.personList if p.working==1]
    numberOfPeopleWorking = len(self.listOfPeopleWorking)
    
    numberOfWorklocations = 0
    numberOfWorkplaces = 0
    personCounter = 0
    
    while(numberOfWorkplaces < numberOfPeopleWorking):
        newWorklocation = WorkplaceOrSchool(self.constantsAndRandom, self.dictHealthStatusNextChange)
        numberOfWorklocations += 1
        numberOfWorkplaces += newWorklocation.capacity
        self.locationList.append(newWorklocation)
        while(personCounter < numberOfPeopleWorking and personCounter < numberOfWorkplaces):
            self.listOfPeopleWorking[personCounter].setWorkplaceOrSchool(newWorklocation)
            personCounter += 1
    
  def checkSimulationCondition(self,day,timeToday):
      if(timeToday >= self.constantsAndRandom.WorklocationVisit_openingTime and timeToday <= self.constantsAndRandom.WorklocationVisit_closingTime-self.constantsAndRandom.WorklocationVisit_duration+1.1*self.constantsAndRandom.WorklocationVisit_maximumWalkDuration+self.constantsAndRandom.minimumContactDurationForPositiveTracingResult):
          return True
      if(timeToday >= self.constantsAndRandom.WorklocationVisit_openingTime + self.constantsAndRandom.WorklocationVisit_duration and timeToday <= self.constantsAndRandom.WorklocationVisit_closingTime+1.1*self.constantsAndRandom.WorklocationVisit_maximumWalkDuration+self.constantsAndRandom.minimumContactDurationForPositiveTracingResult):
          return True
      return False
    
  def assignWorkersToday(self,personList):

      self.listOfPeopleWorkingToday = [p for p in self.listOfPeopleWorking if p.worklocationVisit.activeToday==1]
      self.numberOfPeopleworkingToday = len(self.listOfPeopleWorkingToday)

      if(self.numberOfPeopleworkingToday == 0):
          return
      
      for worklocation in self.locationList:
          worklocation.initNewDay()

      for person in self.listOfPeopleWorkingToday:
          self.locationList[person.worklocation.id].addWorkerToday(person)