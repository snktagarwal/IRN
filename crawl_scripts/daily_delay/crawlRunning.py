# Code to crawl the train running information from http://www.trainenquiry.com/indexNS.aspx
import sys
import os
import logging
import datetime
from BeautifulSoup import BeautifulSoup
import re
from urlparse import urlparse
from html2text import html2text
from sets import Set
import time

now = datetime.datetime.now()
datestring = now.strftime("%Y-%m-%d")
#datestring = '2012-02-28'
running_info_out = 'RunningInfo-'+datestring+'.out'
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('crawlRunningInfo.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

ri = file(running_info_out, 'w')

def parseRunningInfoOutput(filename):

    # parses and returns a list of train numbers already crawled
    crawled = Set()
    ri_out = file(filename, 'r')

    ri_lines = ri_out.readlines()

    for l in ri_lines:

        parts = l.split(':')

        if parts[0] == 'Train Number':

            crawled.add(str(parts[1].strip()))

    return crawled

def parseTrainList(filename, type):

    # Crawls the file based on whether it is old or new.
    # 'old' or 'new'

    f = file(filename, 'r')
    trainList = f.readlines()
    trainDetails = {}
    for t in trainList:

        parts = t.strip().split('||')
        trainNo = parts[0]
        stnList = parts[1:]

        if type == 'old':

            key = trainNo
            trainDetails[key] = stnList

    return trainDetails

def crawlDataWithDate(trainDetails, d, path):
    d1 = d.isoformat().split('-')
    for (k,v) in trainDetails.iteritems():
        for station in v:
            crawlHTTP = "http://www.trainenquiry.com/RunningIslTrSt.aspx?tr="+str(k)+"&st="+str(station)+"+&dt="+d1[2]+"%2f"+d1[1]+"%2f"+d1[0]
            logger.info('Fetching: '+crawlHTTP)
            crawlOP = path+'/'+str(k)+'.'+str(station)+'.'+str(d)+'.html'
            logger.info('Putting: '+crawlOP)
            wgetCall = 'wget -o wget.log -O '+crawlOP+' \"'+crawlHTTP+'\"'
            logger.info('Wget Call: '+wgetCall)
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


    filename = 'RunningInfo-'+datestring+'.out'
    # Always backup before doing any changes. Backup
    # to the current time
    #backupRunningInfo('RunningInfo-2011-08-25.out')
    #crawled = parseRunningInfoOutput('RunningInfo-2011-08-25.out')
    trainDetails = parseTrainList(sys.argv[1],sys.argv[2])
    print trainDetails
    print 'Total trains: '+str(len(trainDetails))
    #print 'Crawled Already: '+str(len(crawled))
    if sys.argv[3] == 'recover':
        trainDetails = pruneCrawledTrains(trainDetails, crawled)
    print 'List to crawl: '+str(len(trainDetails))
    os.system('mkdir ./crawl-'+datestring)
    crawlDataWithDate(trainDetails,  datetime.date(now.year,now.month,now.day),'./crawl-'+datestring)
