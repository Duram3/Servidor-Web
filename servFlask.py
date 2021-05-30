from flask import Flask, render_template, request
import json
import datetime
import MySQLdb
import collections

class lectura:
    
    def __init__(self, a, b, c):

        self.inicio = a
        self.fin = b
        self.duracion = c

    def hora(self):
        return datetime.datetime.time(self.inicio)


LN=['%FORD%', '%Cisco%', '%tp-link%', '%SHENZHEN%', '%NETGEAR%', '%D-Link%', '%Xerox%', '%Asustek%', '%Belkin%', '%AZURE%']

app = Flask(__name__)


def kmeans(start, end, data):
    i=0
    listaDuracion=[]
    for x in data:
        c, conn = connection()
        cons='select distinct registro.Instante, CONCAT (registro.OUI, registro.OUA) from registro  JOIN tramaspb.mac  ON registro.OUI = mac.oui WHERE CONCAT(registro.OUI, registro.OUA) = %s AND DATE(registro.Instante) >= %s AND DATE(registro.Instante) <= %s'
        parametr=([x[0]], start, end)
        c.execute(cons, parametr)
        impr = c.fetchall()
        duracionInicial=impr[0][0]-impr[0][0]
        dif=duracionInicial.seconds/60
        temp=lectura(impr[0][0], impr[0][0], dif)

        for y in range(1,len(impr)):

            intervalo=impr[y][0]-impr[y-1][0]

            if(intervalo.seconds/60 < 60):

                temp.fin=impr[y][0]
                dif=intervalo.seconds/60
                temp.duracion=temp.duracion+dif
            else:
                i=i+1
                elemento=(temp.hora(), temp.duracion)
                listaDuracion.append(elemento)
                duracionInicial=impr[y][0]-impr[y][0]
                dif=duracionInicial.seconds/60
                temp=lectura(impr[y][0], impr[y][0], dif)
        impr=[]
        c.close
    return listaDuracion




@app.route('/chart')
def home():
	return render_template('chart.html')


def connection():
    conn = MySQLdb.connect(host="localhost",
                           user = "usuario",
                           passwd = "Pql.3Nm.3",
                           db = "tramaspb")
    c = conn.cursor()

    return c, conn

@app.route('/diatodos')
def recibir():
    startdate = request.args.get('start','')
    enddate = request.args.get('end','')
    print(startdate)
    print(enddate)
    try:
        c, conn = connection()
        consulta='SELECT Date(Instante), count(*) FROM registro WHERE DATE(Instante) >= %s AND DATE(Instante) <= %s GROUP BY Date(Instante)'
        param=(startdate, enddate)
        c.execute(consulta, param)
        results = c.fetchall()
        return json.dumps(results, indent=4, sort_keys=True, default=str)
    except Exception as e:
        print("Error al intentar consultar a la base 1")
        return(str(e))
    finally:
        c.close

@app.route('/diamovil')
def recibirI():
    startdate = request.args.get('start','')
    enddate = request.args.get('end','')
    print(startdate)
    print(enddate)
    try:
        c, conn = connection()
        consulta='SELECT Date(registro.Instante), count(*) FROM registro JOIN mac ON registro.OUI = mac.oui WHERE DATE(registro.Instante) >= %s AND DATE(registro.Instante) <= %s AND mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s GROUP BY Date(registro.Instante)'
        param=(startdate, enddate, LN[0], LN[1], LN[2], LN[3], LN[4], LN[5], LN[6], LN[7], LN[8], LN[9])
        c.execute(consulta, param)
        results = c.fetchall()
        return json.dumps(results, indent=4, sort_keys=True, default=str)
    except Exception as e:
        print("Error al intentar consultar a la base 2")
        return(str(e))
    finally:
        c.close

