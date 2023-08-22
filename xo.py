# Подключаю цвета для разделения игроков, лучшего ориентирования
# в интерфейсе и, в целом, для настроения
from colorama import init
from colorama import Fore, Back, Style

init()

color_1 = Fore.BLUE
color_2 = Fore.MAGENTA
success_color = Fore.GREEN
error_color = Fore.RED
attention_color = Fore.YELLOW
pale_color = Fore.LIGHTBLACK_EX
end_color = Style.RESET_ALL

cells = {}

# Размер поля. При размере больше 10 поле «едет». Эту проблему не решал
size = 3

def show_cells():
	# Выводим номера столбцов
	print()
	print(' ', end=' ')
	for i in range(size):
		print(pale_color + str(i) + end_color, end=' ')
	print()

	cells_list = list(cells.values())

	# Выводим номера строк и ячейки, а также, красим крестики
	# в цвет Игрока 1, а нолики — в цвет Игрока 2
	n = 0
	m = 0
	while n != size ** 2:
		print(pale_color + str(m) + end_color, end=' ')
		for cell in range(n, n + size):
			if cells_list[cell] == 'X':
				print(color_1 + ''.join(cells_list[cell]) + end_color,
					  end=' ')
			elif cells_list[cell] == '0':
				print(color_2 + ''.join(cells_list[cell]) + end_color,
					  end=' ')
			else:
				print(''.join(cells_list[cell]), end=' ')
		n += size
		m += 1
		print()
	print()


def ask_coords(player, char, color):
	while True:
		print(color + player + Style.RESET_ALL)
		coords = tuple(map(int, input('cтрока cтолбец: ').split()))

		# Меняем значение введённой ячейки на крестик или нолик, а также,
		# проверяем введённые значения на повторы и существование
		if coords in cells:
			if cells[coords] == '-':
				if coords in cells:
					cells[coords] = char
					break
			else:
				print(error_color + '\nЭта ячейка занята. Введите другую.\n' +
					  end_color)
		else:
			print(error_color + '\nТакой ячейки нет. Давайте ещё раз.\n' +
				  end_color)


# Проверяем поле на окончание игры. Проверку на ничью не делал.
def is_win(char):
	cells_list = list(cells.values())

	# Проверяем строки
	n = 0
	for i in range(size):
		win_seq = []
		for j in range(size):
			win_seq.append(cells_list[n])
			n += 1
		if win_seq == [char] * size:
			return True

	# Проверяем столбцы
	n = 0
	for i in range(size):
		win_seq = []
		for j in range(size):
			win_seq.append(cells_list[n])
			n += size
		if win_seq == [char] * size:
			return True
		n = 0
		n += i+1

	# Проверяем первую диагональ
	n = 0
	win_seq = []
	for i in range(size):
		win_seq.append(cells_list[n])
		n += size + 1
	if win_seq == [char] * size:
		return True

	# Проверяем вторую диагональ
	n = size - 1
	win_seq = []
	for i in range(size):
		win_seq.append(cells_list[n])
		n += size - 1
	if win_seq == [char] * size:
		return True


print(success_color + 'Игра «Хрестики-н0лики»' + end_color)
print('Выберите ячейку и введите её координаты через пробел: \n'
	  'сначала номер строки, потом номер столбца.\n' +
      attention_color + 'Пример: ' + end_color + 'cтрока столбец: 0 1')

# Генерируем первоначальное игровое поле
for row in range(size):
	for col in range(size):
		cells.update({(row, col): '-'})
show_cells()

while True:
	ask_coords('Игрок 1', 'X', color_1)
	show_cells()
	if is_win('X'):
		print(success_color + 'Игра окончена. Победил Игрок 1.')
		break

	ask_coords('Игрок 2', '0', color_2)
	show_cells()
	if is_win('0'):
		print(success_color + 'Игра окончена. Победил Игрок 2.')
		break