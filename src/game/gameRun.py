import pygame
import importlib
import random
from src.engine import (
	hue,
	draw,
	topdownscreen
)
assets = importlib.import_module('assets.asset-manager')
pygame.init()

colors = [None, 0, 30, 70, 130, 170, 230, 270]

def collidelist(pos, objlist):
	for obj in objlist:
		if obj == pos:
			return False
	return True

def ifhas(pos, direction, list):
	newpos = (pos[0] + direction[0], pos[1] + direction[1])
	for obj in list:
		if obj.pos == newpos:
			return obj
	return True

def collide(pos, obj):
	if obj == pos:
		return False
	return True

class Level:
	def __init__(self, start, win, walls):
		self.walls = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),
(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),
(1,8),(2,8),(3,8),(4,8),(5,8),(6,8),(7,8),(8,8),(9,8),
(10,1),(10,2),(10,3),(10,4),(10,5),(10,6),(10,7),(10,8)]
		self.start = start
		self.win = win
		self.boxes = []
		self.doors = []
		self.conveyors = []
		self.buttons = []
		self.passes = []
		self.painters = []
		self.teleporters = []
		self.activators = []
		self.paintpasses = []
		self.activatables = []
		for block in walls:
			self.walls.append(block)
	def special(self, specials):
		speclist = []
		for e in specials:
			speclist.append(e.copy())
		self.specials = speclist

		for spec in specials:
			if isinstance(spec, Door):
				self.doors.append(spec)
			if isinstance(spec, Box):
				self.boxes.append(spec)
			if isinstance(spec, Button):
				self.buttons.append(spec)
			if isinstance(spec, Conveyor):
				self.conveyors.append(spec)
			if isinstance(spec, PassThrough):
				self.passes.append(spec)
			if isinstance(spec, Teleporter):
				self.teleporters.append(spec)
			if isinstance(spec, Painter):
				self.painters.append(spec)
			if isinstance(spec, PaintPass):
				self.paintpasses.append(spec)
		self.activators = [self.buttons]
		self.activatables = [self.doors, self.conveyors, self.teleporters]
		self.checkables = [self.buttons, self.boxes, self.painters]
	def reset(self):
		self.boxes = []
		self.doors = []
		self.conveyors = []
		self.buttons = []
		self.passes = []
		self.teleporters = []
		self.activators = []
		self.paintpasses = []
		self.activatables = []
		self.special(self.specials)

class Player:
	def __init__(self):
		self.x = 1
		self.y = 1
		self.level = 0
		self.color = False
	def goto(self, pos):
		self.x = pos[0]
		self.y = pos[1]
		self.checklessmovement((0,0))
	def move(self, key):
		self.direction = (0, 0)
		if key == pygame.K_w:
			if (self.y - 1) >= 0:
				self.direction = (0, -1)

		if key == pygame.K_a:
			if (self.x - 1) >= 0:
				self.direction = (-1, 0)

		if key == pygame.K_s:
			if (self.y + 1) <= 8:
				self.direction = (0, 1)
				
		if key == pygame.K_d:
			if (self.x + 1) <= 10:
				self.direction = (1, 0)

		if key == pygame.K_m:
			levels[self.level].boxes.append(Box(self.x,self.y))
		
		if key == pygame.K_r:
			levels[self.level].reset()
			self.color = False
			self.x = levels[self.level].start[0]
			self.y = levels[self.level].start[1]
			return

		self.movement(self.direction)

		print((self.x,self.y))


		if not collide((self.x, self.y), levels[self.level].win):
			if self.level + 1 == 6:
				self.level = -1
			self.level += 1
			self.color = False
			self.x = levels[self.level].start[0]
			self.y = levels[self.level].start[1]
		if key == pygame.K_p:
			if self.level + 1 == 6:
				self.level = -1
			self.color = False
			self.level += 1
			self.x = levels[self.level].start[0]
			self.y = levels[self.level].start[1]
	def movement(self, direction):
		box = ifhas((self.x, self.y), direction, levels[self.level].boxes)
		door = ifhas((self.x, self.y), direction, levels[self.level].doors)
		paintpass = ifhas((self.x,self.y),direction,levels[self.level].paintpasses)
		if not door == True:
			if door.state == False:
				return
		if not box == True:
			if not direction == (0,0):
				box.move(direction)
		if collidelist((self.x + direction[0], self.y + direction[1]), levels[self.level].walls):
			if ifhas((self.x,self.y),direction,levels[self.level].boxes) == True:
				if not paintpass == True:
					if paintpass.id == self.color:
						pass
					else:
						return
				self.x = self.x + direction[0]
				self.y = self.y + direction[1]

		for belt in levels[self.level].conveyors:
			if belt.pos == (self.x, self.y):
				if belt.state:
					print(belt.direction)
					self.checklessmovement(belt.direction)
					return

		for tp in levels[self.level].teleporters:
			if tp.check() == True:
				break
		for lists in levels[self.level].checkables:
			for acti in lists:
				acti.check()
	def checklessmovement(self, direction):
		box = ifhas((self.x, self.y), direction, levels[level].boxes)
		door = ifhas((self.x, self.y), direction, levels[level].doors)
		if not door == True:
			if door.state == False:
				return
		if not box == True:
			if not direction == (0,0):
				box.move(direction)
		if collidelist((self.x + direction[0], self.y + direction[1]), levels[level].walls):
			if ifhas((self.x,self.y),direction,levels[level].boxes) == True:
				self.x = self.x + direction[0]
				self.y = self.y + direction[1]
	def paint(self, id):
		self.color = id

