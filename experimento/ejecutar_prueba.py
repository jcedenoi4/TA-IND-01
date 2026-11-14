"""Prueba local reproducible: dos replicas, caida de volume1 y recuperacion.

Usa Python 3 (biblioteca estandar) y Docker Compose. No toma capturas.
Cada ejecucion conserva un registro nuevo; no elimina datos existentes.
"""
from datetime import datetime, timezone, timedelta
from pathlib import Path
import getpass
import hashlib
import json
import platform
import socket
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
TZ = timezone(timedelta(hours=-5))
RUN = datetime.now(TZ).strftime('%Y%m%dT%H%M%S%f')
LOG = ROOT / 'evidencias' / ('experimento_' + RUN + '.log')
COMPOSE = ['docker', 'compose', '-f', str(ROOT / 'experimento/docker-compose.yml')]
HTTP = urllib.request.build_opener(urllib.request.ProxyHandler({}))
PORTS = {'volume1:8080': 8080, 'volume2:8080': 8081}

def record(message):
    line = '[' + datetime.now(TZ).isoformat(timespec='seconds') + '] ' + str(message)
    print(line, flush=True)
    with LOG.open('a', encoding='utf-8') as stream:
        stream.write(line + '\n')

def command(args):
    record('COMANDO: ' + subprocess.list2cmdline(args))
    p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=60)
    record('SALIDA:\n' + p.stdout + p.stderr)
    record('EXIT_CODE: ' + str(p.returncode))
    if p.returncode:
        raise RuntimeError('Comando fallido')
    return p.stdout

def request(method, url, data=None, headers=None, timeout=20):
    record('HTTP ' + method + ' ' + url)
    start = time.perf_counter()
    try:
        req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
        with HTTP.open(req, timeout=timeout) as response:
            status, body = response.status, response.read()
    except urllib.error.HTTPError as exc:
        status, body = exc.code, exc.read()
    elapsed = time.perf_counter() - start
    record('HTTP_STATUS: ' + str(status) + '; duracion_s=' + str(round(elapsed, 4)))
    record('CUERPO: ' + body.decode('utf-8', errors='replace'))
    return status, body

def require(condition, message):
    record(('VERIFICACION_OK: ' if condition else 'VERIFICACION_FALLIDA: ') + message)
    if not condition:
        raise AssertionError(message)

def assign(collection):
    query = urllib.parse.urlencode({'replication': '001', 'count': 1, 'collection': collection})
    return request('GET', 'http://127.0.0.1:9333/dir/assign?' + query)

def upload(fid, server, payload):
    boundary = 'TAIND01' + RUN
    data = ('--' + boundary + '\r\nContent-Disposition: form-data; name="file"; filename="prueba.txt"\r\nContent-Type: text/plain\r\n\r\n').encode() + payload + ('\r\n--' + boundary + '--\r\n').encode()
    return request('POST', 'http://127.0.0.1:' + str(PORTS[server]) + '/' + fid, data, {'Content-Type': 'multipart/form-data; boundary=' + boundary})

def check_copy(port, fid, expected):
    status, body = request('GET', 'http://127.0.0.1:' + str(port) + '/' + fid)
    actual = hashlib.sha256(body).hexdigest()
    record('SHA256_OBTENIDO: ' + actual)
    require(status == 200 and actual == expected, 'Contenido identico en puerto ' + str(port))

def wait_locations(volume_id, expected, seconds=45):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        status, body = request('GET', 'http://127.0.0.1:9333/dir/lookup?volumeId=' + volume_id)
        obj = json.loads(body)
        if status == 200 and len(obj.get('locations', [])) == expected:
            return
        time.sleep(2)
    raise TimeoutError('El Master no registro ' + str(expected) + ' ubicaciones')

