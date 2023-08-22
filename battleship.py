from random import randint, choice
from colorama import Fore, Style


class Color:
	def __init__(self, message):
		self.message = message

	def player(self):
		return f"{Fore.BLUE}{self.message}{Style.RESET_ALL}"

	def computer(self):
		return f"{Fore.MAGENTA}{self.message}{Style.RESET_ALL}"

	def shoten(self):
		return f"{Fore.RED}{self.message}{Style.RESET_ALL}"

	def info(self):
		return f"{Fore.GREEN}{Style.BRIGHT}{self.message}{Style.RESET_ALL}"

	def warning(self):
		return f"{Fore.YELLOW}{self.message}{Style.RESET_ALL}"

	def opacity(self):
		return f"{Fore.LIGHTBLACK_EX}{self.message}{Style.RESET_ALL}"


class Dot:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __repr__(self):
		return f"Dot({self.x}, {self.y})"


class BoardException(Exception):
	pass


class BoardOutException(BoardException):
	def __str__(self):
		return Color("Выстрелили за доску. Перестреляйте.\n").opacity()


class BoardUsedException(BoardException):
	def __str__(self):
		return Color("В эту клетку уже стреляли. Перестреляйте.\n").opacity()


class BoardWrongShipException(BoardException):
	pass


class Ship:
	def __init__(self, bow, length, o):
		self.bow = bow
		self.length = length
		self.o = o
		self.lives = length

	@property
	def dots(self):
		ship_dots = []
		for i in range(self.length):
			cur_x = self.bow.x
			cur_y = self.bow.y

			if self.o == 0:
				cur_x += i

			elif self.o == 1:
				cur_y += i

			ship_dots.append(Dot(cur_x, cur_y))

		return ship_dots

	def shoten(self, shot):
		return shot in self.dots


class Board:
	def __init__(self, hid=False, size=6):
		self.size = size
		self.hid = hid

		self.count = 0

		self.field = [[Color("•").opacity()] * size for _ in range(size)]

		self.busy = []
		self.ships = []

	def __str__(self):
		res = ""
		res += "  1 2 3 4 5 6"
		for i, row in enumerate(self.field):
			res += f"\n{chr(97 + i)} " + " ".join(row)

		if self.hid:
			res = res.replace("■", Color("•").opacity())
		return res

	def out(self, d):
		return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

	def contour(self, ship, verb=False):
		near = [
			(-1, -1), (-1, 0), (-1, 1),
			(0, -1), (0, 0), (0, 1),
			(1, -1), (1, 0), (1, 1)
		]
		for d in ship.dots:
			for dx, dy in near:
				cur = Dot(d.x + dx, d.y + dy)
				if not (self.out(cur)) and cur not in self.busy:
					if verb:
						self.field[cur.x][cur.y] = Color("✕").warning()
					self.busy.append(cur)

	def add_ship(self, ship):
		for d in ship.dots:
			if self.out(d) or d in self.busy:
				raise BoardWrongShipException()
		for d in ship.dots:
			self.field[d.x][d.y] = Color("■").player()
			self.busy.append(d)

		self.ships.append(ship)
		self.contour(ship)

	def shot(self, d):
		if self.out(d):
			raise BoardOutException()

		if d in self.busy:
			raise BoardUsedException()

		self.busy.append(d)

		for ship in self.ships:
			if d in ship.dots:
				ship.lives -= 1
				self.field[d.x][d.y] = Color("●").shoten()
				if ship.lives == 0:
					self.count += 1
					self.contour(ship, verb=True)
					print(Color("Корабль уничтожен!").shoten())
					return False
				else:
					print(Color("Корабль ранен!").shoten())
					return True

		self.field[d.x][d.y] = Color("✕").warning()
		print(Color("Мимо!").warning())
		return False

	def begin(self):
		self.busy = []


class Player:
	def __init__(self, board, enemy):
		self.board = board
		self.enemy = enemy

	def ask(self):
		raise NotImplementedError()

	def move(self):
		while True:
			try:
				target = self.ask()
				repeat = self.enemy.shot(target)
				return repeat
			except BoardException as e:
				print(e)


class AI(Player):
	def ask(self):
		d = Dot(choice("abcdef"), randint(0, 5))
		print(Color("Выстрел компьютера:").computer(), d.x, d.y + 1)

		for i in range(self.board.size):
			if d.x == chr(97 + i):
				d.x = i

		return d


class User(Player):
	def ask(self):
		while True:
			try:
				x, y = input(Color("Ваш выстрел: ").player()).split()

				if (len(x) or len(y)) != 1 or x not in "abcdef" or y not in "123456":
					print(Color("Ввели неверные координаты:").opacity())
					print(Color("сначала латинская буква от a до f,").opacity())
					print(Color("через пробел — число от 1 до 6").opacity())
					print(Color("Пример: d 2\n").opacity())
					continue

				for i in range(self.board.size):
					if x == chr(97 + i):
						x = i + 1

				x, y = int(x), int(y)

				return Dot(x - 1, y - 1)

			except ValueError:
				print(Color("Введите координаты через пробел\n").opacity())


class Game:
	def try_board(self):
		lengths = [3, 2, 2, 1, 1, 1, 1]
		board = Board(size=self.size)
		attempts = 0
		for length in lengths:
			while True:
				attempts += 1
				if attempts > 2000:
					return None
				ship = Ship(Dot(randint(0, self.size), randint(0, self.size)),
							length, randint(0, 1))
				try:
					board.add_ship(ship)
					break
				except BoardWrongShipException:
					pass
		board.begin()
		return board

	def random_board(self):
		board = None
		while board is None:
			board = self.try_board()
		return board

	def __init__(self, size=6):
		self.size = size
		pl = self.random_board()
		co = self.random_board()
		co.hid = True

		self.ai = AI(co, pl)
		self.us = User(pl, co)

	@staticmethod
	def greet():
		print(Color("И Г Р А   « М О Р С К О Й   Б О Й »\n").info())
		print("Чтобы выстрелить, введите координаты клетки через пробел: ")
		print("сначала латинская буква от a до f, потом число от 1 до 6")
		print(Color("Пример: d 2\n").warning())

	def loop(self):
		num = 0
		i = 1
		print("Ваша доска:")
		print(self.us.board)
		print()
		print("Доска компьютера:")
		print(self.ai.board)
		print()
		print("-" * 16)
		print()
		while True:
			if num % 2 == 0:
				print(Color(f"★★★ ХОД {i} ★★★\n").info())
				print(self.ai.board)
				print()
				repeat = self.us.move()
				print()
				i += 1
			else:
				repeat = self.ai.move()
				print(self.us.board)
				print()
			if repeat:
				num -= 1

			if self.ai.board.count == 7:
				print()
				print(Color("★ ★ ★ ★ ★ Вы победили! ★ ★ ★ ★ ★").info())
				break

			if self.us.board.count == 7:
				print()
				print(Color("Вы проиграли :(").shoten())
				break
			num += 1

	def start(self):
		self.greet()
		self.loop()


g = Game()
g.start()
