import os
import hashlib
import json
import argparse
from datetime import datetime

def calcular_hash(ruta_archivo):
    hasher = hashlib.sha256()
    try:
        with open(ruta_archivo, 'rb') as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (PermissionError, FileNotFoundError):
        return None

def generar_baseline(directorio, salida_json="baseline.json"):
    print(f"[*] Escaneando directorio: {directorio}")
    registros = {}
    
    for raiz, _, archivos in os.walk(directorio):
        for nombre in archivos:
            ruta_completa = os.path.join(raiz, nombre)
            hash_val = calcular_hash(ruta_completa)
            if hash_val:
                registros[ruta_completa] = hash_val

    with open(salida_json, 'w', encoding='utf-8') as f:
        json.dump({"creado": str(datetime.now()), "archivos": registros}, f, indent=4)
    
    print(f"[+] Baseline completado. {len(registros)} archivos registrados en '{salida_json}'.")

def verificar_integridad(archivo_json="baseline.json"):
    if not os.path.exists(archivo_json):
        print(f"[-] Error: No existe el archivo base '{archivo_json}'. Genera uno primero.")
        return

    with open(archivo_json, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    baseline = datos.get("archivos", {})
    alertas = 0

    print(f"[*] Verificando integridad contra baseline ({datos.get('creado')})...\n")

    for ruta, hash_original in baseline.items():
        if not os.path.exists(ruta):
            print(f"[ALERTA - ELIMINADO] {ruta}")
            alertas += 1
            continue

        hash_actual = calcular_hash(ruta)
        if hash_actual != hash_original:
            print(f"[ALERTA - MODIFICADO] {ruta}")
            alertas += 1
        else:
            print(f"[OK] {ruta}")

    if alertas == 0:
        print("\n[V] Integridad verificada: No se detectaron alteraciones.")
    else:
        print(f"\n[!] Advertencia: Se detectaron {alertas} incidentes de integridad.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor de Integridad de Archivos (FIM) con SHA-256")
    subparsers = parser.add_subparsers(dest="comando", required=True)

    # Subcomando: baseline
    parser_base = subparsers.add_parser("baseline", help="Generar hash baseline de un directorio")
    parser_base.add_argument("-d", "--dir", required=True, help="Ruta de la carpeta a monitorizar")
    parser_base.add_argument("-o", "--output", default="baseline.json", help="Archivo de salida JSON")

    # Subcomando: check
    parser_check = subparsers.add_parser("check", help="Verificar integridad de los archivos")
    parser_check.add_argument("-b", "--baseline", default="baseline.json", help="Ruta del archivo baseline JSON")

    args = parser.parse_args()

    if args.comando == "baseline":
        generar_baseline(args.dir, args.output)
    elif args.comando == "check":
        verificar_integridad(args.baseline)
