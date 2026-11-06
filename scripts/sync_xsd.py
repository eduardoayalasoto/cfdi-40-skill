#!/usr/bin/env python3
"""Sincroniza los XSD/XSLT oficiales del SAT dentro del skill cfdi-40.

Fuente: https://github.com/phpcfdi/resources-sat-xml (dominio público, Unlicense). Ese repo
descarga los archivos del SAT, reescribe las rutas absolutas a relativas y se actualiza solo.
Aquí tomamos únicamente los puntos de entrada que usa OKEA y sus dependencias.

Uso:
    python scripts/sync_xsd.py                    # clona la fuente y sincroniza
    python scripts/sync_xsd.py --upstream RUTA    # usa un clon local de la fuente
    python scripts/sync_xsd.py --verificar        # solo valida lo ya vendorizado (sin red)

Sale con código 0 si todo bien (haya o no cambios), 1 si falla la validación.
Escribe "CAMBIOS=si|no" en $GITHUB_OUTPUT cuando existe, para que el workflow decida abrir PR.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree

REPO_FUENTE = "https://github.com/phpcfdi/resources-sat-xml.git"
RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "skills" / "cfdi-40" / "xsd"
BASE_SAT = "www.sat.gob.mx"

# Rutas relativas a www.sat.gob.mx/ ; se agregan sus dependencias automáticamente.
PUNTOS_DE_ENTRADA = [
    # CFDI 4.0 y cadena original
    "sitio_internet/cfd/4/cfdv40.xsd",
    "sitio_internet/cfd/4/cadenaoriginal_4_0/cadenaoriginal_4_0.xslt",
    # Timbre Fiscal Digital 1.1
    "sitio_internet/cfd/TimbreFiscalDigital/TimbreFiscalDigitalv11.xsd",
    "sitio_internet/timbrefiscaldigital/cadenaoriginal_TFD_1_0.xslt",
    # Complementos
    "sitio_internet/cfd/Pagos/Pagos20.xsd",
    "sitio_internet/cfd/Pagos/Pagos20.xslt",
    "sitio_internet/cfd/CartaPorte/CartaPorte31.xsd",
    "sitio_internet/cfd/CartaPorte/CartaPorte31.xslt",
    "sitio_internet/cfd/nomina/nomina12.xsd",
    "sitio_internet/cfd/nomina/nomina12.xslt",
    "sitio_internet/cfd/ComercioExterior20/ComercioExterior20.xsd",
    "sitio_internet/cfd/ComercioExterior20/ComercioExterior20.xslt",
    "sitio_internet/cfd/implocal/implocal.xsd",
    "sitio_internet/cfd/implocal/implocal.xslt",
    "sitio_internet/cfd/leyendasFiscales/leyendasFisc.xsd",
    "sitio_internet/cfd/leyendasFiscales/leyendasFisc.xslt",
    "sitio_internet/cfd/ine/ine11.xsd",
    "sitio_internet/cfd/ine/ine11.xslt",
    "sitio_internet/cfd/donat/donat11.xsd",
    "sitio_internet/cfd/donat/donat11.xslt",
]
# Esquemas que deben compilar (no se validan instancias, solo que el esquema y sus imports carguen).
ESQUEMAS_A_COMPILAR = [p for p in PUNTOS_DE_ENTRADA if p.endswith(".xsd")]

PATRON_REF = re.compile(r'(?:schemaLocation|href)\s*=\s*"([^"]+)"')


def dependencias(base: Path, rel: str) -> set[str]:
    """Rutas (relativas a base) referenciadas por un XSD/XSLT."""
    texto = (base / rel).read_text(encoding="utf-8", errors="replace")
    salida = set()
    for ref in PATRON_REF.findall(texto):
        if ref.startswith(("http://", "https://")):
            m = re.match(r"https?://" + re.escape(BASE_SAT) + r"/(.+)", ref)
            if not m:
                continue  # URL ajena al SAT (p. ej. espacios de nombres W3C)
            destino = m.group(1)
        else:
            destino = os.path.normpath(os.path.join(os.path.dirname(rel), ref)).replace("\\", "/")
        if destino.endswith((".xsd", ".xslt", ".xsl")):
            salida.add(destino)
    return salida


def cierre(base: Path) -> list[str]:
    pendientes = list(PUNTOS_DE_ENTRADA)
    vistos: set[str] = set()
    while pendientes:
        rel = pendientes.pop()
        if rel in vistos:
            continue
        if not (base / rel).is_file():
            raise SystemExit(f"ERROR: la fuente ya no tiene {rel} (¿renombrado por el SAT/upstream?)")
        vistos.add(rel)
        pendientes.extend(dependencias(base, rel) - vistos)
    return sorted(vistos)


def huella(base: Path, archivos: list[str]) -> str:
    h = hashlib.sha256()
    for rel in archivos:
        h.update(rel.encode())
        h.update((base / rel).read_bytes())
    return h.hexdigest()


def validar(base: Path, archivos: list[str]) -> list[str]:
    """Compila los esquemas y revisa que los XSLT estén bien formados (requiere xmllint)."""
    errores = []
    # 1) Buena formación de todos los archivos, con la biblioteca estándar (no depende de xmllint).
    for rel in archivos:
        try:
            ElementTree.parse(base / rel)
        except ElementTree.ParseError as e:
            errores.append(f"{rel}: XML mal formado ({e})")
    # 2) Compilación de los esquemas: lxml si existe; si no, xmllint; si no, aviso.
    try:
        from lxml import etree
    except ImportError:
        etree = None
    if etree is not None:
        for rel in ESQUEMAS_A_COMPILAR:
            try:
                etree.XMLSchema(etree.parse(str(base / rel)))
            except Exception as e:  # noqa: BLE001 - cualquier fallo de compilación es error
                errores.append(f"{rel}: no compila ({str(e)[:400]})")
        return errores
    if not xmllint_funciona():
        print("AVISO: ni lxml ni xmllint disponibles; se omite la compilación de esquemas "
              "(pip install lxml).")
        return errores
    with tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False) as f:
        f.write("<x/>")
        instancia = f.name
    try:
        for rel in ESQUEMAS_A_COMPILAR:
            r = subprocess.run(["xmllint", "--noout", "--schema", str(base / rel), instancia],
                               capture_output=True, text=True)
            if "parser error" in r.stderr or "failed to load" in r.stderr or "Schemas parser" in r.stderr:
                errores.append(f"{rel}: no compila ({r.stderr.strip()[:600]})")
    finally:
        os.unlink(instancia)
    return errores


def xmllint_funciona() -> bool:
    if not shutil.which("xmllint"):
        return False
    try:
        r = subprocess.run(["xmllint", "--version"], capture_output=True, text=True)
    except OSError:
        return False
    return r.returncode == 0


def validar_agrupador() -> list[str]:
    """El esquema agrupador (validador-cfdi40.xsd) debe compilar con lo vendorizado."""
    agrupador = RAIZ / "skills" / "cfdi-40" / "validador-cfdi40.xsd"
    ns_xs = "{http://www.w3.org/2001/XMLSchema}"
    errores = []
    # libxml2 compila sin error un xs:import con ruta rota, así que se comprueba a mano:
    # el archivo existe y su targetNamespace coincide con el declarado.
    for imp in ElementTree.parse(agrupador).getroot().iter(ns_xs + "import"):
        ns, ruta = imp.get("namespace"), agrupador.parent / imp.get("schemaLocation", "")
        if not ruta.is_file():
            errores.append(f"validador-cfdi40.xsd: no existe {imp.get('schemaLocation')}")
        elif ElementTree.parse(ruta).getroot().get("targetNamespace") != ns:
            errores.append(f"validador-cfdi40.xsd: {imp.get('schemaLocation')} no es del namespace {ns}")
    try:
        from lxml import etree
    except ImportError:
        return errores
    try:
        etree.XMLSchema(etree.parse(str(agrupador)))
    except Exception as e:  # noqa: BLE001
        errores.append(f"validador-cfdi40.xsd: no compila ({str(e)[:400]})")
    return errores


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--upstream", help="ruta a un clon local de resources-sat-xml")
    ap.add_argument("--verificar", action="store_true", help="solo validar lo ya vendorizado")
    args = ap.parse_args()

    if args.verificar:
        base = DESTINO / BASE_SAT if (DESTINO / BASE_SAT).exists() else DESTINO
        archivos = cierre(base)
        errores = validar(base, archivos) + validar_agrupador()
        for e in errores:
            print("ERROR:", e)
        print(f"Verificados {len(archivos)} archivos; {len(errores)} errores.")
        return 1 if errores else 0

    temporal = None
    if args.upstream:
        clon = Path(args.upstream)
    else:
        temporal = tempfile.mkdtemp(prefix="sat-xml-")
        clon = Path(temporal)
        subprocess.run(["git", "-c", "core.longpaths=true", "clone", "--quiet", "--depth", "1",
                        REPO_FUENTE, str(clon)], check=True)
    try:
        commit = subprocess.run(["git", "-C", str(clon), "rev-parse", "HEAD"], capture_output=True,
                                text=True, check=True).stdout.strip()
        fecha = subprocess.run(["git", "-C", str(clon), "log", "-1", "--format=%cI"], capture_output=True,
                               text=True, check=True).stdout.strip()
        edad_dias = (datetime.now(timezone.utc) - datetime.fromisoformat(fecha)).days
        if edad_dias > 90:
            aviso = (f"La fuente {REPO_FUENTE.removesuffix('.git')} no se actualiza hace {edad_dias} días. "
                     "Revisa si el SAT publicó cambios y la fuente quedó rezagada.")
            print(f"::warning::{aviso}" if os.environ.get("GITHUB_ACTIONS") else f"AVISO: {aviso}")
        base = clon / "resources" / BASE_SAT
        archivos = cierre(base)
        errores = validar(base, archivos)
        if errores:
            for e in errores:
                print("ERROR:", e)
            return 1

        nueva = huella(base, archivos)
        meta_ruta = DESTINO / "UPSTREAM.json"
        anterior = json.loads(meta_ruta.read_text(encoding="utf-8")).get("contenido_sha256") if meta_ruta.exists() else None
        cambios = nueva != anterior
        if cambios:
            if DESTINO.exists():
                shutil.rmtree(DESTINO)
            for rel in archivos:
                destino = DESTINO / rel
                destino.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(base / rel, destino)
            lic = clon / "LICENSE"
            if lic.exists():
                shutil.copyfile(lic, DESTINO / "LICENSE-upstream")
            meta = {
                "fuente": REPO_FUENTE.removesuffix(".git"),
                "commit": commit,
                "commit_fecha": fecha,
                "archivos": len(archivos),
                "contenido_sha256": nueva,
                "licencia": "Unlicense (dominio público; información pública del SAT)",
                "nota": "Generado por scripts/sync_xsd.py. No editar a mano.",
            }
            meta_ruta.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            manifiesto = "".join(f"{hashlib.sha256((DESTINO / r).read_bytes()).hexdigest()}  {r}\n" for r in archivos)
            (DESTINO / "MANIFEST.sha256").write_text(manifiesto, encoding="utf-8")
        errores = validar_agrupador()
        if errores:
            for e in errores:
                print("ERROR:", e)
            return 1
        print(f"{'ACTUALIZADO' if cambios else 'SIN CAMBIOS'}: {len(archivos)} archivos, fuente {commit[:10]} ({fecha})")
        salida = os.environ.get("GITHUB_OUTPUT")
        if salida:
            with open(salida, "a", encoding="utf-8") as f:
                f.write(f"CAMBIOS={'si' if cambios else 'no'}\nCOMMIT_FUENTE={commit}\nARCHIVOS={len(archivos)}\n")
        return 0
    finally:
        if temporal:
            shutil.rmtree(temporal, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
