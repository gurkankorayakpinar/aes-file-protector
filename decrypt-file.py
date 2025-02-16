from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import unpad
import os

# Parolayı kullanarak AES için 32 baytlık bir anahtar türetme
def derive_key(password: str, salt: bytes):
    return PBKDF2(password, salt, dkLen=32)

# Şifre çözme fonksiyonu
def decrypt_file(input_filename, output_filename, password):
    try:
        # Dosyayı okuma
        with open(input_filename, 'rb') as f:
            salt = f.read(16)  # İlk 16 bayt salt
            iv = f.read(16)    # Sonraki 16 bayt IV
            ciphertext = f.read()  # Geri kalan kısmı şifreli metin olarak al

        # Paroladan anahtar türetme ve AES şifreleme işlemi
        key = derive_key(password, salt)  # Paroladan anahtar türet
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        try:
            # Şifre çözme
            decrypted_padded = cipher.decrypt(ciphertext)
            decrypted_text = unpad(decrypted_padded, AES.block_size)  # Padding'i kaldır

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

# Kullanıcıdan dosya adı ve parolayı al
input_file = "deneme.bin"
output_file = "deneme2.txt"
password = input("Parolayı girin: ")

# Şifreyi çözmeyi dene
decrypt_file(input_file, output_file, password)
