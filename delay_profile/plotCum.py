f = file('DelayDist','r')

lines = f.readlines()
stats = map(lambda x: float(x), lines)

cum_stats = []

for i in range(len(stats)):
  cum_stats.append([stats[i], float(len(stats)-i)/len(stats)])

for c in cum_stats:
  print c[0], c[1]

