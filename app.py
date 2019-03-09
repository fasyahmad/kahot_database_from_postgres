from flask  import Flask, jsonify, request, json, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models import Laptop

app = Flask (__name__)

POSTGRES = {
        'user': 'postgres',
        'pw': 'fasyaemad03',
        'db': 'postgres',
        'host': 'localhost',
        'port': '5432'
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# postgresql://username:password@localhost:5432/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db.init_app(app)

@app.route('/')
def main():
    return 'Hello World!'

@app.route('/getAllModel', methods=["GET"])
def get_all_model():
        try:
                laptop = Laptop.query.order_by(Laptop.serial_number).all()
                return jsonify([cstr.serialize() for cstr in laptop])
        except Exception as e:
                return (str(e))

@app.route('/getModelSerialNumberBy/<id_>', methods=["GET"])
def get_laptop_serial_number(id_):
    try:
        laptop=Laptop.query.filter_by(serial_number=id_).first()
        return jsonify(laptop.serialize())
    except Exception as e:
        return(str(e))

@app.route('/addCModel', methods=["POST"])
def add_model():
    model=request.args.get('model')
    serial_number=request.args.get('serial_number')
    harga=request.args.get('harga')
    kapasitas_memory=request.args.get('kapasitas_memory')

    try:
        laptop=Laptop(
            model=model,
            serial_number=serial_number,
            harga=harga,
            kapasitas_memory=kapasitas_memory
        )

        db.session.add(laptop)
        db.session.commit()
        return "Laptop added. laptop id={}".format(laptop.serial_number)

    except Exception as e:
        return(str(e))

@app.route('/deleteModel/<id_>', methods=["DELETE"])
def delete_model(id_):
    try:
        laptop =  Laptop.query.filter_by(serial_number=id_).first()
        db.session.delete(laptop)
        db.session.commit()
        return 'laptop delete'
    except Exception as e:
        return(str(e))

@app.route('/updateModel/<id_>', methods=["PUT"])
def update_model(id_):
    model_existing = get_laptop_serial_number(id_).json
    
    if request.args.get('model') == None:
        model = model_existing['model']
    else:
        model = request.args.get('model')
    if request.args.get('serial_number') == None:
        serial_number = model_existing['serial_number']
    else:
        serial_number = request.args.get('serial_number')
    if request.args.get('harga') == None:
        harga = model_existing['harga']
    else:
        harga = request.args.get('harga')
    if request.args.get('kapasitas_memory') == None:
        kapasitas_memory = model_existing['kapasitas_memory']
    else:
        kapasitas_memory = request.args.get('kapasitas_memory')

    try:
        laptopUpdate = {
            'model' : model,
            'serial_number' : serial_number,
            'harga' : harga,
            'kapasitas_memory' : kapasitas_memory
        }
        laptop = Laptop.query.filter_by(serial_number=id_).update(laptopUpdate)
        db.session.commit()
        return 'update laptop'
    except Exception as e:
        return(str(e))

if __name__ == '__main__':
    app.run()