---
name: cfdi-40
description: >
  Referencia técnica completa del estándar CFDI 4.0 (Anexo 20, SAT México).
  Usar SIEMPRE que el usuario mencione: CFDI, factura electrónica, timbrado,
  PAC, XML fiscal, Complemento de Pagos, errores CFDI40xxx, cadena original,
  XSLT de cadena original, XSD de CFDI, RFC, régimen fiscal, UsoCFDI,
  FormaPago, MetodoPago, ObjetoImp, TasaOCuota, PPD, PUE, nodo Emisor,
  nodo Receptor, nodo Conceptos, nodo Impuestos, ClaveProdServ, o cualquier
  problema de validación, transformación o integración con sistemas de
  facturación mexicanos. También aplica a CentroCFDI, eAdaptor, o cualquier
  sistema receptor/emisor de comprobantes fiscales digitales.
---

# Skill: CFDI 4.0 — Referencia Técnica Completa

Este skill contiene toda la información necesaria para resolver cualquier
problema relacionado con CFDI versión 4.0: estructura XML, reglas de llenado,
catálogos, matriz de errores, transformaciones XSLT, y Complemento de Pagos 2.0.

## Cómo usar este skill

Según el tipo de problema, lee el archivo de referencia correspondiente:

| Problema | Archivo a leer |
|---|---|
| Error CFDI40xxx del PAC/SAT | `references/errores.md` |
| Cómo llenar un campo / qué valor poner | `references/guia.md` |
| Qué clave usar de un catálogo (FormaPago, UsoCFDI, etc.) | `references/catalogos.md` |
| Error en transformación XSLT / cadena original | `references/guia.md` → sección XSLT |
| Estructura XML del CFDI o Complemento de Pagos | `references/guia.md` |
| Validar contra XSD | `references/guia.md` → sección XSD |

## Arquitectura de archivos

```
cfdi-40/
├── SKILL.md                  ← este archivo (carga siempre)
└── references/
    ├── guia.md               ← estructura XML, reglas campo a campo,
    │                            XSLT, XSD, Complemento de Pagos 2.0,
    │                            tipos de comprobante, FAQ, glosario
    ├── catalogos.md          ← todos los catálogos pequeños completos
    │                            (FormaPago, UsoCFDI, RegimenFiscal,
    │                            TasaOCuota, ObjetoImp, etc.)
    └── errores.md            ← matriz completa de 122 errores CFDI40xxx
```

## Contexto del dominio

- **Versión vigente:** CFDI 4.0 (Anexo 20 SAT, publicado 13/01/2022)
- **Complemento de Pagos:** versión 2.0 (publicado 29/12/2021)
- **Matriz de errores:** vigente al 25/03/2026
- **Namespace:** `http://www.sat.gob.mx/cfd/4`
- **XSD oficial:** `https://www.sat.gob.mx/sitio_internet/cfd/4/cfdv40.xsd`
- **XSLT cadena original:** `https://www.sat.gob.mx/sitio_internet/cfd/4/cadenaoriginal_4_0.xslt`
- **XSLT Complemento Pagos:** `https://www.sat.gob.mx/sitio_internet/cfd/Pagos/Pagos20.xslt`

## Reglas de oro (siempre en contexto)

1. El campo `Nombre` del Emisor y Receptor **debe coincidir exactamente** con la l_RFC del SAT — diferencia de un espacio o acento causa rechazo (CFDI40139 / CFDI40145)
2. CFDI tipo `P` (Pago): SubTotal=0, Total=0, Moneda=XXX, sin FormaPago, sin MetodoPago, sin nodo Impuestos, UsoCFDI=CP01
3. CFDI tipo `T` (Traslado): sin FormaPago, sin MetodoPago, Total=0
4. FormaPago=`99` **requiere** MetodoPago=`PPD` — son inseparables
5. ObjetoImp=`02` **requiere** nodo Impuestos en el concepto; ObjetoImp=`01` o `03` **prohíbe** ese nodo
6. TipoFactor=`Exento` en Traslados: NO se registran TasaOCuota ni Importe
7. TipoFactor=`Exento` en Retenciones: **no está permitido**
8. La cadena original se genera con XSLT 1.0 — no compatible con XSLT 2.0/3.0
9. RegimenFiscalReceptor es **obligatorio** en v4.0 (campo nuevo vs. v3.3)
10. DomicilioFiscalReceptor debe coincidir con el CP registrado en el SAT para ese RFC
