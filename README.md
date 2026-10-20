# File Integrity Sentinel (FIM)

Herramienta de monitorización y verificación de integridad de archivos basada en hashing criptográfico SHA-256. Permite detectar alteraciones, eliminaciones o corrupciones en directorios críticos de sistemas operativos.

## Características
- **Hashing SHA-256:** Generación de huellas digitales criptográficas bloque a bloque.
- **Detección de incidentes:** Alerta inmediata de modificaciones y eliminaciones.
- **Sin dependencias externas:** Desarrollado con bibliotecas estándar de Python.
- **Registro persistente:** Exportación de líneas base estructuradas en JSON.

## Uso

### 1. Generar línea base (Baseline)
```bash
python fim.py baseline -d /ruta/a/auditar -o baseline.json
