from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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

def export_user_to_json():
    with app.app_context():
        db.create_all()
        users = Personel.query.all()

        data = [user.to_dict() for user in users]

        json_path = os.path.join(os.path.dirname(__file__), 'personeller.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Toplam {len(data)} kullanıcı başarıyla {json_path} dosyasına kaydedildi.")

if __name__ == '__main__':
    export_user_to_json()
