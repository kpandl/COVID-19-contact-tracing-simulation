# -*- coding: utf-8 -*-

from scipy import spatial
import math

class Location:
    
  def __init__(self, constantsAndRandom, dictHealthStatusNextChange):
    self.constantsAndRandom = constantsAndRandom
    self.dictHealthStatusNextChange = dictHealthStatusNextChange
    self.initDay()
    self.initLocations()
    self.visitorsTodayHistory = []
    
  def simulateTimestep(self,day,timeToday,timeTotal):
    if(timeToday in self.visitTimesToday):
        newVisitors = self.visitTimesToday[timeToday]
        for person in newVisitors:
            self.assignPhysicsNewVisitor(person, timeToday)
            self.visitorsNowList.append(person)
            self.noteVisitFromPersonCustom(person)
            if(self.constantsAndRandom.contactTracingOn and not self.constantsAndRandom.proximityBasedContactTracing and person.adoptsContactTracing): # QR code based
                self.visitorsToday.append(person)
        if(len(self.visitorsNowList) == 0):
            return
    self.__spreadDiseaseAndTraceContacts(timeTotal)
    self.__movePeople(timeToday)
        
  def __spreadDiseaseAndTraceContacts(self, timeTotal):
    if(len(self.visitorsNowList) < 2):
        return
    tree = spatial.cKDTree(self.visitorsNowList)

    queryRadius = self.constantsAndRandom.MaximumInfectionRadiusMeter
    if(self.constantsAndRandom.contactTracingOn and queryRadius < self.constantsAndRandom.ContactTracingRadiusMeter):
        queryRadius = self.constantsAndRandom.ContactTracingRadiusMeter

    queryResult = tree.query_ball_tree(tree,queryRadius)

    for pointIndex in range(len(queryResult)):
        otherPoints = queryResult[pointIndex]
        centerPerson = self.visitorsNowList[pointIndex]
        for otherPoint in otherPoints:
            if(otherPoint == pointIndex):
                continue
            otherPerson = self.visitorsNowList[otherPoint]
            distance = math.sqrt((centerPerson.position[0]-otherPerson.position[0])**2+(centerPerson.position[1]-otherPerson.position[1])**2)
            if(centerPerson.isInfectious() and otherPerson.isSusceptible() and distance < self.constantsAndRandom.MaximumInfectionRadiusMeter):
                if(distance <= self.constantsAndRandom.randomNumberFromHalfNormalDistribution(0,centerPerson.standardDeviationInfectionSpreading) and self.constantsAndRandom.drawProbability(self.constantsAndRandom.infectionProbability)):
                    timesHealthStatusChange = otherPerson.setHealthStatusToExposed(timeTotal)
                    self.dictHealthStatusNextChange.setdefault(timesHealthStatusChange[0],[]).append(otherPerson.id)
                    self.dictHealthStatusNextChange.setdefault(timesHealthStatusChange[1],[]).append(otherPerson.id)
                    self.dictHealthStatusNextChange.setdefault(timesHealthStatusChange[2],[]).append(otherPerson.id)
            if(self.constantsAndRandom.contactTracingOn and self.constantsAndRandom.proximityBasedContactTracing and centerPerson.adoptsContactTracing and otherPerson.adoptsContactTracing and distance < self.constantsAndRandom.ContactTracingRadiusMeter):
                lastContactTracingPositiveTime = -1
                timeOfFirstContact = timeTotal
                timeOfLastContact = timeTotal
                if(otherPerson.id in centerPerson.tracingAppSignalReceivers2):
                    lastContactTracingPositiveTime = centerPerson.tracingAppSignalReceivers2[otherPerson.id][0]
                    timeOfFirstContact = centerPerson.tracingAppSignalReceivers2[otherPerson.id][1]
                    timeOfLastContact = centerPerson.tracingAppSignalReceivers2[otherPerson.id][2]

                if(timeOfLastContact >= timeTotal - self.constantsAndRandom.simulationTimeStepInMillisecond):
                    if(timeTotal - timeOfFirstContact == self.constantsAndRandom.minimumContactDurationForPositiveTracingResult):
                        lastContactTracingPositiveTime = timeTotal
                else:
                    timeOfFirstContact = timeTotal

                timeOfLastContact = timeTotal
                centerPerson.tracingAppSignalReceivers2[otherPerson.id] = (lastContactTracingPositiveTime,timeOfFirstContact,timeOfLastContact)

  def __movePeople(self, timeToday):
        for person in self.visitorsNowList:
            currentXpos = person.position[0]
            nextXpos = currentXpos + person.Xspeed * self.constantsAndRandom.simulationTimeStepInMillisecond + 0.5 * person.Xacceleration * self.constantsAndRandom.simulationTimeStepInMillisecond**2
            currentYpos = person.position[1]
            nextYpos = currentYpos + person.Yspeed * self.constantsAndRandom.simulationTimeStepInMillisecond + 0.5 * person.Yacceleration * self.constantsAndRandom.simulationTimeStepInMillisecond**2
            
            person.position=(nextXpos,nextYpos)
            person.Xspeed += person.Xacceleration * self.constantsAndRandom.simulationTimeStepInMillisecond
            person.Yspeed += person.Yacceleration * self.constantsAndRandom.simulationTimeStepInMillisecond

            self.assignPhysicsUpdate(person, timeToday)
    
  def initDay(self):
    self.visitTimesToday = {}
    self.visitorsNowList = []
    self.visitorsToday = []
    
  def endDay(self):
    if(not self.constantsAndRandom.proximityBasedContactTracing and self.constantsAndRandom.contactTracingOn):
        self.visitorsTodayHistory.append(self.visitorsToday)
    
  def addVisitorToday(self, person, visitTime):
    self.visitTimesToday.setdefault(visitTime,[]).append(person)