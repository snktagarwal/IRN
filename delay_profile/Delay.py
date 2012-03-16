""" The basic idea is to create a few classes which could define
data availabe in our delay dataset. The basic class will contain
information pertaining to a station and we construct a sequence of
station-objects into a form of a train. """

import fileinput
import sys
import glob
import numpy
# File containing segments of Indian Railways
import Segments
import TrainModel
from TrainModel import *
from Utilities import *


util = UtilitiesStat()

class Delay:

  """ Contains a list of segments and associated structures to add
  delay from various trains running on it. This single class contains
  all the segments and should be used as an external reference to *any*
  delay calculation """

  # DS for delay calculation
  def __init__(self):
    self.delay_stat = []
    for i in range(len(Segments.all_segments)):
      self.delay_stat.append({})


  def runDelayOverAllTrainsAllSegments(self, idx):
    """ Take each train on the idx, and for each train take each
    segment. Now find if the segment lies for the train and accumulate
    the delay if it is so. """

    for (k,t) in idx.iteritems():
      #print 'Running over train: '+k
      for i in range(len(Segments.all_segments)):
        lidx, ridx = t.isSegment(Segments.all_segments[i])
        if lidx!=-1 and ridx!=-1:
          self.delay_stat[i][t.tr_no] = t.getDelayOverSegment(lidx, ridx)

  def generateAvgDelayStatsForSegments(self, filename):
    """ We now finally calculate a few statistics about each segment
    in a nice readable format. Including sorted list delay wise """

    f = file(filename+'.avgdel', 'w')
    f_det = file(filename+'.detail', 'w')
    del_list = []
    for i in range(len(self.delay_stat)):

      avg_del = -1000 # Cannot have such delay => seg not found
      if(len(self.delay_stat[i].keys())==0): pass
      else:
        #print Segments.all_segments[i]
        #print map(lambda (k,v): k+':'+str(v)+' ', self.delay_stat[i].iteritems())
        # Sum the delays for the segment
        f_det.write(str(Segments.all_segments[i])+':')
        tot_items = len(self.delay_stat[i].keys())
        tot_del = 0
        for (k,v) in self.delay_stat[i].iteritems():
          if(v>-100):
            f_det.write(str(k)+':'+str(v)+';')
            tot_del = tot_del + v
        f_det.write('\n')

        avg_del = float(tot_del)/tot_items
      del_list.append([Segments.all_segments[i], avg_del])

    # Sort the delay list according to avg del encountered
    self.avg_del_list = del_list
    #print self.avg_del_list
    for x in self.avg_del_list:
      f.write(str(x[0])+':'+str(x[1])+'\n')
    f.close()
    f_det.close()

    print len(self.avg_del_list)


if __name__=='__main__':

  print len(Segments.all_segments)
  d = Delay()
  fn = 'daily_data/RunningInfo-2012-02-05.out'
  idx = TrainModel.Indexing.constructTrainIndex(fn,10)
  #print idx['12340'].isSegment(Segments.all_segments[19])
  d.runDelayOverAllTrainsAllSegments(idx)
  d.generateAvgDelayStatsForSegments(fn)
