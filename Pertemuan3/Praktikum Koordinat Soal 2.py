# Ukuran layar
lebar = 10
tinggi = 5

# Koordinat titik X
x = 3
y = 2

# Tampilkan layar
for j in range(tinggi):
    for i in range(lebar):
        if i == x and j == y:
            print("X", end=" ")
        else:
            print(".", end=" ")
    print()
