#Dibuat oleh Pak Prayit
#Politeknik Negeri Semarang
def guess_number():
    secret_number = 10
    guess = 0
    guess_limit = 3
    
    while guess < guess_limit:
        user = int(input("Masukkan angka >"))
        if user == secret_number:
            print("Selamat, anda berhasil menebaknya")
            break
        else:
            print("Salah >//<")
            guess += 1
    else:
        print(f"Anda tidak menemukan angkanya, angka rahasianya adalah {secret_number}")