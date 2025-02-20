# AES File Protector

- Bu proje, ".txt" uzantılı dosyaları AES kullanarak şifreleyen bir uygulamadır.

***

# 1. Encryption

- Şifreleme için, öncelikle klasördeki ".txt" uzantılı dosyaların listelenmesi ve kullanıcının seçim yapması sağlanmıştır.

- Kullanıcının parola belirlemesi zorunludur.

- Şifrelenen dosyanın ismi, şu anki "tarih ve saat" olarak kaydedilmektedir.

***

# 2. Decryption

- Şifre çözme için, öncelikle klasördeki ".bin" uzantılı dosyaların listelenmesi ve kullanıcının seçim yapması sağlanmıştır.

- Şifresi çözülen dosyanın ismi, şu anki "tarih ve saat" olarak kaydedilmektedir.

***

- Tarih ve saat bilgisi için `datetime` modülü kullanılmıştır.

- Olası hatalar için "Exception Handling" uygulanmıştır.