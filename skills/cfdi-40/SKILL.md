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
  facturación mexicanos. También cubre el Complemento Carta Porte 3.1 (CCP):
  transporte de bienes, Autotransporte, Transporte Marítimo/Aéreo/Ferroviario,
  Ubicaciones origen/destino, Mercancías, material peligroso, Figura de
  Transporte, errores CPxxx (CP101–CP204), TranspInternac, IdCCP, carta de porte.
  También cubre el Complemento de Nómina 1.2 (CFDI tipo N): recibo de nómina,
  percepciones, deducciones, otros pagos, subsidio al empleo, TipoPercepcion,
  TipoDeduccion, TipoOtroPago, TipoContrato, TipoRegimen, RegistroPatronal,
  salario diario integrado (SDI), IMSS, NSS, aguinaldo, PTU, finiquito,
  indemnización, incapacidades, horas extra, viáticos, asimilados a salarios,
  errores NOMxxx (NOM1–NOM111).
  También aplica a CentroCFDI, eAdaptor, o cualquier sistema receptor/emisor de
  comprobantes fiscales digitales.
---

# Skill: CFDI 4.0 — Referencia Técnica Completa

## Contexto del dominio

- **Versión:** CFDI 4.0 (Anexo 20 SAT, publicado 13/01/2022, obligatorio desde 1/05/2022)
- **Complemento de Pagos:** versión 2.0 (publicado 29/12/2021)
- **Namespace obligatorio:** `http://www.sat.gob.mx/cfd/4`
- **XSD oficial:** `https://www.sat.gob.mx/sitio_internet/cfd/4/cfdv40.xsd`
- **XSLT cadena original CFDI:** `https://www.sat.gob.mx/sitio_internet/cfd/4/cadenaoriginal_4_0.xslt`
- **XSLT cadena original Pagos:** `https://www.sat.gob.mx/sitio_internet/cfd/Pagos/Pagos20.xslt`
- **Verificador UUID:** `https://verificacfdi.facturaelectronica.sat.gob.mx/`

---

## Cuándo leer los archivos de referencia

Solo cuando el problema requiere más profundidad de la que hay en este archivo:

| Situación | Archivo |
|---|---|
| Error CFDI40xxx poco común (fuera de los top-10 de abajo) | `references/errores.md` |
| Catálogo completo de RegimenFiscal, TipoRelacion, Meses, Estado | `references/catalogos.md` |
| Estructura XML completa con ejemplo / Complemento de Pagos 2.0 detallado | `references/guia.md` |
| Problema de XSLT que no resuelven los checks de abajo | `references/guia.md` sección 13 |
| Validación XSD con código | `references/guia.md` sección 14 |
| **Carta Porte 3.1**: estructura, nodos por modo, catálogos de decisión, flujo de captura | `references/carta-porte.md` |
| **Carta Porte 3.1**: error CPxxx (CP101–CP204) → atributo, regla y cómo resolver | `references/carta-porte-errores.md` |
| **Pagos 2.0**: error CRPxxxxx (CRP201xx/202xx) → atributo, regla y cómo resolver | `references/pagos-errores.md` |
| **Nómina 1.2**: estructura, catálogos de percepciones/deducciones, casos especiales (viáticos, ajuste subsidio, ISR anual) | `references/nomina.md` |
| **Nómina 1.2**: error NOMxxx (NOM1–NOM111) → atributo, regla y cómo resolver | `references/nomina-errores.md` |

---

## Diagnóstico de errores CFDI40xxx — Top 10

Estos cubren el 80% de los rechazos. Resolver primero aquí antes de ir a `references/errores.md`.

### CFDI40101 — Fecha con formato incorrecto
Formato exacto requerido: `AAAA-MM-DDThh:mm:ss`
No va zona horaria (`-06:00`), no va milisegundos. Hora local del lugar de expedición.
✓ `2024-01-15T10:30:00` ✗ `2024-01-15T10:30:00-06:00` ✗ `2024-01-15`

