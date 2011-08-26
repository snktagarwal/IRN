import networkx as nx
import time
import random
import bisect
import itertools
#from numpy import *
#import Gnuplot, Gnuplot.funcutils
import math

class GraphAPI:

	def __init__(self, u, y, t, n):

		self.u = u	# u as defined in paper
		self.y = y	# y as defined in paper
		self.t = t	# t -- time to run the simulation
		self.n = n	# n -- the number of nodes

	def genBottomDegreeDist(self):

		bottom = self.getPatternNodes('bot_')
		bottom_deg = map(lambda x: self.G.degree(x,weighted=True), bottom)

		# now generate the degree distribution( non-cumulative )
		highest_deg = max(bottom_deg)

		bottom_deg_dist = dict(zip(range(highest_deg+1), [0]*(highest_deg+1)))
		for deg in bottom_deg:
			bottom_deg_dist[deg] = bottom_deg_dist[deg]+1
		total_deg = len(bottom)
		bottom_deg_dist_list = []
		for k in bottom_deg_dist.iterkeys():
			bottom_deg_dist[k]=float(bottom_deg_dist[k])/total_deg
			#bottom_deg_dist_list.append([k,bottom_deg_dist[k]])
		#print sum(map(lambda x: x[1], bottom_deg_dist_list))
		return bottom_deg_dist


	def genEmptyBipGraph(self):

		# Add 'n' bottom nodes to the graph and assign 1 as a default degree
		self.G = nx.Graph()
		bottom_nodes = map(lambda x: 'bot_'+str(x), range(self.n))
		self.G.add_nodes_from(bottom_nodes)

	def clear(self):
		# clear the existing graph and regenerate
		try:
			del self.G
		except:
			pass
		self.genEmptyBipGraph()

	def weighted_choice_bisect_compile(self, items):
		"""Returns a function that makes a weighted random choice from items."""
		added_weights = []
		last_sum = 0

		for item, weight in items:
			last_sum += weight
			added_weights.append(last_sum)
		#print 'last sum '+str(last_sum)
		#print 'items: '+str(items)
		#print 'added_weights: '+str(added_weights)
		rand_sum = random.random()*last_sum
		#print 'rand sum '+str(rand_sum)
		ind = items[bisect.bisect(added_weights, rand_sum)][0]
		#print 'returning: '+str(ind)
		return ind

	def getPatternNodes(self, pat):
		pat_list = []
		for node in self.G.nodes():
			if pat in node:
				pat_list.append(node)
		return sorted(pat_list)

	def printGraph(self):
		X = self.getPatternNodes('bot_')
		print '---------'
		print 'Total (w) Deg: '+str(sum(map(lambda x: self.G.degree(x,weighted=True), X)))
		print 'Total (u/w) Deg: '+str(sum(map(lambda x: self.G.degree(x), X)))
		for node in X:
			print node +'->'+str(map(lambda x: [x,self.G[x][node]['weight']], self.G.neighbors(node)))

	def SimulateModelPworII(self):
		random.seed(int(time.time()))
		self.genEmptyBipGraph()

		for i in range(self.t):

			# Obtain the list of bottom-node degrees
			top_s, bottom_s = nx.bipartite.sets(self.G)
			top = self.getPatternNodes('top_')
			bottom = self.getPatternNodes('bot_')

			# Add a new node
			top_node = 'top_'+str(i)
			self.G.add_node(top_node)

			# Choose 'u' links w/o replacement
			for j in range(self.u):
				bottom_deg_dist = map(lambda x: self.y*self.G.degree(x,weighted=True)+1, bottom)
				bottom_deg_sum = sum(map(lambda x: self.y*self.G.degree(x,weighted=True), bottom))
				bottom_deg_dist = map(lambda x: float(x)/(bottom_deg_sum+len(bottom)), bottom_deg_dist)

				bottom_deg_dist_map = map(lambda x: [x, int(bottom_deg_dist[x]*1000)], range(len(bottom)))


				# Choose an index by Preferential Attachement
				ind = self.weighted_choice_bisect_compile(bottom_deg_dist_map)
				#print 'index of chosen node from bottom: '+str(ind)

				# Increment it's degree along with the top node's degree
				self.G.add_edge(top_node, bottom[ind])

				# Delete the index from the bottom_deg_list and bottom
				# Replacement
				bottom.pop(ind)

				# Continue
			#self.printGraph()

