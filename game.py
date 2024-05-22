import pygame as p
import copy
import math
import random


# класс кнопок
class button:
    def __init__(self, color, x, y, width, height, text=""):
        # цвет RGB (0-255, 0-255, 0-255)
        self.color = color
        # координаты
        self.x = x
        self.y = y
        # ширина
        self.width = width
        # высота
        self.height = height
        # текст
        self.text = text

    def draw(self, win, outline=None):
        # если с контуром, отрисовка происходит по другому
        if outline:
            p.draw.rect(
                win,
                outline,
                (self.x - 2, self.y - 2, self.width + 4, self.height + 4),
                0,
            )
        p.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text != "":
            font = p.font.SysFont("ebrima", self.width - 70)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(
                text,
                (
                    self.x + (self.width / 2 - text.get_width() / 2),
                    self.y + (self.height / 2 - text.get_height() / 2),
                ),
            )

    # проверка на позицию мыши над кнопкой
    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


# класс игры - жизнь
class conways_life:
    def __init__(self):
        # инициализация окна
        p.init()
        # задание название окна
        p.display.set_caption("Игра 'Жизнь'")
        # задание размеров окна
        self.screen = p.display.set_mode((500, 670))
        # буфер в котором определяется жива клетка или нет (0 мертва, 1 жива)
        self.data = [[0 for j in range(50)] for i in range(50)]
        # переменная отвечающая за запуск программы
        self.run = True
        # переменная времени
        self.clock = p.time.Clock()
        # запуск игры
        self.start = False
        # переменная инициализации
        self.initial = True
        # кнопка очистки
        self.resetButton = button((255, 255, 255), 33, 553, 95, 75, "Reset")
        # кнопка запуска
        self.startButton = button((255, 255, 255), 203, 553, 95, 75, "Start")
        # кнопка случайного расположения
        self.randomButton = button((255, 255, 255), 373, 553, 95, 75, "Random")

    def getData(self):
        return self.data

    # функция поиска соседей
    def get_neighbour(self, i, j):
        neighbour = [
            [i + 1, j],
            [i - 1, j],
            [i, j + 1],
            [i, j - 1],
            [i + 1, j + 1],
            [i - 1, j + 1],
            [i + 1, j - 1],
            [i - 1, j - 1],
        ]
        neighbour = [i for i in neighbour if 0 <= i[0] < 50 and 0 <= i[1] < 50]
        return neighbour

    # функция новой эволюции клетки
    def next_generation(self):
        # возвращаем прошлую версию массива
        self.last_generation = copy.deepcopy(self.data)
        # проходимся по массиву
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                # ищем количество соседних клеток
                self.count = [
                    self.last_generation[k[0]][k[1]] for k in self.get_neighbour(i, j)
                ].count(1)
                # в зависимости от количества соседних, оживляем
                if self.last_generation[i][j] == 1:
                    self.data[i][j] = 1 if self.count in range(2, 4) else 0
                elif self.last_generation[i][j] == 0:
                    self.data[i][j] = 1 if self.count == 3 else 0

    # обновление окна
    def update(self):
        # закрашивание окна белым
        self.screen.fill((255, 255, 255))
        # Рисуем сетку
        for i in range(0, self.screen.get_height() // 10):
            p.draw.line(
                self.screen, (0, 0, 0), (0, i * 10), (self.screen.get_width(), i * 10)
            )
        for j in range(0, self.screen.get_width() // 10):
            p.draw.line(
                self.screen, (0, 0, 0), (j * 10, 0), (j * 10, self.screen.get_height())
            )
        # установка кнопок
        self.resetButton.draw(self.screen, (0, 0, 0))
        self.startButton.draw(self.screen, (0, 0, 0))
        self.randomButton.draw(self.screen, (0, 0, 0))
        # вывод клеток
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j] == 1:
                    p.draw.rect(self.screen, (0, 0, 0), (j * 10, i * 10, 10, 10))

    # функция действий пользователя - расстановка клеток и удаление
    def user_initial(self):
        if self.initial:
            x, y = p.mouse.get_pos()
            # до 500 по Y расположено окно игры
            if y < 500:
                if p.mouse.get_pressed()[0]:
                    self.data[math.floor(y / 10)][math.floor(x / 10)] = 1
                if p.mouse.get_pressed()[2]:
                    self.data[math.floor(y / 10)][math.floor(x / 10)] = 0
            self.clock.tick(60)

    # функция запуска
    def start_game(self):
        while self.run:
            # обработка событий окна
            for event in p.event.get():
                # получение координат мыши ока
                pos = p.mouse.get_pos()
                # если нажата кнопка
                if event.type == p.MOUSEBUTTONDOWN:
                    # если координаты мыши совпадают с координатами кнопки, то происходят соответствующие действия
                    # Нажата Reset
                    if self.resetButton.isOver(pos):
                        # передаем новый массив с нулям
                        self.data = [[0 for j in range(50)] for i in range(50)]
                        # выводим в консоль для отслеживания действий
                        print("очистка поля")
                        # указываем что игра завершена в этот момент
                        self.start = False
                        # указываем что пользователь может расставлять клетки, эта переменная активирует действия в функции сверху
                        self.initial = True
                    # Нажата Start
                    if self.startButton.isOver(pos):
                        # если запуск уже произведен, т.е. значение self.start = true, то меняем значение на false, иначе true
                        if self.start:
                            self.start = False
                            self.initial = True
                        else:
                            self.start = True
                            self.initial = False
                        # вывод в консоль переменной для отслеживания действий той самой self.start
                        print(self.start)
                    # Нажат Random
                    if self.randomButton.isOver(pos):
                        # заполнение буфера в котором клетки случайными цифрами 0 или 1
                        for i in range(len(self.data)):
                            for j in range(len(self.data[i])):
                                self.data[i][j] = random.randint(0, 1)
                        print("Случаное расположение живых клеток")
                # если окно закрыто, программа завершается
                if event.type == p.QUIT:
                    self.run = False
            # обновление объектов в окне
            self.update()
            # вызов функции в которой происходит расположение пользователем клеток, в случае initial = True
            self.user_initial()
            # если игра начата
            if self.start:
                # происходит вызов функции в которой происходит новое поколение клеток
                self.next_generation()
                # задержка(иначе будет все слишком быстро)
                self.clock.tick(10)
            # обновление окна
            p.display.update()


if __name__ == "__main__":
    # создаем объекты класса игры
    game = conways_life()
    # вызываем функцию запуска игры
    game.start_game()
