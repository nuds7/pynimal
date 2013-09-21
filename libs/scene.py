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

import camera

#pyglet.resource.path = ['']
#pyglet.resource.reindex()

import pyglet_util

def clear_space(space):
	for c in space.constraints:
		space.remove(c)
	for s in space.shapes:
		space.remove(s)
	for b in space.bodies:
		space.remove(b)
		
class Scene(object):
	def __init__(self, screen_resolution):
		pass
	def update(self, dt):
		raise NotImplementedError
	def update_half(self, dt):
		raise NotImplementedError
	def update_third(self, dt):
		raise NotImplementedError
	def world_pos(self, x, y):
		raise NotImplementedError
	def keyboard_input(self, dt):
		raise NotImplementedError
	def on_key_press(self, symbol, modifiers):
		raise NotImplementedError
	def on_key_release(self, symbol, modifiers):
		raise NotImplementedError
	def on_mouse_press(self, x, y, button, modifierse):
		raise NotImplementedError
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		raise NotImplementedError
	def on_mouse_release(self, x, y, button, modifiers):
		raise NotImplementedError
	def on_mouse_motion(self, x, y, dx, dy):
		raise NotImplementedError
	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		raise NotImplementedError

class Pymunk_Scene(Scene):
	def __init__(self, screen_resolution):
		super(Pymunk_Scene, self).__init__(screen_resolution)
		self.screen_resolution 	= screen_resolution

		self.debug_batch 		= pyglet.graphics.Batch()
		self.normal_batch 		= pyglet.graphics.Batch()
		self.ui_batch 			= pyglet.graphics.Batch()

		# The common_group parent keeps groups from 
		# overlapping on accident. Silly Pyglet!
		common_group 			= pyglet.graphics.OrderedGroup(1) 
		self.ordered_group10	= pyglet.graphics.OrderedGroup(10, 	parent = common_group)
		self.ordered_group9 	= pyglet.graphics.OrderedGroup(9, 	parent = common_group)
		self.ordered_group8 	= pyglet.graphics.OrderedGroup(8, 	parent = common_group)
		self.ordered_group7		= pyglet.graphics.OrderedGroup(7, 	parent = common_group)
		self.ordered_group6		= pyglet.graphics.OrderedGroup(6, 	parent = common_group)
		self.ordered_group5		= pyglet.graphics.OrderedGroup(5, 	parent = common_group)
		self.ordered_group4		= pyglet.graphics.OrderedGroup(4, 	parent = common_group)
		self.ordered_group3 	= pyglet.graphics.OrderedGroup(3,	parent = common_group)
		self.ordered_group2		= pyglet.graphics.OrderedGroup(2, 	parent = common_group)
		self.ordered_group1		= pyglet.graphics.OrderedGroup(1, 	parent = common_group)

		self.space 						= pymunk.Space()
		self.space.sleep_time_threshold = 1
		self.space.gravity 				= (0,-800)

		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glEnable(GL_LINE_SMOOTH)
		glPointSize(4)
		glLineWidth(1)

		self.map_size = [1920,1080]
		self.camera = camera.Camera(self.screen_resolution, 
									self.map_size, [0,0])

		#### Test Junk ####

		segs = (pymunk.Segment(self.space.static_body, (-200,0), (200,0), 		3),
				pymunk.Segment(self.space.static_body, (-200,0), (-200,100), 	3),
				pymunk.Segment(self.space.static_body, (200,0),  (200,100), 	3),
				pymunk.Segment(self.space.static_body, (-180,20), (100,0), 	3),)
		for seg in segs:
			seg.friction = .8
		self.space.add(segs)

		radius = 15
		circle_moment = pymunk.moment_for_circle(.01, 0, radius)
		for i in range(10):
			circle_body = pymunk.Body(.01, circle_moment)
			circle_body.position = 0,100
			circle_shape = pymunk.Circle(circle_body, radius)
			circle_shape.friction = .3
			self.space.add(circle_body, circle_shape)

		size = (30,20)
		box_moment = pymunk.moment_for_box(.01, size[0], size[1])
		for i in range(5):
			box_body = pymunk.Body(.01, box_moment)
			box_body.position = 80,300
			box_shape = pymunk.Poly.create_box(box_body, size=size)
			box_shape.friction = .3
			self.space.add(box_body, box_shape)

		vertices = [(0,16),(18,-16),(-18,-16)]
		for i in range(5):
			poly_moment = pymunk.moment_for_poly(.01, vertices)
			poly_body = pymunk.Body(.01, poly_moment)
			poly_body.position = (-50,100)
			poly_shape = pymunk.Poly(poly_body, vertices)
			poly_shape.friction = .5
			self.space.add(poly_body, poly_shape)
		#### Test Junk ####

		self.pymunk_util = pyglet_util.PymunkUtil2(self)
		self.pymunk_util.setup()

		self.keys_held = []

	def update(self, dt):
		self.space.step(.015)
		self.pymunk_util.update()

	def update_half(self, dt):
		#self.pymunk_util.update()
		pass
		
	def update_third(self, dt):
		pass

	def draw(self):
		self.camera.update([self.map_size[0]//2,self.map_size[1]//2], 0)
		self.normal_batch.draw()
		self.debug_batch.draw()
		self.camera.ui_mode()
		self.ui_batch.draw()

	def world_pos(self, x, y):
		# Depends on the position of the camera.
		pass
	def keyboard_input(self, dt):
		pass
	def on_key_press(self, symbol, modifiers):
		pass
	def on_key_release(self, symbol, modifiers):
		pass
	def on_mouse_press(self, x, y, button, modifierse):
		pass
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		pass
	def on_mouse_release(self, x, y, button, modifiers):
		pass
	def on_mouse_motion(self, x, y, dx, dy):
		pass
	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		pass

class SceneManager(object):
	def __init__(self, screen_resolution):
		self.go_to(Pymunk_Scene(screen_resolution))
	def go_to(self, scene):
		self.scene = scene
		self.scene.manager = self