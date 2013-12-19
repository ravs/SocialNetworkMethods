#!/usr/bin/env python
'''
Implement Cascade Maximization for Linear Threshold Model
Assumptions:
weight w_i2j = 1/out_deg(i) (for edge from i to j)
Threshold = 0.5
k = 10

Instruction:
rename edgelist to file name of your edge list and execute

Ravs Fall 2013
'''

import operator

edgelist = open("edgelist.txt","r")

# Assumed values
threshold = 0.5
k = 10

# Adjacency list implemented as dict
alist = {}

# To keep track of visited nodes for each source node which has edges with
# weight more than threshold
visited = []

# To keep track for the nodes being activated by the source node
nodeCoverage = {}

# Method to prepare Adjacency list as dict of list from edge list
def prepareAdjList():
	for line in edgelist:
		src,dest = line.split()
		#print src + " -> " + dest
		if int(src) not in alist:
			alist[int(src)] = []
		alist[int(src)].append(int(dest))

# Method to return the weight, where w = 1/degree_out of node
def getWeight(nodeId):
	if nodeId in alist:
		degree = len(alist[nodeId])
		return 1.0/degree
		#print "Node : " + str(nodeId) + " has " + str(degree) + " childs."

# Method to recursively find the path through which node activation can propagate
# i.e. the chain of nodes activated from single source node
def getNodeCoverage(nodeId, sourceNode):
	if nodeId in alist:
		# print str(nodeId) + "'s uniform edge weight : " + str(getWeight(nodeId))
		if getWeight(nodeId)>=threshold:
			if nodeId not in visited:
				nodeCoverage[sourceNode].append(nodeId)
				visited.append(nodeId)
			#print "Node's unifrom weight is more than threshold"
			for child in alist[nodeId]:
				if child not in visited:
					nodeCoverage[sourceNode].append(child)
					visited.append(child)
					if getWeight(child)>=threshold:
						# print "calling getNodeCoverage for " + str(child)
						getNodeCoverage(child, sourceNode)

def main():
	prepareAdjList()
	for key in alist:
		global visited
		visited = []
		if getWeight(key)>=threshold:
			nodeCoverage[key] = []
			getNodeCoverage(key, key)
	# print ",".join(str(item) for item in visited)
	# for key in nodeCoverage:
	# 	print str(key) + " -> " + ",".join(str(node) for node in nodeCoverage[key])
	# Sort the node coverage in descending order
	sorted_nodeCoverage = sorted(nodeCoverage, key=lambda x: len(nodeCoverage[x]))
	sorted_nodeCoverage.reverse()
	
	# Top 10 nodes with max activation coverage
	idx = 0
	print "Top 10 Nodes with maximum activation:"
	for key in sorted_nodeCoverage:
		if idx<10:
			print "{ " + str(key) + " -> " + ", ".join(str(node) for node in nodeCoverage[key]) + " }"
		idx = idx + 1
	
	# Remove redundant nodes from the dict
	print "Top 10 Nodes with max activation after removing the redundant nodes:"
	activated_nodes = []
	for key in sorted_nodeCoverage:
		temp = []
		for node in nodeCoverage[key]:
			if node not in activated_nodes:
				activated_nodes.append(node)
				temp.append(node)
		nodeCoverage[key] = temp
	count = 0
	activated_nodes = []
	depth = len(nodeCoverage[sorted_nodeCoverage[0]])
	for node in sorted_nodeCoverage:
		# Run for k-times
		if count<k and len(nodeCoverage[node])!=0 :
			print "{ " + str(node) + " -> " + ",".join(str(item) for item in nodeCoverage[node]) + " }"
			for nodeId in nodeCoverage[node]:
				if nodeId not in activated_nodes:
					activated_nodes.append(nodeId)
			count = count + 1
	print "After k = " + str(k) + " rounds, activated nodes are :"
	print "Total number of nodes acivated : " + str(len(activated_nodes))
	print "[ " + ", ".join(str(node) for node in activated_nodes) + " ]"

if __name__ == "__main__":
	main()

'''

Output:
Top 10 Nodes with maximum activation:
{ 65321 -> 65321, 23519, 26077, 26078, 83883, 85293 }
{ 185140 -> 185140, 85943, 101802, 130574, 101803, 170025 }
{ 43521 -> 43521, 43520, 35854, 68988, 35853, 114718 }
{ 43520 -> 43520, 35854, 43521, 68988, 35853, 114718 }
{ 163509 -> 163509, 113663, 189239, 191201, 64267 }
{ 194213 -> 194213, 163965, 122187, 199124, 224127 }
{ 239871 -> 239871, 194370, 221973, 215504, 200912 }
{ 191201 -> 191201, 64267, 189239, 163509, 113663 }
{ 189239 -> 189239, 163509, 113663, 191201, 64267 }
{ 221973 -> 221973, 215504, 200912, 239871, 194370 }
Top 10 Nodes with max activation after removing the redundant nodes:
{ 65321 -> 65321,23519,26077,26078,83883,85293 }
{ 185140 -> 185140,85943,101802,130574,101803,170025 }
{ 43521 -> 43521,43520,35854,68988,35853,114718 }
{ 163509 -> 163509,113663,189239,191201,64267 }
{ 194213 -> 194213,163965,122187,199124,224127 }
{ 239871 -> 239871,194370,221973,215504,200912 }
{ 214826 -> 214826,206022,225298,228166,228167 }
{ 205015 -> 205015,124126,107021,124127,195925 }
{ 82786 -> 82786,105165,105166,26099,155298 }
{ 81300 -> 81300,94199,16622,75393,118539 }
After k = 10 rounds, activated nodes are :
Total number of nodes acivated : 53
[ 65321, 23519, 26077, 26078, 83883, 85293, 185140, 85943, 
  101802, 130574, 101803, 170025, 43521, 43520, 35854, 68988, 
  35853, 114718, 163509, 113663, 189239, 191201, 64267, 194213, 
  163965, 122187, 199124, 224127, 239871, 194370, 221973, 215504, 
  200912, 214826, 206022, 225298, 228166, 228167, 205015, 124126, 
  107021, 124127, 195925, 82786, 105165, 105166, 26099, 155298, 81300, 
  94199, 16622, 75393, 118539 ]

'''