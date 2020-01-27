from flask import Flask
from flask_mqtt import Mqtt
from flask_sqlalchemy import SQLAlchemy
import json
import datetime
import eventlet

app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = '127.0.0.1'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False
app.config['SECRET_KEY'] = 'clave secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://yoel:micontraseña@localhost:3306/recibido'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
mqtt = Mqtt(app)

#De modelos import Datos

class Datos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    piso = db.Column(db.String(20), nullable=False)
    zona = db.Column(db.String(20), nullable=False)
    mac = db.Column(db.String(20),  nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    


@app.route('/')
def index():
    print('Home')


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("intentando aqui")
    mqtt.subscribe('1/A')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(topic=message.topic, payload=message.payload.decode())
    jdata = json.loads(message.payload.decode())
    dato = Datos(
		piso=jdata["piso"],
		zona=jdata["zona"],
		mac=jdata["MAC"],
        fecha=datetime.datetime.now())
    db.session.add(dato)  # Se añade nuevo dato a la base
    db.session.commit()  # COMMIT de los datos
     
   


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    if level == MQTT_LOG_ERR:
        print('Error: {}'.format(buf))


if __name__ == '__main__':
    app.run(port = 5000, debug =True)