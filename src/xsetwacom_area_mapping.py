#!/usr/bin/env python

# Taken from:
# https://github.com/linuxwacom/xf86-input-wacom/wiki/Area-mapping


# from __future__ import division
def main():
    area = get_area_bounds()
    print("xsetwacom set DEVICE_ID area %d %d %d %d" % (area[0], area[1], area[2], area[3]))


def get_area_bounds():
    tablet = Device("58752x33048")         # Replace with the resolution of your tablet

    monitor_0 = Device("2560x1440")        # Replace with the resolution of your left screen
    monitor_1 = Device("1920x1080")        # Replace with the resolution of your right screen (tablet)
    monitors = [monitor_0, monitor_1]

    # monitor_1.place_right_of(monitor_0)
    monitor_1.place_below(monitor_0)
    desktop = bounding_box(monitors)

    area = map_tablet_onto(tablet, desktop, monitor_1)  # Specify monitor to map tablet to here

    return area.p1[0], area.p1[1], area.p2[0], area.p2[1]

#######################################################################
## Do not edit below this line.
##

class Vector:
    def __init__(self, *data):
        self.data = data
    def __repr__(self):
        return repr(self.data) 
    def __add__(self, other):
        return Vector( *[a+b for a,b in zip(self.data, other.data) ] )  
    def __sub__(self, other):
        return Vector( *[a-b for a,b in zip(self.data, other.data) ] )
    def __mul__(self, other):
        return Vector( *[a*b for a,b in zip(self.data, other.data) ] )
    def __truediv__(self, other):
        return Vector( *[1.0*a/b for a,b in zip(self.data, other.data) ] )
    def __iter__(self):
        return iter(self.data)
    def __getitem__(self, index):
        return self.data[index]

class Rectangle:
    def __init__(self, p1=(0,0), p2=(0,0)):
        self.p1, self.p2 = Vector(*p1), Vector(*p2)
    def __repr__(self):
        return repr((self.p1, self.p2))
    def __add__(self, point):
        return Rectangle(self.p1 + point, self.p2 + point)
    def __sub__(self, point):
        return Rectangle(self.p1 - point,  self.p2 - point)
    def getSize(self):
        return self.p2 - self.p1
    def setSize(self, size):
        self.p2 = self.p1 + size
    def getOrigin(self):
        return self.p1
    def setOrigin(self, point):
        self.p2, self.p1 = self.size + point, point
    size = property(getSize, setSize)
    origin = property(getOrigin, setOrigin)

class Device(Rectangle):
    def __init__(self, resolution):
        x, y = resolution.split("x")
        Rectangle.__init__(self, (0,0), Vector(int(x), int(y)))
    def place_right_of(self, other):
        self.setOrigin(other.origin + Vector(other.size[0], 0))
    def place_left_of(self, other):
        self.setOrigin(other.origin - Vector(self.size[0], 0))
    def place_above(self, other):
        self.setOrigin(other.origin - Vector(0, self.size[1]))
    def place_below(self, other):
        self.setOrigin(other.origin + Vector(0, other.size[1]))

def bounding_box(rectangles):
    points = [rect.p1 for rect in rectangles]
    min_x = min([x for x,y in points])
    min_y = min([y for x,y in points])

    points = [rect.p2 for rect in rectangles]
    max_x = max([x for x,y in points])
    max_y = max([y for x,y in points])

    return Rectangle((min_x, min_y), (max_x, max_y))

def normalize(desktop, monitor):
    rect = Rectangle([ (monitor.p1 - desktop.p1)[i] / desktop.size[i] for i in [0,1] ])
    rect.setSize(monitor.size / desktop.size)
    return rect

def map_tablet_onto(tablet, desktop, monitor):
    norm = normalize(desktop, monitor)
    rect = Rectangle()
    rect.setSize(tablet.size / norm.size)
    rect.setOrigin ( tablet.origin - (rect.size * norm.origin) )
    return rect


if __name__=="__main__":
    main()

