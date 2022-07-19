"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Fav_people, Fav_planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_people():
    allpeople = People.query.all() #retorna un arreglo de clases
    allpeople = list(map(lambda elemento: elemento.serialize(), allpeople)) #itero en cada una de las clases y almaceno el resutlado 
    print (allpeople)
    return jsonify({"resultado": allpeople})

@app.route('/planets', methods=['GET'])
def get_planets():
    allplanets = Planets.query.all() #retorna un arreglo de clases
    allplanets = list(map(lambda elemento: elemento.serialize(), allplanets)) #itero en cada una de las clases y almaceno el resutlado 
    print (allplanets)
    return jsonify({"resultado": allplanets})

@app.route('/users', methods=['GET'])
def get_users():
    allusers = User.query.all() #retorna un arreglo de clases
    allusers = list(map(lambda elemento: elemento.serialize(), allusers)) #itero en cada una de las clases y almaceno el resutlado 
    print (allusers)
    return jsonify({"resultado": allusers})

@app.route('/people/<int:id>', methods=['GET'])
def get_one_people(id):
    #bajo un parametro especifico
    #onepeople = People.query.filter_by(id=id).first()
    #return jsonify({"resultado": onepeople})
    #buscar solo por el id
    onepeople = People.query.get(id).serialize()
    #onepeople = onepeople.serialize()
    return jsonify({"resultado": onepeople})

@app.route('/planets/<int:id>', methods=['GET'])
def get_one_planet(id):
    #buscar solo por el id
    oneplanet = Planets.query.get(id)
    if oneplanet:
        oneplanet = Planets.query.get(id).serialize()
        return jsonify({"resultado": oneplanet})

    else:
        return jsonify({"resultado": "El planeta no existe"})

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_fav_people(people_id):
     onepeople = People.query.get(people_id)
     if onepeople:
        new = Fav_people()
        new.user_id = 1
        new.people_id = people_id
        db.session.add(new)
        db.session.commit()

        return jsonify({"mensaje": "todo salio bien"})
     else:
          
        return jsonify({"mensaje": "error"}) 


@app.route('/favorite/planets/<int:planets_id>', methods=['POST'])
def add_fav_planet(planets_id):
     oneplanet = Planets.query.get(planets_id)
     if oneplanet:
        new = Fav_planets()
        new.user_id = 1
        new.planets_id = planets_id
        db.session.add(new)
        db.session.commit()

        return jsonify({"mensaje": "todo salio bien"})
     else:
          
        return jsonify({"mensaje": "error"})  


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
