import fileinput
import sys
import glob
import numpy
# File containing segments of Indian Railways
import Segments
from Utilities import *

util = UtilitiesStat()

class Station:

  def __init__(self, tr_no, tr_nm, stn_nm, sch_arr, del_arr, act_arr, sch_dep, del_dep, act_dep):

    self.tr_no = tr_no
    self.tr_nm = tr_nm
    self.stn_nm = stn_nm
    try:
      self.stn_code = Station.disambiguate(util.stn_codes[self.stn_nm])
    except:
      print self.stn_nm
      self.stn_code = 'NA'
    self.sch_arr = sch_arr
    self.act_arr = act_arr
    self.del_arr = del_arr
    self.sch_dep = sch_dep
    self.act_dep = act_dep
    self.del_dep = del_dep

  def _print(self):
    print 'Train Name: ' + str(self.tr_nm)
    print 'Train No.: ' + str(self.tr_no)
    print 'Sch Arr: ' + str(self.sch_arr)
    print 'Act Arr: ' + str(self.act_arr)
    print 'Del Arr: ' + str(self.del_arr)

  @staticmethod
  def disambiguate(stn_name):
    """ Given that many stations have closeby allyby we keep a single
    name for all of them! """
    mod_name = stn_name
    if stn_name in Segments.Delhi_stations:
      mod_name = 'DELHI'
    elif stn_name in Segments.Kolkata_stations:
      mod_name = 'KOLKATA'
    elif stn_name in Segments.Mumbai_stations:
      mod_name = 'MUMBAI'
    elif stn_name in Segments.Chennai_stations:
      mod_name = 'CHENNAI'
    elif stn_name in Segments.Bangalore_stations:
      mod_name = 'BLORE'
    elif stn_name in Segments.Hyderabad_stations:
      mod_name = 'HYDBAD'
    return mod_name



class Train:

  """ Defines a train in terms of list of stations. We can query
  a train to find which segments (or segment intersection), avg
  delay over a segment, and other statistics *particular to a train* """

  def __init__(self, tr_no):
    """ Starts a simple train as an empty object """
    self.stn_list = []
    self.tr_no = tr_no

  def addStn(self, stn):
    self.stn_list.append(stn)


  def checkStationsWithTT(self):

    """ Checks if the current configuration of station list is consistent with
    time table. This tells us if the Delay information is giving same stations
    as in our database.
    Consistency: Check if the list have same stations, set wise """

    tt_stn_set, del_stn_set = None, None
    try:
      tt_stn_set = set(util.trn_stn[str(self.tr_no)])
      del_stn_set = set(map(lambda x: x.stn_code, self.stn_list))
      if len(tt_stn_set.symmetric_difference(del_stn_set)) > 0:
        print self.tr_no + tt_stn_set.symmetric_difference(del_stn_set)
      else:
        print self.tr_no + " OKAY"

    except:
      print self.tr_no + " Does not exist in TT"

  def isSegment(self, seg):
    """ Given a segment as a list of stops and train information
    figure out the left and right end points of segment on the train
    A Train is said to cross a segment if it has atleast 2 stops from
    the segment as a part of the train schedule """
    # Find the intersection of segment with train
    if len(set(map(lambda x: x.stn_code, self.stn_list)).intersection(set(seg)))>=2:
      # Find the min intersection point
      mini = 100
      for stn in seg:
        for i in range(len(self.stn_list)):
          if self.stn_list[i].stn_code==stn and mini > i:
            mini = i

      maxi = -1
      for stn in seg:
        for i in range(len(self.stn_list)):
          if self.stn_list[i].stn_code==stn and maxi < i:
            maxi = i

      return [mini, maxi]
    else:
      return [-1,-1] # Segment intersection not found

  def getDelayOverSegment(self, lidx, ridx):
    """ Once we know the left and right indices it is easy to
    accumulate the segment delays over a train """

    #print 'Running from: '+str(lidx)+' to '+str(ridx) +' on '+self.tr_no

    # Find how much a train should run over the segment
    # It is when it should come at the left end and leave the right
    sch_stay_seg = self.stn_list[ridx].sch_dep - self.stn_list[lidx].sch_arr

    # If the train is running overnite, we truncate it as the data
    # is not consistent as of now

    act_stay_seg = self.stn_list[ridx].act_dep - self.stn_list[lidx].act_arr

    if sch_stay_seg < 0 or act_stay_seg < 0: return 0

    delay = act_stay_seg - sch_stay_seg

    #print delay
    return delay



  @staticmethod
  def runConsistencyCheck(idx):
    for (k,v) in idx.iteritems():
      v.checkStationsWithTT()

class Indexing:

  """ Construct an Index from files read everyday using running information """
  @staticmethod
  def constructTrainIndex(self, filename, blk_size):

    # Read the file for a chunk

    block = []
    idx = {}
    tot_blk = 0
    stn_codes = util.stnCodes('datasets/AllStationCodes.txt')
    succ = 0
    print 'Dataset: ' + filename


    for line in fileinput.input(filename):

     # Read a block, delimited by new-lines
      if(not len(line.strip())):
        tot_blk = tot_blk + 1
        succ = succ + Station.processBlock(block, blk_size, idx, stn_codes)
        block = []
      else: block.append(line)

    print 'Total Trains: ' + str(len(idx))
    print 'Total blokcs: ' + str(tot_blk) + '\nSuccessful Blocks: ' + str(succ)
    print 'Ratio: ' + str(float(succ)/tot_blk)

    return idx

  @staticmethod
  def processBlock(blk, blk_size, idx, stn_codes):

    if(len(blk) < blk_size):
      return 0
    else:
      # Construct a structure for the block and return it
      tr_no = blk[0].strip().split(':')[1].strip()
      tr_nm = blk[1].strip().split(':')[1].strip()
      stn_nm = blk[2].strip().split(':')[1].strip()
      tr_sch_arr = util.toMin(blk[3].strip().split('Time:')[1].split(',')[0])
      tr_del_arr = util.toMin(blk[4].strip().split('):')[1].strip())
      tr_act_arr = util.toMin(blk[5].strip().split('val:')[1].split(',')[0])
      tr_sch_dep = util.toMin(blk[6].strip().split('Time:')[1].split(',')[0])
      tr_del_dep = util.toMin(blk[7].strip().split('):')[1].strip())
      tr_act_dep = util.toMin(blk[8].strip().split('ure:')[1].split(',')[0])

      #print tr_no, tr_nm, stn_nm, tr_sch_arr, tr_del_arr, tr_act_arr

      if not tr_no in idx: idx[tr_no] = Train(tr_no)
      idx[tr_no].addStn(Station(tr_no, tr_nm, stn_nm, tr_sch_arr, tr_del_arr, tr_act_arr, tr_sch_dep, tr_del_dep, tr_act_dep))

      return 1



