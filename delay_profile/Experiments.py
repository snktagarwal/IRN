""" We attempt to write experiments specific to the Master matrices
created through pickling in pickled/*.p. These matrices will have a structure
of Segments x hours averaged over all the days of data that we currently have """

import fileinput
import sys
import glob
import numpy
# File containing segments of Indian Railways
import Segments
from Utilities import *
from scipy.stats.stats import pearsonr
import pickle
import copy

util = UtilitiesStat()

class Experiments:

  def __init__(self):

    """ Sets up the pickled objects """

    self._split = 120
    self._hours = xrange(0, 1441, self._split)

    self.seg_hour_delay_mat = pickle.loads(file('pickled/SegHourDelayMat.p').read())
    self.seg_hour_traffic_mat = pickle.loads(file('pickled/SegHourTrafficMat.p').read())

  def getTopN(self, mat, n):

    """ Gets the top n elements from the Segments x hours matrix and
    reports the result in a human readable fashion """

    l = []
    for i in range(len(Segments.all_segments)):
      for j in range(len(self._hours)):
        l.append([Segments.all_segments[i], self._hours[j], mat[i][j]])

    l = sorted(l, key = lambda x: -x[2])

    # Return the top n
    return l[:n]

  def correlateTrafficAndDelay(self):

    """ Correlates each row of traffic and delay matrix """

    delay = self.seg_hour_delay_mat
    traf  = self.seg_hour_traffic_mat

    corr_vec = map(lambda i: pearsonr( \
        list(delay[i].itervalues()), list(traf[i].itervalues()))[0], \
        range(len(Segments.all_segments)))

    return corr_vec

if __name__=='__main__':

  e = Experiments()
  top_del =  e.getTopN(e.seg_hour_delay_mat, 10)
  top_traf = e.getTopN(e.seg_hour_traffic_mat, 10)

  print 'TOP DEL'
  print '-'*len('TOP DEL')

  for t_d in top_del:

    print t_d[0], t_d[1], t_d[2]

  print '\n\nTOP TRAFFIC'
  print '-'*len('TOP TRAFFIC')

  for t_d in top_traf:

  # Correlation of traffic and delay

  print '\n\nCORRELATION'
  print '-'*len('Correlation')
  corr_vec = e.correlateTrafficAndDelay()

  for i in range(len(Segments.all_segments)):

    print Segments.all_segments[i], corr_vec[i]
