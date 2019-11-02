import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import random

fig = plt.figure();
ax = plt.axes(xlim=(-1.5, 1.5), ylim=(-1.5, 1.5));

square = patches.Rectangle((-1, -1), 2, 2, fill=False);
ax.add_patch(square);
points = []
for i in range(99):
    points.append(plt.scatter(random.uniform(-0.995, 0.995), random.uniform(-0.995, 0.995), color='black', s=7));
    
def init():
    return points
    
def animate(i):
    j = 0;
    while j < len(points):
        xy = points[j].get_offsets();
        if xy[0][0] * 1.005 >= 1.000 or xy[0][1] * 1.005 >= 1.000 or xy[0][0] * 1.005 <= -1.000 or xy[0][1] * 1.005 <= -1.000:
            points.pop(j).remove(); 
        else:
            xy[0][0] *= 1.005;
            xy[0][1] *= 1.005;
            points[j].set_offsets(xy);
            j += 1;
    points.append(plt.scatter(random.uniform(-0.995, 0.995), random.uniform(-0.995, 0.995), color='black', s=5));
    return points
    
anim = animation.FuncAnimation(fig, animate, init_func=init, frames=21600, interval=100)
    
plt.show();
