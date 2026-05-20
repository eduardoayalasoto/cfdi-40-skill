# cfdi-40-skill

Skill para Claude Code CLI con referencia técnica completa del estándar **CFDI 4.0** (Anexo 20, SAT México).

Cubre: estructura XML, reglas de llenado campo a campo, todos los catálogos, matriz completa de 122 errores CFDI40xxx, transformaciones XSLT, validación XSD, y Complemento de Pagos 2.0.

---

## Instalación en Claude Code CLI

### Opción 1 — Instalar directo desde GitHub (recomendado)

```bash
claude skill install https://github.com/TU_USUARIO/cfdi-40-skill
```

Eso descarga el skill y lo instala globalmente. Disponible en todas tus sesiones de Claude Code.

### Opción 2 — Clonar y instalar localmente

```bash
git clone https://github.com/TU_USUARIO/cfdi-40-skill.git
claude skill install ./cfdi-40-skill
```

### Opción 3 — Instalar solo en un proyecto

Si quieres el skill disponible solo dentro de un proyecto específico (no globalmente):

```bash
cd tu-proyecto/
claude skill install https://github.com/TU_USUARIO/cfdi-40-skill --project
```

---

## Verificar instalación

```bash
claude skill list
```

Debes ver `cfdi-40` en la lista.

---

## Cómo funciona

Una vez instalado, Claude Code lo activa automáticamente cuando detecta preguntas relacionadas con CFDI, como:

- "¿Por qué me da el error CFDI40139?"
- "Cómo llenar el campo RegimenFiscalReceptor"
- "El XSLT de cadena original me devuelve vacío"
- "Cuál es la clave de FormaPago para transferencia"
- "Qué campos lleva un CFDI de tipo P"
- Cualquier pregunta sobre CentroCFDI, timbrado, PAC, XML fiscal

No necesitas hacer nada especial. Claude lo usa cuando es relevante.

---

## Estructura del skill

```
cfdi-40/
├── SKILL.md                  ← Descripción y reglas de oro (siempre en contexto)
└── references/
    ├── guia.md               ← Estructura XML completa, reglas campo a campo,
    │                            XSLT, XSD, Complemento de Pagos 2.0, FAQ, glosario
    ├── catalogos.md          ← Todos los catálogos pequeños completos
    │                            (FormaPago, UsoCFDI, RegimenFiscal, TasaOCuota, etc.)
    └── errores.md            ← Matriz completa de 122 errores CFDI40xxx
                                 con causa y solución para cada uno
```

Claude carga solo el archivo de referencia que necesita según el problema, manteniendo el contexto eficiente.

---

## Cobertura

| Área | Detalle |
|---|---|
| Versión | CFDI 4.0 (Anexo 20, publicado 13/01/2022) |
| Complemento | Pagos 2.0 (publicado 29/12/2021) |
| Matriz de errores | 122 errores CFDI40101–CFDI40999 (versión 25/03/2026) |
| Catálogos completos | FormaPago, MetodoPago, TipoDeComprobante, Exportacion, TipoRelacion, RegimenFiscal, UsoCFDI, ObjetoImp, Impuesto, TipoFactor, TasaOCuota, Periodicidad, Meses, Estado (MEX) |
| Catálogos referenciados | ClaveProdServ, ClaveUnidad, CodigoPostal, Moneda, Pais y otros de alto volumen |
| XSD | cfdv40.xsd, catCFDI.xsd, Pagos10.xsd, catPagos.xsd, tdCFDI.xsd |
| XSLT | cadenaoriginal_4_0.xslt, Pagos20.xslt, TimbreFiscalDigitalv11.xslt |
| Snippets de código | C# (.NET), Python (lxml), Bash (xsltproc) |

---

## Actualizar

```bash
claude skill update cfdi-40
```

---

## Desinstalar

```bash
claude skill uninstall cfdi-40
```

---

## Fuentes

- [Anexo 20 v4.0 — SAT](https://www.sat.gob.mx/consultas/43074/actualizacion-factura-electronica---reforma-fiscal-2022-)
- [Referencia GNcys CFDI 4.0](https://www.gncys.com/anexo20/4.0/)
- [Complemento de Pagos 2.0 — GNcys](https://www.gncys.com/complementos/pagos20/)
- [Matriz de errores CFDI 4.0](https://www.gncys.com/anexo20/4.0/errores/)
