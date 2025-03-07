# AES File Protector

- Bu proje, ".txt" uzantılı dosyaları AES (Advanced Encryption Standard) kullanarak şifreleyen bir uygulamadır.

***

# 1. Encryption

- Şifreleme işlemi için, öncelikle klasördeki ".txt" uzantılı dosyaların listelenmesi ve kullanıcının seçim yapması sağlanmıştır.

- Klasörde ".txt" uzantılı dosya yoksa, hata mesajı alınması sağlanmıştır.

- Şifreleme işlemi için, kullanıcının parola belirlemesi zorunludur.

- Sadece "space" karakterleri ile parola oluşturulması engellenmiştir.

- Şifrelenen dosyanın ismi, "şu anki tarih ve saat" olarak kaydedilmektedir. Böylece, her defasında "benzersiz bir isim" oluşması sağlanmaktadır.

***

# 2. Decryption

- Şifre çözme işlemi için, öncelikle klasördeki ".bin" uzantılı dosyaların listelenmesi ve kullanıcının seçim yapması sağlanmıştır.

- Şifresi çözülen dosyanın ismi, "şu anki tarih ve saat" olarak kaydedilmektedir. Böylece, her defasında "benzersiz bir isim" oluşması sağlanmaktadır.

***

- Şifreleme işlemleri için `pycryptodome` modülü kullanılmıştır.

- Olası hatalar için "Exception Handling" uygulanmıştır.