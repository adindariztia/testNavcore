from flask import Flask, request, json, session, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_restful import marshal, fields
from requests.utils import quote
import requests
import datetime
import os
import jwt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:adinda@localhost:5432/pemilu'
app.config['SECRET_KEY'] = os.urandom(24)
CORS(app, support_credentials=True)
db = SQLAlchemy(app)
jwtSecretKey = "companysecret"
db = SQLAlchemy(app)

class Pemilih(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nama = db.Column(db.String)
    no_ktp = db.Column(db.Integer)

class Calondpr(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nama = db.Column(db.String)

class Calonpresiden(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nama = db.Column(db.String)

class Perolehandpr(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    pemilih = db.Column(db.Integer, db.ForeignKey('pemilih.id'))
    dpr_terpilih = db.Column(db.Integer, db.ForeignKey('calondpr.id'))

class Perolehanpresiden(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    pemilih = db.Column(db.Integer, db.ForeignKey('pemilih.id'))
    presiden_terpilih = db.Column(db.Integer, db.ForeignKey('calonpresiden.id'))

@app.route('/login', methods=['POST'])
def login():
    request_data = request.get_json()

    req_nama = request_data.get('nama')
    req_ktp = request_data.get('ktp')
    userDB = Pemilih.query.filter_by(nama=req_nama, no_ktp= req_ktp).first()
    if userDB:
        payload = {
            "name": userDB.nama
        }
        encoded_jwt = jwt.encode(payload, jwtSecretKey, algorithm='HS256')
        return encoded_jwt, 200
@app.route('/votedpr', methods=['POST'])
def votedpr():
    request_data = request.get_json()
    decoded = jwt.decode(request.headers["Authorization"], jwtSecretKey, algorithm=['HS256'])
    name = decoded['name']
    userDB = Pemilih.query.filter_by(nama=name).first()

    if name and userDB:
        alreadyVoted = Perolehandpr.query.filter_by(pemilih=userDB.id).first()
        if alreadyVoted:
            return "Anda sudah menggunakan Hak suara Anda!", 400
        voting = Perolehandpr(
            pemilih = userDB.id,
            dpr_terpilih = request_data.get('pilihan')
        )
        db.session.add(voting)
        db.session.commit()
        return 'sudah tervote', 201
    else:
        return "Silahkan Login terlebih dahulu"

@app.route('/votepresiden', methods=['POST'])
def votePresiden():
    request_data = request.get_json()
    decoded = jwt.decode(request.headers["Authorization"], jwtSecretKey, algorithm=['HS256'])
    name = decoded['name']
    userDB = Pemilih.query.filter_by(nama=name).first()

    if name and userDB:
        alreadyVoted = Perolehandpr.query.filter_by(pemilih=userDB.id).first()
        if alreadyVoted:
            return "Anda sudah menggunakan Hak suara Anda!", 400
        voting = Perolehanpresiden(
            pemilih = userDB.id,
            presiden_terpilih = request_data.get('pilihan')
        )
        db.session.add(voting)
        db.session.commit()
        return "sudah tervote", 201
    else:
        return "Gagal"

@app.route('/hitungdpr', methods=['POST'])
def hitungdpr():
    request_data = request.get_json()

    calon_dpr = request_data.get('caleg')
    perolehanSuara = Perolehandpr.query.filter_by(dpr_terpilih=calon_dpr).count()
    return str(perolehanSuara)

@app.route('/hitungpresiden', methods=['POST'])
def hitungpresiden():
    request_data = request.get_json()
    calon_presiden = request_data.get('capres')
    perolehanSuara = Perolehanpresiden.query.filter_by(presiden_terpilih= calon_presiden).count()
    return str(perolehanSuara)

@app.route('/tampilkancaleg')
def tampilkandpr():
    listDpr = Calondpr.query.all()

    if listDpr:
        dprDetail = {
            "id": fields.Integer,
            "nama": fields.String
        }

        return (json.dumps(marshal(listDpr,dprDetail)))


if __name__ == '__main__':
    app.run(debug=True, host=os.getenv("HOST"), port=os.getenv("PORT"))
