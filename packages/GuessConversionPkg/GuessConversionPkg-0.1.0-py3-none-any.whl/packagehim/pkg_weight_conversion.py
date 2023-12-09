#Dibuat oleh Pak Prayit
#Politeknik Negeri Semarang
def weight_conversion():
    berat = int(input("Masukkan berat Anda > "))
    satuan = input("Dalam satuan apa berat yang Anda masukkan ? (K untuk KG, L untuk LBS) > ")

    if satuan.lower() == 'l':
        print(f"Berat Anda dikonversi menjadi kilogram adalah {round(berat * 0.453592)} kg")
    elif satuan.lower() == 'k':
        print(f"Berat Anda dikonversi menjadi pons adalah {round(berat * 2.20462)} lbs")