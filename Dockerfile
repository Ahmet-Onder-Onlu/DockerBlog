# Python 3.9 (veya istediğiniz bir sürüm) üzerine kurulur
FROM python:3.9-slim

# Çalışma dizinini belirler
WORKDIR /app

# Gereksinimler dosyasını kopyalar
COPY requirements.txt .

# Gerekli kütüphaneleri yükler
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyalar
COPY app/ /app/

# Flask uygulamasının çalışacağı portu belirtir
EXPOSE 5000

# Uygulamayı Gunicorn ile başlatır
# Gunicorn, Flask uygulamasını production sınıfı bir web sunucusu gibi çalıştırır.
# Flask'ın kendi sunucusu (app.run) geliştirme amaçlıdır.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]