# Runs tests using other modules
# Generally we will import a large number of files from
# datasets and run using our core algorithms/core
# this relieves us from having to worry about datasets in the main program
# and also make life easy to refactor code/datasets

# In this file we extract the delay information on all segments

import fileinput
import sys
import glob
import numpy
# File containing segments of Indian Railways
import Segments
# Main delay statistic extraction code
from Delay import *
import TrainModel
from TrainModel import *
from Utilities import *
# from Traffic import *
from scipy.stats.stats import pearsonr

def new_test():

  handle = DailySets(glob.glob('daily_data/*.out'))
  handle.index()

  for idx in handle.idx_list:
    idx.dailyAverageDelayPS()
    idx.dailyAverageTrafficPS()
    idx.hourlyAverageTrafficPS()
    idx.hourlyAverageDelayPS()

  handle.hourVsSegmentDelayMat()
  handle.hourVsSegmentTrafficMat()

def getSegmentsSortedByTraffic(handle):

  seg_traf_list = map(lambda x: [Segments.all_segments[x], \
      handle.total_average_traffic[x]], range(len(Segments.all_segments)))

  seg_traf_list_sorted = sorted(seg_traf_list, key = lambda x: -x[1])

  for i in range(len(Segments.all_segments)):
    print seg_traf_list_sorted[i][0]
    print seg_traf_list_sorted[i][1]

def getSegmentsSortedByDelay(handle):

  seg_del_list = map(lambda x: [Segments.all_segments[x], \
      handle.total_average_delay[x]], range(len(Segments.all_segments)))

  seg_del_list_sorted = sorted(seg_del_list, key = lambda x: -x[1])

  for i in range(len(Segments.all_segments)):
    print seg_del_list_sorted[i][0]
    print seg_del_list_sorted[i][1]

def getTimeTableAugmented():

  c = Indexing('delay_profile/datasets/NewTrainStationDetail.txt')
  c.constructTimeTableIndex()
  c.augmentTimeTableWithSegments()
  c.printAugmentedTimeTableP('NewTrainStationDetailWSegments.p')
  idx = c.tt_idx

  # Some debugging info
  print map(lambda x: [x.stn_nm, x.seg_info, x.src_dist ], idx['12280'].stn_list)
  return idx


if __name__=='__main__':
  new_test()
  #getTimeTableAugmented()
