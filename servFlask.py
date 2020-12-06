from flask import Flask, render_template, request
import json
import datetime
import MySQLdb

app = Flask(__name__)


startdate='20191202'
enddate='20200409'


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

@app.route('/aserver.ashx')
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
        print (results)
        return json.dumps(results, indent=4, sort_keys=True, default=str)
    except Exception as e:
        print("Error al intentar consultar a la base")
        return(str(e))


@app.route('/data.json')
def data():
    try:
        c, conn = connection()   
        consulta='SELECT Date(Instante), count(*) FROM registros WHERE DATE(Instante) >= %s AND DATE(Instante) <= %s GROUP BY Date(Instante)'
        param=(startdate, enddate)
        c.execute(consulta, param)
        results = c.fetchall()
        print (results)
        return json.dumps(results, indent=4, sort_keys=True, default=str)
    except Exception as e:
        return(str(e))
		
if __name__ == "__main__":
    app.run()