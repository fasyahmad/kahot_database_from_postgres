import datetime
from flask_sqlalchemy import SQLAlchemy
from app import db

# db = SQLAlchemy()

class Laptop(db.Model):
    tablename = 'customer'

    serial_number = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String())
    harga = db.Column(db.Integer())
    kapasitas_memory = db.Column(db.Integer())
    # created_on = db.Column(db.DateTime, default=datetime.datetime.now())


    def __init__(self, model, serial_number, harga, kapasitas_memory):
        self.model = model
        self.serial_number = serial_number
        self.harga = harga
        self.kapasitas_memory = kapasitas_memory 

    def __repr__(self):
        return '<serial number {}>'.format(self.serial_number)
    
    def serialize(self):
        return{
            'model': self.model,
            'serial_number': self.serial_number,
            'harga': self.harga,
            'kapasitas_memory': self.kapasitas_memory
        }
