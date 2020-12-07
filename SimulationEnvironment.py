# -*- coding: utf-8 -*-

from Person import Person
from SupermarketManager import SupermarketManager
from WorkplaceOrSchoolManager import WorkplaceOrSchoolManager
from ConstantsAndRandom import ConstantsAndRandom
from Household import Household
from HouseholdManager import HouseholdManager
import time as tm
import pickle
import cProfile
import pstats
import math
import numpy as np

class SimulationEnvironment:
    
    def __init__(self, constantsAndRandom):
        self.constantsAndRandom = constantsAndRandom
        self.constantsAndRandom.initBeforeFirstDay()
        self.personList = []
        self.dictHealthStatusNextChange = {}
        
        for x in range(self.constantsAndRandom.Main_populationSize):
          self.personList.append(Person(x,self.constantsAndRandom))   
        
        constantsAndRandom.personList = self.personList
        numberOfPeopleWorkingOrInSchool = math.ceil(constantsAndRandom.shareOfPeopleWorkingOrInSchool * constantsAndRandom.Main_populationSize / 100)
        numberOfPeopleNotWorkingOrInSchool = constantsAndRandom.Main_populationSize - numberOfPeopleWorkingOrInSchool
        copyOfPersonList = constantsAndRandom.personList.copy()
        np.random.shuffle(copyOfPersonList)
        i = 0
        for person in copyOfPersonList:
            if(i < numberOfPeopleWorkingOrInSchool):
                constantsAndRandom.personList[person.id].working = True
            else:
                constantsAndRandom.personList[person.id].working = False
            i = i + 1

        if(constantsAndRandom.contactTracingOn):
            numberOfAdopters = math.ceil(constantsAndRandom.Main_populationSize * constantsAndRandom.contactTracingAdoptionPercentage / 100)
            numberOfNonAdopters = constantsAndRandom.Main_populationSize - numberOfAdopters
            np.random.shuffle(copyOfPersonList)
            i = 0
            for person in copyOfPersonList:
                if(i < numberOfAdopters):
                    constantsAndRandom.personList[person.id].adoptsContactTracing = True
                else:
                    constantsAndRandom.personList[person.id].adoptsContactTracing = False
                i = i + 1

        self.hhm = HouseholdManager(self.personList, self.constantsAndRandom, self.dictHealthStatusNextChange)
        self.wsm = WorkplaceOrSchoolManager(self.personList, self.constantsAndRandom, self.dictHealthStatusNextChange)
        self.smm = SupermarketManager(self.personList, self.constantsAndRandom, self.dictHealthStatusNextChange)
        
        timeTotal = 0
        self.time = 0
        self.day = 0
        self.constantsAndRandom.time_day = self.day

        for i in range(self.constantsAndRandom.numberOfPeopleInitiallyInfectious):
             timesHealthStatusChange = self.personList[i].setHealthStatusToExposed(timeTotal)
             self.dictHealthStatusNextChange.setdefault(timesHealthStatusChange[0],[]).append(self.personList[i].id)
             self.dictHealthStatusNextChange.setdefault(timesHealthStatusChange[1],[]).append(self.personList[i].id)
             self.dictHealthStatusNextChange.setdefault(timesHealthStatusChange[2],[]).append(self.personList[i].id)

        self.simulationEndingCondition = False
        self.numberSusceptibleEndOfDay = []
        self.numberExposedEndOfDay = []
        self.numberInfectiousEndOfDay = []
        self.numberRecoveredEndOfDay = []
        self.numberInQuarantineEndOfDay = []
        self.numberInQuarantineAndSusceptibleEndOfDay = []
        self.numberInQuarantineAndExposedEndOfDay = []
        self.numberInQuarantineAndInfectiousEndOfDay = []
        self.numberInQuarantineAndRecoveredEndOfDay = []
        self.numberSickEndOfDay = []
        
    def simulateDay(self):
      self.wsm.initDay()
      self.smm.initDay()

      timeToday = 0
      timeTotal = 86400 * 1000 * self.day + timeToday

      susceptible = len([p for p in self.personList if p.isSusceptible()])
      exposed = len([p for p in self.personList if p.isExposed()])
      infectious = len([p for p in self.personList if p.isInfectious()])
      recovered = len([p for p in self.personList if p.isRecovered()])
      inQuarantine = len([p for p in self.personList if p.isInQuarantine()])
      inQuarantineAndSusceptible = len([p for p in self.personList if (p.isInQuarantine() and p.isSusceptible())])
      inQuarantineAndExposed = len([p for p in self.personList if (p.isInQuarantine() and p.isExposed())])
      inQuarantineAndInfectious = len([p for p in self.personList if (p.isInQuarantine() and p.isInfectious())])
      inQuarantineAndRecovered = len([p for p in self.personList if (p.isInQuarantine() and p.isRecovered())])
      sick = len([p for p in self.personList if p.isSick])

      self.numberSusceptibleEndOfDay.append(susceptible)
      self.numberExposedEndOfDay.append(exposed)
      self.numberInfectiousEndOfDay.append(infectious)
      self.numberRecoveredEndOfDay.append(recovered)
      self.numberInQuarantineEndOfDay.append(inQuarantine)
      self.numberInQuarantineAndSusceptibleEndOfDay.append(inQuarantineAndSusceptible)
      self.numberInQuarantineAndExposedEndOfDay.append(inQuarantineAndExposed)
      self.numberInQuarantineAndInfectiousEndOfDay.append(inQuarantineAndInfectious)
      self.numberInQuarantineAndRecoveredEndOfDay.append(inQuarantineAndRecovered)

      self.numberSickEndOfDay.append(sick)

      self.simulationEndingCondition = (exposed == 0 and infectious == 0 and sick == 0 and inQuarantine == 0)
      if(self.simulationEndingCondition):
          return

      print("Now starting day",self.day, ":", susceptible, "susceptible,", exposed, "exposed,", infectious, "infectious,", recovered, "recovered,", inQuarantine, "in quarantine,", sick, "sick.")
      
      for person in self.personList:
          person.scheduleToday(self.day, timeTotal)
      
      while(timeToday < 86400000):
          if(timeToday % 8640000 == 0 and self.constantsAndRandom.printDuringDay):
              print("percentage:",100*timeToday/86400000)
          timeTotal = 86400 * 1000 * self.day + timeToday
          if(timeTotal in self.dictHealthStatusNextChange):
              peopleHealthStatusChangingID = self.dictHealthStatusNextChange[timeTotal]
              for personID in peopleHealthStatusChangingID:
                  person = self.personList[personID]
                  person.setNextHealthStatus(timeTotal)
          
          if(self.constantsAndRandom.workplaceOrSchoolSimulationOn):
            self.wsm.simulateTimestep(self.day,timeToday,timeTotal)
          if(self.constantsAndRandom.supermarketSimulationOn):
            self.smm.simulateTimestep(self.day,timeToday,timeTotal)

          timeToday += self.constantsAndRandom.simulationTimeStepInMillisecond

      self.hhm.simulateDay(self.day,timeToday,timeTotal)
      
      self.wsm.endDay()
      self.smm.endDay()
      
      self.day += 1
      self.constantsAndRandom.time_day = self.day

      self.constantsAndRandom.refreshRandomState()