class Formula:
	"""Defines the formulas as described in the paper and generates output"""

	def __init__(self, n_max, r_max):
		# precalculate the nCr combination matrix for fast calculation
		self.precalculate(n_max, r_max)

	def precalculate(self, n_max, r_max):
		self.mat = []
		for i in range(n_max):
			self.mat.append([0]*r_max)

		for i in range(n_max):
			for j in range(r_max):
				if i==0:
					pass
				elif j==0 or i==j:
					self.mat[i][j]=1
				else:
					self.mat[i][j]=self.mat[i-1][j-1]+self.mat[i-1][j]

	def C(self, n, r):
		return self.mat[n][r]

	def PwrEq3Terms(self, i, j):

		if i < 0:
			return 0
		elif i == 0 and j == 0:
			return 1
		else:
			return self.eq3_dp[i][j]

	def PwrEq3(self, u, y, t, n, k):
		""" Equation 3 as in the paper draft"""

		self.eq3_dp = []
		for i in range(k):
			self.eq3_dp.append([0]*t)

		for i in range(t):
			for j in range(k):
					self.eq3_dp[j][i] = sum(map(lambda l: \
					self.mat[u][l]*math.pow(float(y*(j-l)+1)/(u*y*(i-1)+n), l)*math.pow(1-float(y*(j-l)+1)/(u*y*(i-1)+n), u-l)*self.PwrEq3Terms(j-l, i-1),range(u+1)))

		return map(lambda x: [x, self.eq3_dp[x][k-1]], range(k))


	def Formula_PwrRandomEq11(self, u, t, n, k):
		"""Defines the equation 11 in paper draft"""
		p = self.C(u*t, k)*math.pow(float(1)/n, k)*math.pow(1-float(1)/n, u*t-k)
		return p




class WithReplacement:

	def __init__(self, handle):
		self.handle = handle

	def Pwr_eq11(self, formula_handle, deg_range):
		return map(lambda x:[x, formula_handle.Formula_PwrRandomEq11(self.handle.u, self.handle.t, self.handle.n, x)], range(deg_range))

	def Pwr(self):
		handle = self.handle
		random.seed(int(time.time()))
		handle.genEmptyBipGraph()

		for i in range(handle.t):

			# Obtain the list of bottom-node degrees
			top_s, bottom_s = nx.bipartite.sets(handle.G)
			top = handle.getPatternNodes('top_')
			bottom = handle.getPatternNodes('bot_')

			# Add a new node
			top_node = 'top_'+str(i)
			handle.G.add_node(top_node)

			bottom_deg_dist = map(lambda x: handle.y*handle.G.degree(x,weighted=True)+1, bottom)
			bottom_deg_sum = sum(map(lambda x: handle.y*handle.G.degree(x,weighted=True), bottom))
			bottom_deg_dist = map(lambda x: float(x)/(bottom_deg_sum+len(bottom)), bottom_deg_dist)
			bottom_deg_dist_map = map(lambda x: [x, int(bottom_deg_dist[x]*1000)], range(len(bottom)))

			# Choose 'u' links w/ replacement
			for j in range(handle.u):

				# Choose an index by Preferential Attachement
				ind = handle.weighted_choice_bisect_compile(bottom_deg_dist_map)
				#print 'index of chosen node from bottom: '+str(ind)

				# Increment it's degree along with the top node's degree
				if not (top_node, bottom[ind]) in handle.G.edges() \
				and not (bottom[ind], top_node) in handle.G.edges():
					handle.G.add_edge(top_node, bottom[ind], weight=1)
				else:
					handle.G[top_node][bottom[ind]]['weight'] = \
					handle.G[top_node][bottom[ind]]['weight']+1

			# Print the graph
			#handle.printGraph()



class WithoutReplacement:

	def __init__(self, handle):
		self.handle = handle

	def PworI(self):
		handle = self.handle
		random.seed(int(time.time()))
		handle.genEmptyBipGraph()
		bottom = handle.getPatternNodes('bot_')
		bottom_comb = list(itertools.combinations(bottom, handle.u))

		for i in range(handle.t):

			# Add a new node
			top_node = 'top_'+str(i)
			handle.G.add_node(top_node)

			# Choose 'u' links w/o replacement and using bottom_comb
			bottom_comb_deg_dist = map(lambda x: \
			handle.y*(sum(map(lambda y: handle.G.degree(y,weighted=True), x)))+1, \
			bottom_comb)
			#print bottom_comb_deg_dist

			bottom_comb_deg_sum = sum(bottom_comb_deg_dist)
			#print bottom_comb_deg_sum

			bottom_comb_deg_dist = map(lambda x: \
			float(x)/(bottom_comb_deg_sum), bottom_comb_deg_dist)
			#print bottom_comb_deg_dist

			bottom_comb_deg_dist_map = map(lambda x: [bottom_comb[x], bottom_comb_deg_dist[x]], range(len(bottom_comb)))
			#print bottom_comb_deg_dist_map

			node_set = handle.weighted_choice_bisect_compile(bottom_comb_deg_dist_map)

			for node in node_set:
				handle.G.add_edge(top_node, node, weight=1)

			#handle.printGraph()


	def PworII(self):
		handle = self.handle
		random.seed(int(time.time()))
		handle.genEmptyBipGraph()

		for i in range(handle.t):

			# Obtain the list of bottom-node degrees
			top_s, bottom_s = nx.bipartite.sets(handle.G)
			top = handle.getPatternNodes('top_')
			bottom = handle.getPatternNodes('bot_')

			# Add a new node
			top_node = 'top_'+str(i)
			handle.G.add_node(top_node)

			# Choose 'u' links w/o replacement
			for j in range(handle.u):

				bottom_deg_dist = map(lambda x: handle.y*handle.G.degree(x,weighted=True)+1, bottom)
				bottom_deg_sum = sum(map(lambda x: handle.y*handle.G.degree(x,weighted=True), bottom))
				bottom_deg_dist = map(lambda x: float(x)/(bottom_deg_sum+len(bottom)), bottom_deg_dist)

				bottom_deg_dist_map = map(lambda x: [x, int(bottom_deg_dist[x]*1000)], range(len(bottom)))


				# Choose an index by Preferential Attachement
				ind = handle.weighted_choice_bisect_compile(bottom_deg_dist_map)
				#print 'index of chosen node from bottom: '+str(ind)

				# Increment it's degree along with the top node's degree
				handle.G.add_edge(top_node, bottom[ind], weight=1)

				# Delete the index from the bottom_deg_list and bottom
				# Replacement
				bottom.pop(ind)

				# Continue
			#handle.printGraph()

