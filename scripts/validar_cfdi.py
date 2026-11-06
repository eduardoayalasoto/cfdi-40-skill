#!/usr/bin/env python3
"""Valida un CFDI 4.0 (con timbre y complementos) contra los XSD oficiales del skill.

Uso:  python scripts/validar_cfdi.py factura.xml [otra.xml ...]
Requiere: pip install lxml
Sale con 0 si todos son válidos, 1 si alguno no lo es.
Solo valida estructura XSD; no sustituye la validación de sello, certificado ni lista 69-B.
"""
import sys
from pathlib import Path

from lxml import etree

ESQUEMA = Path(__file__).resolve().parent.parent / "skills" / "cfdi-40" / "validador-cfdi40.xsd"


def main(rutas):
    if not rutas:
        print(__doc__)
        return 2
    esquema = etree.XMLSchema(etree.parse(str(ESQUEMA)))
    malos = 0
    for ruta in rutas:
        try:
            doc = etree.parse(ruta)
        except (OSError, etree.XMLSyntaxError) as e:
            print(f"NO PARSEA  {ruta}: {e}")
            malos += 1
            continue
        if esquema.validate(doc):
            print(f"VÁLIDO     {ruta}")
        else:
            malos += 1
            print(f"INVÁLIDO   {ruta}")
            for err in esquema.error_log:
                print(f"  línea {err.line}: {err.message}")
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
