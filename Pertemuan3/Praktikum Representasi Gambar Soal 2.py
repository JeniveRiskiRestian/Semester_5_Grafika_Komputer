x1, y1 = 0, 0
x2, y2 = 5, 3

# Hitung jumlah langkah
steps = max(abs(x2 - x1), abs(y2 - y1))

# Hitung increment tiap langkah
x_inc = (x2 - x1) / steps
y_inc = (y2 - y1) / steps

# Inisialisasi titik awal
x, y = x1, y1

print("Titik-titik koordinat garis dari (0,0) ke (5,3):")
for i in range(steps + 1):
    print(f"({round(x)}, {round(y)})")
    x += x_inc
    y += y_inc
