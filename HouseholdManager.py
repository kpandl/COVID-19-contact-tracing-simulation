# -*- coding: utf-8 -*-

from Household import Household
import numpy as np

class HouseholdManager:
    
  def __init__(self, personList, constantsAndRandom, dictHealthStatusNextChange):
    self.personList = personList
    self.constantsAndRandom = constantsAndRandom
    self.dictHealthStatusNextChange = dictHealthStatusNextChange
    self.householdList = []

    shuffledPersonList = personList.copy()
    np.random.shuffle(shuffledPersonList)

    numberOfPeopleInHoushold = 0
    while (numberOfPeopleInHoushold < self.constantsAndRandom.Main_populationSize):
        houseHoldSize = self.constantsAndRandom.getRandomHouseholdSize_1()
        personsInHoushold = []
        i = numberOfPeopleInHoushold
        while (i < numberOfPeopleInHoushold + houseHoldSize and i < self.constantsAndRandom.Main_populationSize):
            personsInHoushold.append(shuffledPersonList[i])
            i+=1
        for person in personsInHoushold:
            otherPersonsInHoushold = personsInHoushold.copy()
            otherPersonsInHoushold.remove(person)
            person.houseHoldMembers = otherPersonsInHoushold
        self.householdList.append(Household(personsInHoushold))
        numberOfPeopleInHoushold += houseHoldSize

  def simulateDay(self,day,timeToday,timeTotal):
    for household in self.householdList:
        if(not household.everybodyInfected):
            for person in household.personList:
                if(person.isInfectious()):
                    for otherPerson in person.houseHoldMembers:
                        if(otherPerson.isSusceptible()):
                            timesHealthStatusChange = otherPerson.setHealthStatusToExposed(timeTotal)
                            self.dictHealthStatusNextChange.setdefault(timesHealthStatusChange[0],[]).append(otherPerson.id)
                            self.dictHealthStatusNextChange.setdefault(timesHealthStatusChange[1],[]).append(otherPerson.id)
                            self.dictHealthStatusNextChange.setdefault(timesHealthStatusChange[2],[]).append(otherPerson.id)
                    household.everybodyInfected=True