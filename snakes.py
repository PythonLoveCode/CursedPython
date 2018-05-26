#!/usr/bin/python3
# Created by PythonLove.com and Jean Paul

import curses
import time
import random

class Snake():
	x = 5
	y = 15
	snake_matrix = []
	current_head_position = []
	score = 0
	obstacles = []
	lives = 3
	game_on = False

	def __init__(self, scr):

		curses.curs_set(0) # hide the cursor so it doesn't distract us from the game

		self.scr = scr
		max_y, max_x = self.scr.getmaxyx()

		self.max_y = max_y - 1
		self.max_x = max_x - 1


	def start(self):

		message = """

			====== Cursed Python ======

	The Python has been cursed. 
	The snake has to look for food for all eternity. But... 
	any time it eats a good food, poisonous fruits appear.
	If it eats three (3) bad foods, the Cursed Python dies.

			@ = good food (eat these!)
			* = bad food  (DON'T eat these!)

	Use arrow keys to control the Python. Press Ctrl + C to quit.


			(Press any key to continue...)
		"""

		self.scr.clear()
		self.scr.nodelay(False)
		
		self.scr.addstr(3, 3, message)
		self.scr.refresh()

		self.scr.getkey()
		
		self.game_on = True
		self.scr.nodelay(True)

		self.scr.clear()
		
		self.update_score()
		self.show_lives()
		self.init_snake()
		self.place_food()

		self.move()
		self.game_over()


	def random_position(self):
		position_generated = False

		while position_generated == False:
			rand_y = random.randint(2, self.max_y - 2)
			rand_x = random.randint(2, self.max_x - 2)

			if [rand_y, rand_x] not in self.snake_matrix:
				position_generated = True

		return [rand_y, rand_x]

	def place_food(self):

		food_position = self.random_position()

		self.food_y = food_position[0]
		self.food_x = food_position[1]

		curses.init_pair(1, curses.COLOR_RED, 236)

		self.scr.addstr(self.food_y, self.food_x, "@", curses.color_pair(1))
		self.scr.refresh()


	def init_snake(self):
		self.snake_matrix = [[self.y, self.x + 1], [self.y, self.x + 2], [self.y, self.x + 3], [self.y, self.x + 4], [self.y, self.x + 5], [self.y, self.x + 6], [self.y, self.x + 7] ]
		

	def update_score(self):
		self.scr.addstr(0,2, "Score: " + str(self.score) + "     ")

	def draw_snake(self):
		_extend = False

		if self.y == self.food_y and self.x == self.food_x:
			#self.scr.addstr(self.y, self.x, "o")
			# let's extend the snake
			_extend = True 
			self.score += 10
			self.update_score()
			self.place_food()

		tail_end = self.snake_matrix[0]

		if _extend:
			# instead of earasing the tail we will add another piece
			self.scr.addstr(tail_end[0], tail_end[1], "o")
			self.create_obstacle()


		#delete snake end from matrix
		if _extend == False:
			self.scr.addstr(tail_end[0], tail_end[1], " ")
			self.snake_matrix.pop(0)
			

		self.scr.addstr(self.y, self.x, "o")
		self.snake_matrix.append( [self.y, self.x] )		

		self.scr.refresh()

		

	def create_obstacle(self):

		obstacle_number = random.randint(0, 2)

		while obstacle_number > 0:
			obstacle_position = self.random_position()
			self.scr.addstr(obstacle_position[0], obstacle_position[1], "*")
			self.obstacles.append(obstacle_position)
			obstacle_number -= 1

	
	def obstacle_collided(self):
		if [self.y, self.x] in self.obstacles:
			# remove the obstacle from obstacles list
			self.obstacles.remove([self.y, self.x])
			curses.beep()

			return True
		else:
			return False



	def move(self):

		
		


		next_direction = "right"
		current_direction_key = 261 # right
		while self.game_on:

			key = self.scr.getch()

			key_gotten = str(str(key))
			

			directions = {259: "up", 258: "down", 260: "left",
			261: "right"}

			if key in directions:

				if key != current_direction_key:

					if key == 258 and next_direction == "up":
						current_direction_key = 259

					elif key == 259 and next_direction == "down":
						current_direction_key = 258

					elif key == 260 and next_direction == "right":
						current_direction_key = 261

					elif key == 261 and next_direction == "left":
						current_direction_key = 260

					else:
						current_direction_key = key

					next_direction = directions[current_direction_key]


			self.direction(next_direction)
			self.draw_snake()
			if self.obstacle_collided():
				self.check_lives()
				
			curses.napms(100)
		
		self.scr.clear()

		self.game_over()

	def check_lives(self):
		self.lives -= 1

		if self.lives <= 0:
			self.game_on = False
			pass

		self.show_lives()

	def show_lives(self):
		self.scr.addstr(0, 20, "Lives: " + str(self.lives))


	def game_over(self):
		self.scr.clear()
		self.scr.nodelay(False)
		#self.game_on = False
		# while True:
		self.scr.addstr(5, 10, "*****************Game Over*********************")
		self.scr.addstr(7, 10, "Your Final Score: " + str(self.score))
		self.scr.addstr(9, 10, "       ( Press any key to exit. )")
		self.scr.refresh()
		self.scr.getkey()

	def direction(self, _direction):

		self._direction = _direction

		if _direction == "right":
			# right edge

			if self.x + 1 >= self.max_x:
				self.x = 1
			else:
				self.x += 1
		elif _direction == "up":
			#top edge

			if self.y -1 <= 0:
				self.y = self.max_y - 1
			else:
				self.y -= 1

		elif _direction == "down":
			# bottom edge

			if self.y + 1 >= self.max_y:
				self.y = 1
			else:
				self.y += 1
		elif _direction == "left":
			# left edge

			if self.x - 2 <= 0:
				self.x = self.max_x - 2
			else:
				self.x -= 1


def snakes_init(scr):

	snake = Snake(scr)
	snake.start()


curses.wrapper(snakes_init)