import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import random
import math

# Matplotlib colors without white
COLORS = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
# change this variable to customize the number of initial points
INITIAL_POINTS = 500


# custom point class to enable some features
class Point:
	
	def __init__(self, x, y):
		self.x = x;
		self.y = y;
	
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y
	
	def distance(self, other):
		return math.sqrt((other.x - self.x) * (other.x - self.x) + (other.y - self.y) * (other.y - self.y));
		
	def middlePoint(self, other):
		return Point((other.x + self.x) / 2, (other.y + self.y) / 2);
		
	def shift(self, factor):
		self.x *= factor;
		self.y *= factor;
		
	def __hash__(self):
		return hash((self.x, self.y))

# create a figure
fig = plt.figure();
ax = plt.axes(xlim=(-1.0, 1.0), ylim=(-1.0, 1.0));

# create a rectangle
# square = patches.Rectangle((-1, -1), 2, 2, fill=False);
# ax.add_patch(square);

# add initial points and lines
points = [];
edges = [];

# add initial points
for i in range(INITIAL_POINTS):
	global newPoint
	# create a new point
	newPoint = Point(random.uniform(-0.999, 0.999), random.uniform(-0.999, 0.999));
	while newPoint in points:
		newPoint = Point(random.uniform(-0.999, 0.999), random.uniform(-0.999, 0.999));
	points.append(newPoint);

total_length = 0.0

# generate edges
for i in range(len(points)):
	for j in range(i+1, len(points)):
		p = points[i]
		p1 = points[j]
		connect = True
		# check for edge eligibility
		for p2 in points:
			if p2 == p or p2 == p1:
				continue
			# don't connect if p2 is found to be within the circle
			if p2.distance(p) < p.distance(p1) and p2.distance(p1) < p.distance(p1):
				connect = False
				break
		for e in edges:
			x = e.get_xdata();
			y = e.get_ydata();
			cosVal = -2.0
			if x[0] == p.x and y[0] == p.y:
				dotProduct = (x[1] - p.x) * (p1.x - p.x) + (y[1] - p.y) * (p1.y - p.y)
				magProduct = math.sqrt((x[1] - p.x)**2 + (y[1] - p.y)**2) * math.sqrt((p1.x - p.x)**2 + (p1.y - p.y)**2)
				cosVal = dotProduct / magProduct
			elif x[1] == p.x and y[1] == p.y:
				dotProduct = (x[0] - p.x) * (p1.x - p.x) + (y[0] - p.y) * (p1.y - p.y)
				magProduct = math.sqrt((x[0] - p.x)**2 + (y[0] - p.y)**2) * math.sqrt((p1.x - p.x)**2 + (p1.y - p.y)**2)
				cosVal = dotProduct / magProduct
			elif x[0] == p1.x and y[0] == p1.y:
				dotProduct = (x[1] - p1.x) * (p.x - p1.x) + (y[1] - p1.y) * (p.y - p1.y)
				magProduct = math.sqrt((x[1] - p1.x)**2 + (y[1] - p1.y)**2) * math.sqrt((p.x - p1.x)**2 + (p.y - p1.y)**2)
				cosVal = dotProduct / magProduct
			elif x[1] == p1.x and y[1] == p1.y:
				dotProduct = (x[0] - p1.x) * (p.x - p1.x) + (y[0] - p1.y) * (p.y - p1.y)
				magProduct = math.sqrt((x[0] - p1.x)**2 + (y[0] - p1.y)**2) * math.sqrt((p.x - p1.x)**2 + (p.y - p1.y)**2)
				cosVal = dotProduct / magProduct
			if cosVal != -2.0:
				if math.acos(cosVal) <= 0.2618:
					connect = False
					break
		# connect p and p1
		if connect:
			edge = ax.plot([p.x, p1.x], [p.y, p1.y], color='k', marker='.');
			edges.append(edge[0]);
			total_length += math.sqrt((p.x-p1.x)**2 + (p.y-p1.y)**2);
			
txt1 = plt.figtext(0.1, 0.03, "Points = " + str(len(points)));
txt2 = plt.figtext(0.3, 0.03, "Edges = " + str(len(edges)));
txt3 = plt.figtext(0.5, 0.03, "Total length = " + str(total_length));
	
def init():
	return edges, txt1, txt2, txt3;
	
