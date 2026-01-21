import turtle

# ================== SETUP TURTLE ==================
t = turtle.Turtle()
t.speed(0)
t.hideturtle()
turtle.setworldcoordinates(-200, -200, 200, 200)
turtle.bgcolor("white")

# =================================================
# ALGORITMA GARIS DDA
# =================================================
def dda(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    steps = int(max(abs(dx), abs(dy)))
    x_inc = dx / steps
    y_inc = dy / steps

    x, y = x1, y1
    t.penup()
    t.goto(round(x), round(y))
    t.pendown()

    for _ in range(steps):
        x += x_inc
        y += y_inc
        t.goto(round(x), round(y))

# =================================================
# ALGORITMA GARIS BRESENHAM
# =================================================
def bresenham(x1, y1, x2, y2):
    t.penup()
    t.goto(x1, y1)
    t.pendown()

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    x, y = x1, y1

    if dx > dy:
        p = 2*dy - dx
        while x != x2:
            t.goto(x, y)
            x += sx
            if p < 0:
                p += 2*dy
            else:
                y += sy
                p += 2*(dy - dx)
    else:
        p = 2*dx - dy
        while y != y2:
            t.goto(x, y)
            y += sy
            if p < 0:
                p += 2*dx
            else:
                x += sx
                p += 2*(dx - dy)

    t.goto(x2, y2)

# =================================================
# MIDPOINT CIRCLE ALGORITHM
# =================================================
def plot_circle_points(xc, yc, x, y):
    points = [
        (xc + x, yc + y), (xc - x, yc + y),
        (xc + x, yc - y), (xc - x, yc - y),
        (xc + y, yc + x), (xc - y, yc + x),
        (xc + y, yc - x), (xc - y, yc - x)
    ]
    for px, py in points:
        t.goto(px, py)

def midpoint_circle(xc, yc, r):
    x = 0
    y = r
    p = 1 - r

    t.penup()
    plot_circle_points(xc, yc, x, y)
    t.pendown()

    while x < y:
        x += 1
        if p < 0:
            p += 2*x + 1
        else:
            y -= 1
            p += 2*(x - y) + 1
        plot_circle_points(xc, yc, x, y)

# =================================================
# POLIGON (MENGGUNAKAN GARIS SENDIRI)
# =================================================
def polygon(points):
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        bresenham(x1, y1, x2, y2)

# =================================================
# CONTOH PEMANGGILAN
# =================================================

# Garis DDA
dda(-150, -150, 150, -50)

# Garis Bresenham
bresenham(-150, 100, 150, 100)

# Lingkaran Midpoint
midpoint_circle(0, 0, 60)

# Poligon (Persegi)
polygon([
    (-80, -20),
    (-20, -20),
    (-20, 40),
    (-80, 40)
])

turtle.done()
