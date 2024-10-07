from math import sqrt
from random import random as ran

import pygame as pg

SCREEN_DIM = (800, 600)
WHITE = (255, 255, 255)
DARKGREY = (10, 10, 10)
GREY = (100, 100, 100)


class Vec2d(tuple):
    """
    определяет методы для основных математических операций, необходимых для
    работы с вектором
    """

    def __init__(self, point):
        self.p = point
        self.x = self.p[0]
        self.y = self.p[1]

    def __add__(self, other):
        """возвращает сумму двух векторов"""
        if not isinstance(other, Vec2d):
            raise ArithmeticError("Second operand is not type Vec2d")
        return self.__class__((self.x + other.p[0],
                               self.y + other.p[1]))

    def __sub__(self, other):
        """"возвращает разность двух векторов"""
        if not isinstance(other, Vec2d):
            raise ArithmeticError("Second operand is not type Vec2d")
        return self.__class__((self.x - other.p[0],
                               self.y - other.p[1]))

    def __mul__(self, other):
        """возвращает произведение вектора на число"""
        return self.__class__((self.x * other,
                               self.y * other))

    def __lt__(self, other):
        if self.x < other.x and self.y < other.y:
            return True
        return False

    def __abs__(self):
        """возвращает абсолютное значение координат вектора"""
        return self.__class__((abs(self.x), abs(self.y)))

    def invert_x(self):
        """the same is it name :)"""
        return self.__class__((-self.x, self.y))

    def invert_y(self):
        """the same is it name :)"""
        return self.__class__((self.x, -self.y))

    @staticmethod
    def sign(num):
        return -1 if num < 0 else 1

    def speed_down(self, delta):
        """уменьшает значение вектора на коэфф. delta
        с учётом знака составляющих вектора"""
        if abs(self.x) < delta or abs(self.y) < delta:
            return self.__class__(
                (self.x - self.x * 4 * delta * self.sign(self.x),
                 self.y - self.y * 4 * delta * self.sign(self.y)))
        else:
            return self.__class__(
                (self.x - delta * self.sign(self.x),
                 self.y - delta * self.sign(self.y)))

    def speed_up(self, delta):
        """увеличивает значение вектора на коэфф. delta
        с учётом знака составляющих вектора"""
        if not self.x or not self.y:
            return self.__class__((ran() * 0.5, ran() * 0.5))
        return self.__class__((self.x + delta * self.sign(self.x),
                               self.y + delta * self.sign(self.y)))

    def length(self):
        """возвращает длину вектора"""
        return sqrt(self.x * self.x + self.y * self.y)

    def int_pair(self):
        return round(self.x), round(self.y)
    # def vec(self, v1, v2): """возвращает пару координат, определяющих
    # вектор (координаты точки конца вектора), координаты начальной точки
    # вектора совпадают с началом системы координат (0, 0) """ return
    # self.sub(v2, v1)


class Polyline:
    """
    определяет методы, отвечающие за добавление в ломаную точки (Vec2d)
    c её скоростью, пересчёт координат точек (set_points)
    и отрисовку ломаной (draw_points)
    """

    @staticmethod
    def set_points(points, speeds):
        """функция перерасчета координат опорных точек"""
        for p in range(len(points)):
            points[p] = points[p] + speeds[p]
            if points[p][0] > SCREEN_DIM[0] or points[p][0] < 0:
                speeds[p] = speeds[p].invert_x()

            if points[p][1] > SCREEN_DIM[1] or points[p][1] < 0:
                speeds[p] = speeds[p].invert_y()

    @staticmethod
    def draw_points(points, style="points", width=3, color=(255, 255, 255)):
        """функция отрисовки точек на экране"""
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pg.draw.line(screen, color,
                             (points[p_n].int_pair()),
                             (points[p_n + 1].int_pair()), width)

        elif style == "points":
            for p in points:
                x = p.int_pair()[0]
                y = p.int_pair()[1]
                pg.draw.circle(screen, color,
                               (x, y), width)


class Knot(Polyline):
    """
    определяет функции, отвечающие за расчет сглаживания ломаной
    """

    def __init__(self):
        self.points = []
        self.speeds = []

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + \
               self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self, count):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            res.extend(self.get_points(ptn, count))
        return res

    def del_points(self, left_upper, right_lower):
        """ remove selected points from list"""
        for _ in self.points:
            if left_upper < _ < right_lower:
                self.points.pop(self.points.index(_))


def draw_help():
    """функция отрисовки экрана справки программы"""
    screen.fill((50, 50, 50))
    font1 = pg.font.SysFont("courier", 24)
    font2 = pg.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["N", "Add another line"])
    data.append(["UP", "+ Speed"])
    data.append(["DOWN", "- Speed"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append(["", "For removing points press 'P',"])
    data.append(["", "select points witn PKM and press DEL"])
    data.append(["", ""])
    data.append(["[!]", "Warning! Selection will take effect "])
    data.append(["[!]", "is ONLY when you drag mouse"])
    data.append(["[!]", "from Upper Left to Lower Right "])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pg.draw.lines(screen, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        screen.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 30 + 30 * i))
        screen.blit(font2.render(
            text[1], True, (128, 128, 255)), (270, 30 + 30 * i))


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode(SCREEN_DIM)
    pg.display.set_caption("MyScreenSaver")

    sp_delta = 0.08  # step for change speed
    num_c = 0  # curve number
    curve = [Knot()]
    steps = 35
    working = True
    show_help = False
    pause = True
    hue = 0
    color = pg.Color(0)
    draw_mask = False
    begin_pos = None
    end_pos = None
    left_up = None

    while working:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                working = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    working = False
                if event.key == pg.K_r:
                    num_c = 0
                    curve = [Knot()]
                if event.key == pg.K_n:
                    curve.append(Knot())
                    num_c += 1
                if event.key == pg.K_UP:
                    for i in curve:
                        for j in range(len(i.speeds)):
                            i.speeds[j] = i.speeds[j].speed_up(sp_delta)
                if event.key == pg.K_DOWN:
                    for i in curve:
                        for j in range(len(i.speeds)):
                            i.speeds[j] = i.speeds[j].speed_down(sp_delta)
                if event.key == pg.K_p:
                    pause = not pause
                if event.key == pg.K_KP_PLUS:
                    steps += 1
                if event.key == pg.K_F1:
                    show_help = not show_help
                if event.key == pg.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                if event.key == pg.K_DELETE:
                    pause = True
                    draw_mask = True

            #   add points with LKM
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                curve[num_c].points.append(Vec2d(event.pos))
                curve[num_c].speeds.append(Vec2d((ran() * 2, ran() * 2,)))

        press = pg.mouse.get_pressed(3)
        if pause and press[2]:
            # draw select frame with PKM and remember frame corner coords
            pos = Vec2d(pg.mouse.get_pos())
            if left_up is None:
                left_up = pos
                begin_pos = Vec2d(pg.mouse.get_pos())
            wid_hei = pos - left_up
            pg.draw.rect(screen, GREY, (left_up, wid_hei), 3)
            pg.display.update()
        else:
            end_pos = Vec2d(pg.mouse.get_pos())
            left_up = None

        screen.fill(DARKGREY)
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)

        for _ in curve:
            # remove selected points
            if begin_pos and end_pos and draw_mask:
                _.del_points(begin_pos, end_pos)
        draw_mask = False

        for _ in curve:
            # draw points
            _.draw_points(_.points)
            _.draw_points(_.get_knot(steps), "line", 3, color)
            if not pause:
                _.set_points(_.points, _.speeds)
        if show_help:
            draw_help()
        pg.display.update()