def main():
    record('ENTORNO: ' + json.dumps({'usuario': getpass.getuser(), 'equipo': socket.gethostname(), 'sistema': platform.platform(), 'python': platform.python_version(), 'zona': 'America/Guayaquil UTC-05:00', 'ejecucion': RUN}, ensure_ascii=False))
    command(['docker', 'version'])
    command(['docker', 'compose', 'version'])
    command(COMPOSE + ['config', '--quiet'])
    command(COMPOSE + ['ps', '-a'])
    command(COMPOSE + ['exec', '-T', 'master', 'weed', 'version'])
    command(['docker', 'image', 'inspect', 'chrislusf/seaweedfs:3.85@sha256:d67f9b5586f73b6623c143489849c958ae0ec36a698bf4243a19df07cfa28c22', '--format', '{{.Id}} {{json .RepoDigests}}'])
    record('ESPERA: dos servidores registrados, cupos disponibles y servicios HTTP listos')
    deadline = time.monotonic() + 60
    ready = False
    while time.monotonic() < deadline:
        try:
            status, body = request('GET', 'http://127.0.0.1:9333/dir/status', timeout=5)
            topology = json.loads(body).get('Topology', {})
            nodes = [node for dc in topology.get('DataCenters', []) for rack in dc.get('Racks', []) for node in rack.get('DataNodes', [])]
            if status == 200 and len(nodes) == 2 and all(node['Max'] - node['Volumes'] >= 4 for node in nodes):
                statuses = [request('GET', url, timeout=5)[0] for url in ['http://127.0.0.1:8080/status', 'http://127.0.0.1:8081/status', 'http://127.0.0.1:8888/', 'http://127.0.0.1:8333/']]
                if all(code == 200 for code in statuses):
                    ready = True
                    break
        except (OSError, ValueError, KeyError) as exc:
            record('AUN_NO_LISTO: ' + repr(exc))
        time.sleep(2)
    require(ready, 'Dos servidores, capacidad suficiente y servicios listos antes del experimento')

    record('ETAPA 1: escritura y comprobacion directa de ambas replicas')
    payload = ('TA-IND-01 SeaweedFS replication=001\nusuario=' + getpass.getuser() + '\nequipo=' + socket.gethostname() + '\nejecucion=' + RUN + '\n').encode()
    expected = hashlib.sha256(payload).hexdigest()
    record('SHA256_ESPERADO: ' + expected)
    status, body = assign('base' + RUN.lower())
    require(status == 200, 'Asignacion inicial con dos servidores')
    assignment = json.loads(body)
    fid = assignment['fid']
    volume_id = fid.split(',')[0]
    status, _ = upload(fid, assignment['url'], payload)
    require(status in (200, 201), 'Carga inicial')
    wait_locations(volume_id, 2)
    check_copy(8080, fid, expected)
    check_copy(8081, fid, expected)

    record('PRUEBA COMPLEMENTARIA: acceso por S3 y Filer')
    bucket = 'ta-ind-01-' + RUN.lower()
    status, _ = request('PUT', 'http://127.0.0.1:8333/' + bucket, b'')
    require(status in (200, 201), 'Creacion de bucket S3 local')
    status, _ = request('PUT', 'http://127.0.0.1:8333/' + bucket + '/prueba.txt', payload, {'Content-Type': 'text/plain'})
    require(status in (200, 201), 'Escritura S3 local')
    status, body = request('GET', 'http://127.0.0.1:8333/' + bucket + '/prueba.txt')
    require(status == 200 and body == payload, 'Lectura S3 identica')
    status, body = request('GET', 'http://127.0.0.1:8888/buckets/' + bucket + '/prueba.txt')
    require(status == 200 and body == payload, 'Lectura mediante Filer identica')

    stopped = False
    try:
        record('ETAPA 2: detencion controlada de volume1 (no particion de red)')
        command(COMPOSE + ['stop', '-t', '5', 'volume1'])
        stopped = True
        command(COMPOSE + ['ps', '-a'])
        wait_locations(volume_id, 1)
        check_copy(8081, fid, expected)
        request('GET', 'http://127.0.0.1:9333/dir/status')
        status, body = request('GET', 'http://127.0.0.1:8333/' + bucket + '/prueba.txt')
        require(status == 200 and body == payload, 'Lectura S3 del objeto previo con volume1 detenido')
        record('ETAPA 3: intento de asignar NUEVA coleccion con replication=001 y un solo servidor')
        status, body = assign('degradado' + RUN.lower())
        require(status == 406 and b'No writable volumes' in body and b'replication:001' in body, 'Nueva asignacion rechazada: no hay dos servidores para replication=001')
    finally:
        if stopped:
            record('ETAPA 4: reinicio del mismo volume1 con sus datos persistentes')
            command(COMPOSE + ['start', 'volume1'])

    wait_locations(volume_id, 2)
    check_copy(8080, fid, expected)
    check_copy(8081, fid, expected)
    status, body = assign('recuperado' + RUN.lower())
    require(status == 200, 'Nueva asignacion tras reiniciar volume1')
    recovered = json.loads(body)
    status, _ = upload(recovered['fid'], recovered['url'], payload)
    require(status in (200, 201), 'Nueva escritura tras recuperacion')
    check_copy(8080, recovered['fid'], expected)
    check_copy(8081, recovered['fid'], expected)
    command(COMPOSE + ['ps', '-a'])
    command(COMPOSE + ['logs', '--no-color', '--tail', '35', 'master', 'volume1', 'volume2', 'filer', 's3'])
    record('RESULTADO: prueba completada; cinco servicios activos. No se tomaron capturas.')

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        record('ERROR: ' + repr(exc))
        raise
