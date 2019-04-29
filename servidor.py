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

    query = 'select * from oferta'
    cursor.execute(query)
    ofertas = cursor.fetchall()
    lista_materias = []

    for oferta in ofertas:
        nrc = oferta[0]
        id_clave = oferta[1]
        id_seccion = oferta[2]
        id_detalle = oferta[3]
        id_profesor = oferta[4]
        carrera = oferta[5]

        query2 = 'select * from detalle where nrc = %s'
        cursor.execute(query2, (nrc,))
        detalle = cursor.fetchall()

        creditos = detalle[1]
        ct = detalle[2]
        cd = detalle[3]

        query3 = 'select clave, materia from clave where id = %s'
        cursor.execute(query3, (id_clave,))
        cla = cursor.fetchall()

        clave = cla[0]
        materia = cla[1]


        query4 = 'select id_horario from horarios where nrc = %s'
        cursor.execute(query4, (nrc,))
        id_horarios = cursor.fetchall()

        query5 = 'select id_dia from dias where nrc = %s'
        cursor.execute(query5, (nrc,))
        id_dias = cursor.fetchall()

        query6 = 'select id_aula from aulas where nrc = %s'
        cursor.execute(query6, (nrc,))
        id_aulas = cursor.fetchall()

        horarios =[]
        for id_horario in id_horarios:
            query7 = 'select * from horario where id = %s'
            cursor.execute(query7, (id_horario,))
            hr = cursor.fetchall()
            horario ={
                'hi': hr[1],
                'hf': hr[2],
                'periodo': hr[3]
            }
            horarios.append(horario)

        dias = []
        for id_dia in id_dias:
            query8 = 'select dia from dia where id = %s'
            cursor.execute(query8, (id_dia,))
            di = cursor.fetchall()
            dia = {
                'dia': di[0]
            }
            dias.append(dia)


        aulas = []
        for id_aula in id_aulas:
            query9 = 'select aula, edificio from aula where id = %s'
            cursor.execute(query9, (id_aula,))
            au = cursor.fetchall()

            query10 = 'select edificio from edificio where id = %s'
            cursor.execute(query10, (au[1],))
            edificio = cursor.fetchall()

            aula = {
                'aula': au[0],
                'edificio': edificio
            }
            aulas.append(aula)

        count = len(id_dias)

        infos = []
        for i in range(count):
            info = {
                'horario': horarios[i],
                'dia':dias[i],
                'aula':aulas[i]
            }
            infos.append(info)

        materia ={
            'nrc':nrc,
            'carrera':carrera,
            'creditos':creditos,
            'cupos_totales':ct,
            'cupos_disponibles': cd,
            'clave': clave,
            'materia':materia,
            'horarios': infos
        }

        lista_materias.append(materia)
    return jsonify(ofertas = lista_materias)
app.run()