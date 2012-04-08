import fileinput
import sys
import glob
import numpy
# File containing segments of Indian Railways
import Segments

class UtilitiesStat:

  def __init__(self):
    self.stn_codes, self.stn_names = self.stnCodes('datasets/AllStationCodes.txt')
    self.trn_stn = self.trainStnList('datasets/NewTrainStation.txt')
    self.tr_conv= self.trainNoConv('datasets/TrainNoConv.txt')

  def toMin(self, time):

      try:
        minutes = int(time.split(':')[0])*60 + int(time.split(':')[1])
      except:
        minutes = 0

      return minutes

  def stnCodes(self, filename):

    f = open(filename, 'r')
    stn_codes = {}
    stn_names = {}

    for l in f.readlines():

      code, station = l.strip().split('||')
      stn_codes[station] = code
      stn_names[code] = station

    return stn_codes, stn_names

  def trainStnList(self, filename):

    trn_stn = {}
    f = file(filename, 'r')

    for l in f.readlines():
      p = l.strip().split('||')
      trn_stn[p[0]] = p[1:]
    return trn_stn

  def trainNoConv(self, filename):
    f = file(filename, 'r')
    tr_conv = {}
    for l in f.readlines():
      p = l.strip().split('||')
    tr_conv[p[0]] = p[1]
    return tr_conv

  def convTrNo(self, tr_no):
    """ Currently we have a bit of mess. The train numbers are appended
    with a 1 and then used to query, which is very incorrect. Hence
    remove that 1, and then find the actual train it should co-incide with"""
    return self.tr_conv[tr_no[1:]]


