# Pratikum Dasar Pemrograman
# Created By Azani Fattur Fahika
# Politeknik Negeri Semarang

def guess_number():
    secret_number = 9
    guess = 0
    guess_limit = 3
    
    while guess < guess_limit:
        user = int(input("Masukkan angka > "))
        if user == secret_number:
            print("Selamat, anda berhasil menemukan angkanya")
            break
        else:
            print("Salah!")
    
    else:
        print("Anda tidak menemukan angkanya, angka rahasianya salah {secret_number}")