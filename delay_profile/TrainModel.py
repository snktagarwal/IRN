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

class Station:

  def __init__(self, tr_no, tr_nm, stn_nm, sch_arr, del_arr, act_arr, sch_dep, del_dep, act_dep, stn_code = None, src_dist = 0):

    self.SEG_INFO_TYPE = ['START', 'MID', 'END']

    # A station might be part of multiple segments, hence use of lists
    self.seg_info = []

    self.run_day = 1 # By default train in running on the same day

    self.tr_no = tr_no
    self.tr_nm = tr_nm
    self.stn_nm = stn_nm
    if stn_code: self.stn_code = stn_code
    else:
      try:
        self.stn_code = Station.disambiguate(util.stn_codes[self.stn_nm])
      except:
        self.stn_code = 'NA'
    self.sch_arr = sch_arr
    self.act_arr = act_arr
    self.del_arr = del_arr
    self.sch_dep = sch_dep
    self.act_dep = act_dep
    self.del_dep = del_dep
    self.src_dist = src_dist

  def _print(self):
    print 'Train Name: ' + str(self.tr_nm)
    print 'Train No.: ' + str(self.tr_no)
    print 'Sch Arr: ' + str(self.sch_arr)
    print 'Act Arr: ' + str(self.act_arr)
    print 'Del Arr: ' + str(self.del_arr)

  def augment_seg_info(self, seg_number, info_type):
    """ Augments information to a train regarding the segment.
    see self.SEG_INFO_TYPE for the types of information available"""

    self.seg_info.append([seg_number, info_type])

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


  def update_segment(self, seg_no):

    """ Takes a segment number as argument and fills in information
    to various stations if they lie on this segment. This is useful
    for constructing Train -> STN1 || STN2 .. list augmented with
    segment information """


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


  def addStn(self, stn):

    """ Given a station, adds it to the list of existing station stops
    of a train. Additional check require to update the day if train has
    run overnight """

    if len(self.stn_list) > 1 and self.stn_list[-1].sch_arr > stn.sch_arr:
      stn.run_day = self.stn_list[-1].run_day + 1
    elif len(self.stn_list) > 1:
      stn.run_day = self.stn_list[-1].run_day

    self.stn_list.append(stn)

  def getDelayOverSegment(self, lidx, ridx):
    """ Once we know the left and right indices it is easy to
    calculate the segment delays over a train.

    By our definition of delay, we calculate the expected run as:
    exp_run = sch dep from destination - sch dep from source
    and act_run = act dep from dest - act dep from source.

    Delay is just the difference of the two above """


    if lidx == ridx: return 0

    if ridx == len(self.stn_list) - 1: # Last station
      #sch_stay_seg = self.stn_list[ridx].sch_arr - self.stn_list[lidx].sch_dep
      #act_stay_seg = self.stn_list[ridx].act_arr - self.stn_list[lidx].act_dep
      delay = self.stn_list[ridx].del_arr - self.stn_list[lidx].del_dep
    else:
      #sch_stay_seg = self.stn_list[ridx].sch_dep - self.stn_list[lidx].sch_dep
      #act_stay_seg = self.stn_list[ridx].act_dep - self.stn_list[lidx].act_dep
      delay = self.stn_list[ridx].del_dep - self.stn_list[lidx].del_dep

    # If the train is running overnite, we truncate it as the data
    # is not consistent as of now
    #if sch_stay_seg < 0 or act_stay_seg < 0: return 0

    #delay = act_stay_seg - sch_stay_seg

    #if delay < -100: return 0

    return delay

  def getTrafficOverSegment(self, lidx, ridx):

    # Find how much a train should run over the segment
    # It is when it should come at the left end and leave the right
    sch_stay_seg = self.stn_list[ridx].sch_dep - self.stn_list[lidx].sch_arr

    # If the train is running overnite, we truncate it as the data
    # is not consistent as of now

    act_stay_seg = self.stn_list[ridx].act_dep - self.stn_list[lidx].act_arr
    if(act_stay_seg <0):
      act_stay_seg = self.stn_list[lidx].act_arr + 1440 - self.stn_list[ridx].act_dep

    #if sch_stay_seg < 0 or act_stay_seg < 0: return 0

    #delay = act_stay_seg - sch_stay_seg

    #print delay
    return act_stay_seg