char = Player()

class PaintPass:
	def __init__(self,x,y,id):
		self.pos = (x,y)
		self.id = id
		self.starter = [x,y,id]
	def copy(self):
		return PaintPass(self.starter[0],self.starter[1],self.starter[2])

class Painter:
	def __init__(self,x,y,id):
		self.pos = (x,y)
		self.id = id
		self.starter = [x,y,id]
	def check(self):
		if self.pos == (char.x,char.y):
			char.paint(self.id)
	def copy(self):
		return Painter(self.starter[0],self.starter[1],self.starter[2])

class Conveyor:
	def __init__(self, x, y, direction, id):
		self.pos = (x, y)
		self.direction = direction
		self.id = id
		self.state = True
		self.starter = (x,y,direction,id)
	def changestate(self, state):
		self.state = not state
	def copy(self):
		return Conveyor(self.starter[0],self.starter[1],self.starter[2],self.starter[3])

class Teleporter:
	def __init__(self,x,y,id,ways,type):
		self.pos = (x,y)
		self.id = id
		self.type = type
		if type == 0: 
			self.state = False 
		else: 
			self.state = True
		self.ways = ways
		self.starter = (x,y,id,ways,type)
	def telepos(self):
		for tele in levels[char.level].teleporters:
			if tele.id == self.id:
				if tele.pos == self.pos:
					continue
				return tele.pos
	def check(self):
		if self.ways == 0:
			return
		if self.pos == (char.x, char.y):
			if self.state == True:
				char.goto(self.telepos())
				return True
	def changestate(self,state):
		if self.type == 0:
			self.state = state
		if self.type == 1:
			self.state = not state
	def copy(self):
		return Teleporter(self.starter[0],self.starter[1],self.starter[2],self.starter[3],self.starter[4])

class Box:
	def __init__(self, x, y):
			self.pos = (x, y)
			self.starter = (x,y)
	def move(self, direction):
		belt = ifhas(self.pos, (0,0), levels[char.level].conveyors)
		frontbox = ifhas(self.pos, direction, levels[char.level].boxes)
		newpos = (self.pos[0] + direction[0], self.pos[1] + direction[1])
		if frontbox == True:
			if collidelist(newpos,levels[char.level].walls):
				door = ifhas(self.pos, direction, levels[char.level].doors)
				if not door == True:
					if door.state == False:
						return
				passthrough = ifhas(self.pos, direction, levels[char.level].passes)
				if not passthrough == True:
					return
						
				self.pos = newpos
		else:
			frontbox.move(direction)
			frontbox2 = ifhas(self.pos, direction, levels[char.level].boxes)
			if not frontbox2 == True:
				return
			if collidelist(newpos,levels[char.level].walls):
				self.pos = newpos
	def check(self):
		belt = ifhas(self.pos, (0,0), levels[char.level].conveyors)
		if not belt == True:
			if belt.state == False:
				return
			direction = belt.direction
			frontbox = ifhas(self.pos, direction, levels[char.level].boxes)
			newpos = (self.pos[0] + direction[0], self.pos[1] + direction[1])
			if frontbox == True:
				if collidelist(newpos,levels[char.level].walls):
					door = ifhas(self.pos, direction, levels[char.level].doors)
					passthrough = ifhas(self.pos, direction, levels[char.level].passes)
					if not passthrough == True:
						return
					if not door == True:
						if door.state == False:
							return
					self.pos = newpos
			else:
				frontbox.move(direction)
				frontbox2 = ifhas(self.pos, direction, levels[char.level].boxes)
				if not frontbox2 == True:
					return
				if collidelist(newpos,levels[char.level].walls):
					self.pos = newpos
	def copy(self):
		return Box(self.starter[0],self.starter[1])
			