class SimAvg:
	"""Averages the results over many-a-runs"""
	def __init__(self, graph_handle, sim_handle, data_handle):
		self.graph_handle = graph_handle
		self.sim_handle = sim_handle
		self.data_handle = data_handle

	def runningAverage(self, title, runs):

		degDict = {}
		for i in range(runs):
			t_st = time.time()
			print('Iteration %d started at %f' % (i, t_st))
			# specify the model you want to run here
			self.sim_handle.Pwr()
			bottom_deg_dist_run = self.graph_handle.genBottomDegreeDist()
			# averaging logic
			for deg in bottom_deg_dist_run.iterkeys():
				if deg not in degDict:
					degDict[deg]=bottom_deg_dist_run[deg]
				else:
					degDict[deg]=degDict[deg]+bottom_deg_dist_run[deg]
			self.graph_handle.clear()
			t_end = time.time()
			print('Iteration %d ended at %f' % (i, t_end))
			print('Completition time: %f' % (t_end-t_st))
			out =  map(lambda (k,v):[k,v/(i+1)],degDict.iteritems())
			self.data_handle.spitDataToFile(title, out, runs)
		print degDict
		return out

class DataAPI:
	def __init__(self, graph_handle):
		self.graph_handle = graph_handle

	def spitDataToFile(self, title, data, runs):

		f = file('datasets/'+title+'avg_'+str(runs)+'_u='+str(self.graph_handle.u)+'_y='+str(self.graph_handle.y)+'_n='+str(self.graph_handle.n)+'_t='+str(self.graph_handle.t),'w')
		f.write('#Title: '+title+'avg_'+str(runs)+'_u='+str(self.graph_handle.u)+'_y='+str(self.graph_handle.y)+'_n='+str(self.graph_handle.n)+'_t='+str(self.graph_handle.t)+'_r='+str(runs)+'\n')
		f.write('#Degree Percentage\n')
		f.writelines(["%d\t%f\n" % (item[0],item[1]) for item in data])
		f.flush()
		f.close()

	def genGraph(self, title, data, runs):

		# Generate a graph by an appropirate name and axis

		g = Gnuplot.Gnuplot(debug=1)
		g('set style data linespoints')
		g.title(title+'avg_'+str(runs)+'_u='+str(self.graph_handle.u)+'_y='+str(self.graph_handle.y)+'_n='+str(self.graph_handle.n) \
		+'_t='+str(self.graph_handle.t))
		g.xlabel('Degree')
		g.ylabel('Percentage of nodes')
		g.plot(data)
		g.hardcopy('graphs/'+title+'avg_'+str(runs)+'_u='+str(self.graph_handle.u)+'_y='+str(self.graph_handle.y)+'_n='+str(self.graph_handle.n) \
		+'_t='+str(self.graph_handle.t)+'.ps')
		g.reset()

if __name__=='__main__':
	# u, y , t, n
	title='Pwr_'
	runs=5000
	u=5
	y=5
	t=500
	n=100
	k=1000
	#frm = Formula(u+1,u+1)
	#eq3_mat = frm.PwrEq3(u,y,t,n,k)
	#print eq3_mat
	graph = GraphAPI(u, y, t, n)
	data = DataAPI(graph)
	mod2 = WithReplacement(graph)
	#out = mod2.Pwr_eq11(frm, 150)
	#g = DataAPI(graph)
	#g.spitDataToFile('Eq3_', eq3_mat, 0)
	#g.genGraph('Eq11_', out, 0)
	avg = SimAvg(graph, mod2, data )
	out = avg.runningAverage(title, runs)
	print 'sum: '+str(sum(map(lambda x:x[1], out)))
	#graph.spitDataToFile(title, out, runs)
	#graph.genGraph(title, out, runs)