class Segment:

  """ This class describes each segment defined in Segments.py.
  The reason for constructing a new class is to have granular details
  about exact traffic and delay happening over it. It helps to find
  final statistics in an easy way. It should ideally encapsulate each
  day's activity as explicitly as possible. """

  def __init__(self, seg, seg_name=None):

    # Self information
    self.seg = seg
    if seg_name: self.seg_name = seg_name
    else: self.seg_name = self.getName()


    # Hourly split, current window is 2 hours
    self._split = 120
    self._hours = xrange(0, 1441, self._split)

    # Construct a dictionary which gets information in hourly
    # fashion. A tuple of hour range AND statistic

    self.hourly_delay= {}
    self.hourly_traffic = {}
    self.daily_traffic = {}
    self.total_delay = {}

    for x in range(len(self._hours)):
      # Capture the hourly delay and traffic
      self.hourly_delay[x] = {}
      self.hourly_traffic[x] = {}



  def getName(self):
    """ Concat the names of stations to get a doable name """

    name = self.seg[0]
    for stn in self.seg[1:]:
      name = name + '-' + stn
    return name

  @staticmethod
  def getNameStat(seg):
    """ Concat the names of stations to get a doable name """

    name = seg[0]
    for stn in seg[1:]:
      name = name + '-' + stn
    return name


  def isSegment(self, train):

    """ Given a segment as a list of stops and train information
    figure out the left and right end points of segment on the train
    A Train is said to cross a segment if it has atleast 2 stops from
    the segment as a part of the train schedule """

    # Find the intersection of segment with train
    if len(set(map(lambda x: x.stn_code, train.stn_list)).intersection(set(self.seg)))>=2:
      # Find the min intersection point
      mini = 100
      for stn in self.seg:
        for i in range(len(train.stn_list)):
          if train.stn_list[i].stn_code==stn and mini > i:
            mini = i

      maxi = -1
      for stn in self.seg:
        for i in range(len(train.stn_list)):
          if train.stn_list[i].stn_code==stn and maxi < i:
            maxi = i

      return [mini, maxi]
    else:
      return [-1,-1] # Segment intersection not found

  def findSlot(self, train, i):

    # Calculate the slot in which a time falls
    time = train.stn_list[i].act_arr
    if time == 0: time = train.stn_list[i].act_dep
    arr_rounded = (time/self._split)
    return arr_rounded

  def processHourly(self, train, lidx, ridx):

    self.total_delay[train.tr_no] = train.getDelayOverSegment(lidx, ridx)

    for i in range(lidx, ridx+1):

      # Bit mask for segment traffic
      bit_mask = [0]*len(self.hourly_traffic.keys())

      # find the correct slot of traffic
      arr_rounded = self.findSlot(train, i)
      # Now add the traffic to correct slot
      bit_mask[arr_rounded] = 1

    for i in range(len(self.hourly_traffic.keys())):
      if bit_mask[i]:
        self.hourly_traffic[i][train.tr_no] = 1

    # Binning the Delay profile
    # We need to construct consecutive delays by finding indices
    # which belong to each time slot for a segment.
    # We should get total delay (sum) over all time slots
    # to be the end-to-end delay for the segment

    #print 'Start: '+str(train.tr_no)+' '+str(lidx) + ' '+ str(ridx)
    # The total delay captured should be lidx to ridx
    exp_tot_del = train.getDelayOverSegment(lidx, ridx)

    s_lidx = lidx # The left index to start with is lidx
    s_ridx = -1   # s_ridx is just a placeholder for now
    act_tot_del = 0 # Assert that act_tot_del = exp_tot_del

    # We make a map of stn idx to time slot first
    base = lidx
    slot_list= map(lambda i: self.findSlot(train, i), range(lidx, ridx+1))
    #print slot_list

    # Now break the list into disjoint (ends cotinuous ranges)
    s_lidx = 0
    r_lidx = 0
    act_tot_del = 0

    while(s_lidx < len(slot_list)):
      while r_lidx < len(slot_list) and \
          slot_list[r_lidx] == slot_list[s_lidx]: \
          r_lidx = r_lidx + 1

      t_l = lidx + s_lidx

      if r_lidx + lidx > ridx:  t_r = ridx
      else: t_r = lidx + r_lidx

      #print 'T: '+str(t_l)+' '+str(t_r)

      delay = train.getDelayOverSegment(t_l, t_r)
      self.hourly_delay[slot_list[s_lidx]][train.tr_no] = delay
      act_tot_del = act_tot_del + delay

      s_lidx = r_lidx



    #print 'Diff in delays: '+str(act_tot_del)+' '+str(exp_tot_del)

    # Raise alarm if thigns don't match!
    if act_tot_del!= exp_tot_del: raise Exception


  def processTrain(self, train):

    # Processes a train the ideal flow should be:
    # 1. Take the train and see if has this segment
    # 2. Find the indices
    # 3. Suck the heck out of it for our analysis

    [lidx, ridx] = self.isSegment(train)
    if -1 in [lidx, ridx]: return
    else:
      # Process for hourly stats
      self.processHourly(train, lidx, ridx)
      # Process for cumulative total stats
      self.daily_traffic[train.tr_no] = 1

