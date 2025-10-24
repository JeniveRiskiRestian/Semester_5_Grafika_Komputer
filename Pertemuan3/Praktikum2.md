# Pertemuan 3
Project ini berisi latihan Representasi Koordinat di Python pada pertemuan ke-3.
Buat program Python untuk:
Menerima input dua titik (x1, y1) dan (x2, y2).
Hitung jarak antara kedua titik. Tentukan di kuadran mana titik pertama berada (berdasarkan sistem Kartesius).

# Koding
import math

# Input titik
x1 = float(input("Masukkan x1: "))
y1 = float(input("Masukkan y1: "))
x2 = float(input("Masukkan x2: "))
y2 = float(input("Masukkan y2: "))

# Hitung jarak antara dua titik
jarak = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Tentukan kuadran titik pertama
if x1 > 0 and y1 > 0:
    kuadran = "Kuadran I"
elif x1 < 0 and y1 > 0:
    kuadran = "Kuadran II"
elif x1 < 0 and y1 < 0:
    kuadran = "Kuadran III"
elif x1 > 0 and y1 < 0:
    kuadran = "Kuadran IV"
elif x1 == 0 and y1 == 0:
    kuadran = "titik pusat (0,0)"
elif x1 == 0:
    kuadran = "sumbu Y"
else:
    kuadran = "sumbu X"

# Hasil
print("\n=== HASIL ===")
print(f"Titik pertama : ({x1}, {y1})")
print(f"Titik kedua   : ({x2}, {y2})")
print(f"Jarak antar titik: {jarak:.2f}")
print(f"Titik pertama berada di: {kuadran}")


# Hasil Program
![Hasil Program](../screenshots/Praktikum2.png)
