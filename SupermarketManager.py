# -*- coding: utf-8 -*-

from LocationManager import LocationManager
from Supermarket import Supermarket
from intervaltree import Interval, IntervalTree
import numpy as np
import math

class SupermarketManager(LocationManager):
    
  def initLocations(self):
    self.invervaltreeAisles = IntervalTree()
    self.supermarketAislesTotal=0
      
    for x in range(self.constantsAndRandom.Main_numberOfSupermarkets):
        supermarket = Supermarket(self.constantsAndRandom, self.dictHealthStatusNextChange)
        self.supermarketAislesTotal += supermarket.aisles
        self.locationList.append(supermarket)
      
    i=0
    for x in range(self.constantsAndRandom.Main_numberOfSupermarkets):
        supermarket = self.locationList[x]
        self.invervaltreeAisles[i:i+supermarket.aisles]=supermarket
        i += supermarket.aisles
    
    for person in self.personList:
        supermarket = self.invervaltreeAisles[self.constantsAndRandom.randomIntUniform(0,self.supermarketAislesTotal-1)].pop().data
        person.setStandardSupermarket(supermarket)
    
  def checkSimulationCondition(self,day,timeToday):
      if(timeToday >= self.constantsAndRandom.SupermarketVisit_openingTime and timeToday <= self.constantsAndRandom.SupermarketVisit_lastPossibleTime):
          return True
      if(timeToday >= self.constantsAndRandom.SupermarketVisit_lastPossibleTime and len(self.locationList[0].visitorsNowList) > 0):
          return True
      return False