class Indexing:

  """ Contains information extracted out of each day """

  def __init__(self, filename):

    self.filename = filename

  def constructTimeTableIndex(self):

    """ Constructs a static index of train information using a train
    station index. """

    f = file(self.filename, 'r')
    idx = {}

    lines = f.readlines()

    # Skip all the comments
    while lines[0].startswith('#') or lines[0].startswith(' '):
      lines = lines[1:]

    # Read each train carefully
    for train in lines:

      parts = train.strip().split()
      if len(parts) < 3: continue
      tr_no = parts[0]
      parts = parts[1:]

      # Create a new train
      idx[tr_no] = Train(tr_no)

      # Read each station
      while parts:
        [stn_code, arr_time, dep_time, dist_source] = parts[0:4]
        print parts[0:4]
        arr_time = util.toMin(arr_time)
        dep_time = util.toMin(dep_time)
        parts = parts[4:]
        idx[tr_no].addStn(Station(tr_no, 'X', 'X', arr_time, 0, 0, dep_time, 0, 0, stn_code, int(dist_source)))

    self.tt_idx = idx
    return self.tt_idx

  def augmentTimeTableWithSegments(self):

    """ Augments information about segments in the time table object """

    for i in range(len(Segments.all_segments)):

      s = Segment(Segments.all_segments[i])

      for (tr_no, train) in self.tt_idx.iteritems():

        l1, l2 = s.isSegment(train)


        if not -1 in [l1, l2]:

          # Starting station
          train.stn_list[l1].augment_seg_info(i, 0)

          # Ending station
          train.stn_list[l2].augment_seg_info(i, 2)

          # Rest are all mid segments
          for j in range(l1+1, l2):
            train.stn_list[j].augment_seg_info(i, 1)

    return self.tt_idx

  def printAugmentedTimeTable(self, output):

    """ Prints the new segment information augmented timetable
    The format is as follows:
      TRAIN || STN1 || STN2 || ... || STN_N
    where each STN_i expands as:
      STN_i : STN_CODE || ARR || DEP || SOURCE || SEG_INFO_LIST
    where SEG_INFO_LIST expands as:
      SEG_INFO_LIST : SEG_NO, STATUS, SEG_NO, STATUS, -1 -1 (ends with -1)
    Please look at the final output to gain idea. """

    f = file(output, 'w')

    for (tr_no, train) in self.tt_idx.iteritems():

      f.write(tr_no + '||')

      for stn in train.stn_list:

        f.write(stn.stn_code+ '||')
        f.write(str(stn.sch_arr) + '||')
        f.write(str(stn.sch_dep) + '||')

        for e in stn.seg_info:
          f.write(str(e[0]) + ',' + str(e[1]))
        f.write('-1,-1')
        f.write('||')

      f.write('\n')

  def printAugmentedTimeTableP(self, output):
    """ Prints the augmented time table in augmented form. Read the
    above documentation for an explanation.
    A dictionary containing train no as keys, has a dictionary
    having each key as a station name having list arr, dep, source_dist,
    and a dict having seg_no and status -- complicated huh ;) """

    sol_dict= {}

    for (tr_no, train) in self.tt_idx.iteritems():

      sol_dict[tr_no] = []

      for stn in train.stn_list:

        sol_dict[tr_no].append([ stn.stn_code, stn.sch_arr, stn.sch_dep, {}, stn.src_dist])

        for e in stn.seg_info:
          sol_dict[tr_no][-1][3][str(e[0])] = str(e[1])

    pickle.dump(sol_dict, open(output, 'wb'))



  def constructSegmentsIndex(self):
    """ Constructs a segment index. Note that we do not do any
    processing about average delay daily, hourly or averge traffic
    daily, hourly unless a specific function is called. This gives
    us the advantage that any averaging does not happen in functions.

    Any debugging (mostly which happens with averaging) can then be
    separated out. -- DESIGN LESSON """

    self.seg_set =  [Segment(x) for x in Segments.all_segments]
    for (tr_id, train) in self.idx.iteritems():
      for seg in self.seg_set:
        seg.processTrain(train)

  def dailyAverageDelayPS(self):

    """ Finds the average delay for this particular day (self.filename)
    The average delay is a list/dict of segments vs avg. delay over them """

    # Read the seg set for total_delay, which contains a dictionary of
    # of train and the delay caused by it

    self.daily_delay = []
    for x in self.seg_set:
      s = 0
      if x.total_delay and len(x.total_delay) > 0:
        s = s + float(sum(x.total_delay.values()))/len(x.total_delay.values())
      self.daily_delay.append(s)

  def dailyAverageTrafficPS(self):

    """ Finds the average traffic, which is simply the number of trains
    running through each segment in that day """

    self.daily_traffic = map(lambda x: \
        len(x.daily_traffic.keys()), self.seg_set)

  def hourlyAverageTrafficPS(self):

    # A dictionary containing mapping from hours -> traffic
    # and there are Segment number of such dictionaries
    self.hourly_traffic_dict = []

    # Convert the hourly_traffic ditionary in segments into
    # a dictionary containing total hourly traffic

    t_traffic = map(lambda x: x.hourly_traffic, self.seg_set)

    self.hourly_traffic_dict = []

    for t in t_traffic:
      t1 = {}
      for (k, l) in t.iteritems():
        t1[k] = sum(l.values())
      self.hourly_traffic_dict.append(t1)


    # print self.hourly_traffic_dict

  def hourlyAverageDelayPS(self):

    self.hourly_delay_dict = []
    t_delay= map(lambda x: x.hourly_delay, self.seg_set)

    for t in t_delay:
      t1 = {}
      for (k,l) in t.iteritems():
        if len(l.values())>0:
          t1[k] = float(sum(l.values())/len(l.keys()))
        else: t1[k] = 0
      self.hourly_delay_dict.append(t1)

  def constructTrainIndex(self, blk_size):

    """ Construct an Index from files read everyday using running information """
    # Read the file for a chunk

    block = []
    idx = {}
    tot_blk = 0
    stn_codes = util.stnCodes('datasets/AllStationCodes.txt')
    succ = 0
    print 'Dataset: ' + self.filename

    for line in fileinput.input(self.filename):

     # Read a block, delimited by new-lines
      if(not len(line.strip())):
        tot_blk = tot_blk + 1
        succ = succ + Indexing.processBlock(block, blk_size, idx, stn_codes)
        block = []
      else: block.append(line)

    #print 'Total Trains: ' + str(len(idx))
    #print 'Total blokcs: ' + str(tot_blk) + '\\nSuccessful Blocks: ' + str(succ)
    #print 'Ratio: ' + str(float(succ)/tot_blk)

    self.idx = idx

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


