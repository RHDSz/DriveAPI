#!/bin/bash

# Ir a la ruta de trabajo
cd /home/ubuntu/respaldo_drive || exit 1

# Carpeta a respaldar
CARPETA_ORIGEN="/home/ubuntu/Documentos"

# Verifica si la carpeta existe
if [ ! -d "$CARPETA_ORIGEN" ]; then
  echo "❌ Carpeta a respaldar no existe: $CARPETA_ORIGEN"
  exit 1
fi

# Nombre del archivo con fecha
FECHA=$(date +%F)
ARCHIVO_ZIP="respaldo_$FECHA.zip"

# Comprimir
zip -r "$ARCHIVO_ZIP" "$CARPETA_ORIGEN"

# Subir
python3 subir_drive.py "$ARCHIVO_ZIP"

