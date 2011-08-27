# Collects statistical information from the file RunningInfo.out<TIMESTAMP>
import sys
import sets
def getTrainStationInfoActual(filename):

	trainDetailsActual = {}
	lines = file(filename, 'r').readlines()

	for line in lines:	
		parts = line.split('||')
		trainDetailsActual[parts[0]] = len(parts)-1
	
	return trainDetailsActual

def getDelayFromToken(delay_block):
	
	# parses the token and gets the delay value in minutes!
	parts = delay_block.split(':')
	if len(parts) != 4 or '*' in parts[3]:
		
		return 0
	
	else:
		delay = int(parts[2])*60+int(parts[3])
		return delay

def printDelayVecToFile(filename, delayVector):
	
	f = file(filename,'w')

	for (k,v) in delayVector.iteritems():
		
		f.write(k)
		f.write(' ')
		for elem in v:
			f.write(str(elem))
			f.write(' ')
		f.write(str(sum(v)/len(v)))
		f.write('\n')

def getTimeFromToken(token):
	
	parts = token.split(':')
	if len(parts) !=3:
		return -1
	else:
		time_in_min = int(parts[1])*60 + int(parts[2].split(',')[0])
	return time_in_min

def printTrainInfoToFile(filename, trainInfo):
	
	f = file(filename, 'w')

	for train in trainInfo:
		
		for data in trainInfo:
			
			f.write(data)
			f.write(' ')
		f.write('\n')
	f.close()

def timediff(t1, t2):
	
	t1_hr = t1/60
	t1_min = t1%60

	t2_hr = t2/60
	t2_min = t2%60

	if((t2-t1)>720 and t1_hr < t2_hr):
		t1_hr = t1_hr+24
	return (t2_hr - t1_hr)*60 + (t2_min - t1_min)

def getStnDelay(trainVector):
	
	stnDelayTemp = {}

	for (t,train) in trainVector.iteritems():
		for i  in range(len(train)-1):
			station_this = train[i+1]
			station_last = train[i]
			if station_this[0] not in stnDelayTemp:
				stnDelayTemp[station_this[0]] = []
			
			route_delay = timediff(station_this[3], station_last[6]) - timediff(station_this[1], station_last[4])
			station_delay = timediff(station_this[6], station_this[3]) - timediff(station_this[4], station_this[1])
			if route_delay < 0:
				route_delay = 0

			stnDelayTemp[station_this[0]].append([route_delay, station_this[2], station_this[5], station_delay])

	stnDelay = {}
	for (k,v) in stnDelayTemp.iteritems():
		sum_route = 0
		sum_arr = 0
		sum_dep = 0
		sum_stn = 0
		for k1 in v:
			sum_route = sum_route + k1[0]
			sum_arr = sum_arr + k1[1]
			sum_dep = sum_dep + k1[2]
			sum_stn = sum_stn + k1[3]

		avg_route = float(sum_route)/len(k)
		avg_arr = float(sum_arr)/len(k)
		avg_dep = float(sum_dep)/len(k)
		avg_stn = float(sum_stn)/len(k)
		stnDelay[k] = [avg_route, avg_arr, avg_dep, avg_stn]
	return stnDelay

def printTop200(stnDelay):
	
	# prints the top 200 stations which have high average route delays!
	tempList = []
	for (k,v) in stnDelay.iteritems():
		tempList.append([k,v])
	print tempList[0]	
	tempList = sorted(tempList, key = lambda stn: -(stn[1])[0])

	for i in range(200):
		print tempList[i]


			


def printStatistics(crawled_file, actual_file):

	# prints statistic useful for user view
	# note this is a data consistency/strength values

	f = file(crawled_file, 'r')
	success = 0
	faliure = 0
	block = []
	blocks = []
	for l in f.readlines():
		if(l == '\n'):
			blocks.append(block)
			block = []
			continue

		block.append(l)
	
	actual = getTrainStationInfoActual(actual_file)
	trainCount = {}
	trainVector = {}
	schArrivalVector = {}
	arrivalDelayVector = {}
	actArrivalVector = {}
	schDepVector = {}
	depDelayVector = {}
	actDepVector = {}
	for block in blocks:
		tno = block[0].split(':')[1].strip()
		if tno not in trainCount:
			trainCount[tno] = 1
		else:
			trainCount[tno] = trainCount[tno]+1

		if len(block)==10:
			success = success+1
			sname = block[2].split(':')[1].strip()
			tno = block[0].split(':')[1].strip()
			if tno not in trainVector:
				trainVector[tno] = []
			if sname not in arrivalDelayVector:
				schArrivalVector[sname] = []
				arrivalDelayVector[sname] = []
				actArrivalVector[sname] = []
				schDepVector[sname] = []
				depDelayVector[sname] = []
				actDepVector[sname] = []
			sav = getTimeFromToken(block[3])
			adv = getDelayFromToken(block[4])
			aav = getTimeFromToken(block[5])
			sdv = getTimeFromToken(block[6])
			ddv = getDelayFromToken(block[7])
			acdv = getTimeFromToken(block[8])
			schArrivalVector[sname].append(sav)
			arrivalDelayVector[sname].append(adv)
			actArrivalVector[sname].append(aav)
			schDepVector[sname].append(sdv)
			depDelayVector[sname].append(ddv)
			actDepVector[sname].append(acdv)
			trainVector[tno].append([block[2].split(':')[1].strip(), sav, adv, aav, sdv, ddv, acdv])

		else:
			faliure = faliure + 1

	print 'Success: '+str(success)+'\nFaliure: '+str(faliure)
	print 'Trains crawled: '+str(len(trainVector))
	printDelayVecToFile('ArrivalDelay.out',arrivalDelayVector)
	printDelayVecToFile('DepDelay.out',depDelayVector)
	printTrainInfoToFile('TrainInfo.out', trainVector)
	stnDelay = getStnDelay(trainVector)
	printTop200(stnDelay)


if __name__=='__main__':
	printStatistics(sys.argv[1], sys.argv[2])
