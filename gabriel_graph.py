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
# change
for i in range(INITIAL_POINTS):
    global newPoint
    # create a new point
    newPoint = Point(random.uniform(-0.999, 0.999), random.uniform(-0.999, 0.999));
    while newPoint in points:
        newPoint = Point(random.uniform(-0.999, 0.999), random.uniform(-0.999, 0.999));
    points.append(newPoint);

# generate edges
for p in points:
    for p1 in points:
        if p1 == p:
            continue
        center = p.middlePoint(p1);
        connect = True
        # check for edge eligibility
        for p2 in points:
            if p2 == p or p2 == p1:
                continue
            if p2.distance(center) < p.distance(center):
                connect = False
                break
        if connect:
            edge = ax.plot([p.x, p1.x], [p.y, p1.y], color='k');
            edges.append(edge[0]);

def init():
    return edges;
    
def animate(i):
    global points, edges, newPoint
    
    # update points
    newPoints = [];
    for p in points:
        p.shift(1.005);
        if inRange(p):
            newPoints.append(p);
    points = newPoints;
    
    # update edges
    newEdges = []
    for e in edges:
        x = e.get_xdata();
        y = e.get_ydata();
        x[0] *= 1.005;
        x[1] *= 1.005;
        y[0] *= 1.005;
        y[1] *= 1.005;
        if edgeInRange(x, y):
            e.set_xdata(x);
            e.set_ydata(y);
            newEdges.append(e);
        else:
            e.remove();
            del e;
    edges = newEdges;
    
    # add a new point
    newPoint = Point(random.uniform(-0.999, 0.999), random.uniform(-0.999, 0.999));
    while newPoint in points:
        newPoint = Point(random.uniform(-0.999, 0.999), random.uniform(-0.999, 0.999));
    # sort existing points by ascending distance to new point to improve performance
    points.sort(key=cmp_to_key(point_cmp))
    # iterate through existing points
    for p in points:
        center = p.middlePoint(newPoint);
        connect = True
        # check for edge eligibility
        for p2 in points:
            if p2 == p:
                continue
            if point_cmp(p, p2) < 0:
                break
            if p2.distance(center) < p.distance(center):
                connect = False
                break
        if connect:
            edge = ax.plot([p.x, newPoint.x], [p.y, newPoint.y], color=COLORS[i % 7]);
            edges.append(edge[0]);
    points.append(newPoint);
    return edges;

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

FFwriter = animation.FFMpegWriter(fps=60, extra_args=['-vcodec', 'libx264'])
anim.save('gabriel_graph.mp4', writer=FFwriter)
                
plt.show();
