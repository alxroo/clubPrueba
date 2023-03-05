from . import fixture
from flask import request,redirect,url_for,render_template,send_from_directory
from werkzeug.utils import secure_filename
import os
from datetime import datetime

from .forms import TeamForm
from .. import db
from ..funciones import allowed_file,getFolder
from ..models import Team,Fixture,Positions
 
@fixture.route("/addTeam",methods=['GET','POST'])
def addTeam():
    form = TeamForm()
    equipos = Team.query.all()

    if request.method == 'POST' and form.validate_on_submit():
        equipo = form.team.data
        #comprueba si la peticion contiene la parte del fichero
        if "img_logo" not in request.files:
            return "El formulario no tiene parte del archivo"
        f = request.files["img_logo"]
        if f.filename == f.filename == "":
            return "Ningun archivo seleccionado"
        if f and allowed_file(f.filename):
            image_name = secure_filename(f.filename)
            f.save(os.path.join(getFolder(),image_name))

        AddEquipo = Team(teamName=equipo)
        AddEquipo.logo = image_name
        db.session.add(AddEquipo)
        db.session.commit()
        return redirect(url_for('fixture.addTeam'))
    return render_template("form_addTeam.html",form=form,equipos = equipos)

@fixture.route("/get_file/<filename>")
def get_file(filename):
    return send_from_directory(getFolder(),filename)

@fixture.route("/updateTeam/<int:id>", methods=['GET','POST'])
def updateTeam(id):
    teamUpdate = Team.query.get_or_404(id)
    form = TeamForm()

    if request.method == 'POST' and form.validate_on_submit():
        
        f = request.files["img_logo"]
        if f.filename != "":
            if "img_logo" not in request.files:
                return "El formulario no tiene parte del archivo"
            
            if f and allowed_file(f.filename):
                image_name = secure_filename(f.filename)
                f.save(os.path.join(getFolder(),image_name))
            teamUpdate.logo = image_name

        teamUpdate.teamName = form.team.data

        db.session.add(teamUpdate)
        db.session.commit()
        return redirect(url_for('fixture.addTeam'))

    
    form.team.data = teamUpdate.teamName
    return render_template('form_updTeam.html',form=form,teamUpdate=teamUpdate)

@fixture.route("/deleteTeam/<int:id>")
def deleteTeam(id):
    teamDelete = Team.query.get_or_404(id)
    db.session.delete(teamDelete)
    db.session.commit()
    return redirect(url_for('fixture.addTeam'))

# -------------------------------------------------------------------------

@fixture.route("/versus",methods=['GET','POST'])
def versus():
    equipos = Team.query.all()
    partidos = Fixture.query.order_by((Fixture.fecha_hora).asc()).all()
    ahora = datetime.now()
    datos = []

    if request.method == 'POST':
        equipoLocal = request.form["equipoLocal"]
        equipoVisita = request.form["equipoVisita"]
        lugar = request.form["lugar"]
        fecha = request.form["fecha"]
        hora = request.form["hora"]
        fecha_hora = datetime.strptime(fecha + " " + hora,'%Y-%m-%d %H:%M')

        registroVersus = Fixture(Local_id=equipoLocal,Visita_id=equipoVisita,lugar=lugar,fecha_hora=fecha_hora,estado="pendiente")
        db.session.add(registroVersus)
        db.session.commit()
        return redirect(url_for('fixture.versus'))
    
    for partido in partidos:
        diferencia =  partido.fecha_hora - ahora
        if diferencia.days < 0 and partido.estado!="culminado" and partido.estado!="cancelado":
            partido.estado = "culminado"
            db.session.add(partido)
            db.session.commit()

        datos.append(diferencia.days)

    return render_template('versus.html',equipos=equipos,partidos=partidos,datos=datos)

@fixture.route("/deleteVersus/<int:id>")
def deleteVersus(id):
    fixtureDelete = Fixture.query.get_or_404(id)
    db.session.delete(fixtureDelete)
    db.session.commit()
    return redirect(url_for('fixture.versus'))

