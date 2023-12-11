import abc
import os
from turtle import Turtle
from pyturtle.shapes.point import Point2D

class Shape(metaclass=abc.ABCMeta):

    def __init__(
        self,
        turtle: Turtle,
        steps: int,
        coordinates = {},
    ):
        self.turtle = turtle
        self.steps = steps  # step = len(coordinates)
        self.coordinates = coordinates  # key will depend on shape.

    @abc.abstractmethod
    def draw(self):
        pass

    @abc.abstractmethod
    def translate_x(self, x_shift):
        pass

    @abc.abstractmethod
    def translate_y(self, y_shift):
        pass

    @abc.abstractmethod
    def translate_xy(self, x_shift, y_shift):
        pass

    @abc.abstractmethod
    def rotate(self, degrees):
        pass

    @abc.abstractmethod
    def get_slice(self, step_one, step_two):
        pass

    @abc.abstractmethod
    def get_random_slice(self):
        pass

    def _update_coordinate(self, key, value):
        self.coordinates[key] = value

    def get_coordinate(self, key):
        return self.coordinates[key]

    def get_coordinates(self):
        return self.coordinates

    def get_turtle(self):
        return self.turtle