@app.route('/ouitodos')
def recibir2():
    startdate = request.args.get('start','')
    enddate = request.args.get('end','')
    try:
        c, conn = connection()
        consulta='SELECT mac.nombre, COUNT(registro.OUI) FROM registro JOIN tramaspb.mac ON registro.OUI = mac.oui WHERE DATE(registro.Instante) >= %s AND DATE(registro.Instante) <= %s group by mac.nombre'
        param=(startdate, enddate)
        c.execute(consulta, param)
        results = c.fetchall()
        return json.dumps(results, indent=4, sort_keys=True, default=str)
    except Exception as e:
        print("Error al intentar consultar a la base 3")
        return(str(e))
    finally:
        c.close

@app.route('/ouimoviles')
def recibir4():
    startdate = request.args.get('start','')
    enddate = request.args.get('end','')
    try:
        c, conn = connection()
        consulta='SELECT mac.nombre, COUNT(registro.OUI) FROM registro JOIN tramaspb.mac ON registro.OUI = mac.oui WHERE DATE(registro.Instante) >= %s AND DATE(registro.Instante) <= %s AND mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s group by mac.nombre'
        param=(startdate, enddate, LN[0], LN[1], LN[2], LN[3], LN[4], LN[5], LN[6], LN[7], LN[8], LN[9])
        c.execute(consulta, param)
        results = c.fetchall()
        return json.dumps(results, indent=4, sort_keys=True, default=str)
    except Exception as e:
        print("Error al intentar consultar a la base 4")
        return(str(e))
    finally:
        c.close

@app.route('/dispmoviles')
def recibir5():
    startdate = request.args.get('start','')
    enddate = request.args.get('end','')
    try:
        c, conn = connection()
        consulta='SELECT CONCAT (registro.OUI, registro.OUA), COUNT(registro.OUA) FROM registro JOIN tramaspb.mac ON registro.OUI = mac.oui WHERE DATE(registro.Instante) >= %s AND DATE(registro.Instante) <= %s AND mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s GROUP BY registro.OUA'
        param=(startdate, enddate, LN[0], LN[1], LN[2], LN[3], LN[4], LN[5], LN[6], LN[7], LN[8], LN[9])
        c.execute(consulta, param)
        results = c.fetchall()
        return json.dumps(results, indent=4, sort_keys=True, default=str)
    except Exception as e:
        print("Error al intentar consultar a la base 4")
        return(str(e))
    finally:
        c.close

@app.route('/all.ashx')
def recibir3():
    startdate = request.args.get('start','')
    enddate = request.args.get('end','')
    try:
        c, conn = connection()
        consulta='SELECT Instante, OUA FROM registro WHERE DATE(registro.Instante) >= %s AND DATE(registro.Instante) <= %s'
        param=(startdate, enddate)
        c.execute(consulta, param)
        results = c.fetchall()
        objects_list = []
        for row in results:
            d = collections.OrderedDict()
            d['Instante'] = row[0]
            d['OUA'] = row[1]
            objects_list.append(d)
        return json.dumps(objects_list, indent=4, sort_keys=True, default=str)
    except Exception as e:
        print("Error al intentar consultar a la base 5")
        return(str(e))
    finally:
        c.close

@app.route('/dwell')
def dwell():
    startdate = request.args.get('start','')
    enddate = request.args.get('end','')
    try:
            c, conn = connection()
            consulta='SELECT distinct CONCAT(registro.OUI, registro.OUA) FROM registro JOIN tramaspb.mac ON registro.OUI = mac.oui WHERE DATE(registro.Instante) >= %s and DATE(registro.Instante) <= %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s and mac.nombre NOT LIKE %s'
            param=(startdate, enddate, LN[0], LN[1], LN[2], LN[3], LN[4], LN[5], LN[6], LN[7], LN[8], LN[9])
            c.execute(consulta, param)
            results = c.fetchall()
            lista=[]
            lista=kmeans(startdate, enddate, results)
            lista.sort()
            c.close
            print(json.dumps(lista, indent=4, sort_keys=True, default=str))  
            return json.dumps(lista, indent=4, sort_keys=True, default=str)
    except Exception as e:
            print("Error al intentar consultar a la base tramaspb")
            c.close
    finally:
            results=[]
		
if __name__ == "__main__":
    app.run()