def animate(i):
	global points, edges, newPoint, txt1, txt2, total_length
	
	# remove out-of-bound points
	newPoints = [];
	for p in points:
		p.shift(1.005);
		if inRange(p):
			newPoints.append(p);
	points = newPoints;
	
	# remove out-of-bound edges
	newEdges = []
	for e in edges:
		x = e.get_xdata();
		y = e.get_ydata();
		l = math.sqrt((x[0]-x[1])**2 + (y[0]-y[1])**2)
		x[0] *= 1.005;
		x[1] *= 1.005;
		y[0] *= 1.005;
		y[1] *= 1.005;
		if edgeInRange(x, y):
			e.set_xdata(x);
			e.set_ydata(y);
			newEdges.append(e);
			total_length -= l
			total_length += math.sqrt((x[0]-x[1])**2 + (y[0]-y[1])**2)
		else:
			e.remove();
			total_length -= l
	edges = newEdges;
	
	# add a new point
	newPoint = Point(random.uniform(-0.999, 0.999), random.uniform(-0.999, 0.999));
	while newPoint in points:
		newPoint = Point(random.uniform(-0.999, 0.999), random.uniform(-0.999, 0.999));
		
	# sort existing points by ascending distance to new point to improve performance
	points.sort(key=cmp_to_key(point_cmp))
	
	# reconnect the graph
	newEdges = []
	for e in edges:
		x = e.get_xdata();
		y = e.get_ydata();
		lenAB = math.sqrt((x[0]-x[1])**2 + (y[0]-y[1])**2)
		lenAC = math.sqrt((x[0]-newPoint.x)**2 + (y[0]-newPoint.y)**2)
		lenBC = math.sqrt((x[1]-newPoint.x)**2 + (y[1]-newPoint.y)**2)
		if (lenAC + lenBC) < 1.02 * lenAB:
			e.remove();
			new_ac = ax.plot([x[0], newPoint.x], [y[0], newPoint.y], color=COLORS[i % 7], marker='.');
			new_bc = ax.plot([x[1], newPoint.x], [y[1], newPoint.y], color=COLORS[i % 7], marker='.');
			newEdges.append(new_ac[0]);
			newEdges.append(new_bc[0]);
			total_length -= lenAB
			total_length += lenAC + lenBC
		else:
			newEdges.append(e);
	edges = newEdges
	
	# add new edges based on modification 2
	for p in points:
		connect = True
		# check for edge eligibility
		for p2 in points:
			if p2 == p:
				continue
			if p2.distance(p) < newPoint.distance(p) and p2.distance(newPoint) < newPoint.distance(p):
				connect = False
				break
		p1 = newPoint
		for e in edges:
			x = e.get_xdata();
			y = e.get_ydata();
			cosVal = -2.0
			if x[0] == p.x and y[0] == p.y:
				dotProduct = (x[1] - p.x) * (p1.x - p.x) + (y[1] - p.y) * (p1.y - p.y)
				magProduct = math.sqrt((x[1] - p.x)**2 + (y[1] - p.y)**2) * math.sqrt((p1.x - p.x)**2 + (p1.y - p.y)**2)
				cosVal = dotProduct / magProduct
			elif x[1] == p.x and y[1] == p.y:
				dotProduct = (x[0] - p.x) * (p1.x - p.x) + (y[0] - p.y) * (p1.y - p.y)
				magProduct = math.sqrt((x[0] - p.x)**2 + (y[0] - p.y)**2) * math.sqrt((p1.x - p.x)**2 + (p1.y - p.y)**2)
				cosVal = dotProduct / magProduct
			elif x[0] == p1.x and y[0] == p1.y:
				dotProduct = (x[1] - p1.x) * (p.x - p1.x) + (y[1] - p1.y) * (p.y - p1.y)
				magProduct = math.sqrt((x[1] - p1.x)**2 + (y[1] - p1.y)**2) * math.sqrt((p.x - p1.x)**2 + (p.y - p1.y)**2)
				cosVal = dotProduct / magProduct
			elif x[1] == p1.x and y[1] == p1.y:
				dotProduct = (x[0] - p1.x) * (p.x - p1.x) + (y[0] - p1.y) * (p.y - p1.y)
				magProduct = math.sqrt((x[0] - p1.x)**2 + (y[0] - p1.y)**2) * math.sqrt((p.x - p1.x)**2 + (p.y - p1.y)**2)
				cosVal = dotProduct / magProduct
			if cosVal != -2.0:
				# print(cosVal)
				if cosVal >= 1.0 or cosVal <= -1.0 or math.acos(cosVal) <= 0.2618:
					connect = False
					break
		if connect:
			edge = ax.plot([p.x, newPoint.x], [p.y, newPoint.y], color=COLORS[i % 7], marker='.');
			edges.append(edge[0]);
			total_length += math.sqrt((p.x-p1.x)**2 + (p.y-p1.y)**2);
			
	points.append(newPoint);
	txt1.set_text("Points = " + str(len(points)))
	txt2.set_text("Edges = " + str(len(edges)))
	txt3.set_text("Total length = " + str(total_length))
	return edges, txt1, txt2, txt3;

# compare two points' distances to the latest added point
def point_cmp(a, b):
	return newPoint.distance(a) - newPoint.distance(b);
	
def cmp_to_key(mycmp):
	'Convert a cmp= function into a key= function'
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
	
# check if a point is within the visible area
def inRange(p):
	return p.x < 1.000 and p.x > -1.000 and p.y < 1.000 and p.y > -1.000;

# check if an edge is within the visible area
def edgeInRange(x, y):
	if min(x[0], x[1]) >= 1.000 or max(x[0], x[1]) <= -1.000:
		return False
	if min(y[0], y[1]) >= 1.000 or max(y[0], y[1]) <= -1.000:
		return False
	return True

# animate
anim = animation.FuncAnimation(fig, animate, init_func=init, frames=10800, interval=20)

FFwriter = animation.FFMpegWriter(fps=60, extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p'])
anim.save('RNG_v3.mp4', writer=FFwriter)
				
plt.show();