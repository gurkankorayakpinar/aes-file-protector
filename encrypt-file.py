from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad
import os
from datetime import datetime

# Parolayı kullanarak AES için 32 byte boyutunda bir anahtar türetme
def derive_key(password: str, salt: bytes):
    return PBKDF2(password, salt, dkLen=32)

# Şifreleme fonksiyonu
def encrypt_file(input_filename, output_filename, password):
    try:
        with open(input_filename, 'rb') as f:
            plaintext = f.read()  # Dosya içeriğini oku

        salt = os.urandom(16)  # 16 byte boyutunda rastgele salt
        iv = os.urandom(16)    # 16 byte boyutunda rastgele IV

        key = derive_key(password, salt)  # Paroladan anahtar türet.
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))  # Şifrele.

        with open(output_filename, 'wb') as f:
            f.write(salt)  # Salt yaz.
            f.write(iv)    # IV yaz.
            f.write(ciphertext)  # Şifreli metni yaz.

        print(f"Dosya başarıyla şifrelendi ve kaydedildi: {output_filename}")
        return True  # Başarılı şifreleme

    except FileNotFoundError:
        print(f"Hata: Dosya '{input_filename}' bulunamadı.")
        return False  # Dosya bulunamadı hatası

    except PermissionError:
        print(f"Hata: Dosyayı okuma veya yazma izniniz yok.")
        return False  # Erişim hatası

    except ValueError as e:
        print(f"Hata: Şifreleme hatası - {e}")
        return False  # Şifreleme hatası

# Proje klasöründeki tüm ".txt" dosyalarını bul.
txt_files = [f for f in os.listdir() if f.endswith(".txt")]

if not txt_files:
    print("Hata: Şifrelenecek .txt dosyası bulunamadı.")
else:
    # Kullanıcıya hangi dosyanın şifreleneceğini sor.
    print("Mevcut .txt dosyaları:")
    for i, file in enumerate(txt_files, 1):
        print(f"{i}. {file}")
    
    # Kullanıcıdan dosya seçmesi istenir.
    choice = input(f"Lütfen şifrelenecek dosyanın numarasını girin (1-{len(txt_files)}): ").strip()
    
    try:
        choice = int(choice)
        if 1 <= choice <= len(txt_files):
            selected_file = txt_files[choice - 1]
            
            # Kullanıcıdan parola al.
            password = ""
            while not password:
                password = input("Parolayı girin: ").strip()  # Parolayı al ve boşlukları kaldır

                if not password:  # Parola boşsa
                    print("Parola boş olamaz. Lütfen geçerli bir parola girin.")

            # Benzersiz bir dosya ismi oluşturmak için tarih ve saat bilgisini kullan.
            current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            output_file = f"{current_time}.bin"
            
            # Şifrelemeyi dene.
            encrypt_file(selected_file, output_file, password)
        else:
            print("Geçersiz seçim.")
    except ValueError:
        print("Lütfen geçerli bir sayı girin.")
