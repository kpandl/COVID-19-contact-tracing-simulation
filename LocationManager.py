# -*- coding: utf-8 -*-

class LocationManager:
    
  def __init__(self, personList, constantsAndRandom, dictHealthStatusNextChange):
    self.personList = personList
    self.constantsAndRandom = constantsAndRandom
    self.dictHealthStatusNextChange = dictHealthStatusNextChange
    self.locationList = []
    self.initLocations()
    
  def simulateTimestep(self,day,timeToday,timeTotal):
      if(not self.checkSimulationCondition(day,timeToday)):
          return
      for location in self.locationList:
          location.simulateTimestep(day,timeToday,timeTotal)

  def initDay(self):
    for location in self.locationList:
        location.initDay()
        location.initDayCustom()

  def endDay(self):
    for location in self.locationList:
        location.endDay()