### CFDI40102 — Sello inválido (digestión ≠ desencripción)
Causas en orden de frecuencia:
1. XML modificado después de generar el sello (un espacio, un atributo de orden)
2. Cadena original mal generada — ver sección XSLT más abajo
3. CSD caducado o revocado — verificar en SAT
4. BOM (Byte Order Mark) en el XML — `hexdump -C cfdi.xml | head -1` (si empieza con `ef bb bf`, hay BOM)
5. Encoding distinto de UTF-8

### CFDI40103 / CFDI40125 — FormaPago o MetodoPago no debe existir
En TipoDeComprobante `T`, `N` o `P`: eliminar FormaPago.
En TipoDeComprobante `T` o `P`: eliminar MetodoPago.

### CFDI40105 — FormaPago no es "99" cuando debería serlo
Cuando MetodoPago=`PPD` (pago diferido o en parcialidades), FormaPago **debe** ser `99`.
Cuando MetodoPago=`PUE` (pago al contado), FormaPago debe ser la forma real (01, 03, 28, etc.).

### CFDI40108 / CFDI40109 — SubTotal incorrecto
- Tipo `I`, `E`, `N`: `SubTotal = ROUND(∑ Concepto.Importe, decimales_moneda)` — el redondeo importa
- Tipo `T`, `P`: `SubTotal = 0` obligatorio

### CFDI40119 — Total incorrecto
`Total = SubTotal − Descuento + TotalImpuestosTrasladados − TotalImpuestosRetenidos`
Todos los valores redondeados a los decimales que soporta la moneda (MXN=2).
En tipo `T` y `P`: `Total = 0`.

### CFDI40139 / CFDI40145 — Nombre de Emisor o Receptor no coincide con el SAT
El campo `Nombre` debe ser **byte-a-byte idéntico** al registrado en la l_RFC del SAT.
Un espacio extra, una mayúscula diferente o un acento distinto causa rechazo.
Fuente de verdad: Constancia de Situación Fiscal → `https://www.sat.gob.mx/aplicacion/login/53027/genera-tu-constancia-de-situacion-fiscal`
Si el receptor es público en general (RFC=`XAXX010101000`): Nombre debe ser exactamente `PUBLICO EN GENERAL`.

### CFDI40161 — UsoCFDI no corresponde al tipo de persona o régimen
Los más comunes a verificar:
- CFDI tipo `P` → UsoCFDI **debe** ser `CP01`
- CFDI tipo `N` → UsoCFDI **debe** ser `CN01`
- Claves D01–D10 → **solo personas físicas**, no morales
- Receptor extranjero (RFC=`XEXX010101000`) → usar `S01` o `G03`

### CFDI40171 / CFDI40172 — ObjetoImp inconsistente con nodo Impuestos
- ObjetoImp=`02` → el nodo `Impuestos` **debe existir** en el concepto (con Traslados y/o Retenciones)
- ObjetoImp=`01` o `03` → el nodo `Impuestos` **no debe existir** en el concepto
- En CFDI tipo `P`: todos los conceptos llevan ObjetoImp=`01`

### CFDI40201 — Nodo Impuestos (global) no debe existir
En TipoDeComprobante `T`, `P` o `N`: eliminar el nodo `<cfdi:Impuestos>` del comprobante (el de nivel raíz, no el de los conceptos).

### CFDI40205 / CFDI40221 — TotalImpuestosTrasladados no cuadra
Error de redondeo casi siempre. La regla es:
- El `Importe` de cada `Traslado` en el comprobante = `ROUND(∑ ImporteTraslado de conceptos del mismo impuesto+tasa, 2)`
- `TotalImpuestosTrasladados` = `ROUND(∑ Traslado.Importe, 2)`
**No** calcular como `Base × TasaOCuota` directo — usar la suma de los importes ya calculados en conceptos.

---

## Catálogos de uso frecuente

### c_TipoDeComprobante

