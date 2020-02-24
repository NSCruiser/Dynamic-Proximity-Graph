import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import random
import math
import queue as Q

# Matplotlib colors without white
COLORS = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
# change this variable to customize the number of initial points
INITIAL_POINTS = 500


# custom point class to enable some features
class Point:

	__slots__ = 'x', 'y';
	
	def __init__(self, x, y):
		self.x = x;
		self.y = y;
	
	def __eq__(self, other):
		if not isinstance(other, Point):
			return False;
		return math.isclose(self.x, other.x, abs_tol=0.0001) and math.isclose(self.y, other.y, abs_tol=0.0001);

	def __hash__(self):
		return int(self.x * 1000) * 1000 + int(self.y * 1000);
	
	def distance(self, other):
		return math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2);
		
	def middlePoint(self, other):
		return Point((other.x + self.x) / 2, (other.y + self.y) / 2);
		
	def shift(self, factor):
		return Point(self.x * factor, self.y * factor);

# CORE HELPERS

# optimize graph
# RULE: replace AB with AC and BC if AB + BC < 1.02 * AB
def optimize(C, i):
	global graph, edgeCount, totalLength

	edges = edgeToList();
	newGraph = dict();
	for p in graph.keys():
		newGraph[p] = set();

	for e in edges:
		A, B = getPoint(e);
		lenAB = A.distance(B);
		lenAC = A.distance(C);
		lenBC = B.distance(C);

		if (lenAC + lenBC) < 1.02 * lenAB:
			e.remove();
			AC, = ax.plot([A.x, C.x], [A.y, C.y], color=COLORS[i % 7], marker='.');
			BC, = ax.plot([B.x, C.x], [B.y, C.y], color=COLORS[i % 7], marker='.');
			newGraph[A].add(AC);
			newGraph[B].add(BC);
			newGraph[C].add(AC);
			newGraph[C].add(BC);
			totalLength -= lenAB;
			totalLength += lenAC + lenBC;
			edgeCount += 1;
		else:
			newGraph[A].add(e);
			newGraph[B].add(e);

	graph = newGraph;

# connect point A to other eligible points
# RULES: modification 4 
def connect(A, i):
	global graph, totalLength, edgeCount, source

	candidates = [];
	finalists = [];
	pGraph = dict();
	for p in graph.keys():
		pGraph[p] = set();
	for p in graph.keys():
		for e in graph[p]:
			pGraph[p].add(getOther(p, e));

	for p in pGraph.keys():
		if p == A:
			continue;
		if RNGCheck(p, A) and angleCheck(p, A):
			candidates.append(p);

	if len(candidates) > 0:		
		source = A;
		pointsCmp = cmp_to_key(pointsComparator);
		candidates.sort(key=pointsCmp);
		B = candidates.pop(0);
		pGraph[A].add(B);
		pGraph[B].add(A);
		finalists.append(B);

		while len(candidates) > 0:
			T = candidates.pop(0);
			dist = dijkstra(pGraph, A, T);
			if A.distance(T) < 0.7 * dist:
				pGraph[T].add(A);
				pGraph[A].add(T);
				finalists.append(T);

		for T in finalists:
			edge, = ax.plot([A.x, T.x], [A.y, T.y], color=COLORS[i % 7], marker='.');
			graph[A].add(edge);
			graph[T].add(edge);

# primitive RNG rule check
def RNGCheck(A, B):
	dist = A.distance(B);
	for C in graph.keys():
		if C == A or C == B:
			continue
		if C.distance(A) < dist and C.distance(B) < dist:
			return False
	return True

# wrapper for angle check to check both sides of an edge
def angleCheck(A, B):
	return angleHelper(A, B) and angleHelper(B, A);

# angle check
# RULE: returns False if there exists an edge on A that forms an angle smaller
# 		than or equal to 15 degrees to AB
def angleHelper(A, B):
	for e in graph[A]:
		x = e.get_xdata();
		y = e.get_ydata();
		p1 = Point(x[0], y[0]);
		p2 = Point(x[1], y[1]);
		# check fails if there already exists an edge that connects A and B
		if p1 == B or p2 == B:
			return False
		# calculate angle
		if A == p1:
			dotProduct = (B.x - A.x) * (p2.x - A.x) + (B.y - A.y) * (p2.y - A.y);
			magProduct = math.sqrt((B.x - A.x)**2 + (B.y - A.y)**2) * math.sqrt((p2.x - A.x)**2 + (p2.y - A.y)**2);
			cosVal = dotProduct / magProduct;
		else:
			dotProduct = (B.x - A.x) * (p1.x - A.x) + (B.y - A.y) * (p1.y - A.y);
			magProduct = math.sqrt((B.x - A.x)**2 + (B.y - A.y)**2) * math.sqrt((p1.x - A.x)**2 + (p1.y - A.y)**2)
			cosVal = dotProduct / magProduct;
		if math.acos(cosVal) <= 0.2618:
			return False 
	return True

# HELPER METHODS

