"""This module defines the classes for the main relations
in our database."""

class Player():
  id = 1 # this variable is supposed to be 'read-only'
  def __init__(self,username,password,rating):
    self.username = username
    self.rating   = rating
    self.password = password
    self.id       = Player.id
    Player.id += 1

bjarke = Player("bjarkoff","hugu",1780)
print(Player.id)
print(bjarke.id)

class Team():
  def __init__(self,name):
    self.name = name

class League():
  def __init__(self, name, year):
    self.name = name
    self.year = year

class Chessgame():
  id = 1
  def __init__(self, pgn, result, date):
    self.pgn      = pgn
    self.result   = result
    self.date     = date
    self.id       = Chessgame.id
    Chessgame.id += 1

class Teammatch():
  id = 1
  def __init__(self,round):
    self.round = round
    self.id    = Teammatch.id
    Teammatch.id += 1