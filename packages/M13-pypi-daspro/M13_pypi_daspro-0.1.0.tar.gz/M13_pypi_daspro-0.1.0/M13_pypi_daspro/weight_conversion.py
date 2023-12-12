# Pratikum Dasar Pemrograman
# Created By Azani Fattur Fahika
# Politeknik Negeri Semarang

def weight_conversion():
    berat = int(input("Masukkan berat anda > "))
    satuan = input("Dalam satuan apa berat yang anda masukkan > (K untuk KG, L untuk LBS) > ")
    
    if satuan.lower() == 'l':
        print("Berat anda dikonversi menjadi kilogram adalah {round(berat * 0.453592)} kg")
    elif satuan.lower() == 'k':
        print("Berat anda dikonversi menjadi pons adalah {round(berat * 2.20462)} lbs")