# shift all elements
# RULE: shift all elements by a factor of 1.005
def updateGraph():
	global graph, totalLength, edgeCount

	points = graph.keys();
	edges = edgeToList();
	
	newGraph = dict();

	for p in points:
		newGraph[p.shift(1.005)] = set();
	for e in edges:
		A, B = getPoint(e);
		A = A.shift(1.005);
		B = B.shift(1.005);

		if edgeInRange(A, B):
			e.set_xdata([A.x, B.x]);
			e.set_ydata([A.y, B.y]);
			newGraph[A].add(e);
			newGraph[B].add(e);
		else:
			e.remove();

	graph = newGraph;
	newGraph = dict();

	for p in graph.keys():
		if len(graph[p]) > 0:
			newGraph[p] = graph[p];

	graph = newGraph;

	# count edges
	newEdgeCount = 0;
	for p in graph.keys():
		newEdgeCount += len(graph[p]);

	edgeCount = newEdgeCount / 2;

# find shortest distance from A to B
def dijkstra(g, s, t):
	dist = dict();
	processed = dict();
	for p in g.keys():
		dist[p] = math.inf;
		processed[p] = False;
	dist[s] = 0;
	q = Q.PriorityQueue();
	q.put((0, s));

	while not q.empty():
		u = q.get();
		u = u[1];
		if u == t:
			break;
		if processed[u]:
			continue;
		for v in g[u]:
			alt = dist[u] + u.distance(v);
			if alt < dist[v]:
				dist[v] = alt;
				q.put((alt, v));
		processed[u] = True;
	return dist[t];

# check if a point is within the visible area
def inRange(p):
	return p.x < 1.000 and p.x > -1.000 and p.y < 1.000 and p.y > -1.000;

# check if an edge is within the visible area
def edgeInRange(A, B):
	if min(A.x, B.x) >= 1.000 or max(A.x, B.x) <= -1.000:
		return False
	if min(A.y, B.y) >= 1.000 or max(A.y, B.y) <= -1.000:
		return False
	return True

# return a list of edges
def edgeToList():
	edges = set();
	for p in graph.keys():
		for e in graph[p]:
			edges.add(e);
	return list(edges);

# get the other end of the edge
def getOther(p, e):
	A, B = getPoint(e);
	if p == A:
		return B;
	return A;

# converts an edge to a pair of Points
def getPoint(e):
	x = e.get_xdata();
	y = e.get_ydata();
	A = Point(x[0], y[0]);
	B = Point(x[1], y[1]);
	return [A, B];

# compare distance
def pointsComparator(p1, p2):
	if source.distance(p1) > source.distance(p2):
		return 1;
	elif source.distance(p1) == source.distance(p2):
		return 0;
	return -1;

# Convert a cmp= function into a key= function
def cmp_to_key(mycmp):
	
	class K:
		def __init__(self, obj, *args):
			self.obj = obj
		def __lt__(self, other):
			return mycmp(self.obj, other.obj) < 0
		def __gt__(self, other):
			return mycmp(self.obj, other.obj) > 0
		def __eq__(self, other):
			return mycmp(self.obj, other.obj) == 0
		def __le__(self, other):
			return mycmp(self.obj, other.obj) <= 0
		def __ge__(self, other):
			return mycmp(self.obj, other.obj) >= 0
		def __ne__(self, other):
			return mycmp(self.obj, other.obj) != 0
	return K

# ANIMATION 

def init():
	return edgeToList(), txt1, txt2, txt3;
	
def animate(i):
	global graph, edgeCount, totalLength

	# update locations of points and edges
	# RULE: shift
	updateGraph();
	
	# add a new point
	newPoint = Point(random.uniform(-0.9999, 0.9999), random.uniform(-0.9999, 0.9999));
	while newPoint in graph.keys():
		newPoint = Point(random.uniform(-0.9999, 0.9999), random.uniform(-0.9999, 0.9999));
	graph[newPoint] = set();

	# optimize existing routes
	optimize(newPoint, i);

	# generate new edges
	connect(newPoint, i);
	
	# add eligible new edges
	
	txt1.set_text("Points = " + str(len(graph.keys())))
	txt2.set_text("Edges = " + str(edgeCount))
	txt3.set_text("Total length = " + str(totalLength))

	return edgeToList(), txt1, txt2, txt3;

# create a figure
fig = plt.figure();
ax = plt.axes(xlim=(-1.0, 1.0), ylim=(-1.0, 1.0));

# initialization
graph = dict();
edgeCount = 0;
source = Point(0, 0);

# generate initial points
for n in range(INITIAL_POINTS):	
	# create a new point
	newPoint = Point(random.uniform(-0.9999, 0.9999), random.uniform(-0.9999, 0.9999));
	while newPoint in graph.keys():
		newPoint = Point(random.uniform(-0.9999, 0.9999), random.uniform(-0.9999, 0.9999));
	graph[newPoint] = set();

totalLength = 0.0

# generate initial edges
for p1 in graph.keys():
	for p2 in graph.keys():
		if p1 == p2:
			continue
		if RNGCheck(p1, p2) and angleCheck(p1, p2):
			edge, = ax.plot([p1.x, p2.x], [p1.y, p2.y], color='k', marker='.');
			graph[p1].add(edge);
			graph[p2].add(edge);
			edgeCount += 1;
			totalLength += p1.distance(p2);
			
txt1 = plt.figtext(0.1, 0.03, "Points = " + str(len(graph.keys())));
txt2 = plt.figtext(0.3, 0.03, "Edges = " + str(edgeCount));
txt3 = plt.figtext(0.5, 0.03, "Total length = " + str(totalLength));
	
# animate
anim = animation.FuncAnimation(fig, animate, init_func=init, frames=10800, interval=20)

FFwriter = animation.FFMpegWriter(fps=60, extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p'])
anim.save('RNG_v4.mp4', writer=FFwriter)
				
plt.show();