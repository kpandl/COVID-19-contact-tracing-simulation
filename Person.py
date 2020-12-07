# -*- coding: utf-8 -*-

from intervaltree import Interval, IntervalTree
import numpy as np

class Person:
    
  def __init__(self, id, constantsAndRandom):
    self.id = id
    self.constantsAndRandom = constantsAndRandom
    self.healthStatus=0 # 0=susceptible, 1=exposed, 2=infectious, 3=recovered
    self.isSick = False
    self.healthStatusChanged=0
    self.healthStatusNextChange=0
    self.dailySupermarketVisitProbability = constantsAndRandom.Person_dailySupermarketVisitProbability
    self.working = False

    self.prepareForQuarantine = False
    self.inQuarantine = False
    self.infectiousnessEstimation = []

    self.quarantineDueToInfection = 0
    self.timeWhenSick = 0
    self.quarantineDueToContactTracing = 0
    self.quarantineDueToContactTracingTime = 0
    self.quarantineDueToInfectionOfHouseholdMember = 0
    self.quarantineDueToInfectionOfHouseholdMemberTime = 0
    self.quarantineDueToContactTracingOfHouseholdMember = 0
    self.quarantineDueToContactTracingOfHouseholdMemberTime = 0

    self.partOfLocationSimulation = True

    self.tracingAppSignalReceivers = IntervalTree()
    self.tracingAppSignalReceivers2 = {}
    self.receivedTracingAppNotification = False
    self.receivedTracingAppNotificationTime = 0
    self.houseHoldMembers = []
    self.standardDeviationInfectionSpreading = np.random.triangular(self.constantsAndRandom.infectionRadiusStandardDeviation_Min,self.constantsAndRandom.infectionRadiusStandardDeviation_Mode,self.constantsAndRandom.infectionRadiusStandardDeviation_Max)#self.constantsAndRandom.randomFloatBetweenZeroAndNumber(self.constantsAndRandom.infectionRadiusStandardDeviation)
    self.position=(0,0)
    self.Yspeed=0 # meters per millisecond
    self.Xspeed=0 # meters per millisecond
    self.YbaseSpeed=0
    self.Ycycle_duration = self.constantsAndRandom.Supermarket_CycleDuration
    self.Ycycle_intensity = 0
    self.XtargetSpeed = 0
    self.Yacceleration = 0 # meters per millisecond^2
    self.Xacceleration = 0 # meters per millisecond^2

    self.adoptsContactTracing = False

    self.sick = False

    self.daysInSupermarket = []
    self.daysInWorkplaceOrSchool=[]

  def __getitem__(self, index):        
    if index == 0:
        return self.position[0]
    elif index == 1:
        return self.position[1]
    else:          
        raise IndexError('Unit coordinates are 2 dimensional')
    
  def __len__(self):        
    return 2
    
  def setStandardSupermarket(self,supermarket):
    self.standardSupermarket = supermarket

  def setWorkplaceOrSchool(self,workplaceOrSchool):
    self.workplaceOrSchool = workplaceOrSchool
    
  def isInQuarantine(self):
    return((self.quarantineDueToInfection==2) or (self.quarantineDueToContactTracing==2) or (self.quarantineDueToContactTracingOfHouseholdMember==2) or (self.quarantineDueToInfectionOfHouseholdMember==2))
    
  def scheduleToday(self, day, timeTotal):

    self.evaluateQuarantineEnd(timeTotal)

    if(self.quarantineDueToInfection==1):
        self.quarantineDueToInfection = 2
    if(self.quarantineDueToContactTracing==1):
        self.quarantineDueToContactTracing = 2
    if(self.quarantineDueToContactTracingOfHouseholdMember==1):
        self.quarantineDueToContactTracingOfHouseholdMember = 2
    if(self.quarantineDueToInfectionOfHouseholdMember==1):
        self.quarantineDueToInfectionOfHouseholdMember = 2

    inQuarantine = self.isInQuarantine()

    if(not inQuarantine and not self.isRecovered()):
        workToday = (day % 7 <= 4) and (self.working == 1) # Mon=0, Tue, Wed, Thur, or Friday
        supermarketToday = self.constantsAndRandom.drawProbability(self.constantsAndRandom.Person_dailySupermarketVisitProbability)
        if(day % 7 == 6):
            supermarketToday = False # Sunday

        if(workToday):
            self.timeTodayWorkplaceOrSchoolVisit = self.constantsAndRandom.getRandomTimeWorkplaceVisit_ms()
            self.workplaceOrSchool.addVisitorToday(self, self.timeTodayWorkplaceOrSchoolVisit)
        if(workToday and supermarketToday):
            self.standardSupermarket.addVisitorToday(self, self.constantsAndRandom.getRandomTimeWithinSimulationBetweenTwoTimes_ms(self.constantsAndRandom.WorklocationVisit_closingTime+1000*60*60,self.constantsAndRandom.SupermarketVisit_lastPossibleTime-self.constantsAndRandom.SupermarketVisit_minimumDuration))
        if(not workToday and supermarketToday):
            self.standardSupermarket.addVisitorToday(self, self.constantsAndRandom.getRandomTimeWithinSimulationBetweenTwoTimes_ms(self.constantsAndRandom.SupermarketVisit_openingTime,self.constantsAndRandom.SupermarketVisit_lastPossibleTime-self.constantsAndRandom.SupermarketVisit_minimumDuration))

  def isSusceptible(self):
    return (self.healthStatus==0)
    
  def isExposed(self):
    return (self.healthStatus==1)
    
  def isInfectious(self):
    return (self.healthStatus==2)
    
  def isRecovered(self):
    return (self.healthStatus==3)
    
  def receiveTracingAppNotificationPotentialInfection(self, timeOfNotification):
    if(self.adoptsContactTracing and self.quarantineDueToContactTracing!=2):
        self.quarantineDueToContactTracing = 1
        self.quarantineDueToContactTracingTime = timeOfNotification
        if(self.constantsAndRandom.contactTracingAffectsHouseholdMembers):
            for houseHoldMember in self.houseHoldMembers:
                houseHoldMember.receiveTracingAppNotificationPotentialInfectionOfHouseholdMember(timeOfNotification)
    
  def receiveTracingAppNotificationPotentialInfectionOfHouseholdMember(self, timeOfNotification):
    if(self.adoptsContactTracing and self.quarantineDueToContactTracingOfHouseholdMember!=2):
        self.quarantineDueToContactTracingOfHouseholdMember = 1
        self.quarantineDueToContactTracingOfHouseholdMemberTime = timeOfNotification
    
  def receiveInformationInfectionOfHouseholdMember(self, timeOfInformation):
    self.quarantineDueToInfectionOfHouseholdMember = 1
    self.quarantineDueToInfectionOfHouseholdMemberTime = timeOfInformation
    
  def evaluateQuarantineEnd(self, timeNow):
    if(self.quarantineDueToContactTracing == 2 and self.quarantineDueToContactTracingTime + self.constantsAndRandom.contactTracingQuarantinePeriod < timeNow):
        self.quarantineDueToContactTracing = 0
        if(not self.isSick and not self.isRecovered() and self.constantsAndRandom.drawProbability(self.constantsAndRandom.contactTracingStopProbabilityForPersonAfterFalsePositive)):
            self.adoptsContactTracing = False
    if(self.quarantineDueToContactTracingOfHouseholdMember == 2 and self.quarantineDueToContactTracingOfHouseholdMemberTime + self.constantsAndRandom.contactTracingQuarantinePeriod < timeNow):
        self.quarantineDueToContactTracingOfHouseholdMember = 0
        if(not self.isSick and not self.isRecovered() and self.constantsAndRandom.drawProbability(self.constantsAndRandom.contactTracingStopProbabilityForPersonAfterFalsePositive)):
            self.adoptsContactTracing = False
    if(self.quarantineDueToInfection == 2 and self.timeWhenSick + self.constantsAndRandom.infectionQuarantinePeriod < timeNow):
        self.quarantineDueToInfection = 0
    if(self.quarantineDueToInfectionOfHouseholdMember == 2 and self.quarantineDueToInfectionOfHouseholdMemberTime + self.constantsAndRandom.infectionQuarantinePeriod < timeNow):
        self.quarantineDueToInfectionOfHouseholdMember = 0

  def setHealthStatusToExposed(self, timeTotal):
      self.healthStatus=1
      durationUntilSick = self.constantsAndRandom.getRandomDurationTimeUntilSick_Milliseconds()
      self.timeWhenSick = timeTotal + durationUntilSick
      durationUntilInfectious = durationUntilSick - self.constantsAndRandom.durationInfectiousBeforeSick
      if(durationUntilInfectious < self.constantsAndRandom.simulationTimeStepInMillisecond):
          durationUntilInfectious = self.constantsAndRandom.simulationTimeStepInMillisecond
      self.timeWhenInfectious = timeTotal + durationUntilInfectious
      self.timeWhenRecovered = self.timeWhenInfectious + self.constantsAndRandom.durationInfectious

      return [self.timeWhenSick, self.timeWhenInfectious, self.timeWhenRecovered]
    
  def setNextHealthStatus(self, timeTotal):
      if(timeTotal == self.timeWhenSick):
          self.isSick = True
          if(self.constantsAndRandom.sickPeopleGoInQuarantine):
            self.quarantineDueToInfection = 1
          for k in self.tracingAppSignalReceivers2:
              otherPersonReceivedSignals = self.tracingAppSignalReceivers2[k]
              timeOfLatestContact = otherPersonReceivedSignals[0]
              if(timeTotal <= timeOfLatestContact + self.constantsAndRandom.contactTracingStoragePeriod and timeOfLatestContact >= 0):
                otherPerson = self.constantsAndRandom.personList[k]
                otherPerson.receiveTracingAppNotificationPotentialInfection(timeTotal)

          if(self.constantsAndRandom.contactTracingOn and not self.constantsAndRandom.proximityBasedContactTracing):
              for dayInSupermarket in self.daysInSupermarket:
                  visitorsList=[]
                  if(dayInSupermarket >= self.constantsAndRandom.time_day - self.constantsAndRandom.contactTracingStoragePeriod / 24*3600*1000 and dayInSupermarket < self.constantsAndRandom.time_day):
                      visitorsList = self.standardSupermarket.visitorsTodayHistory[dayInSupermarket]
                  elif(dayInSupermarket == self.constantsAndRandom.time_day):
                      visitorsList = self.standardSupermarket.visitorsToday

                  for otherPerson in visitorsList:
                      otherPerson.receiveTracingAppNotificationPotentialInfection(timeTotal)

              for dayInWorkplaceOrSchool in self.daysInWorkplaceOrSchool:
                  visitorsList=[]
                  if(dayInWorkplaceOrSchool >= self.constantsAndRandom.time_day - self.constantsAndRandom.contactTracingStoragePeriod / 24*3600*1000 and dayInWorkplaceOrSchool < self.constantsAndRandom.time_day):
                      visitorsList = self.workplaceOrSchool.visitorsTodayHistory[dayInWorkplaceOrSchool]
                  elif(dayInWorkplaceOrSchool == self.constantsAndRandom.time_day):
                      visitorsList = self.workplaceOrSchool.visitorsToday

                  for otherPerson in visitorsList:
                      otherPerson.receiveTracingAppNotificationPotentialInfection(timeTotal)
                           
          if(self.constantsAndRandom.HouseholdMembersGoInQuarantine):
              for householdMember in self.houseHoldMembers:
                householdMember.receiveInformationInfectionOfHouseholdMember(timeTotal)

      elif(timeTotal == self.timeWhenInfectious):
          self.healthStatus = 2
      elif(timeTotal == self.timeWhenRecovered):
          self.isSick = False
          self.healthStatus = 3
          self.quarantineDueToInfection = 0