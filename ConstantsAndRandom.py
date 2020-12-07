# -*- coding: utf-8 -*-

# Here you can set various parameters for the simulation

import numpy as np
from scipy.stats import beta
import math

class ConstantsAndRandom:
    
    def __init__(self, randomSeed):
        self.randomSeed = randomSeed
    
        self.Main_populationSize = 10000
        self.numberOfPeopleInitiallyInfectious = 10
        self.Main_numberOfSupermarkets = 3
        
        self.sickPeopleGoInQuarantine = True
        self.HouseholdMembersGoInQuarantine = True
        
        self.Person_dailySupermarketVisitProbability = 0.2 # should be between 0 and 1
        self.shareOfPeopleWorkingOrInSchool = 60 # should be between 0 and 100
        
        self.Supermarket_aisleLength = 40 # meters
        self.Supermarket_aisleWidth = 4 # meters
        self.Supermarket_minimumNumberOfAisles = 10
        self.Supermarket_maximumNumberOfAisles = 10
        
        self.MaximumInfectionRadiusMeter = 2 # meters
        self.ContactTracingRadiusMeter = 2 # meters
        self.Supermarket_MaximumWalkingSpeedMetersPerMilliSecond = 1/1000
        self.Supermarket_MaximumAccelerationXDirection = 0.8 # in m/s^2
        self.Supermarket_CycleDuration = 3 * 60 * 1000 # in ms, equal to 3 min
        
        self.SupermarketVisit_openingTime = 8*3600*1000 # 8 AM in milliseconds
        self.SupermarketVisit_closingTime = 20*3600*1000 # 8 PM in milliseconds
        self.SupermarketVisit_lastPossibleTime = 20*3600*1000 # 8 PM in milliseconds
        self.SupermarketVisit_minimumDuration = 15*60*1000 # 15 minutes in milliseconds
        self.SupermarketVisit_maximumDuration = 45*60*1000 # 60 minutes in milliseconds
        
        self.WorklocationVisit_openingTime = 8*3600*1000 # 8 AM in milliseconds
        self.WorklocationVisit_closingTime = 17*3600*1000 - 0.5*3600*1000 # 4:30 PM in milliseconds
        self.WorklocationVisit_duration = 8*3600*1000 # 8 hours in milliseconds
        
        self.WorklocationManager_WalkingSpeedMetersPerMilliSecond = 1/1000
        
        self.targetHouseHoldSizeDistribution = [0.423,0.332,0.119,0.091,0.035] # nubers should be between 0 and 1, nth array position for share of household size n, n>= 1
        
        self.infectionRadiusStandardDeviation_Min = 0 # meters
        self.infectionRadiusStandardDeviation_Mode = 0.5 # meters
        self.infectionRadiusStandardDeviation_Max = 1 # meters
        self.infectionProbability = 0.05 # should be between 0 and 1

        self.workplaceOrSchoolSimulationOn = True
        self.supermarketSimulationOn = True

        self.MinimumRowCapacityWorkplaceOrSchool = 2
        self.MaximumRowCapacityWorkplaceOrSchool = 8

        self.contactTracingOn = True
        self.proximityBasedContactTracing = True
        self.contactTracingAdoptionPercentage = 60
        self.contactTracingStopProbabilityForPersonAfterFalsePositive = 0
        self.contactTracingAffectsHouseholdMembers = True
        self.contactTracingStoragePeriod = 9*24*3600*1000 # 9 days in milliseconds - must be full days in the case of QR codes
        self.contactTracingQuarantinePeriod = 10*24*3600*1000 # 10 days in milliseconds
        self.minimumContactDurationForPositiveTracingResult = 15000 # 15 seconds in milliseconds
        
        self.simulationTimeStepInMillisecond = 100 # milliseconds
        
        self.infectionQuarantinePeriod = 14*24*3600*1000 # 14 days in milliseconds

        self.printDuringDay = False # true for debugging purposes only

        self.WorkplaceOrSchoolMinimumDistanceBetweenSeats = 1.5 # meters
        self.WorkplaceOrSchoolMaximumDistanceBetweenSeats = 2 # meters

        self.durationTimeUntilSickMinimum = 1 * 86400 * 1000 # 1 day in milliseconds
        self.durationTimeUntilSickMode = 5.5 * 86400 * 1000 # 5.5 days in milliseconds
        self.durationTimeUntilSickMaximum = 14 * 86400 * 1000 # 14 days in milliseconds
        
        self.durationInfectiousBeforeSick = 2 * 86400 * 1000 # 2 days in milliseconds
        self.durationInfectious = 9 * 86400 * 1000 # 9 days in milliseconds
      
    def initBeforeFirstDay(self):
        self.WorklocationVisit_maximumWalkDuration=round(((1.5+10)*self.WorkplaceOrSchoolMaximumDistanceBetweenSeats)/self.WorklocationManager_WalkingSpeedMetersPerMilliSecond)
        print("seeding with", self.randomSeed)
        np.random.seed(self.randomSeed)
        self.randomState = np.random.get_state()
  
    def refreshRandomState(self):
        self.randomState = np.random.get_state()
  
    def setRandomState(self):
        np.random.set_state(self.randomState)
        
    def getRandomDurationTimeUntilSick_Milliseconds(self):
        initialDuration = self.randomFloatTriangular(self.durationTimeUntilSickMinimum+self.simulationTimeStepInMillisecond,self.durationTimeUntilSickMode,self.durationTimeUntilSickMaximum)
        simulationSteps = math.floor(initialDuration / self.simulationTimeStepInMillisecond)
        return simulationSteps * self.simulationTimeStepInMillisecond
  
    def getRandomXaccelerationPerson_mms2(self):
        return self.randomFloatTriangular(-self.Supermarket_MaximumAccelerationXDirection,0,self.Supermarket_MaximumAccelerationXDirection)/1000000
  
    def getRandomNumberOfAislesInSupermarket_1(self):
        return self.randomIntUniform(self.Supermarket_minimumNumberOfAisles,self.Supermarket_maximumNumberOfAisles)
  
    def getRandomNumberRowCapacityOfWorkplace_1(self):
        return self.randomIntUniform(self.MinimumRowCapacityWorkplaceOrSchool,self.MaximumRowCapacityWorkplaceOrSchool)
  
    def getRandomTimeWorkplaceVisit_ms(self):
        visitTimespanDuration = self.WorklocationVisit_closingTime - self.WorklocationVisit_duration - self.WorklocationVisit_openingTime
        numberOfpossibleSimulationTimesteps = int(visitTimespanDuration / self.simulationTimeStepInMillisecond)
        return self.WorklocationVisit_openingTime + self.randomIntUniform(0,numberOfpossibleSimulationTimesteps) * self.simulationTimeStepInMillisecond
  
    def getRandomTimeWithinSimulationBetweenTwoTimes_ms(self, lowerBound, upperBound):
        numberOfpossibleSimulationTimesteps = int((upperBound-lowerBound) / self.simulationTimeStepInMillisecond)
        return lowerBound + self.randomIntUniform(0,numberOfpossibleSimulationTimesteps) * self.simulationTimeStepInMillisecond
  
    def getRandomDistanceBetweenWorkplaceOrSchoolSeats(self):
        return np.random.uniform(self.WorkplaceOrSchoolMinimumDistanceBetweenSeats, self.WorkplaceOrSchoolMaximumDistanceBetweenSeats)

    def getRandomHouseholdSize_1(self):
        return np.random.choice(np.arange(1, len(self.targetHouseHoldSizeDistribution)+1), p=self.targetHouseHoldSizeDistribution)

    def randomNumberFromHalfNormalDistribution(self, mean, std):
        return abs(np.random.normal(loc=mean, scale=std, size=None))
  
    def randomIntUniform(self,lowerBound,upperBound):
        return np.random.randint(lowerBound,upperBound+1)
    
    def randomFloatTriangular(self,minimum,mostLikely,maximum):
        return np.random.triangular(minimum,mostLikely,maximum)
    
    def randomFloatBetweenZeroAndNumber(self,number):
        return number * np.random.rand()

    def drawProbability(self,probability):
        return np.random.uniform(0, 1)<=probability