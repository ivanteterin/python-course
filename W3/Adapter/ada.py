class MappingAdapter:
    def __init__(self, adaptee): #adaptee объект класса Light
        self.adaptee = adaptee
        pass

    def lighten(self, grid):
        self.adaptee.set_dim((len(grid[0]), len(grid)))
        lights = []
        obstacles = []
        for i in range(len(grid) - 1):
            for j in range(len(grid[i])-1):
                if grid[i][j] > 0:
                    lights.append((j, i))
                elif grid[i][j] < 0:
                    obstacles.append((j, i))
        #print(lights)
        self.adaptee.set_lights(lights)
        self.adaptee.set_obstacles(obstacles)
        return self.adaptee.generate_lights()