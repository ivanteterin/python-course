import pygame
import random
import math

SCREEN_DIM = (800, 600)

class Vec2d:
    
    def __init__(self, x, y):
        self.x = x 
        self.y = y
    
    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)
    
    def __mul__(self, digit):
        return Vec2d(self.x*digit, self.y*digit)
    
    def len(self):
        return (x**2 + y**2)**0.5
    
    def int_pair(self):
        return((int(self.x), int(self.y)))
    

class Polyline:
    
    def __init__(self):
        self.points = []
        self.speeds = []
    
    def add(self, point, speed):
        self.points.append(point)
        self.speeds.append(speed)
        
    def drop_point(self):
        del self.points[-1]
        del self.speeds[-1]
    
    def set_points(self):
        for p in range(len(self.points)):
            speed = self.speeds[p]
            self.points[p] += self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(-speed.x, speed.y)
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(speed.x, -speed.y)
    
    def draw_points(self, draw, width=3, color=(255, 255, 255)):
        for p in self.points:
            draw.circle(gameDisplay, color, p.int_pair(), width)  
            
    def increase_speed(self):
        self.speeds = list(map(lambda x: x*1.1, self.speeds))

    def decrease_speed(self):
        self.speeds = list(map(lambda x: x*0.9, self.speeds))


class Knot(Polyline):

    def __init__(self, steps):
        super().__init__()
        self.knot = []
        self.steps = steps

    def add(self, point, speed):
        super().add(point, speed)
        self._update()

    def set_points(self):
        super().set_points()
        self._update()
        
    def drop_point(self):
        super().drop_point()
        self._update()

    def increase_steps(self):
        self.steps += 1
        self._update()
        
    def decrease_steps(self):
        self.steps -= 1 if self.steps > 1 else 0
        self._update()

    def _update(self):
        self.knot = self._get_knot()

    @staticmethod
    def _get_point(points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + Knot._get_point(points, alpha, deg - 1) * (1 - alpha)
    
    @staticmethod
    def _get_points(base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(Knot._get_point(base_points, i * alpha))
        return res

    def _get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            res.extend(Knot._get_points(ptn, self.steps))
        return res  

    def draw_knot(self, draw, width=3, color=(255, 255, 255)):
        for p_n in range(-1, len(self.knot) - 1):
            point = self.knot[p_n]
            next_point = self.knot[p_n + 1]
            draw.line(gameDisplay, 
                      color, 
                      point.int_pair(), 
                      next_point.int_pair(), 
                      width)
                
                

if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    working = True
    pause = True
    knot = Knot(35)
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
                    knot = Knot()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    knot.increase_steps()
                if event.key == pygame.K_KP_MINUS:
                    knot.decrease_steps()
                if event.key == pygame.K_d: # удаления «опорной» точки из кривой
                    knot.drop_point()
                if event.key == pygame.K_q: # замедление
                    knot.decrease_speed()
                if event.key == pygame.K_w: # ускорение
                    knot.increase_speed()

            if event.type == pygame.MOUSEBUTTONDOWN:
                knot.add(Vec2d(event.pos[0], event.pos[1]), Vec2d(random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        knot.draw_points(pygame.draw)
        knot.draw_knot(pygame.draw, 3, color)
        if not pause:
            knot.set_points()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
