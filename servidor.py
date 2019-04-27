from flask import Flask, jsonify
app = Flask(__name__)

import mysql.connector

conexion = mysql.connector.connect(
    user = 'miguel',
    password = '12345',
    database = 'materias'
)

cursor = conexion.cursor()

@app.route("/api/v1/materias/")
def hello():
    query = "SELECT oferta.nrc, clave.clave, clave.materia, seccion.seccion, profesor.nombre, detalle.creditos, detalle.cupos_totales, detalle.cupos_disponibles, dia.identificador, dia.dia, oferta.carrera FROM dias left join oferta on oferta.nrc = dias.nrc left join clave on clave.id = oferta.id_clave left join seccion on seccion.id = oferta.id_seccion left join profesor on profesor.id = oferta.id_profesor left join detalle on detalle.id = oferta.id_detalle left join dia on dia.id = dias.id_dia"
    cursor.execute(query)
    ofertas = cursor.fetchall()

    lista_ofertas = []
    for oferta in ofertas:
        query2 = "SELECT hora.hora from horarios left join horario on horario.id = horarios.id_horario left join hora on hora.id = horario.hora_inicial left join oferta on oferta.nrc = horarios.nrc where oferta.nrc =" + str(oferta[0])
        cursor.execute(query2)
        horaI = cursor.fetchall()
        query3 = "SELECT hora.hora from horarios left join horario on horario.id = horarios.id_horario left join hora on hora.id = horario.hora_final left join oferta on oferta.nrc = horarios.nrc where oferta.nrc =" + str(oferta[0])
        cursor.execute(query3)
        horaF = cursor.fetchall()
        query4 = "SELECT periodo.periodo from horarios left join horario on horario.id = horarios.id_horario left join periodo on periodo.id = horario.periodo left join oferta on oferta.nrc = horarios.nrc where oferta.nrc =" + str(oferta[0])
        cursor.execute(query4)
        per = cursor.fetchall()
        query5 = "SELECT aula.aula from aulas left join aula on aula.id = aulas.id_aula left join oferta on oferta.nrc = aulas.nrc where oferta.nrc =" + str(oferta[0])
        cursor.execute(query5)
        au = cursor.fetchall()
        query6 = "SELECT edificio.edificio from edificios left join edificio on edificio.id = edificios.id_edificio left join oferta on oferta.nrc = edificios.nrc where oferta.nrc =" + str(oferta[0])
        cursor.execute(query6)
        edif = cursor.fetchall()

        c = {
            'nrc': oferta[0],
            'carrera': oferta[10],
            'clave': oferta[1],
            'materia': oferta[2],
            'seccion': oferta[3],
            'profesor': oferta[4],
            'creditos': oferta[5],
            'cupos_totales': oferta[6],
            'cupos_disponibles': oferta[7],
            'dia':oferta[8],
            'dia_iden':oferta[9],
            'hora_inicial':horaI[0],
            'hora_final':horaF[0],
            'periodo':per[0],
            'edificio': edif[0],
            'aula':au[0]
        }

        lista_ofertas.append(c)
    return jsonify(ofertas = lista_ofertas)

app.run()