# -*- coding: utf-8 -*-

class Household:
    
  def __init__(self, personList):
    self.personList = personList
    self.everybodyInfected = False
    self.quarantined = False