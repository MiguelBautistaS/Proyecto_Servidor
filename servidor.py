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

    query = 'select nrc, id_clave, id_seccion, id_detalle, id_profesor, carrera from oferta'
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

        creditos = detalle[0][1]
        ct = detalle[0][2]
        cd = detalle[0][3]

        query3 = 'select * from clave where id = %s'
        cursor.execute(query3, (id_clave,))
        cla = cursor.fetchall()

        clave = cla[0][1]
        materia = cla[0][2]


        query4 = 'select id_horario from horarios where nrc = %s'
        cursor.execute(query4, (nrc,))
        id_h = cursor.fetchall()
        id_horarios = []

        for i in id_h:
            id_horarios.append(i[0])

        query5 = 'select id_dia from dias where nrc = %s'
        cursor.execute(query5, (nrc,))
        id_d = cursor.fetchall()

        query6 = 'select id_aula from aulas where nrc = %s'
        cursor.execute(query6, (nrc,))
        id_a = cursor.fetchall()

        horarios = []
        for id_horario in id_horarios:
            query7 = 'select * from horario where id = %s'
            cursor.execute(query7, (id_horario,))
            hr = cursor.fetchall()

            query7_1 = 'select * from hora where id = %s'
            cursor.execute(query7_1, (hr[0][0],))
            h1 = cursor.fetchall()

            query7_1 = 'select * from hora where id = %s'
            cursor.execute(query7_1, (hr[0][1],))
            h2 = cursor.fetchall()

            query7_1 = 'select * from periodo where id = %s'
            cursor.execute(query7_1, (hr[0][2],))
            pe = cursor.fetchall()
            periodo = pe[0][1]

            horario ={
                'hi': h1[0][1],
                'hf': h2[0][1],
                'periodo': periodo
            }
            horarios.append(horario)

        id_dias = []
        for i in id_d:
            id_dias.append(i[0])

        dias = []
        for id_dia in id_dias:
            query8 = 'select dia from dia where id = %s'
            cursor.execute(query8, (id_dia,))
            di = cursor.fetchall()
            dia = {
                'dia': di[0][0]
            }
            dias.append(dia)

        id_aulas = []
        for i in id_a:
            id_aulas.append(i[0])

        aulas = []
        edificios = []
        for id_aula in id_aulas:
            query9 = 'select aula, edificio from aula where id = %s'
            cursor.execute(query9, (id_aula,))
            au = cursor.fetchall()

            query10 = 'select edificio from edificio where id = %s'
            cursor.execute(query10, (au[0][1],))
            edificio = cursor.fetchall()

            aula = {
                'aula': au[0][0]
            }
            edificio = {
                'edificio': edificio[0][0]
            }
            aulas.append(aula)
            edificios.append(edificio)

        query11 = 'select seccion from seccion where id = %s'
        cursor.execute(query11, (id_seccion,))
        sec = cursor.fetchall()
        seccion = sec[0][0]

        query12 = 'select nombre from profesor where id = %s'
        cursor.execute(query12, (id_profesor,))
        pro = cursor.fetchall()
        profesor = pro[0][0]

        count = len(id_dias)

        infos = []
        for i in range(count-1):
            info = {
                'horario': horarios[i],
                'dia':dias[i],
                'aula':aulas[i],
                'edificio': edificios[i]
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
            'seccion': seccion,
            'profesor':profesor,
            'horarios': infos
        }

        lista_materias.append(materia)
    return jsonify(ofertas = lista_materias)
app.run()