| Clave | Descripción | SubTotal | Total | Moneda | FormaPago | MetodoPago | Nodo Impuestos | UsoCFDI receptor |
|---|---|---|---|---|---|---|---|---|
| I | Ingreso | ∑ conceptos | Calculado | Cualquiera | ✅ | ✅ | ✅ Condicional | Cualquiera |
| E | Egreso | ∑ conceptos | Calculado | Cualquiera | ✅ | ✅ | ✅ Condicional | Cualquiera |
| T | Traslado | ∑ conceptos | 0 | Cualquiera | ❌ | ❌ | ✅ Condicional | Cualquiera |
| N | Nómina | Percep.+OtrosPagos | SubTotal−Descuento | **MXN** | ❌ | **PUE** | ❌ No existe | **CN01** |
| P | Pago | **0** | **0** | **XXX** | ❌ | ❌ | ❌ No existe | **CP01** |

### c_FormaPago

| Clave | Descripción | Bancarizado |
|---|---|---|
| 01 | Efectivo | No |
| 02 | Cheque nominativo | Sí |
| 03 | Transferencia electrónica de fondos | Sí |
| 04 | Tarjeta de crédito | Sí |
| 05 | Monedero electrónico | Sí |
| 06 | Dinero electrónico | Sí |
| 08 | Vales de despensa | No |
| 12 | Dación en pago | No |
| 28 | Tarjeta de débito | Sí |
| 29 | Tarjeta de servicios | Sí |
| 30 | Aplicación de anticipos | No |
| 99 | Por definir — usar con MetodoPago=PPD | Opcional |

Catálogo completo (22 claves): `references/catalogos.md`

### c_MetodoPago

| Clave | Descripción | Cuándo usarlo |
|---|---|---|
| PUE | Pago en una sola exhibición | Se cobra al momento de emitir el CFDI |
| PPD | Pago en parcialidades o diferido | Se cobra después — requiere CFDI de Pago posterior |

### c_UsoCFDI (los más usados)

| Clave | Descripción | Física | Moral |
|---|---|---|---|
| G01 | Adquisición de mercancías | Sí | Sí |
| G03 | Gastos en general | Sí | Sí |
| I01 | Construcciones | Sí | Sí |
| I03 | Equipo de transporte | Sí | Sí |
| I04 | Equipo de cómputo y accesorios | Sí | Sí |
| D01 | Honorarios médicos, dentales y gastos hospitalarios | Sí | **No** |
| S01 | Sin efectos fiscales | Sí | Sí |
| CP01 | Pagos — **obligatorio en tipo P** | Sí | Sí |
| CN01 | Nómina — **obligatorio en tipo N** | Sí | **No** |

Catálogo completo (24 claves) con todas las D y todas las I: `references/catalogos.md`

### c_ObjetoImp

| Clave | Descripción | Nodo Impuestos en concepto |
|---|---|---|
| 01 | No objeto de impuesto | **No debe existir** |
| 02 | Sí objeto de impuesto | **Debe existir** |
| 03 | Sí objeto, no obligado al desglose | **No debe existir** |

### c_Impuesto / c_TipoFactor / c_TasaOCuota (IVA)

| Impuesto | Factor | TasaOCuota | Uso |
|---|---|---|---|
| 002 (IVA) | Tasa | `0.160000` | IVA 16% — tasa general |
| 002 (IVA) | Tasa | `0.080000` | IVA 8% — zona fronteriza norte |
| 002 (IVA) | Tasa | `0.000000` | IVA 0% — alimentos, medicamentos, exportaciones |
| 002 (IVA) | Exento | — | Exento — sin TasaOCuota ni Importe |
| 001 (ISR) | Tasa | `0`–`0.350000` | Retención ISR (variable) |
| 003 (IEPS) | Tasa | `0.265000`–`1.600000` | IEPS (ver catálogo completo) |

**Regla TipoFactor=Exento:** en Traslados — NO se registran TasaOCuota ni Importe. En Retenciones — **Exento no está permitido**.

### RFC genéricos

| RFC | Uso | Nombre obligatorio |
|---|---|---|
| `XAXX010101000` | Público en General (nacional) | `PUBLICO EN GENERAL` |
| `XEXX010101000` | Extranjero | Nombre de la empresa extranjera |

---

## Diagnóstico XSLT — cadena original

Cuando la cadena original sale vacía, mal formada, o el sello no valida, seguir este checklist en orden:

