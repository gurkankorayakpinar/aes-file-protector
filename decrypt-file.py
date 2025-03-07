from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import unpad
import os
from datetime import datetime

# Parolayı kullanarak AES için 32 byte boyutunda bir anahtar türet.
def derive_key(password: str, salt: bytes):
    return PBKDF2(password, salt, dkLen=32)

# Şifre çözme fonksiyonu
def decrypt_file(input_filename, password):
    try:
        # Dosyayı oku.
        with open(input_filename, 'rb') as f:
            salt = f.read(16)  # İlk 16 byte salt
            iv = f.read(16)    # Sonraki 16 byte IV
            ciphertext = f.read()  # Geri kalan kısmı "şifreli metin" olarak al.

        # Paroladan anahtar türetme ve AES şifreleme işlemi
        key = derive_key(password, salt)  # Paroladan anahtar türet.
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        try:
            # Şifre çözme
            decrypted_padded = cipher.decrypt(ciphertext)
            decrypted_text = unpad(decrypted_padded, AES.block_size)  # Padding'i kaldır

            # Şu anki tarih ve saati al
            current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

            # Çözülen dosyanın ismini, tarih ve saat bilgisiyle oluştur
            output_filename = f"{current_datetime}.txt"  # .txt uzantısı veriyoruz, çünkü çözülmüş dosya, metin dosyası olacak.

            # Çözülen dosyayı kaydetme
            with open(output_filename, 'wb') as f:
                f.write(decrypted_text)

            print(f"Dosya başarıyla çözüldü ve kaydedildi: {output_filename}")
            return True  # Başarılı çözüm

        except ValueError as e:
            # Padding hatası veya diğer şifre çözme hataları
            print(f"Hata: Şifre çözme işlemi sırasında bir sorun oluştu. Detay: {e}")
            return False  # Hatalı çözüm

    except FileNotFoundError:
        print(f"Hata: Dosya '{input_filename}' bulunamadı.")
        return False  # Dosya bulunamadı hatası

    except PermissionError:
        print(f"Hata: Dosyayı okuma veya yazma izniniz yok.")
        return False  # Erişim hatası

    except Exception as e:
        print(f"Bilinmeyen bir hata oluştu: {e}")
        return False  # Diğer bilinmeyen hatalar

# Proje klasöründeki tüm ".bin" dosyalarını bul.
bin_files = [f for f in os.listdir() if f.endswith(".bin")]

if not bin_files:
    print("Hata: Şifreli .bin dosyası bulunamadı.")
else:
    # Kullanıcıya hangi dosyanın şifresini çözeceğini sor.
    print("Mevcut şifreli .bin dosyaları:")
    for i, file in enumerate(bin_files, 1):
        print(f"{i}. {file}")
    
    # Kullanıcıdan dosya seçmesini iste.
    choice = input(f"Lütfen şifresini çözmek istediğiniz dosyanın numarasını girin (1-{len(bin_files)}): ").strip()
    
    try:
        choice = int(choice)
        if 1 <= choice <= len(bin_files):
            selected_file = bin_files[choice - 1]
            
            # Kullanıcıdan parola al.
            password = ""
            while not password:
                password = input("Parolayı girin: ").strip()  # Parolayı al ve boşlukları kaldır.

                if not password:  # Parola boşsa
                    print("Parola boş olamaz. Lütfen geçerli bir parola girin.")

            # Şifreyi çözmeyi dene.
            decrypt_file(selected_file, password)
        else:
            print("Geçersiz seçim.")
    except ValueError:
        print("Lütfen geçerli bir sayı girin.")
