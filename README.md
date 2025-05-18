# Basit Docker Blog Projesi (Flask + PostgreSQL)

Bu proje, Python Flask web uygulaması ile PostgreSQL veritabanını Docker konteynerleri kullanarak bir araya getiren basit bir blog sistemidir. Kullanıcılar blog yazıları ekleyebilir ve kullanıcı adına göre yazıları arayabilir.

Proje, çoklu servisli Docker uygulamalarının temelini ve Docker Compose kullanımı, network, volume ve ortam değişkenleri gibi konuları öğrenmek amacıyla oluşturulmuştur.

## Özellikler

* Basit web arayüzü ile blog yazısı ekleme (Kullanıcı Adı, Başlık, İçerik).
* Kullanıcı adına göre blog yazısı arama ve listeleme.
* Veritabanı verilerinin kalıcılığı (Docker Volume kullanarak).
* Servisler arası iletişim (Docker Network kullanarak).
* Yapılandırma (Ortam Değişkenleri kullanarak).
* Docker Compose ile kolay kurulum ve yönetim.

## Ön Gereksinimler

Bu projeyi çalıştırmak için sisteminizde aşağıdakilerin kurulu olması gerekmektedir:

* [Docker](https://www.docker.com/get-started/)
* [Docker Compose](https://docs.docker.com/compose/install/)
* [Git](https://git-scm.com/downloads)

## Kurulum ve Çalıştırma

1. **Depoyu Klonlayın:**

   ```bash
   git clone <Projenizin GitHub Depo URL'si BURAYA>
   cd my-docker-blog-project # Klonladığınız klasöre gidin
   ```

   *(Not: `<Projenizin GitHub Depo URL'si BURAYA>` kısmını kendi GitHub depo URL'niz ile değiştirin.)*
2. **Docker Compose ile Sistemi Ayağa Kaldırın:**
   Proje klasörünüzdeyken aşağıdaki komutu çalıştırın:

   ```bash
   docker-compose up -d
   ```

   Bu komut:

   * Docker Hub'dan `postgres:13` imajını çekecektir (eğer yoksa).
   * Docker Hub'dan web uygulaması imajını (`sizin_dockerhub_kullanici_adiniz/my-docker-blog-web:latest`) çekecektir.
   * `db-data` adında bir Docker Volume oluşturacaktır (eğer yoksa).
   * `my-app-network` adında bir Docker Network oluşturacaktır (eğer yoksa).
   * `db` (PostgreSQL) ve `web` (Flask Uygulaması) servislerini başlatacaktır.
3. **Uygulamaya Erişim:**
   Sistem tamamen başladıktan sonra web tarayıcınızı açın ve `http://localhost:5000` adresine gidin.

## Kullanım

* Ana sayfada blog yazısı ekleme formunu göreceksiniz. Gerekli bilgileri doldurup yazı ekleyebilirsiniz.
* Aynı sayfadaki arama formuna kullanıcı adı girerek o kullanıcıya ait yazıları listeleyebilirsiniz.

## Proje Yapısı

my-docker-blog-project/
├── app/                 # Flask uygulama kodları
│   └── app.py           # Ana Flask uygulaması
├── Dockerfile           # Web uygulaması için Docker imajı build talimatları
├── requirements.txt     # Flask uygulamasının bağımlılıkları
├── compose.yaml         # Docker Compose yapılandırma dosyası
├── .dockerignore        # Docker build sırasında ignore edilecek dosyalar
├── README.md            # Proje açıklaması (bu dosya)
├── LICENSE              # Proje lisansı
├── CONTRIBUTING.md      # Katkıda bulunma yönergeleri
├── NOTICE.md            # Ek bildirimler (isteğe bağlı)
└── CODE_OF_CONDUCT.md   # Davranış Kuralları


## Katkıda Bulunma

Projeye katkıda bulunmak isterseniz lütfen [CONTRIBUTING.md](CONTRIBUTING.md) dosyasındaki yönergelere göz atın.

## Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır. Lisans detayları için [LICENSE](LICENSE) dosyasına bakınız.

## İletişim

Sorularınız veya önerileriniz için lütfen bu depo üzerinden bir "Issue" açmaktan çekinmeyin.