**1. Verificar el namespace del XML**
```bash
grep -o 'xmlns:cfdi="[^"]*"' mi_cfdi.xml
# Debe ser exactamente: xmlns:cfdi="http://www.sat.gob.mx/cfd/4"
# Si dice cfd/3 o cualquier otro → el XSLT no encontrará nada → cadena vacía
```

**2. Verificar que el procesador XSLT use versión 1.0**
El XSLT del SAT es XSLT 1.0. Saxon en modo 2.0/3.0 da resultados incorrectos.
```bash
xsltproc cadenaoriginal_4_0.xslt mi_cfdi.xml   # xsltproc siempre usa 1.0 ✓
```

**3. Detectar BOM en el XML**
```bash
hexdump -C mi_cfdi.xml | head -1
# Si empieza con "ef bb bf" → tiene BOM → eliminar con:
sed -i '1s/^\xEF\xBB\xBF//' mi_cfdi.xml
```

**4. Verificar encoding**
```bash
file mi_cfdi.xml   # debe decir UTF-8
```

**5. Verificar que la cadena sea válida**
Una cadena original correcta:
- Empieza con `||4.0|`
- Termina con `||`
- Sin saltos de línea internos
- Solo contiene los atributos presentes en el XML (los opcionales ausentes no aparecen)

**Snippet C# (.NET)**
```csharp
var xslt = new XslCompiledTransform();
xslt.Load("cadenaoriginal_4_0.xslt");
var xmlDoc = new XmlDocument();
xmlDoc.LoadXml(xmlCfdi);
using var sw = new StringWriter();
using var xw = XmlWriter.Create(sw, xslt.OutputSettings);
xslt.Transform(xmlDoc, null, xw);
string cadena = sw.ToString();
```

**Snippet Python**
```python
from lxml import etree
xml_doc = etree.parse("mi_cfdi.xml")
xslt_doc = etree.parse("cadenaoriginal_4_0.xslt")
cadena = str(etree.XSLT(xslt_doc)(xml_doc))
```

**Nota:** El Complemento de Pagos tiene su propio XSLT (`Pagos20.xslt`) — se transforma por separado, no con el mismo archivo del CFDI.

---

## CFDI de Pago (tipo P) — valores fijos obligatorios

El CFDI "sobre" que contiene el Complemento de Pagos debe tener exactamente:

```xml
TipoDeComprobante="P"
SubTotal="0"
Total="0"
Moneda="XXX"
Exportacion="01"
<!-- NO incluir: FormaPago, MetodoPago, CondicionesDePago, TipoCambio -->
<!-- NO incluir nodo cfdi:Impuestos -->

<!-- Receptor -->
UsoCFDI="CP01"

<!-- Un solo concepto con valores fijos -->
ClaveProdServ="84111506"
Cantidad="1"
ClaveUnidad="ACT"
Descripcion="Pago"
ValorUnitario="0"
Importe="0"
ObjetoImp="01"
<!-- NO incluir Descuento ni nodo Impuestos en el concepto -->
```

Para la estructura completa del complemento `pago20:Pagos` con todos sus nodos y cálculos de Totales: `references/guia.md` sección 11.

**Errores CRP (matriz completa en `references/pagos-errores.md`):** códigos `CRP201xx` (CFDI sobre P, valores fijos) y `CRP202xx` (complemento). Las familias que más rechazan:
- **Cuadres totalizados** (CRP20201–20211, 20265/268/274): TotalRetenciones*/TotalTraslados*/MontoTotalPagos/BaseP/ImporteP = Σ de los DoctoRelacionado × TipoCambioP. **Calcúlalos en servidor**, no los teclee el usuario.
- **Por pago** (CRP20212–20235): FormaDePagoP≠`99`; MonedaP≠`XXX`; TipoCambioP=`1` si MXN (requerido si otra); Monto>0; cuentas (CtaOrd/Ben) solo si forma bancarizada; TipoCadPago solo si forma=`03` y entonces Cert/Cad/Sello obligatorios.
- **Por documento relacionado** (CRP20236–20247, 20278/279): ObjetoImpDR=`02`→ImpuestosDR existe; `01/03/04/05`→no existe; EquivalenciaDR=`1` si misma moneda; ImpSaldoInsoluto = ImpSaldoAnt − ImpPagado.

