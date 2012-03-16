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

def getDelayForEachFile(data_path):

  dataset_files = glob.glob(data_path+'/*23.out')
  delay_set = []

  for fn in dataset_files:

    d = Delay()
    idx = TrainModel.Indexing(fn)
    idx.constructTrainIndex(10)
    d.runDelayOverAllTrainsAllSegments(idx.idx)
    d.generateAvgDelayStatsForSegments(fn)
    delay_set.append(d)

  return delay_set

def getAvgDelayPerSegmentForAllFiles(delay_set):

  util= UtilitiesStat()

  avg_d_each_day = []

  for i in range(len(Segments.all_segments)):
    days = []
    for d in delay_set:

      if d.avg_del_list[i][1] != -1000:
        days.append(d.avg_del_list[i][1])

    print Segments.all_segments[i]
    print days
    if len(days) > 0:
      avg_d_each_day.append(sum(days)/len(days))
    else:
      avg_d_each_day.append(-1000)

  all_seg = []
  all_seg_delays = []

  for i in range(len(Segments.all_segments)):
    all_seg.append([Segments.all_segments[i], avg_d_each_day[i]])
    all_seg_delays.append(avg_d_each_day[i])

  all_seg = sorted(all_seg, key= lambda x: x[1])

  fn = 'FinalDelayStats'
  f = file(fn, 'w')
  for seg in all_seg:
    f.write(str(map(lambda x: util.stn_names[x], seg[0]))+':'+str(seg[1])+'\n')
  f.close()

  return all_seg_delays

def new_test():

  handle = DailySets(glob.glob('daily_data/*.out'))
  handle.index()

  for idx in handle.idx_list:
    idx.dailyAverageDelayPS()
    idx.dailyAverageTrafficPS()
    idx.hourlyAverageTrafficPS()
    idx.hourlyAverageDelayPS()

    #print idx.daily_traffic
    #print idx.daily_delay

  handle.totalAverageTraffic()
  handle.totalAverageDelay()
  handle.totalHourlyTraffic()
  handle.totalHourlyDelay()


  for i in range(len(Segments.all_segments)):
    print Segments.all_segments[i]
    print handle.total_hourly_traffic[i]
    print handle.total_average_traffic[i]
    print handle.total_hourly_delay[i]
    print handle.total_average_delay[i]

  getSegmentsSortedByTraffic(handle)
  getSegmentsSortedByDelay(handle)

  #handle.plotHourlyTraffic()
  #handle.plotHourlyDelay()
  #handle.plotHourlyDelayPS()
  #handle.plotHourlyTrafficPS()
  #handle.corrHourlyTrafficDelayPS()
  handle.plotTrafficVsDelayHourly()

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


if __name__=='__main__':
  #d_s = getDelayForEachFile('daily_data/')
  #getAvgDelayPerSegmentForAllFiles(d_s)
  new_test()