class Button:
	def __init__(self, x, y, id):
		self.pos = (x,y)
		self.id = id
		self.state = False
		self.color = colors[id]
		self.starter = (x,y,id)
	def check(self):
		if not ifhas(self.pos,(0,0),levels[char.level].boxes) == True or (char.x, char.y) == self.pos:
			self.state = True
		else:
			self.state = False
		for able in levels[char.level].activatables:
			for item in able:
				if item.id == self.id:
					item.changestate(self.state)
	def copy(self):
		return Button(self.starter[0],self.starter[1],self.starter[2])

class PassThrough:
	def __init__(self,x,y):
		self.pos = (x,y)
		self.starter = (x,y)
	def copy(self):
		return PassThrough(self.starter[0],self.starter[1])

class Door:
	def __init__(self, x, y, rot, id):
		self.pos = (x,y)
		self.rot = rot
		self.id = id
		self.state = False
		self.color = colors[id]
		self.starter = (x,y,rot,id)
	def changestate(self, state):
		self.state = state
	def copy(self):
		return Door(self.starter[0], self.starter[1], self.starter[2], self.starter[3])

level = 0
levels = [
Level((1,1), (9,7), [(8,6),(8,7)]), 
Level((1,4), (5,4), [(6,4),(5,5),(5,3),(6,5),(6,3)]), 
Level((1,4), (9,7), [(6,3),(4,3),(4,5),(4,6),(8,6),(6,5),(4,1),(4,2),(6,6),(6,7),(6,2),(6,1)]),
Level((1,4), (9,4), [(8,3),(8,5),(9,5),(9,3),(8,6),(7,6),(6,6),(5,6),(4,6),(3,6),(8,2),(8,1),(3,5),(3,3),(3,2),(3,1)]),
Level((1,4), (9,4), [(8,3),(8,5),(5,6),(6,6),(7,6),(7,7)]),
Level((1,4), (9,4), [(9,1),(9,2),(9,3)])
]
levels[0].special([Box(4,3),Box(5,3)])
levels[1].special([Box(4,4)])
levels[2].special([Door(6,4,1,5),Button(5,2,5),Door(5,3,2,1),Door(8,7,1,5),Door(9,6,2,5),Box(3,5),Button(5,4,1),Door(4,4,1,2),Button(3,4,2),Button(5,6,3),Door(5,5,2,3),Door(4,7,1,1)])
levels[3].special([Door(3,4,1,2),Button(9,7,3),Box(2,3),Box(5,4),Button(8,7,2), Conveyor(7,7,(1,0),1),Conveyor(6,7,(1,0),1),Conveyor(5,7,(1,0),1),Conveyor(4,7,(1,0),1),Conveyor(3,7,(1,0),1),Conveyor(2,7,(1,0),1),Conveyor(1,7,(1,0),1),Conveyor(2,7,(1,0),1),Conveyor(8,4,(-1,0),3)])
levels[4].special([
Box(2,4),PassThrough(4,4),PassThrough(4,6),PassThrough(4,5),PassThrough(4,3),PassThrough(4,2),PassThrough(4,1),Teleporter(1,1,1,0,1),Teleporter(2,1,2,0,1),
Teleporter(9,3,2,1,1),Teleporter(3,1,3,0,1),Teleporter(9,5,3,1,1),
Teleporter(8,4,1,1,1),Button(6,7,1),Conveyor(4,7,(1,0),4),Conveyor(5,7,(1,0),4)
])
levels[5].special([
Painter(2,4,1),Painter(3,4,2),Painter(4,4,3),Painter(5,4,4),Painter(6,4,5),Painter(7,4,6),Painter(8,4,7),
PaintPass(1,1,0),PaintPass(2,1,1),PaintPass(3,1,2),PaintPass(4,1,3),PaintPass(5,1,4),PaintPass(6,1,5),PaintPass(7,1,6),PaintPass(8,1,7),
PaintPass(1,2,0),PaintPass(2,2,1),PaintPass(3,2,2),PaintPass(4,2,3),PaintPass(5,2,4),PaintPass(6,2,5),PaintPass(7,2,6),PaintPass(8,2,7),
PaintPass(1,3,0),PaintPass(2,3,1),PaintPass(3,3,2),PaintPass(4,3,3),PaintPass(5,3,4),PaintPass(6,3,5),PaintPass(7,3,6),PaintPass(8,3,7),
Painter(1,4,0),
])

