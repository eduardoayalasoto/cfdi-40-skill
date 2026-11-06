#!/usr/bin/env python3
"""Detecta si el SAT modificó esquemas DESPUÉS de lo que sabe la fuente vendorizada.

La fuente (phpcfdi/resources-sat-xml) puede rezagarse. Este script hace una petición HEAD por cada punto de
entrada al sitio del SAT, lee `Last-Modified` y lo compara con la fecha del commit de la fuente que quedó
registrada en xsd/UPSTREAM.json. Si el SAT es más reciente, hay desfase.

Revisa los 51 archivos vendorizados (los del MANIFEST.sha256), no solo los puntos de entrada.
No descarga archivos, nunca falla por problemas de red del SAT (solo avisa) y es seguro correrlo seguido.
Salida: imprime un resumen; con GITHUB_OUTPUT escribe DESFASE=si|no. Código 0 siempre salvo error de uso.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sync_xsd import DESTINO  # noqa: E402

BASE_URL = "http://www.sat.gob.mx/"
TOLERANCIA = timedelta(days=1)


def ultima_modificacion(ruta: str) -> datetime | None:
    req = urllib.request.Request(BASE_URL + ruta, method="HEAD", headers={"User-Agent": "cfdi-40-skill/verificar"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            valor = r.headers.get("Last-Modified")
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        print(f"  sin respuesta del SAT para {ruta}: {e}")
        return None
    return parsedate_to_datetime(valor) if valor else None


def main() -> int:
    meta_ruta = DESTINO / "UPSTREAM.json"
    if not meta_ruta.exists():
        print("No hay xsd/UPSTREAM.json; corre primero scripts/sync_xsd.py")
        return 2
    fuente = datetime.fromisoformat(json.loads(meta_ruta.read_text(encoding="utf-8"))["commit_fecha"])
    manifiesto = DESTINO / "MANIFEST.sha256"
    archivos = [linea.split("  ", 1)[1].strip() for linea in manifiesto.read_text(encoding="utf-8").splitlines() if "  " in linea]
    print(f"Fuente vendorizada actualizada al {fuente.date()}. Consultando el SAT ({len(archivos)} archivos)...")

    desfasados, consultados = [], 0
    for ruta in archivos:
        modificado = ultima_modificacion(ruta)
        if modificado is None:
            continue
        consultados += 1
        if modificado.astimezone(timezone.utc) > fuente.astimezone(timezone.utc) + TOLERANCIA:
            desfasados.append((ruta, modificado))

    for ruta, fecha in desfasados:
        print(f"::warning::El SAT modificó {ruta} el {fecha:%Y-%m-%d}, posterior a la fuente ({fuente:%Y-%m-%d}).")
    if consultados == 0:
        print("::warning::No se pudo consultar al SAT; no se puede afirmar que la fuente esté al día.")
    print(f"Consultados {consultados}; con desfase {len(desfasados)}.")

    salida = os.environ.get("GITHUB_OUTPUT")
    if salida:
        with open(salida, "a", encoding="utf-8") as f:
            f.write(f"DESFASE={'si' if desfasados else 'no'}\nCONSULTADOS={consultados}\n")
            f.write("DETALLE=" + "; ".join(f"{r} ({d:%Y-%m-%d})" for r, d in desfasados) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
