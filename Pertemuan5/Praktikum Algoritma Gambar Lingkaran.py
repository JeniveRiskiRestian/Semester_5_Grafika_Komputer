import turtle
import time

# =========================
# SETUP DASAR
# =========================
turtle.speed(0)
turtle.hideturtle()
turtle.bgcolor("#f0f0f0")   # Background soft
turtle.title("Visualisasi Algoritma Grafika Komputer")

# =========================
# FUNGSI DASAR
# =========================
def plot(x, y, color="black"):
    turtle.penup()
    turtle.goto(x, y)
    turtle.dot(4, color)
    # time.sleep(0.01)  # Optional delay untuk animasi

def dda(x1, y1, x2, y2, color="red"):
    dx = x2 - x1
    dy = y2 - y1
    steps = int(max(abs(dx), abs(dy)))
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x1, y1
    for _ in range(steps + 1):
        plot(round(x), round(y), color)
        x += x_inc
        y += y_inc

def circle_midpoint(xc, yc, r, color="blue"):
    x, y = 0, r
    p = 1 - r
    while x <= y:
        for dx, dy in [(x,y),(y,x),(x,-y),(y,-x),(-x,y),(-y,x),(-x,-y),(-y,-x)]:
            plot(xc+dx, yc+dy, color)
        x += 1
        if p < 0:
            p += 2*x + 1
        else:
            y -= 1
            p += 2*(x - y) + 1

def polygon(points, color="green"):
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i+1) % len(points)]
        dda(x1, y1, x2, y2, color)

def write_text(text, x, y, size=16, bold=True):
    turtle.penup()
    turtle.goto(x, y)
    style = ("Arial", size, "bold" if bold else "normal")
    turtle.write(text, align="center", font=style)

# =========================
# GRID VISUAL + LABEL
# =========================
def draw_cell(x, y, w=200, h=150):
    turtle.penup()
    turtle.goto(x - w/2, y - h/2)
    turtle.pendown()
    turtle.pencolor("#888")
    for _ in range(2):
        turtle.forward(w); turtle.left(90)
        turtle.forward(h); turtle.left(90)
    turtle.penup()

# 9 posisi cell
grid_centers = [
    (-250, 150), (0, 150), (250, 150),
    (-250, 0),   (0, 0),   (250, 0),
    (-250, -150),(0, -150),(250, -150)
]

for cx, cy in grid_centers:
    draw_cell(cx, cy)

# Label judul
write_text("Demo Algoritma Grafika Komputer", 0, 260, size=20)
write_text("Garis", -250, 200)
write_text("Lingkaran", 0, 200)
write_text("Poligon", 250, 200)

# =========================
# GAMBAR DI GRID
# =========================
colors = {"line":"red", "circle":"blue", "poly":"green"}

# ROW 1
dda(-300, 170, -200, 110, colors["line"])
circle_midpoint(0, 150, 40, colors["circle"])
polygon([(220, 130), (260, 130), (240, 170)], colors["poly"])

# ROW 2
dda(-300, 20, -200, -40, colors["line"])
circle_midpoint(0, 0, 35, colors["circle"])
polygon([(220, -10), (280, -10), (260, 40), (230, 40)], colors["poly"])

# ROW 3
dda(-300, -120, -220, -180, colors["line"])
circle_midpoint(0, -150, 30, colors["circle"])
polygon([(220, -200), (270, -200), (300, -150), (260, -100), (230, -150)], colors["poly"])

turtle.done()