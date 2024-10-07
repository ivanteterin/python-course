import pygame
import random
import math

SCREEN_DIM = (800, 600)

# =======================================================================================
# Функции для работы с векторами
# =======================================================================================

class Vec2d:
    def __init__(self, vector):
        self.x = vector[0]
        self.y = vector[1]
    
    def __sub__(self, other):
        """"возвращает разность двух векторов"""
        return Vec2d((self.x - other.x, self.y - other.y))


    def __add__(self, other):
        """возвращает сумму двух векторов"""
        return Vec2d((self.x + other.x, self.y + other.y))


    def __len__(self):
        """возвращает длину вектора"""
        sum_kv = self.x ** 2 + self.y ** 2
        #print(sum_kv)
        return round(math.sqrt(float(sum_kv)))#self.x * self.x + self.y * self.y)
    
    def __mul__(self, k):
        """возвращает произведение вектора на число"""
        return Vec2d((self.x * k, self.y * k))


    def int_pair(self):
        """возвращает пару координат, определяющих вектор (координаты точки конца вектора),
        координаты начальной точки вектора совпадают с началом системы координат (0, 0)"""
        return (self.x, self.y)

    
class Polyline:    
    def __init__(self, points, speeds):
        self.points = points
        self.speeds = speeds
                
    def draw_points(self, points, style = "points", width=3, color=(255, 255, 255)):
        """функция отрисовки точек на экране"""
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color, (int(points[p_n].x), int(points[p_n].y)), 
                                 (int(points[p_n + 1].x), int(points[p_n + 1].y)), width)
        elif style == "points":
            for p in points:
                pygame.draw.circle(gameDisplay, color, (int(p.x), int(p.y)), width)
                
    def set_points(self):
        """функция перерасчета координат опорных точек"""
        for p in range(len(self.points)):
            self.points[p].x = self.points[p].x + self.speeds[p][0]
            self.points[p].y = self.points[p].y + self.speeds[p][1]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = (- self.speeds[p][0], self.speeds[p][1])
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = (self.speeds[p][0], -self.speeds[p][1])
            
    def speed_up(self):
        substitute=[]
        for i in range(len(self.speeds)):
            substitute.append([self.speeds[i][0] * 2, self.speeds[i][1] * 2])
        self.speeds = substitute
                        
    def speed_down(self):
        substitute=[]
        for i in range(len(self.speeds)):
            substitute.append([self.speeds[i][0] / 2, self.speeds[i][1] / 2])
        self.speeds = substitute

            
class Knot (Polyline):    
    def __init__(self, points, speeds, count):
        self.points = points
        self.speeds = speeds
        self.count = count
    
    
    def get_point(self, points, alpha, deg=None):
        a = 1 / self.count
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg]*alpha + self.get_point(points, alpha, deg-1)*(1-alpha)


    def get_points(self, base_points):
        alpha = 1 / self.count
        res = []
        for i in range(self.count):
            res.append(self.get_point(base_points, i * alpha))
        return res


    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
            res.extend(self.get_points(ptn))
        return res

    

def draw_help():
    """функция отрисовки экрана справки программы"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["A", "Add polyline"])
    data.append(["E", "Erase last polyline"])
    data.append(["I", "Increase speed"])
    data.append(["D", "Decrease speed"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])
    data.append([str(len(knots)), "Polylines count"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")
    
    steps = 35
    working = True
    knots = [Knot([], [], steps)]
    #points = []
    #speeds = []
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    knots = [Knot([], [], steps)]
                    points = []
                    speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                    if not knots == []:
                        knots[len(knots)-1].count = steps
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                    if not knots == []:
                        knots[len(knots)-1].count = steps
                if event.key == pygame.K_a:
                    knots.append(Knot([], [], steps))
                if event.key == pygame.K_e:
                    if len(knots) > 0:
                        knots = knots[:-1]
                if event.key == pygame.K_i:
                    for knot in knots:
                        knot.speed_up()
                if event.key == pygame.K_d:
                    for knot in knots:
                        knot.speed_down()
                

            if event.type == pygame.MOUSEBUTTONDOWN:
                if knots == []:
                    knots.append(Knot(event.pos, steps))
                else:
                    knots[len(knots)-1].points.append(Vec2d(event.pos))
                    knots[len(knots)-1].speeds.append(list([random.random() * 2, random.random() * 2]))
                #points.append(event.pos)
                #speeds.append((random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        for knot in knots:
            knot.draw_points(knot.points)
            knot.draw_points(knot.get_knot(), "line", 3, color)
        #draw_points(points)
        #draw_points(get_knot(points, steps), "line", 3, color)
        if not pause:
            for knot in knots:
                knot.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)