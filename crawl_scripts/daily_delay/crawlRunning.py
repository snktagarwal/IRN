# Code to crawl the train running information from http://www.trainenquiry.com/indexNS.aspx
import sys
import os
import logging
from BeautifulSoup import BeautifulSoup
import re
from urlparse import urlparse
from html2text import html2text
from sets import Set
import time
import Utilities
from datetime import date
from dateutil.relativedelta import relativedelta
import copy

util = Utilities.UtilitiesStat()


now = date.today() - relativedelta(days = 2)

datestring = now.strftime("%Y-%m-%d")
running_info_out = 'RunningInfo-'+datestring+'.out'
print now

ri = file(running_info_out, 'w')

def parseTrainListNew(filename):

  """ Parses the list of train and stations including information about
  timings """

  f = file(filename, 'r')
  lines = f.readlines()

  trainDetails = {}

  for l in lines:

    parts = l.split()
    tr_no = parts[0]
    parts = parts[1:]
    trainDetails[tr_no] = []

    while(len(parts)>0):
      stn_code, sch_arr, sch_dep, src_dist = parts[0:4]
      if sch_arr == 'Source': sch_arr = -1
      else: sch_arr = util.toMin(sch_arr)
      if sch_dep == 'Desitation': sch_dep = -1
      else: sch_dep = util.toMin(sch_dep)
      trainDetails[tr_no].append([stn_code, sch_arr, sch_dep])
      parts = parts[4:]

  return trainDetails

def crawlDataWithDate(trainDetails, path):


    for (k,v) in trainDetails.iteritems():

        d = date.today() - relativedelta(days = 2)
        prev_arr = -10

        for t in v:

            # Check if the train changes day
            if t[1] < prev_arr: d = d + relativedelta(days = +1)
            prev_arr = t[1]

            d1 = d.isoformat().split('-')

            station = t[0]
            crawlHTTP = "http://www.trainenquiry.com/o/RunningIslTrSt.aspx?tr="+str(k)+"&st="+str(station)+"+&dt="+d1[2]+"%2f"+d1[1]+"%2f"+d1[0]
            crawlOP = path+'/'+str(k)+'.'+str(station)+'.'+str(now)+'.html'
            wgetCall = 'wget -o wget.log -O '+crawlOP+' \"'+crawlHTTP+'\"'
            print wgetCall
            os.system(wgetCall)
            parseFile(crawlOP, str(k))

def parseFile(filename, tno):

    """ parses the file for relevant information """

    f = file(filename, 'r').read()
    html = f.decode('ascii','ignore')
    soup = BeautifulSoup(html)

    detailTable = soup.find('table',{'id':'Table3'})
    detailRows = BeautifulSoup(str(detailTable)).findAll('td')
    ri.write('Train Number: '+tno+'\n')
    for i in range(len(detailRows)/2):
        md = detailRows[2*i].contents[0]
        if i==0 or i==1:
            temp = str(md)
            md =  temp.split('>')[1].split('<')[0]
        data = detailRows[2*i+1].contents[0]

        op = md.strip()+': '+data.strip()+'\n'
        ri.write(op)

    ri.write('\n')
    ri.flush()

def pruneCrawledTrains(trainDetails, crawled):
    trainDetails1 = {}
    for (k,v) in trainDetails.iteritems():

        if k not in crawled:

            trainDetails1[k] = v
    return trainDetails1

def backupRunningInfo(filename):

    newFileName = filename+str(str(int(time.time())))

    os.system('cp '+filename+' '+newFileName)


if __name__=='__main__':

    trainDetails = parseTrainListNew('NewTrainStationDetail.txt')

    filename = 'RunningInfo-'+datestring+'.out'

    print trainDetails

    print 'Total trains: '+str(len(trainDetails))

    os.system('mkdir ./crawl-'+datestring)
    crawlDataWithDate(trainDetails, './crawl-'+datestring)
