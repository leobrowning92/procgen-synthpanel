import numpy as np

class Container(object):
    def __init__(self,x_center,y_center,l,h,collision_distance):
        self.x_center=x_center
        self.y_center=y_center
        self.width=l
        self.height=h
        self.collision_distance=collision_distance
        self.children=[]
    def check_inside(self,x,y):
        if self.x_center-self.collision_distance <= x <= self.x_center+self.collision_distance:
            if self.y_center-self.collision_distance <= y <= self.y_center+self.collision_distance:
                return True
        return False
    def make_child(self):
        self.children.append(child)
    def get_children(self,recursive):
        return self.children
