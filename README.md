# cfdi-40-skill

Skill para Claude Code CLI con referencia técnica completa del estándar **CFDI 4.0** (Anexo 20, SAT México).

Cubre: estructura XML, reglas de llenado campo a campo, todos los catálogos, matriz completa de 122 errores CFDI40xxx con causa y solución, transformaciones XSLT, validación XSD y los complementos **Pagos 2.0**, **Carta Porte 3.1** y **Nómina 1.2 (Rev. E)** con sus matrices de error (CRPxxxxx, CPxxx, NOMxxx).

---

## Instalación

### Opción 1 — Copiar directo a tu directorio de skills (más simple)

```bash
# Clonar el repositorio
git clone https://github.com/eduardoayalasoto/cfdi-40-skill.git

# Copiar la carpeta del skill a tu directorio personal de Claude Code
cp -r cfdi-40-skill/cfdi-40 ~/.claude/skills/cfdi-40
```

Reinicia Claude Code. El skill estará disponible en todas tus sesiones.

### Opción 2 — Agregar como marketplace y luego instalar

Esto requiere que el repo tenga un `marketplace.json`. Si lo tienes configurado:

```bash
# Dentro de Claude Code CLI, agregar el marketplace (una sola vez)
/plugin marketplace add eduardoayalasoto/cfdi-40-skill

# Luego instalar el plugin
/plugin install cfdi-40@cfdi-40-skill
```

### Opción 3 — Instalar solo en un proyecto específico

Si quieres el skill disponible solo dentro de un repositorio (compartido con el equipo vía git):

```bash
# Dentro del directorio del proyecto
cp -r cfdi-40-skill/cfdi-40 .claude/skills/cfdi-40
git add .claude/skills/cfdi-40
git commit -m "feat: agregar skill CFDI 4.0 para Claude Code"
```

---

## Verificar instalación

Abre Claude Code y ejecuta:

```bash
/skills
```

Debes ver `cfdi-40` en la lista. También puedes verificar directamente:

```bash
ls ~/.claude/skills/cfdi-40/
# Debe mostrar: SKILL.md  references/
```

---

## Actualizar

```bash
cd cfdi-40-skill
git pull
cp -r cfdi-40 ~/.claude/skills/cfdi-40
```

---

## Cómo funciona

Una vez instalado, Claude Code activa el skill automáticamente cuando detecta preguntas relacionadas con CFDI, por ejemplo:

- "¿Por qué me da el error CFDI40139?"
- "Cómo llenar el campo RegimenFiscalReceptor"
- "El XSLT de cadena original me devuelve vacío"
- "Qué campos lleva un CFDI de tipo P"
- "Cuál es la clave de FormaPago para SPEI"
- Cualquier pregunta sobre timbrado, PAC, XML fiscal, CentroCFDI

No necesitas hacer nada especial — Claude lo usa cuando es relevante al problema.

---

## Estructura

```
cfdi-40/
├── SKILL.md                  ← Trigger + 10 reglas de oro (siempre en contexto)
└── references/
    ├── guia.md               ← Estructura XML completa, reglas campo a campo,
    │                            XSLT diagnóstico con snippets C#/Python/bash,
    │                            XSD validación, Complemento de Pagos 2.0,
    │                            tabla de restricciones por TipoDeComprobante,
    │                            FAQ y glosario
    ├── catalogos.md          ← Todos los catálogos pequeños completos:
    │                            FormaPago, MetodoPago, TipoDeComprobante,
    │                            Exportacion, TipoRelacion, RegimenFiscal,
    │                            UsoCFDI, ObjetoImp, Impuesto, TipoFactor,
    │                            TasaOCuota (todas las tasas IEPS/IVA/ISR),
    │                            Periodicidad, Meses, Estado MEX
    ├── errores.md            ← 122 errores CFDI40101–CFDI40999 con causa
    │                            exacta, cómo corregir cada uno, y sección
    │                            de los 5 errores más frecuentes
    ├── carta-porte.md        ← Carta Porte 3.1: estructura, nodos por modo de
    │                            transporte, catálogos de decisión, cuadres y flujo
    ├── carta-porte-errores.md ← Matriz CP101–CP204 (+CP999) por sección
    ├── pagos-errores.md      ← Matriz CRP201xx/CRP202xx del Complemento de Pagos
    ├── nomina.md             ← Nómina 1.2 (Rev. E): CFDI sobre tipo N, árbol de
    │                            nodos, orden de decisión, cuadres, catálogos
    │                            (TipoPercepcion/TipoDeduccion/TipoOtroPago…)
    │                            y casos especiales (viáticos, ajuste de subsidio,
    │                            ISR anual, indemnización, fallecidos, asimilados)
    └── nomina-errores.md     ← Matriz NOM1–NOM111 por sección con patrón de
                                 error handling para pantallas
```

Claude carga solo el archivo de referencia que necesita según el problema — el contexto se mantiene eficiente.

---

## Cobertura

| Área | Detalle |
|---|---|
| Versión | CFDI 4.0 (Anexo 20, publicado 13/01/2022) |
| Complementos | Pagos 2.0 (29/12/2021) · Carta Porte 3.1 · Nómina 1.2 Rev. E |
| Errores | 122 errores CFDI40101–CFDI40999 (versión 25/03/2026) · CP101–CP204 · CRP201xx/202xx · NOM1–NOM111 (Rev. E) |
| Catálogos completos | FormaPago, MetodoPago, TipoDeComprobante, Exportacion, TipoRelacion, RegimenFiscal, UsoCFDI, ObjetoImp, Impuesto, TipoFactor, TasaOCuota, Periodicidad, Meses, Estado (MEX), y de nómina: TipoNomina, PeriodicidadPago, TipoContrato, TipoRegimen, TipoJornada, RiesgoPuesto, TipoIncapacidad, TipoHoras, OrigenRecurso, TipoPercepcion (001–057), TipoOtroPago |
| Catálogos referenciados por URL | ClaveProdServ, ClaveUnidad, CodigoPostal, Moneda, Pais, Banco, TipoDeduccion completo (ajustes 024–115) y otros de alto volumen |
| Archivos técnicos | cfdv40.xsd, catCFDI.xsd, Pagos10.xsd, nomina12.xsd, catNomina.xsd, cadenaoriginal_4_0.xslt, Pagos20.xslt, nomina12.xslt |
| Snippets de código | C# (.NET XslCompiledTransform), Python (lxml), Bash (xsltproc) |

---

## Fuentes

- [Anexo 20 v4.0 — SAT](https://www.sat.gob.mx/consultas/43074/actualizacion-factura-electronica---reforma-fiscal-2022-)
- [Referencia GNcys CFDI 4.0](https://www.gncys.com/anexo20/4.0/)
- [Complemento de Pagos 2.0](https://www.gncys.com/complementos/pagos20/)
- [Matriz de errores CFDI 4.0](https://www.gncys.com/anexo20/4.0/errores/)
- [Complemento de Nómina — SAT](http://omawww.sat.gob.mx/tramitesyservicios/Paginas/complemento_nomina.htm) (Guía de llenado CFDI 4.0 + Nómina 1.2, Matriz de errores Rev. E, nomina12.xsd, catNomina)
