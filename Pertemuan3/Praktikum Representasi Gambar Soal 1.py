# Ukuran grid
lebar = 10
tinggi = 10

# Koordinat yang akan diubah
x = 4
y = 6

# Tampilkan grid
for j in range(tinggi):
    for i in range(lebar):
        if i == x and j == y:
            print("X", end=" ")
        else:
            print(".", end=" ")
    print()
