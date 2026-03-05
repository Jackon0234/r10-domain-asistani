<p align="center">
  <img src="https://capsule-render.vercel.app/render?type=soft&color=auto&height=200&section=header&text=Python%20Domain%20Sniper%20v1.5&fontSize=50&animation=fadeIn" />
</p>

<div align="center">

# 🎯 Domain Asistanı & Sniper Bot
**Yapay Zeka Destekli, Profesyonel Domain Analiz ve Takip Sistemi**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot_Alerts-26A5E4.svg?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/BotFather)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Stable-brightgreen.svg?style=for-the-badge)]()

</div>

---

## 📖 Proje Hakkında
Sıradan bir Whois sorgulayıcıdan çok daha fazlası. **Domain Asistanı**, değerli domainleri sizin yerinize 7/24 nöbet tutarak takip eden, boşa düştüğü an Telegram üzerinden sizi uyandıran bir **Sniper** (Keskin Nişancı) botudur.

> [!IMPORTANT]
> Bu bot, Whois sunucularındaki sorgu limitlerini aşmamak için akıllı bekleme (rate-limit handling) sistemine sahiptir.

---

## 🚀 Öne Çıkan Özellikler

| Özellik | Açıklama |
| :--- | :--- |
| **🔍 Derin Analiz** | Kayıt/Bitiş tarihi, DNS, Registrar ve kapsamlı yaş analizi. |
| **🎯 Sniper Modu** | "Pending Delete" sürecini izler, boşa düştüğü an haber verir. |
| **💡 Akıllı Öneriler** | Dolu domainler için yapay zeka destekli prefix/suffix varyasyonları üretir. |
| **🚦 Trafik Işığı** | Kalan süreye göre görsel uyarı: 🔴 Kritik (<30 gün) / 🟢 Güvenli. |
| **🛡️ Anti-Crash** | Hata anında sistemi kapatmaz, log tutar ve otomatik yeniden bağlanır. |

---

## 📸 Önizleme
<p align="center">
  <img src="https://i.imgur.com/cEwKd4t.png" width="85%" style="border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); border: 1px solid #333;">
</p>

---

## 🛠️ Kurulum & Kullanım

### 1️⃣ Gereksinimler
Öncelikle depoyu klonlayın ve kütüphaneleri yükleyin:
```bash
git clone [https://github.com/KULLANICI_ADIN/Domain-Sniper.git](https://github.com/KULLANICI_ADIN/Domain-Sniper.git)
cd Domain-Sniper
pip install -r requirements.txt

2️⃣ Yapılandırma
Ana dizinde bir .env dosyası oluşturun ve Telegram bilgilerinizi ekleyin:

Kod snippet'i
TELEGRAM_TOKEN=123456789:ABCDefghIJKL-mnopq
# Not: Token'ı @BotFather üzerinden alabilirsiniz.
3️⃣ Başlatma
Sistemi ayağa kaldırmak için terminale şu komutu girin:

Bash
python main.py
📂 Proje Mimarisi
Plaintext
├── 📄 main.py           # Ana Giriş & UI Kontrolü
├── ⚙️ config.py         # Ayarlar & Sistem Sabitleri
├── 🔍 domain_checker.py # Whois Motoru & Analiz Algoritması
├── 🗄️ database.py       # SQLite Veritabanı Yönetimi (Sniper Listesi)
└── 📄 .env              # Hassas Veriler (Tokenlar)

