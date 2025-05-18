import os
from flask import Flask, render_template_string, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# --- Veritabanı Yapılandırması ---
# Ortam değişkenlerinden veritabanı bağlantı bilgilerini alıyoruz
# Bu bilgiler compose.yaml dosyasında tanımlanacak
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:password@db:5432/mydatabase")

# SQLAlchemy için Base oluşturma
Base = declarative_base()

# Blog Yazısı Modeli
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)

    def __repr__(self):
        return f"<Post(username='{self.username}', title='{self.title}')>"

# Veritabanı Motoru Oluşturma
engine = create_engine(DATABASE_URL)

# Veritabanı Tablosunu Oluşturma (Eğer yoksa)
# Docker Compose ilk ayağa kalktığında veritabanı servisi hazır olmayabilir.
# Uygulama başlarken tabloyu oluşturmaya çalışacağız.
def init_db():
    try:
        Base.metadata.create_all(engine)
        print("Veritabanı tabloları oluşturuldu veya zaten mevcut.")
    except Exception as e:
        print(f"Veritabanı bağlantı hatası veya tablo oluşturma hatası: {e}")
        # Hata durumunda uygulama başlangıcında beklemek veya tekrar denemek gerekebilir
        # Bu basit örnekte sadece hata mesajı veriyoruz.

# Session Oluşturma
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Flask Uygulaması ---
app = Flask(__name__)

# Uygulama başladığında veritabanı tablolarını kontrol et/oluştur
with app.app_context():
    init_db()

# HTML Şablonları (Basitlik için doğrudan kod içine gömüldü)
HOME_PAGE_HTML = """
<!doctype html>
<html>
<head><title>Basit Blog</title></head>
<body>
    <h1>Yeni Blog Yazısı Ekle</h1>
    <form method="POST" action="{{ url_for('add_post') }}">
        <label for="username">Kullanıcı Adı:</label><br>
        <input type="text" id="username" name="username" required><br><br>
        <label for="title">Başlık:</label><br>
        <input type="text" id="title" name="title" required><br><br>
        <label for="content">İçerik:</label><br>
        <textarea id="content" name="content" rows="4" cols="50" required></textarea><br><br>
        <input type="submit" value="Yazıyı Ekle">
    </form>

    <hr>

    <h1>Kullanıcıya Göre Yazıları Ara</h1>
    <form method="GET" action="{{ url_for('search_posts') }}">
        <label for="search_username">Kullanıcı Adı:</label><br>
        <input type="text" id="search_username" name="username" required><br><br>
        <input type="submit" value="Ara">
    </form>
</body>
</html>
"""

SEARCH_RESULTS_HTML = """
<!doctype html>
<html>
<head><title>Arama Sonuçları</title></head>
<body>
    <h1>'{{ username }}' Kullanıcısının Yazıları</h1>
    {% if posts %}
        {% for post in posts %}
            <h2>{{ post.title }} (Yazan: {{ post.username }})</h2>
            <p>{{ post.content }}</p>
            <hr>
        {% endfor %}
    {% else %}
        <p>Bu kullanıcıya ait yazı bulunamadı.</p>
    {% endif %}
    <p><a href="{{ url_for('index') }}">Ana Sayfaya Dön</a></p>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(HOME_PAGE_HTML)

@app.route('/add', methods=['POST'])
def add_post():
    session = SessionLocal()
    try:
        username = request.form['username']
        title = request.form['title']
        content = request.form['content']

        new_post = Post(username=username, title=title, content=content)
        session.add(new_post)
        session.commit()
        print(f"Yazı eklendi: Başlık='{title}', Yazar='{username}'")
        return redirect(url_for('index'))
    except Exception as e:
        session.rollback()
        print(f"Yazı eklenirken hata oluştu: {e}")
        return "Yazı eklenirken bir hata oluştu.", 500
    finally:
        session.close()

@app.route('/search', methods=['GET'])
def search_posts():
    username_to_search = request.args.get('username')
    if not username_to_search:
        return redirect(url_for('index')) # Kullanıcı adı yoksa ana sayfaya yönlendir

    session = SessionLocal()
    try:
        posts = session.query(Post).filter_by(username=username_to_search).all()
        return render_template_string(SEARCH_RESULTS_HTML, username=username_to_search, posts=posts)
    except Exception as e:
        print(f"Yazılar aranırken hata oluştu: {e}")
        return "Yazılar aranırken bir hata oluştu.", 500
    finally:
        session.close()

# Flask uygulamasını çalıştırma (Docker'da Gunicorn veya benzeri ile çalıştırılacak)
# Bu kısım sadece lokal test için. Dockerfile'da komut farklı olacak.
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')