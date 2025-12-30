Python ile geliştirilmiş profesyonel bir domain sorgulama, analiz ve "Sniper" (Düşecek domain yakalama) aracıdır.

Whois verilerini analiz eder, domain yaşını hesaplar ve dolu olan domainleri veritabanına kaydederek boşa düştüğü an size **Telegram üzerinden bildirim** gönderir.

 Domain Asistanı Ekran Görüntüsü](https://i.imgur.com/cEwKd4t.png)

## 🌟 Özellikler

* **🔍 Detaylı Whois Analizi:** Kayıt tarihi, bitiş tarihi ve firma bilgilerini çeker.
* **⏳ Akıllı Yaş Hesaplama:** Domainin tam yaşını (Yıl/Ay/Gün) olarak hesaplar.
* **🎯 Sniper Modu (Takip Sistemi):** Sorguladığınız domain doluysa veritabanına ekler, 7/24 arka planda nöbet tutar ve boşa düştüğü saniye haber verir.
* **💡 Jenerik Öneri Sistemi:** Aradığınız domain doluysa, yapay zeka mantığıyla boşta olan benzer ve değerli varyasyonları (Prefix/Suffix) otomatik önerir.
* **🚦 Trafik Işığı Sistemi:** Domain bitiş süresine göre görsel uyarı verir (🔴 Kritik / 🟢 Güvenli).
* **🛡️ Anti-Crash:** Hata durumunda bot durmaz, log tutar ve çalışmaya devam eder.

## 🛠️ Kurulum

Projeyi bilgisayarınıza indirin (veya `git clone` yapın) ve proje klasörüne gidin.

### 1. Gerekli Kütüphaneleri Yükleyin
Terminal veya CMD açarak şu komutu çalıştırın:

pip install -r requirements.txt
2. Yapılandırma (.env Ayarı)
Proje ana dizininde .env adında bir dosya oluşturun (yoksa oluşturun) ve Telegram Bot Tokeninizi girin:


TELEGRAM_TOKEN=BURAYA_TELEGRAM_BOT_TOKENINIZ_GELECEK
(Telegram Bot Token'ı @BotFather üzerinden alabilirsiniz.)

3. Çalıştırın
Terminalden uygulamayı başlatın:


python main.py
📂 Dosya Yapısı
main.py: Botun ana çalışma dosyası ve kullanıcı arayüzü.

domain_checker.py: Whois sorgularını yapan ve verileri analiz eden motor.

database.py: Takip edilen domainleri saklayan SQLite veritabanı yöneticisi.

config.py: Sistem ayarları ve sabitler.

🤝 Katkıda Bulunma
Bu proje açık kaynaklıdır ve geliştirmeye açıktır. Pull request göndererek veya "Issue" açarak gelişmesine katkıda bulunabilirsiniz.

Geliştirici: JACKON
