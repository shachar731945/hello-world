"""
this class is used to represent a player's character on the game board as a
snake. the class enables the game to control their movement, check attributes 
of the snake such as their location for the game mechanics to use.the classes 
attributes are their position, radius, x and y of the circle the snake's head
will follow at start, and the drawing angle, which part of the circle the 
snake will round, the color of the snake, the x and y of the snake's head and 
sizes of the malben that blocks the circle. The classe's functions will be 
initialization, draw_update which updates the snake's head position according 
to a movement on the circle. switch_direction that will change the circle that
the the snake moves on and will change his direction from clockwise to against 
it and the opposite. the function get_draw_params is used by the game to draw 
the snake, each time a little bit of the circle. Another function will let the
game know the color that the snake is gonna be on when he moves for game use
such as disqualify the player.
"""

from math import cos, sin, radians
import pygame


class Snake:
    def __init__(self, radius, xy, color, drawing_angle):
        """
        the function initializes a Snake instance on the program which uses 
        this class. the function sets the new Snake params: radius, color, x 
        and y of the circle that thesnake surrounds and the head of the snake,
        the drawing and starting angle, the sizes of the rectangle that blocks 
        the circle that the snake surrounds.
        :param radius: settels the radius of the circle that the snake rounds  
        :param xy: the x and y of the center of the circle that the snake
        surrounds
        :param color: the color of the snake, RGB format 
        :param drawing_angle: the angle that each draw the snake moves on the
        circle (out of 360=2*pi)
        """
        self._radius = radius
        self._color = color
        self._circle_x = xy[0]
        self._circle_y = xy[1]
        self._angle = 0
        self._drawing_angle = drawing_angle
        self._rect = [self._radius * 2, self._radius * 2]
        self._posx = self._circle_x + self._radius * cos(radians(self._angle))
        self._posy = self._circle_y - self._radius * sin(radians(self._angle))

    def draw_update(self):
        """
        this function updates the head of the snake coordinates according to 
        circle which the snake surrounds using math functions sin, cos and rads 
        :return: the x and y positions of the head of the snake after the 
        update
        """
        self._angle = self._angle + self._drawing_angle
        if self._angle >= 360:
            self._angle = self._angle - 360
        self._posx = self._circle_x + self._radius * cos(radians(self._angle))
        self._posy = self._circle_y - self._radius * sin(radians(self._angle))
        return self._posx, self._posy

    def swich_direction(self):
        """
        this function updates a new circle that the snake surrounds because of 
        a change in the direction which the snake surrounds, from clockwise to 
        against and the opposite, because of that the drawing angles becomes 
        negative to its before and using "middle of a line" formula from math 
        to identify the new center of the circle
        :return: nothing
        """
        self._circle_x = 2 * self._posx - self._circle_x
        self._circle_y = 2 * self._posy - self._circle_y
        self._drawing_angle = -1 * self._drawing_angle
        self._angle = self._angle - 180

    def get_draw_params(self, screen):
        """
        :param screen: the screen which the draw is being outputted to
        :return: the params for pygame.draw.arc function according to the 
        angels to draw, the radius of the circle, the rect that surrounds the
        circle, the posses of the center of the circle that the snakes moves 
        around
        """
        return (screen, self._color, [
            self._circle_x - self._radius,
            self._circle_y - self._radius] + self._rect,
                radians(self._angle),
                radians(self._angle + self._drawing_angle))

    def get_going_to_color(self):
        """
        :return: the color of the pixel which the head of the snake will 
        override by his if he would move (the snake) normallly.  
        """
        new_angle  = self._angle + self._drawing_angle
        return pygame.Surface.get_at(
            (self._circle_x + self._radius * cos(radians(new_angle)),
             self._circle_y - self._radius * sin(radians(new_angle))))
