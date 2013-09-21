import os, sys
import pyglet
from pyglet.gl import *
'''
import pymunkoptions
pymunkoptions.options["debug"] = False
'''
import pymunk
from pymunk import Vec2d
import math
from math import sin,cos,tan,degrees,sqrt,atan2,radians

def distance(a, b):
	return sqrt(((a[0]-b[0])**2)+((a[1]-b[1])**2))

def angle_between_points(a, b):
	xDiff = b[0]-a[0]
	yDiff = b[1]-a[1]
	#print(atan2(yDiff,xDiff))
	return degrees(atan2(yDiff,xDiff))

def midpoint(a, b):
	return [((a[0]+b[0])/2),((a[1]+b[1])/2)]

def define_circle_points(radius, position, res):
	# decagon
	add 	= (res*3.14)/180
	angle 	= 0
	points 	= []
	iter_count = 360//res
	for i in range(iter_count):
		x = radius*cos(angle) + position[0]
		y = radius*sin(angle) + position[1]
		points.append(x)
		points.append(y)
		angle += add
	return points

def calc_index(length):
	index = []
	index.append(0)
	for i in range(length):
		if i != 0:
			index.append(i)
			index.append(i)
	index.append(0)
	#print(index)
	return index

def calc_index_tri(length):
	index = []
	for i in range(length):
		if ((i+1) % 3) != 0:
			index.append(i)
		else:
			index.append(i)
			if length > 3:
				index.append(i)
		if (i+1) == length and length > 3:
			index.append(0)
		
	print(index)
	return index

class PymunkUtil2(object):
	def __init__(self, scene):
		self.scene = scene
		self.space = scene.space
		self.segments 	= []
		self.polygons  	= []
		self.circles  	= []

		for shape in self.space.shapes:
			if isinstance(shape, pymunk.Segment):
				self.segments.append(shape)
			if isinstance(shape, pymunk.Circle):
				self.circles.append(shape)
			if isinstance(shape, pymunk.Poly):
				self.polygons.append(shape)

		self.circle_color 		= (155,155,255)
		self.circle_line_color 	= (0,255,255)

		self.poly_color1	 	= (200,18,18,140)
		self.poly_sleep_color1 	= (200,200,200,70)
		self.poly_color2	 	= (230,18,18)

		self.sleep_color 		= (200,200,200)

	def setup(self):
		for segment in self.segments:
			length = distance(segment.a, segment.b)
			angle = angle_between_points(segment.a, segment.b)

			verts = [Vec2d(-length/2, segment.radius), Vec2d(length/2, segment.radius),
					 Vec2d(length/2, -segment.radius), Vec2d(-length/2, -segment.radius)]

			for vert in verts:
				vert.rotate_degrees(angle)
				vert += midpoint(segment.a, segment.b)

			points = []
			for vert in verts:
				points.append(vert[0])
				points.append(vert[1])

			res = len(points)//2
			
			segment.pyglet_debug = self.scene.debug_batch.add_indexed(res, GL_TRIANGLES, self.scene.ordered_group1,
																	  calc_index_tri(res),
									  								  ('v2f', points),
									  								  ('c3B', (110,110,110)*res))
			

		for circle in self.circles:
			points = define_circle_points(circle.radius, circle.body.position, 40)

			res = len(points)//2
			circle.res = res

			circle.pyglet_debug = self.scene.debug_batch.add_indexed(res, GL_LINES, self.scene.ordered_group1,
													  					calc_index(res),
													  					('v2f', points),
											  		  					('c3B', self.circle_color*res))
			circle.rotation_line = self.scene.debug_batch.add_indexed(2, GL_LINES, self.scene.ordered_group1,
													  				  [0,1,1,0],
													  				  ('v2f', (0,0,0,0)),
											  		  				  ('c3B', self.circle_line_color*2))
		for poly in self.polygons:
			p = poly.get_vertices()
			points = []
			for vert in p:
				points.append(vert[0])
				points.append(vert[1])

			res = len(points)//2
			poly.res = res

			# fill and outline for polygons
			poly.pyglet_debug1 = self.scene.debug_batch.add_indexed(res, GL_TRIANGLES, self.scene.ordered_group1,
													  			   calc_index_tri(res),
													  			   ('v2f', points),
											  		  			   ('c4B', self.poly_color1*res))

			poly.pyglet_debug2 = self.scene.debug_batch.add_indexed(res, GL_LINES, self.scene.ordered_group2,
													  			   calc_index(res),
													  			   ('v2f', points),
											  		  			   ('c3B', self.poly_color2*res))

	def update(self):
		# update active circles
		for circle in self.circles:
			if not circle.body.is_rogue and not circle.body.is_sleeping:
				circle.pyglet_debug.vertices = define_circle_points(circle.radius, circle.body.position, 40)
				x = circle.radius*cos(circle.body.angle) + circle.body.position[0]
				y = circle.radius*sin(circle.body.angle) + circle.body.position[1]
				circle.rotation_line.vertices = (circle.body.position[0], circle.body.position[1], x, y)

				# sleepy colors
				circle.pyglet_debug.colors = self.circle_color*circle.res
			else:
				circle.pyglet_debug.colors = self.sleep_color*circle.res

		# update active polygons
		for poly in self.polygons:
			if not poly.body.is_rogue and not poly.body.is_sleeping:
				p = poly.get_vertices()
				points = []
				for vert in p:
					points.append(vert[0])
					points.append(vert[1])
				poly.pyglet_debug1.vertices, poly.pyglet_debug2.vertices = points,points		# outline points set here 
																								# (may be intensive, i don't know)

				# sleepy colors
				poly.pyglet_debug1.colors = self.poly_color1*poly.res
				poly.pyglet_debug2.colors = self.poly_color2*poly.res 							# outline
			else:
				poly.pyglet_debug1.colors = self.poly_sleep_color1*poly.res
				poly.pyglet_debug2.colors = self.sleep_color*poly.res 							# outline
