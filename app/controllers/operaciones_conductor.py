from ..conexion.conexionBD import connectDB
import datetime 
import os
from os import remove, path

def procesar_form_empleado(dataForm):

    try:
        with connectDB() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:

                query = """INSERT INTO Usuarios (uid, nombre, placa ,E_1 ,E_2 ,E_3 ,E_4 ,E_5 ,E_6 ,T_1 ,T_2 ,T_3 ,T_4 ,T_5 ,T_6 , Procesos, Activo, Turno, Codigo)
                              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

                valores = (dataForm['uid'], dataForm['nombre'], dataForm['placa'],0,0,0,0,0,0,None,None,None,None,None,None,0,0,'',dataForm['codigo'])
                cursor.execute(query, valores)
                conexion_MySQLdb.commit()
                
                resultado_insert = cursor.rowcount
                
                return resultado_insert

    except Exception as e:

        return f'Se produjo un error en procesar_form_empleado: {str(e)}'

def lista_empleadosBD():
    try:
        with connectDB() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = (f"""
                    SELECT uid, nombre, placa, Codigo 
                    FROM Usuarios
                    ORDER BY nombre DESC
                    """)
                cursor.execute(querySQL,)
                empleadosBD = cursor.fetchall()
        return empleadosBD
    except Exception as e:
        print(
            f"Errro en la función sql_lista_empleadosBD: {e}")
        return None

def detalles_conductorBD(idEmpleado):
    try:
        with connectDB() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                query = ('SELECT uid, nombre, placa, Codigo FROM Usuarios where uid = %s')
                query_acciones = ("""
                                    SELECT Proceso, MAX(Fecha) AS Fecha_Limite, SUM(TMA_Descarga_envase+TMA_Descarga_producto+TMA_carga) AS TMA
                                    FROM Arribos
                                    WHERE uid = %s
                                    group by Proceso
                                    order by Fecha_Limite DESC
                                    Limit 1
                                    """)
                cursor.execute(query, (str(idEmpleado),))
                empleadosBD = cursor.fetchone()
                cursor.execute(query_acciones, (str(idEmpleado),))
                datos_empleadoBD = cursor.fetchone()
                if datos_empleadoBD != None:
                    empleadosBD.update(datos_empleadoBD)
        cursor.close()
        return empleadosBD
    except Exception as e:
        print(
            f"Errro en la función sql_detalles_empleadosBD: {e}")
        return None

def buscar_conductor_unicoBD(id):
    try:
        with connectDB() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                query = ("""SELECT uid, nombre, placa, Codigo
                           FROM Usuarios
                           WHERE uid = %s""")
                mycursor.execute(query, (id,))
                empleado = mycursor.fetchone()
                return empleado

    except Exception as e:
        print(f"Ocurrió un error en def buscarEmpleadoUnico: {e}")
        return []
    
def eliminar_conductorBD(id_empleado):
    try:
        with connectDB() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "DELETE FROM Usuarios WHERE uid=%s"
                cursor.execute(querySQL, (id_empleado,))
                conexion_MySQLdb.commit()
                resultado_eliminar = cursor.rowcount
  
        return resultado_eliminar
    except Exception as e:
        print(f"Error en eliminarEmpleado : {e}")
        return []
    
def actualizar_datos_conductorBD(data):
    try:
        with connectDB() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                nombre = data.form['nombre'] 
                placa = data.form['placa']
                codigo = data.form['codigo']
                uid = data.form['uid']                
                querySQL = """
                        UPDATE Usuarios
                        SET nombre = %s,
                            placa = %s,
                            Codigo = %s
                        WHERE uid = %s
                """
                values = (nombre, placa, codigo, uid)

                cursor.execute(querySQL, values)
                conexion_MySQLdb.commit()

        return cursor.rowcount or []
    except Exception as e:
        print(f"Ocurrió un error en procesar_actualizacion_form: {e}")
        return None
    
def buscar_empleadoBD(search):
    try:
        with connectDB() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:

                query = ("""SELECT uid, nombre, placa, Codigo
                           FROM Usuarios
                           WHERE uid LIKE %s OR nombre LIKE %s
                           ORDER BY nombre DESC""")
                
                search_pattern = f"%{search}%"  # Agregar "%" alrededor del término de búsqueda
                mycursor.execute(query, (search_pattern,search_pattern,))
                resultado_busqueda = mycursor.fetchall()
                return resultado_busqueda

    except Exception as e:
        print(f"Ocurrió un error en def buscarEmpleadoBD: {e}")
        return []