class DailySets:

  """ The purpose of this class is to process each of the days
  (by creating indexes) run various tests using the associated
  classes BUT most importantly implement funcs to average datasets
  over varous days. """

  def __init__(self, fileset):

    """ Takes a list of files as input """

    self.fileset = fileset
    self.days = len(self.fileset)
    print self.fileset, self.days
    # List of indexes
    self.idx_list = []
    # Hourly split, current window is 2 hours
    self._split = 120
    self._hours = xrange(0, 1441, self._split)

  def index(self):

    """ This is the first step, create a universal index """

    # A basic parsing of file -> Trains -> Segments

    for fn in self.fileset:
      print fn
      idx = Indexing(fn)
      idx.constructTrainIndex(10)
      idx.constructSegmentsIndex()
      #idx.normalizeDelay()
      self.idx_list.append(idx)

  def hourVsSegmentDelayMat(self, p = True):

    """ Constructs a segment vs hours matrix ( 54 x 12 ) which contains
    Delay metrics """

    self.seg_hour_delay_mat = None

    for idx in self.idx_list:

      # Create a copy if still none
      if not self.seg_hour_delay_mat:
        self.seg_hour_delay_mat = copy.deepcopy(idx.hourly_delay_dict)
        continue

      # Update
      for i in range(len(Segments.all_segments)):
        for j in range(len(self._hours)):
          self.seg_hour_delay_mat[i][j] += idx.hourly_delay_dict[i][j]

    # Average
    for i in range(len(Segments.all_segments)):
      for j in range(len(self._hours)):
        self.seg_hour_delay_mat[i][j] = float(self.seg_hour_delay_mat[i][j])/len(self.idx_list)

    # If pickle is true then we save the matrix in a picked file
    if p:
      pickle.dump(self.seg_hour_delay_mat, open('pickled/SegHourDelayMat.p','w'))

  def hourVsSegmentTrafficMat(self, p = True):

    """ Constructs a segment vs hours matrix ( 54 x 12 ) which contains
    Delay metrics """

    self.seg_hour_traffic_mat = None

    for idx in self.idx_list:

      # Create a copy if still none
      if not self.seg_hour_traffic_mat:
        self.seg_hour_traffic_mat = copy.deepcopy(idx.hourly_traffic_dict)
        continue

      # Update
      for i in range(len(Segments.all_segments)):
        for j in range(len(self._hours)):
          self.seg_hour_traffic_mat[i][j] += idx.hourly_traffic_dict[i][j]

    # Average
    for i in range(len(Segments.all_segments)):
      for j in range(len(self._hours)):
        self.seg_hour_traffic_mat[i][j] = float(self.seg_hour_traffic_mat[i][j])/len(self.idx_list)

    if p:
      pickle.dump(self.seg_hour_traffic_mat ,open('pickled/SegHourTrafficMat.p','w'))



  def averageTrafficPS(self):
    """ Total hourly traffic for each hour slot using the master matrix """
    self.total_average_traffic_ps = \
        map(lambda x: sum(x.itervalues()), self.seg_hour_traffic_mat)
    if p:
      pickle.dump(file('SegHourDelayMat.p','w'), self.seg_hour_delay_mat)


  def averageTrafficPHS(self):

    """ Total hourly traffic for each hour slot using the master matrix """

    self.total_average_traffic_phs = []

    for j in range(len(self._hours)):
      # Sum up over the column; and avg it
      val = 0
      for seg in self.seg_hour_traffic_mat:
        val = val + seg[j]
      self.total_average_traffic_phs.append(val)

  def averageDelayPS(self):
    """ Total hourly traffic for each hour slot using the master matrix """
    self.total_average_delay_ps = \
        map(lambda x: sum(x.itervalues()), self.seg_hour_delay_mat)


  def averageDelayPHS(self):

    """ Total hourly delay for each hour slot using the master matrix """

    self.total_average_delay_phs = []

    for j in range(len(self._hours)):
      # Sum up over the column; and avg it
      val = 0
      for seg in self.seg_hour_delay_mat:
        val += seg[j]
      self.total_average_delay_phs.append(val)

  def plotHourlyTraffic(self):

    """ For a first view let us create segmentsxhours insatances of
    delay. And plot them with x axis as hours and y axis as the corresponding
    delay. """

    f = file('plots/HourlyTrafficOfAllSegments','w')

    for hs in range(len(self._hours)):
      for e1 in self.total_hourly_traffic:
        f.write(str(self._hours[hs]/self._split)[:5]+' '+str(e1[hs])[:5]+'\n')

  def plotHourlyDelay(self):

    """ For a first view let us create segmentsxhours insatances of
    delay. And plot them with x axis as hours and y axis as the corresponding
    delay. """

    f = file('plots/HourlyDelayOfAllSegments','w')

    for hs in range(len(self._hours)):
      for e1 in self.total_hourly_delay:
        f.write(str(self._hours[hs]/self._split)[:5]+' '+str(e1[hs])[:5]+'\n')
  def plotTrafficVsDelayHourly(self):

    """ Construct a plot where x-axis is traffic, y-axis is delay and
    color coding is done according to the hour. The simple way to do
    this will be to, construct len(self._hours) file each containing a
    list of traffic-vs-delay statistics (len(Segments.__all_segments))
    actually . """

    base = 'traffic-vs-delay/'

    for hs in range(len(self._hours)):
      f = file(base + str(hs) + '.dat', 'w')
      for i in range(len(Segments.all_segments)):
        f.write("%f\t%f\n" % (self.total_hourly_traffic[i][hs], self.total_hourly_delay[i][hs]))
      f.close()

  def plotHourlyDelayPS(self):

    """ For each segment create points for each bin and store in file """

    for i in range(len(self.total_hourly_delay)):
      f = file('plots/'+Segment.getNameStat(Segments.all_segments[i])+'.hourly_delay','w')
      for hs in range(len(self._hours)):
        f.write(str(hs)+' '+str(self.total_hourly_delay[i][hs])+'\n')
      f.close()

  def plotHourlyTrafficPS(self):

    """ For each segment create points for each bin and store in file """

    for i in range(len(self.total_hourly_traffic)):
      f = file('plots/'+Segment.getNameStat(Segments.all_segments[i])+'.hourly_traffic','w')
      for hs in range(len(self._hours)):
        f.write(str(hs)+' '+str(self.total_hourly_traffic[i][hs])+'\n')
      f.close()

  def corrHourlyTrafficDelayPS(self):

    """ Compute the delay and traffic vectors per hour and compute
    the associated correlation """

    corr_vec = map(lambda x: pearsonr( \
        self.total_hourly_traffic[x], self.total_hourly_delay[x]), \
        range(len(self.total_hourly_traffic)))

    for i in range(len(Segments.all_segments)):

      print Segment.getNameStat(Segments.all_segments[i]) \
          + str(' ') + str(corr_vec[i][0])