---

## Campos nuevos en v4.0 vs. v3.3 (causas frecuentes de migración fallida)

| Campo | Nodo | Obligatorio | Descripción |
|---|---|---|---|
| `Exportacion` | Comprobante | Sí | Siempre requerido. Sin exportación: `01` |
| `RegimenFiscalReceptor` | Receptor | Sí | El régimen fiscal del receptor — nuevo |
| `DomicilioFiscalReceptor` | Receptor | Sí | CP del domicilio fiscal del receptor en el SAT |
| `ObjetoImp` | Concepto | Sí | En cada concepto — nuevo |
| Validación Nombre | Emisor y Receptor | — | Ahora el SAT valida Nombre contra l_RFC en tiempo real |

---

## Complemento Carta Porte 3.1 (CCP) — navegador

Complemento dentro de un CFDI 4.0 **tipo T (Traslado)** o **tipo I (Ingreso)** que acredita el transporte de bienes. Detalle profundo en `references/carta-porte.md`; errores en `references/carta-porte-errores.md`.

**Valores fijos por tipo de comprobante:**
| | Tipo T (Traslado, medios propios) | Tipo I (Ingreso, transportista cobra flete) |
|---|---|---|
| Moneda | `XXX` | ≠ XXX (MXN/USD…) |
| SubTotal / Total | `0` / `0` | calculado |
| Receptor.Rfc | = Emisor.Rfc | RFC del cliente (en l_RFC) o genérico |
| UsoCFDI | `S01` | el que aplique |
| ClaveProdServ | la del bien | clave de **servicio de transporte** (78101xxx…, ver CP109) |
| `CartaPorte:Version` | `3.1` | `3.1` |

**Orden de decisión (gobierna qué nodos son obligatorios):**
`TipoComprobante (T/I)` → `modo(s) de transporte` (01 Auto · 02 Marítimo · 03 Aéreo · 04 Ferroviario) → `TranspInternac (Sí/No)` → `RegistroISTMO` → `SectorCOFEPRIS` → `MaterialPeligroso`. Cada switch habilita/obliga/prohíbe bloques completos.

**Reglas que causan el 80% de los rechazos CPxxx:**
- **Condicionales "no debe existir"**: si TranspInternac=`No`, omitir (no enviar vacío) RegimenesAduaneros/EntradaSalidaMerc/PaisOrigenDestino/ViaEntradaSalida (CP120/122/124). Igual con ISTMO (CP127).
- **Conteo de Ubicaciones por modo**: Auto/Marítimo/Aéreo ≥2 (1 Origen+1 Destino, CP130); Ferroviario ≥1 Origen + ≥5 Destino (CP128/129).
- **Cuadres**: `TotalDistRec`=Σ DistanciaRecorrida(Destino) (CP126); `PesoBrutoTotal`/`PesoNetoTotal` según modo (CP149–152); `NumTotalMercancias`=conteo (CP154).
- **Material peligroso**: si la ClaveProdServCP tiene flag → MaterialPeligroso + CveMaterialPeligroso + Embalaje (CP155–157) + seguro medio ambiente en Auto (CP182).
- **Autotransporte**: obliga FiguraTransporte con Operador `01` + NumLicencia (CP193/194/196); Remolques según col Remolque de c_ConfigAutotransporte (CP184).
- **Catálogos con columna de decisión**: c_ConfigAutotransporte.Remolque, c_TipoDeServicio.Contenedor, c_ClaveProdServCP.MaterialPeligroso, c_RegimenAduanero.ImpoExpo — el valor de la columna decide obligatorio/opcional/prohibido (ver `carta-porte.md` §4).

**Patrón de error handling**: pre-valida local en el orden de decisión de arriba **antes** de enviar al PAC; cuando el PAC devuelva `CPxxx`, traduce el código → sección/paso del wizard y resalta el campo (no solo mostrar el texto del SAT). Tabla completa en `carta-porte-errores.md`.

---

## Complemento de Nómina 1.2 (CFDI tipo N) — navegador

