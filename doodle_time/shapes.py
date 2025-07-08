import math


class Rectangle:
    def __init__(self):
        self.x = 100
        self.y = 200
        self.width = 80
        self.height = 50
        self.color = (50, 50, 255)

    def covers(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

    def move(self, direction):
        if direction == 'UP':
            self.y -= 10
        elif direction == 'DOWN':
            self.y += 10
        elif direction == 'LEFT':
            self.x -= 10
        elif direction == 'RIGHT':
            self.x += 10

    def resize(self, factor):
        self.width *= factor
        self.height *= factor


class Circle:
    def __init__(self):
        self.x = 200
        self.y = 200
        self.r = 40
        self.color = (50, 50, 255)

    def covers(self, x, y):
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= self.r ** 2

    def move(self, direction):
        if direction == 'UP':
            self.y -= 10
        elif direction == 'DOWN':
            self.y += 10
        elif direction == 'LEFT':
            self.x -= 10
        elif direction == 'RIGHT':
            self.x += 10

    def resize(self, factor):
        self.r *= factor


class Triangle:
    def __init__(self):
        self.x1, self.y1 = 300, 250
        self.x2, self.y2 = 270, 310
        self.x3, self.y3 = 330, 310
        self.color = (50, 50, 255)
        self.points = [self.x1, self.y1, self.x2, self.y2, self.x3, self.y3]

    def covers(self, x, y):
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - \
                   (p2[0] - p3[0]) * (p1[1] - p3[1])
        b1 = sign((x, y), (self.x1, self.y1), (self.x2, self.y2)) < 0.0
        b2 = sign((x, y), (self.x2, self.y2), (self.x3, self.y3)) < 0.0
        b3 = sign((x, y), (self.x3, self.y3), (self.x1, self.y1)) < 0.0
        return b1 == b2 == b3

    def move(self, direction):
        if direction == 'UP':
            self.y1 -= 10; self.y2 -= 10; self.y3 -= 10
        elif direction == 'DOWN':
            self.y1 += 10; self.y2 += 10; self.y3 += 10
        elif direction == 'LEFT':
            self.x1 -= 10; self.x2 -= 10; self.x3 -= 10
        elif direction == 'RIGHT':
            self.x1 += 10; self.x2 += 10; self.x3 += 10

    def resize(self, factor):
        cx = (self.x1 + self.x2 + self.x3) / 3
        cy = (self.y1 + self.y2 + self.y3) / 3
        self.x1 = cx + (self.x1 - cx) * factor
        self.y1 = cy + (self.y1 - cy) * factor
        self.x2 = cx + (self.x2 - cx) * factor
        self.y2 = cy + (self.y2 - cy) * factor
        self.x3 = cx + (self.x3 - cx) * factor
        self.y3 = cy + (self.y3 - cy) * factor

    def rotate(self, angle_degrees):
        # Calculate centroid
        cx = sum(p[0] for p in self.points) / 3
        cy = sum(p[1] for p in self.points) / 3

        angle_radians = math.radians(angle_degrees)
        cos_a = math.cos(angle_radians)
        sin_a = math.sin(angle_radians)

        new_points = []
        for x, y in self.points:
            dx, dy = x - cx, y - cy
            rx = cx + dx * cos_a - dy * sin_a
            ry = cy + dx * sin_a + dy * cos_a
            new_points.append((rx, ry))

        self.points = new_points
