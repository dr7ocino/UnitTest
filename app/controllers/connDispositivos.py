import subprocess
import platform

def verificar_conexion(direccion_ip):
    parametros = '-n' if platform.system().lower() == 'windows' else '-c'
    comando = ['ping', parametros, '1', direccion_ip]
    try:
        subprocess.check_output(comando, timeout=1)
        return True
    except subprocess.CalledProcessError:
        return False
    except subprocess.TimeoutExpired:
        return False
