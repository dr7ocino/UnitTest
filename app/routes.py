from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from .controllers.operaciones_conductor import *
from app.events import emitir_uid
main = Blueprint("main", __name__)
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/registrar-conductor', methods=['GET'])
def viewFormEmpleado():
    return render_template('conductores/registro.html')

@main.route('/form-registrar-empleado', methods=['POST'])
def formEmpleado():   
    resultado = procesar_form_empleado(request.form)
    if resultado == 1:
        flash('Agregado exitosamente', 'success')
    else :
        uid = request.form['uid']
        flash(f'El uid {uid} ya se encuentra registrado','error')
    return redirect(url_for('main.viewFormEmpleado'))
    #return render_template('conductores/registro.html')

@main.route('/lista-de-conductores', methods=['GET'])
def lista_empleados():   
    return render_template('conductores/listado.html', empleados=lista_empleadosBD())

@main.route('/detalles-conductor', methods=['GET'])
@main.route('/detalles-conductor/<string:idConductor>', methods=['GET'])
def detalle_conductor(idConductor=None):
    if idConductor is None:
        return redirect(url_for('inicio'))
    else:
        detalle_del_conductor = detalles_conductorBD(idConductor) or []
        print(detalle_del_conductor)
        return render_template('conductores/detalle.html', detalle_conductor=detalle_del_conductor)
    
@main.route('/actualizar-conductor', methods=['POST'])
def actualizar_conductor():
    print(request.form)
    resultData = actualizar_datos_conductorBD(request)
    print(resultData)
    if resultData == 1:
        flash('Actualizado correctamente','success')
        return redirect(url_for("main.lista_empleados"))
    else:
        flash('no se pudo validar', 'error')
        return redirect(url_for("main.lista_empleados"))
    
@main.route("/editar-conductor/<string:id>", methods=['GET'])
def viewEditarEmpleado(id):
    
    conductor = buscar_conductor_unicoBD(id)
    if conductor:
        
        return render_template('conductores/actualizar.html', respuestaConductor=conductor)
    else:
        #flash('El empleado no existe.', 'error')
        return redirect(url_for('inicio'))

@main.route("/eliminar-conductor/<string:id>", methods=['GET'])
def eliminarConductor(id):
    respuesta = eliminar_conductorBD(id)
    if respuesta:
        return redirect(url_for('main.lista_empleados'))
    
@main.route('/api/id', methods=['POST'])
def obtenerUid():
    global uid_fromEsp32
    data = request.get_json()
    uid_fromEsp32 = data.get('tag_uid')
    mensaje_respuesta = '{} recibido'.format(uid_fromEsp32)
    print(uid_fromEsp32)
    emitir_uid(uid_fromEsp32)
    return jsonify({'message':mensaje_respuesta}),200

@main.route("/buscando-conductor", methods=['POST'])
def viewBuscarEmpleadoBD():
    resultadoBusqueda = buscar_empleadoBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template('conductores/busqueda.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})