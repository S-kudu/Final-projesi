# Personel Takip Sistemi
Bu proje, bir şirket veya kurumun personellerini takip edebilmesini sağlayan basit ve kullanıcı dostu web tabanlı bir yönetim paneli uygulamasıdır.

## Tasarım Özellikleri
- Bootstrap 5 framework kullanım: Modern tasarım ve hızlı geliştirme için Bootstrap 5 kullanılmıştır.
- Bootstrap Icons entegrasyonu: İkonlar kullanılarak kullanıcı arayüzü zenginleştirilmiştir.
- Kullanıcı dostu arayüz: Kolay navigasyon ve anlaşılır bir arayüz sunulmuştur.
- Personel yönetimi: Personel bilgileri ekleme, düzenleme, silme işlemleri yapılabilir.
- Raporlama: Personel maaş ortalamaları, pozisyon dağılımı gibi raporlar kullanıcıya sunulmaktadır.

## Kurulum ve Çalıştırma 
- Gerekli kütüphaneleri yüklemek için 'requirements.txt' dosyasını kullanın.
- 'app.py' dosyasını çalıştırarak uygulamayı başlatın.
- Tarayıcıda 'http://127.0.0.1:5000' adresine gidin.

## Sayfalar

### 1. **Anasayfa**
- Kullanıcılar sisteme giriş yapmadan önce bu sayfayla karşılaşır
- Kullanıcıya karşılama mesajı sunar ve sisteme davet eder.


### 2. **Dashboard**
- **Personel Takip Sistemi** başlığı altında kullanıcıya genel bilgi sunulur.
- Personel'in iş hakkında kendi bilgilerini görebilmesi mümkündür'.

### 3. **Personel Ekleme (ekleme.html)**
- Yeni personel eklemek için bir form sunulur.
- Personel adı, soyadı, pozisyonu, maaşı, işe başlama tarihi gibi alanlar doldurulup form kaydedilir.
- Ekleme formu başarıyla gönderildikten sonra personel veritabanına eklenir.

### 4. **(duzenle.html)**
-Kullanıcının kaydettiği personel bilgilerinde herhangi bir değişiklik yapılacağı zaman bilgilerin güncellenmesini sağlar

### 5. **Login (login.html)**
- Kullanıcıların sisteme giriş yapabilmesi için e-posta ve şifre ile giriş yapabileceği bir sayfa.
- Giriş başarılı olduğunda personel kendisi hakkındaki bilgilere ulaşabilir.

### 6. **Register (register.html)**
- Yeni kullanıcıların sisteme kaydolması için form alanları sunulur.
- Kullanıcı adı, e-posta, şifre ve şifre tekrar alanları doldurularak kaydolunur.

### 7. **Raporlar (raporlar.html)**
- Personel maaş ortalaması, pozisyonlara göre çalışan dağılımı ve işe başlama tarihine göre sıralı çalışanlar gibi istatistiksel raporlar görüntülenir.
- İstatistik kartları ve detaylı raporlar admin sayfasında görsel bir şekilde sunulur.

### 8. **Personel Listesi (liste.html)**
- Personellerin listelendiği, her bir personel için düzenleme ve silme işlemlerinin yapılabildiği bir sayfa olarak tasarlanmıştır.
- Admin sayfaya yeni personel ekleyebilir, raporlar sayfasına ulaşabilir, personeller hakkındaki bilgilere ulaşabilir.

## Kullanılan Teknolojiler

- HTML5: Web sayfalarının yapısal tasarımı için kullanıldı.
- CSS3: Sayfa stil ve tasarımı için kullanıldı.
- Bootstrap 5: Responsive tasarım ve hızlı geliştirme için kullanıldı.
- Bootstrap Icons: Görsel öğelerin yerleştirilmesi için simgeler kullanıldı.
- Jinja2 Template Engine: Dinamik içerik için Jinja2 şablon motoru kullanıldı.
- Python Flask: Backend geliştirme ve web uygulaması sunucusu olarak kullanıldı.

## Proje Yapısı

```
1.Hafta/
├── instance/
│   ├── site.db
├── static/
│   ├── anasayfa.css
│   ├── dashboard.css
│   ├── ekleme.css
│   ├── liste.css
│   ├── login.css
│   ├── raporlar.css
│   ├──register.css
├── templates/
│   ├── anasayfa.html
│   ├── base.html
│   ├── dashboard.html
│   ├── duzenle.html
│   ├── ekleme.html
│   ├── liste.html
│   ├── login.html
│   ├── raporlar.html
│   └── register.html
├── app.py
├── db2json.py
├── db3json.py
├── final_versiyon.md
├── personeller.json
├── requirements.txt 
└── users.json
```
## Tasarım Özellikleri

### Renkler
- Primary: Mavi (#0d6efd)
- Success: Yeşil (#198754)
- Info: Açık Mavi (#0dcaf0)
- Warning: Sarı (#ffc107)

### Responsive Tasarım
- Tablet ve masaüstü için optimize edilmiş görünüm: Sayfa, farklı cihaz boyutlarına göre optimize edilmiştir.
- Grid sistemi ile esnek yerleşim: Sayfa elemanları grid sistemi kullanılarak yerleştirilmiştir.

### Kartlar
- Gölgeli tasarım: Kartlar, kullanıcı arayüzüne modern bir görünüm kazandırmak için gölgelendirilmiştir.
- Hover efektleri: Kartlar üzerinde hover efektleri ile görsel etkileşim sağlanır.
- İkon entegrasyonu: Her kartta ve butonlarda simgeler kullanılarak görsel zenginlik sağlanmıştır.
- Badge'ler ile kategori gösterimi: Her personel pozisyonu ve durumu badge'ler ile gösterilmektedir.

### Render Link
https://personnel-tracking-system-re1k.onrender.com/
