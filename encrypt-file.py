from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad
import os

# Parolayı kullanarak AES için 32 baytlık bir anahtar türetme
def derive_key(password: str, salt: bytes):
    return PBKDF2(password, salt, dkLen=32)

# Şifreleme fonksiyonu
def encrypt_file(input_filename, output_filename, password):
    try:
        with open(input_filename, 'rb') as f:
            plaintext = f.read()  # Dosya içeriğini oku

        salt = os.urandom(16)  # 16 baytlık rastgele salt
        iv = os.urandom(16)    # 16 baytlık rastgele IV

        key = derive_key(password, salt)  # Paroladan anahtar türet
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))  # Şifrele

        with open(output_filename, 'wb') as f:
            f.write(salt)  # Salt yaz
            f.write(iv)    # IV yaz
            f.write(ciphertext)  # Şifreli metni yaz

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

# Kullanıcıdan dosya adı ve parolayı al
input_file = "deneme.txt"
output_file = "deneme.bin"
password = input("Parolayı girin: ")

# Şifrelemeyi dene
encrypt_file(input_file, output_file, password)