@fixture.route("/add_result/<int:id>",methods=['GET','POST'])
def add_result(id):

    fix = Fixture.query.get_or_404(id)
    if request.method == 'POST':
        golesLocal = request.form["golA"]
        golesVisita = request.form["golB"]

        if golesLocal > golesVisita:
            local = "Victoria"
            visita = "Derrota"
        elif golesLocal < golesVisita:
            local = "Derrota"
            visita = "Victoria"
        elif golesLocal == golesVisita:
            local = "Empate"
            visita = "Empate"

        fix.golLocal =golesLocal
        fix.golVisita = golesVisita
        fix.resLocal= local
        fix.resVisita = visita

        db.session.add(fix)
        db.session.commit()
        return redirect(url_for('fixture.versus'))
    return render_template('form_addResFix.html',fix=fix)

@fixture.route('/cancelfix/<int:id>')
def cancelfix(id):
    fix = Fixture.query.get_or_404(id)
    if fix.estado == "cancelado":
        fix.estado = "culminado"
    else:
        fix.estado = "cancelado"
    db.session.add(fix)
    db.session.commit()
    return redirect(url_for('fixture.versus'))

# -------------------------------------------------------------------------

@fixture.route('/positions')
def positions():
    tablaPosiciones = Positions.query.all()
    equipos = Team.query.all()

    totalGolesA = totalGolesB = EnContraA= EnContraB = 0
    VictoriasA = PerdidasA = EmpatesA = 0
    VictoriasB = PerdidasB = EmpatesB = 0
   
    if tablaPosiciones == []:
        for equipo in equipos:
            tabla = Positions(teamName=equipo.teamName,id_team=equipo.id)
            db.session.add(tabla)
            db.session.commit()
        return redirect(url_for('fixture.positions'))
    else:
        for equipo in equipos:

            resultadosA = Fixture.query.filter_by(Local_id = equipo.id).all()

            for res in resultadosA:
                if res.estado == "culminado":
                    if res.resLocal == "Victoria":
                        VictoriasA = VictoriasA + 1
                    elif res.resLocal == "Empate":
                        EmpatesA = EmpatesA + 1
                    elif res.resLocal == "Derrota":
                        PerdidasA = PerdidasA + 1

                    if res.golLocal is not None:
                        totalGolesA = totalGolesA + res.golLocal
                        EnContraA = EnContraA + res.golVisita

            resultadosB = Fixture.query.filter_by(Visita_id = equipo.id).all()
            for res in resultadosB:
                if res.estado == "culminado":
                    if res.resVisita == "Victoria":
                        VictoriasB = VictoriasB + 1
                    elif res.resVisita == "Empate":
                        EmpatesB = EmpatesB + 1
                    elif res.resVisita == "Derrota":
                        PerdidasB = PerdidasB + 1

                    if res.golVisita is not None:
                        totalGolesB = totalGolesB + res.golVisita
                        EnContraB = EnContraB + res.golLocal
        
            totalGoles = totalGolesA + totalGolesB
            EnContra = EnContraA + EnContraB
            diferencia = totalGoles - EnContra
            Victoria = VictoriasA + VictoriasB
            Empates = EmpatesA + EmpatesB
            Perdidas = PerdidasA + PerdidasB

            equipoAct= Positions.query.filter_by(id_team = equipo.id).first()
            equipoAct.p_ganado = Victoria
            equipoAct.p_empatado = Empates
            equipoAct.p_perdido = Perdidas
            equipoAct.p_jugados = Victoria + Empates + Perdidas
            equipoAct.puntos = Victoria*3 + Empates*1 + Perdidas*0
            equipoAct.gf = totalGoles
            equipoAct.ge = EnContra
            equipoAct.df = diferencia

            db.session.add(equipoAct)
            db.session.commit()

            totalGolesA = totalGolesB = totalGoles = 0
            EnContraA = EnContraB = EnContra = 0
            VictoriasA = PerdidasA = EmpatesA = VictoriasB = PerdidasB = EmpatesB = 0
            Victoria = Perdidas = Empates = 0

    return redirect(url_for('fixture.see_result'))

@fixture.route("/see_result")
def see_result():
    partidos = Fixture.query.order_by((Fixture.fecha_hora).asc()).all()
    fixture = Fixture.query.all()
    tabla = Positions.query.order_by((Positions.puntos).desc(),(Positions.df).desc()).all()

    return render_template('resultados.html',fixture=fixture,tabla=tabla,partidos=partidos)

