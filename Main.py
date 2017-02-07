import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.colors as colors

class Ray:
    def __init__(self, origin, direction):
        self.origin = np.array(origin)
        self.direction = np.array(direction)


class Hit:
    def __init__(self, t, location, normal, obj):
        self.location = np.array(location)
        self.normal = np.array(normal)
        self.obj = obj
        self.t = t


class Sphere:
    def __init__(self, c, r, color = None):
        self.center = np.array(c)
        self.radius = r
        if color == None:
            self.color = cm.rainbow(np.random.rand())
        else:
            self.color = color

    def intersect(self, ray):
        o = ray.origin - self.center
        d = ray.direction
        d = d / np.linalg.norm(d)
        r = self.radius
        #  solve |o+td|^2 - r^2 = 0
        a = 1
        b = 2 * o.dot(d)
        c = o.dot(o) - r * r

        diter = b ** 2 - 4 * a * c
        if diter < 0:
            return None
        t0 = (-b + np.sqrt(diter)) / (2 * a)
        t1 = (-b - np.sqrt(diter)) / (2 * a)

        if  t0 > t1:
            t0 = t1
        hit_loc = ray.origin + ray.direction*t0
        hit_n = hit_loc - self.center
        return Hit(t0, hit_loc, hit_n / np.linalg.norm(hit_n),self)

class Path:
    def __init__(self,start, dir, ):


    def set_next(self,next_path):
        self.next = next_path

render_target_size = (128,128)
render_target = np.ndarray(shape=(render_target_size+(4,)))

objs = [Sphere((-4, 2, 10), 2), Sphere((7, 3, 10), 2), Sphere((-4, -2, 14), 1)]
light = Sphere((0,0,100),100)




for x,px in zip(np.linspace(-1,1,render_target_size[0]),range(render_target_size[0])):
    for y,py in zip(np.linspace(-1, 1, render_target_size[1]), range(render_target_size[1])):
        dir = np.array((x,y,1))
        dir = dir/np.linalg.norm(dir)
        r = Ray((0, 0, 0), dir)
        min_intersect = 10000000
        hit = None
        for obj in objs:
            h = obj.intersect(r)
            if h != None and h.t < min_intersect:
                min_intersect = h.t
                hit = h
        if hit != None:
            render_target[px,py] = hit.obj.color
        else:
            render_target[px, py] = (0,0,0,1)
plt.imshow(render_target)
plt.show()