def gameRun():
	# main game loop
	running = True
	paused = False
	pausescreen = pygame.Surface((704,576))
	screen = topdownscreen(11,9,64)
	pygame.mixer.music.load(assets.crazy)
	pygame.mixer.music.play(-1)
	while running:
		level = char.level
		for event in pygame.event.get():
				# only do something if the event is of type QUIT
				if event.type == pygame.QUIT:
					# change the value to False, to exit the main loop
					running = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						paused = not paused
					if not paused:
						char.move(event.key)
		screen.fill((255,255,255))
		
		for x in range(0, 11):
			for y in range(0, 9):
				draw(screen, assets.floor, (x,y))
		draw(screen, assets.portal, levels[level].win)
		for door in levels[level].doors:
			if door.state == False:
				if door.rot == 1:
					draw(screen, assets.door1, door.pos)
				if door.rot == 2:
					draw(screen, assets.door2, door.pos)
				draw(screen, hue(assets.door_color, door.color), door.pos)
		for btn in levels[level].buttons:
			draw(screen, hue(assets.off, btn.color), btn.pos)
		for belt in levels[level].conveyors:
			if belt.direction == (1, 0):
				draw(screen, hue(assets.conveyor, colors[belt.id]), belt.pos)
			if belt.direction == (0, -1):
				draw(screen, hue(pygame.transform.rotate(assets.conveyor, 90), colors[belt.id]), belt.pos)
			if belt.direction == (-1, 0):
				draw(screen, hue(pygame.transform.rotate(assets.conveyor, 180), colors[belt.id]), belt.pos)
			if belt.direction == (0, 1):
				draw(screen, hue(pygame.transform.rotate(assets.conveyor, -90), colors[belt.id]), belt.pos)
		
		for tp in levels[level].teleporters:
			if tp.state == True:
				draw(screen, hue(assets.teleporter, colors[tp.id]), tp.pos)
			if tp.state == False:
				draw(screen, assets.teleporter, tp.pos)

		for painter in levels[level].painters:
			if not painter.id == 0:
				draw(screen, hue(assets.painter, colors[painter.id]), painter.pos)
			else:
				draw(screen, assets.painter, painter.pos)

		if not char.color:
			screen.blit(pygame.transform.scale(assets.char, (64,64)), (char.x * 64,char.y * 64))
		else:
			draw(screen, hue(assets.huechar, colors[char.color]), (char.x, char.y))
			draw(screen, assets.charface, (char.x, char.y))

		for paintpass in levels[level].paintpasses:
			if not paintpass.id == 0:
				draw(screen, hue(assets.paintpass, colors[paintpass.id]), paintpass.pos)
			else:
				draw(screen, assets.paintpass, paintpass.pos)

		# draw(screen, assets.charface, (char.x,char.y))
		for pos in levels[level].walls:
			draw(screen, assets.wall, pos)
		
		for box in levels[level].boxes:
			draw(screen, assets.box, box.pos)
		
		for passthrough in levels[level].passes:
			draw(screen, assets.passthrough, passthrough.pos)
			
		if paused:
			pausescreen.set_alpha(128)
			pausescreen.fill((10,10,10))
			screen.blit(pausescreen, (0,0))
			pausedtext = assets.gameboy.render('Paused', True, (255,255,255))
			screen.blit(pausedtext, (64 * 3 + 16,64))
		
		pygame.display.flip()