from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import datetime
from db2json import export_user_to_json
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gelistirme_anahtari' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) 
login_manager = LoginManager(app)  
login_manager.login_view = 'login' 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    personeller = db.relationship('Personel', backref='user', lazy=True)  

class Personel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    ad = db.Column(db.String(100), nullable=False)
    soyad = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    pozisyon = db.Column(db.String(100), nullable=False)
    maas = db.Column(db.Float, nullable=False)
    ise_baslama_tarihi = db.Column(db.Date, nullable=False)
    giris_zamani = db.Column(db.Time, nullable=False)
    cikis_zamani = db.Column(db.Time, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "ad": self.ad,
            "soyad": self.soyad,
            "email": self.email,
            "pozisyon": self.pozisyon,
            "maas": self.maas,
            "ise_baslama_tarihi": self.ise_baslama_tarihi.isoformat() if self.ise_baslama_tarihi else None,
            "giris_zamani": self.giris_zamani.strftime("%H:%M:%S") if self.giris_zamani else None,
            "cikis_zamani": self.cikis_zamani.strftime("%H:%M:%S") if self.cikis_zamani else None,
        }

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    if current_user.is_authenticated: 
        logout_user() 
    return render_template('anasayfa.html')

@app.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        print(f"Gelen email: {email}, şifre: {password}")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))  
        flash('E-posta veya şifre hatalı!', 'danger')  

    return render_template('login.html')  

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        if User.query.filter_by(email=email).first():
            flash('Bu e-posta zaten kayıtlı!', 'danger')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        export_user_to_json()
        flash('Kayıt başarılı! Giriş yapabilirsiniz.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/ekleme', methods=['GET', 'POST'])
@login_required
def ekleme():
    if request.method == 'POST':
        ad = request.form.get('ad')
        soyad = request.form.get('soyad')
        email = request.form.get('email')
        pozisyon = request.form.get('pozisyon')
        maas = float(request.form.get('maas'))
        ise_baslama_tarihi = datetime.strptime(request.form.get('ise_baslama_tarihi'), '%Y-%m-%d').date()
        giris_zamani = datetime.strptime(request.form.get('giris_zamani'), '%H:%M').time()
        cikis_zamani = datetime.strptime(request.form.get('cikis_zamani'), '%H:%M').time()

        yeni_personel = Personel(
            user_id=current_user.id, 
            ad=ad, soyad=soyad, email=email, pozisyon=pozisyon, maas=maas,
            ise_baslama_tarihi=ise_baslama_tarihi, giris_zamani=giris_zamani, cikis_zamani=cikis_zamani
        )
        db.session.add(yeni_personel)
        db.session.commit()

        export_personel_to_json()  # JSON dosyasını güncelle

        flash('Personel başarıyla eklendi!', 'success')
        return redirect(url_for('liste'))

    return render_template('ekleme.html')

@app.route('/liste')
@login_required
def liste():
    personeller = Personel.query.filter_by(user_id=current_user.id).all()  
    return render_template('liste.html', personeller=personeller)

@app.route('/raporlar')
@login_required
def raporlar():
    personeller = Personel.query.filter_by(user_id=current_user.id).all()

    toplam_maas = sum([personel.maas for personel in personeller])
    ortalama_maas = round(toplam_maas / len(personeller), 2) if personeller else 0

    pozisyon_dagilimi = {}
    for personel in personeller:
        pozisyon_dagilimi[personel.pozisyon] = pozisyon_dagilimi.get(personel.pozisyon, 0) + 1

    sirali_personeller = sorted(personeller, key=lambda x: x.ise_baslama_tarihi)

    return render_template(
        'raporlar.html',
        personeller=personeller,
        ortalama_maas=ortalama_maas,
        pozisyon_dagilimi=pozisyon_dagilimi,
        sirali_personeller=sirali_personeller
    )

@app.route('/dashboard')
@login_required
def dashboard():
    personeller = Personel.query.filter_by(user_id=current_user.id).all()
    
    ortalama_maas = round(sum(p.maas for p in personeller) / len(personeller), 2) if personeller else 0

    son_personel = personeller[-1] if personeller else None

    from datetime import datetime, timedelta
    toplam_sure = timedelta()
    for p in personeller:
        giris = datetime.combine(datetime.today(), p.giris_zamani)
        cikis = datetime.combine(datetime.today(), p.cikis_zamani)
        toplam_sure += (cikis - giris)
    ortalama_sure = str((toplam_sure / len(personeller)).seconds // 3600) + " saat" if personeller else "0 saat"

    return render_template('dashboard.html', personeller=personeller, ortalama_maas=ortalama_maas,
                           son_personel=son_personel, ortalama_sure=ortalama_sure)

@app.route('/duzenle/<int:personel_id>', methods=['GET', 'POST'])
@login_required
def duzenle(personel_id):
    personel = Personel.query.get_or_404(personel_id)

    if personel.user_id != current_user.id:
        flash("Bu personele erişim yetkiniz yok!", "danger")
        return redirect(url_for('liste'))

    if request.method == 'POST':
        personel.ad = request.form['ad']
        personel.soyad = request.form['soyad']
        personel.email = request.form['email']
        personel.pozisyon = request.form['pozisyon']
        personel.maas = float(request.form['maas'])
        personel.ise_baslama_tarihi = datetime.strptime(request.form['ise_baslama_tarihi'], '%Y-%m-%d').date()
        personel.giris_zamani = datetime.strptime(request.form['giris_zamani'], '%H:%M').time()
        personel.cikis_zamani = datetime.strptime(request.form['cikis_zamani'], '%H:%M').time()

        db.session.commit()
        flash("Personel bilgileri güncellendi!", "success")
        return redirect(url_for('liste'))

    return render_template('duzenle.html', personel=personel)

@app.route('/logout')
@login_required
def logout():
    logout_user() 
    return redirect(url_for('home')) 

@app.route('/sil/<int:personel_id>', methods=['POST'])
@login_required
def sil(personel_id):
    print(f"Silinecek personel ID: {personel_id}") 

    personel = Personel.query.get(personel_id)
    if not personel:
        flash('Hata: Personel bulunamadı!', 'danger')
        return redirect(url_for('dashboard'))
    
    db.session.delete(personel)
    db.session.commit()
    flash('Personel başarıyla silindi!', 'success')
    return redirect(url_for('dashboard'))

def export_personel_to_json():
    with app.app_context():
        personeller = Personel.query.all()
        data = [personel.to_dict() for personel in personeller]
        
        json_path = os.path.join(os.path.dirname(__file__), 'personeller.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Toplam {len(data)} personel başarıyla {json_path} dosyasına kaydedildi.")

#if _name_ == '_main_':
#    with app.app_context():
#        db.create_all()
#    app.run(debug=True)

import os
if __name__ == '__main__': 
    app.run(host=0.0.0.0, port =int(os.environ.get("PORT",5000)))