Complemento `nomina12:Nomina` (namespace `http://www.sat.gob.mx/nomina12`, Version fija `1.2`) dentro de un CFDI 4.0 **tipo N**, uno por trabajador y periodo. Detalle profundo en `references/nomina.md`; errores NOM1–NOM111 en `references/nomina-errores.md`.

**CFDI "sobre" — valores fijos (NOM1–NOM29):** `Moneda=MXN` · `Exportacion=01` · `MetodoPago=PUE` · sin FormaPago/CondicionesDePago/TipoCambio/InformacionGlobal · Receptor: RFC del trabajador (13, en l_RFC), `RegimenFiscalReceptor=605`, `UsoCFDI=CN01` · **un solo concepto** sin hijos: `ClaveProdServ=84111505`, `Cantidad=1`, `ClaveUnidad=ACT`, `Descripcion="Pago de nómina"`, `ObjetoImp=01`, sin nodo Impuestos. `SubTotal=TotalPercepciones+TotalOtrosPagos`, `Descuento=TotalDeducciones`, `Total=SubTotal−Descuento`.

**Orden de decisión (gobierna qué nodos son obligatorios):**
`TipoContrato (01–08 vs 09+)` → `TipoRegimen (02/03/04 vs 05–99)` → `RegistroPatronal` (obligatorio 01–08, prohibido 09+) → bloque IMSS (NSS, FechaInicioRelLaboral, Antigüedad, RiesgoPuesto, SDI si hay RegistroPatronal) → subsidio (TipoRegimen 02 → OtroPago 002 obligatorio) → por cada `TipoPercepcion`, sus nodos hijo.

**Reglas que causan el 80% de los rechazos NOMxxx:**
- **TipoPercepcion dispara nodos**: 019→HorasExtra · 014→Incapacidades (Σ ImporteMonetario = gravado+exento) · 022/023/025→SeparacionIndemnizacion + su total · 039/044→JubilacionPensionRetiro (039: TotalUnaExhibicion; 044: TotalParcialidad+MontoDiario, excluyentes) · 045→AccionesOTitulos · 038→ImporteExento=0 (previsión social sin clave → 056).
- **Cuadres**: TotalPercepciones = TotalSueldos+TotalSepInd+TotalJubPR = TotalGravado+TotalExento; TotalDeducciones = TotalOtrasDeducciones+TotalImpuestosRetenidos (este último = Σ deducciones 002, y no existe si no hay 002); TotalOtrosPagos = Σ importes. **Calcular en servidor.**
- **Cuenta de depósito**: CLABE 18 → sin atributo Banco (y dígito de control válido); cuenta 10/11/16 → Banco obligatorio.
- **Ninguna percepción con gravado=0 y exento=0** a la vez; deducciones con Importe > 0.
- **Subsidio**: OtroPago 002 con nodo SubsidioAlEmpleo e Importe ≤ SubsidioCausado; topes de SubsidioCausado (NOM101/108) cambian por decreto/UMA — parametrizables.

**Casos especiales** (ver `nomina.md` §7): viáticos (OtroPago 003 → Percepcion 050 + Deduccion 081), ajuste mensual de subsidio (Deduccion 107/002/071 + OtroPago 007/008), ISR anual, separación con TipoRegimen 13, trabajador fallecido (XAXX010101000 + CURP), asimilados (contrato 09, régimen 05–11, sin subsidio).

---

## Fórmulas de cuadre (para verificar antes de timbrar)

```
SubTotal     = ROUND(∑ Concepto.Importe, decimales_moneda)
Descuento    = ROUND(∑ Concepto.Descuento, decimales_moneda)  [si aplica]
TotalRetenidos   = ROUND(∑ Retencion.Importe, decimales_moneda)
TotalTrasladados = ROUND(∑ Traslado.Importe, decimales_moneda)
Total        = SubTotal - Descuento + TotalTrasladados - TotalRetenidos

Traslado.Importe (global) = ROUND(∑ Traslado.Importe del mismo tipo en conceptos, decimales)
Retencion.Importe (global) = ROUND(∑ Retencion.Importe del mismo tipo en conceptos, decimales)

[MXN = 2 decimales | BHD = 3 decimales | CLP, BIF, DJF = 0 decimales]
```
