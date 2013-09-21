import os, sys
import pyglet
from pyglet.gl import *
lib_path = os.path.abspath('libs/')
sys.path.append(lib_path)
import scene
pyglet.resource.path = ['resources']
pyglet.resource.reindex()

print("AVBin: "+str(pyglet.media.have_avbin))

class Window(pyglet.window.Window):
	def __init__(self, *args, **kwargs):
		super(Window, self).__init__(*args, **kwargs)
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

		self.overlay_batch = pyglet.graphics.Batch()
		self.ver_label = pyglet.text.Label(text = 'Pyglet + Pymunk',
										   font_name = 'Calibri', font_size = 8, bold = True,
										   x = self.width, y = self.height,
										   anchor_x = 'right', anchor_y = 'top',
										   color = (255,255,255,200),
										   batch = self.overlay_batch)
		self.ver_label.set_style('background_color', (0,0,0,80))
		self.overlay_batch.draw()

		self.fps_display = pyglet.window.FPSDisplay(self)
		self.fps_display.label.x, self.fps_display.label.y = self.width, self.height-13
		self.fps_display.label.anchor_x, self.fps_display.label.anchor_y = 'right', 'top'
		self.fps_display.label.font_name 	= 'Calibri'
		self.fps_display.label.font_size 	= 8
		self.fps_display.label.bold 		= True
		self.fps_display.label.color 		= (5,245,120,255)
		self.fps_display.label.set_style('background_color', (0,0,0,80))

		self.manager = scene.SceneManager((self.width, self.height))
		self.keys_held = []

		pyglet.clock.schedule_interval(self.dummy_update, 	1/500.0)
		pyglet.clock.schedule_interval(self.update, 		1/60.0)
		pyglet.clock.schedule_interval(self.update_half, 	1/30.0)
		pyglet.clock.schedule_interval(self.update_third, 	1/20.0)

	def dummy_update(self, dt):
		pass
	def update(self, dt):
		self.manager.scene.update(dt)
	def update_half(self, dt):
		self.manager.scene.update_half(dt)
	def update_third(self, dt):
		self.manager.scene.keys_held = self.keys_held
		self.manager.scene.update_third(dt)

	def on_draw(self):
		self.clear()
		self.manager.scene.draw()
		self.overlay_batch.draw()
		self.fps_display.draw()

	def on_key_press(self, symbol, modifiers):
		self.keys_held.append(symbol)
	def on_key_release(self, symbol, modifiers):
		self.keys_held.pop(self.keys_held.index(symbol))
	def on_mouse_press(self, x, y, button, modifiers):
		self.manager.scene.on_mouse_press(x, y, button, modifiers)
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.manager.scene.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
	def on_mouse_release(self, x, y, button, modifiers):
		self.manager.scene.on_mouse_release(x, y, button, modifiers)
	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		self.manager.scene.on_mouse_scroll(x, y, scroll_x, scroll_y)
	def on_mouse_motion(self, x, y, dx, dy):
		self.manager.scene.on_mouse_motion(x, y, dx, dy)
	
if __name__ == '__main__':
	window = Window(1280, 720, # 960, 540
					caption 	= 'Pyglet + Pymunk', 
					fullscreen 	= False,
					vsync 		= False) 
	pyglet.app.run()