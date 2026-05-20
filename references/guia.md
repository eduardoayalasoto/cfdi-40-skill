# Guía Técnica CFDI 4.0 — Estructura, Campos, XSLT, XSD y Complemento de Pagos

> Fuente: Anexo 20 SAT v4.0 (13/01/2022), GNcys, Complemento de Pagos 2.0 (29/12/2021)

## Tabla de contenido

1. [Marco legal y vigencia](#1-marco-legal-y-vigencia)
2. [Estructura XML del CFDI 4.0](#2-estructura-xml-del-cfdi-40)
3. [Nodo Comprobante — todos los campos](#3-nodo-comprobante--todos-los-campos)
4. [Nodo Emisor](#4-nodo-emisor)
5. [Nodo Receptor](#5-nodo-receptor)
6. [Nodo Conceptos y Concepto](#6-nodo-conceptos-y-concepto)
7. [Nodo Impuestos (nivel comprobante)](#7-nodo-impuestos-nivel-comprobante)
8. [Nodo CfdiRelacionados](#8-nodo-cfdirelacionados)
9. [Nodo InformacionGlobal](#9-nodo-informacionglobal)
10. [Restricciones por TipoDeComprobante](#10-restricciones-por-tipodecomprobante)
11. [Complemento de Pagos 2.0](#11-complemento-de-pagos-20)
12. [Cadena Original y Firma Digital](#12-cadena-original-y-firma-digital)
13. [XSLT — Problemas y soluciones](#13-xslt--problemas-y-soluciones)
14. [XSD — Validación de esquema](#14-xsd--validación-de-esquema)
15. [FAQ](#15-faq)
16. [Glosario](#16-glosario)
17. [URLs de recursos técnicos](#17-urls-de-recursos-técnicos)

---

## 1. Marco Legal y Vigencia

- **Versión:** CFDI 4.0 | **Publicación:** 13 enero 2022 | **Obligatoria desde:** 1 mayo 2022
- **Base legal:** Artículos 29 y 29-A del CFF; Reglas 2.7.1.29 y 2.7.1.32 de la RMF vigente
- **Complemento de Pagos 2.0:** vigente desde 1 enero 2022
- **Principales cambios vs. v3.3:**
  - RegimenFiscalReceptor: nuevo campo obligatorio
  - DomicilioFiscalReceptor: nuevo campo obligatorio
  - Exportacion: nuevo campo obligatorio
  - ObjetoImp: nuevo campo obligatorio en cada concepto
  - Nombre de Emisor y Receptor: validado contra l_RFC del SAT en tiempo real

---

## 2. Estructura XML del CFDI 4.0

```xml
<?xml version="1.0" encoding="UTF-8"?>
<cfdi:Comprobante
  xmlns:cfdi="http://www.sat.gob.mx/cfd/4"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.sat.gob.mx/cfd/4
                      http://www.sat.gob.mx/sitio_internet/cfd/4/cfdv40.xsd"
  Version="4.0"
  Serie="A"
  Folio="123"
  Fecha="2024-01-15T10:30:00"
  Sello="..."
  FormaPago="03"
  NoCertificado="..."
  Certificado="..."
  SubTotal="1000.00"
  Moneda="MXN"
  Total="1160.00"
  TipoDeComprobante="I"
  Exportacion="01"
  MetodoPago="PUE"
  LugarExpedicion="06600">

  <!-- Opcional: solo en facturas globales -->
  <cfdi:InformacionGlobal Periodicidad="04" Meses="01" Año="2024"/>

  <!-- Opcional: cuando se relaciona con otros CFDIs -->
  <cfdi:CfdiRelacionados TipoRelacion="04">
    <cfdi:CfdiRelacionado UUID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"/>
  </cfdi:CfdiRelacionados>

  <cfdi:Emisor
    Rfc="AAA010101AAA"
    Nombre="EMPRESA EJEMPLO SA DE CV"
    RegimenFiscal="601"/>

  <cfdi:Receptor
    Rfc="BBB010101BBB"
    Nombre="CLIENTE EJEMPLO SA DE CV"
    DomicilioFiscalReceptor="06700"
    RegimenFiscalReceptor="601"
    UsoCFDI="G03"/>

  <cfdi:Conceptos>
    <cfdi:Concepto
      ClaveProdServ="84111506"
      Cantidad="1"
      ClaveUnidad="E48"
      Descripcion="Servicio de consultoría"
      ValorUnitario="1000.00"
      Importe="1000.00"
      ObjetoImp="02">
      <cfdi:Impuestos>
        <cfdi:Traslados>
          <cfdi:Traslado
            Base="1000.00"
            Impuesto="002"
            TipoFactor="Tasa"
            TasaOCuota="0.160000"
            Importe="160.00"/>
        </cfdi:Traslados>
      </cfdi:Impuestos>
    </cfdi:Concepto>
  </cfdi:Conceptos>

  <cfdi:Impuestos TotalImpuestosTrasladados="160.00">
    <cfdi:Traslados>
      <cfdi:Traslado
        Base="1000.00"
        Impuesto="002"
        TipoFactor="Tasa"
        TasaOCuota="0.160000"
        Importe="160.00"/>
    </cfdi:Traslados>
  </cfdi:Impuestos>

  <cfdi:Complemento>
    <!-- El PAC agrega aquí el Timbre Fiscal Digital (TFD) -->
    <tfd:TimbreFiscalDigital
      xmlns:tfd="http://www.sat.gob.mx/TimbreFiscalDigital"
      Version="1.1"
      UUID="..."
      FechaTimbrado="..."
      RfcProvCertif="..."
      SelloCFD="..."
      NoCertificadoSAT="..."
      SelloSAT="..."/>
  </cfdi:Complemento>

</cfdi:Comprobante>
```

---

## 3. Nodo Comprobante — Todos los Campos

### Version
- **Valor fijo:** `4.0` — lo integra el sistema, no el usuario

### Serie
- Control interno del contribuyente | 1–25 caracteres alfanuméricos | Opcional

### Folio
- Control interno del contribuyente | 1–40 caracteres alfanuméricos | Opcional

### Fecha
- **Formato:** `AAAA-MM-DDThh:mm:ss` (hora local del lugar de expedición, sin zona horaria)
- **Error si mal:** CFDI40101

### Sello
- Firma digital SHA-256+RSA del emisor sobre la cadena original, en base64
- Lo genera el sistema de facturación con el CSD
- **Error si mal:** CFDI40102

### FormaPago
- Clave de c_FormaPago — ver references/catalogos.md
- **NO debe existir** en TipoDeComprobante T, N o P → CFDI40103
- FormaPago=`99` requiere MetodoPago=`PPD` → CFDI40105

### NoCertificado / Certificado
- Número e contenido (base64) del CSD del emisor — los integra el sistema
- **Error si mal:** CFDI40106

### CondicionesDePago
- Texto libre de condiciones comerciales | 1–1000 chars | Opcional
- **NO debe existir** en TipoDeComprobante T, P o N

### SubTotal
- Suma de Importe de todos los conceptos (antes de descuentos e impuestos)
- Para T y P: debe ser `0`
- Para I, E, N: `ROUND(∑Concepto.Importe, decimales_moneda)`
- **Errores:** CFDI40107, CFDI40108, CFDI40109

### Descuento
- Suma de descuentos de todos los conceptos | Opcional
- Solo en I, E, N cuando algún concepto tiene descuento
- Debe ser ≤ SubTotal
- **Errores:** CFDI40110, CFDI40111, CFDI40112

### Moneda
- Código ISO 4217: `MXN`, `USD`, `EUR`, etc.
- CFDI tipo P: siempre `XXX`
- **Error si inválido:** CFDI40113

### TipoCambio
- Requerido cuando Moneda ≠ MXN y ≠ XXX
- No debe existir cuando Moneda = XXX (CFDI de Pago)
- Cuando Moneda = MXN: valor `1`
- **Errores:** CFDI40114–CFDI40118

### Total
- `SubTotal - Descuento + TotalImpuestosTrasladados - TotalImpuestosRetenidos`
- Para T y P: debe ser `0`
- **Errores:** CFDI40119, CFDI40120

### TipoDeComprobante
- I, E, T, N o P — ver tabla de restricciones en sección 10
- **Error si inválido:** CFDI40121

### Exportacion
- Campo **obligatorio** en todos los CFDI
- `01` = no aplica (la mayoría de casos)
- `02` = exportación definitiva A1 (requiere Complemento Comercio Exterior)
- **Errores:** CFDI40122, CFDI40123

### MetodoPago
- PUE o PPD
- **NO debe existir** en T o P
- **Errores:** CFDI40124, CFDI40125

### LugarExpedicion
- Código postal del lugar de expedición (matriz o sucursal)
- Debe existir en c_CodigoPostal
- **Error:** CFDI40126

### Confirmacion
- 5 chars alfanuméricos — asignada por el PAC
- Solo cuando TipoCambio o Total están fuera del rango permitido
- **Errores:** CFDI40127–CFDI40129

---

## 4. Nodo Emisor

```xml
<cfdi:Emisor
  Rfc="AAA010101AAA"
  Nombre="NOMBRE EXACTO SEGUN SAT"
  RegimenFiscal="601"
  FacAtrAdquirente="..."/>  <!-- Opcional -->
```

| Campo | Req. | Notas |
|---|---|---|
| Rfc | Sí | 12 chars (moral) o 13 chars (física) |
| Nombre | Sí | Debe coincidir **exactamente** con la l_RFC del SAT. Consultar Constancia de Situación Fiscal |
| RegimenFiscal | Sí | Clave de c_RegimenFiscal — debe corresponder al tipo de persona |
| FacAtrAdquirente | No | Número de operación para facturación atribuible al adquirente |

**Errores frecuentes:** CFDI40138 (RFC no activo), CFDI40139 (Nombre no coincide), CFDI40140–CFDI40141 (RegimenFiscal inválido)

---

## 5. Nodo Receptor

```xml
<cfdi:Receptor
  Rfc="BBB010101BBB"
  Nombre="NOMBRE EXACTO SEGUN SAT"
  DomicilioFiscalReceptor="06700"
  ResidenciaFiscal="USA"        <!-- Solo extranjeros -->
  NumRegIdTrib="12345678"       <!-- Solo extranjeros con Comercio Exterior -->
  RegimenFiscalReceptor="601"
  UsoCFDI="G03"/>
```

| Campo | Req. | Notas |
|---|---|---|
| Rfc | Sí | Debe estar en l_RFC del SAT. Genérico nacional: XAXX010101000. Genérico extranjero: XEXX010101000 |
| Nombre | Sí | Exacto según l_RFC. Si RFC=XAXX010101000: debe ser `PUBLICO EN GENERAL` |
| DomicilioFiscalReceptor | Sí | CP del domicilio fiscal del receptor en el SAT |
| ResidenciaFiscal | Condicional | Solo para extranjeros. No puede ser MEX |
| NumRegIdTrib | Condicional | Solo extranjeros + Complemento Comercio Exterior |
| RegimenFiscalReceptor | Sí | **Nuevo en v4.0** — obligatorio. Para XEXX010101000 usar 616 |
| UsoCFDI | Sí | CP01 en tipo P; CN01 en tipo N; ver catálogo completo |

**Errores frecuentes:** CFDI40143–CFDI40161

---

## 6. Nodo Conceptos y Concepto

```xml
<cfdi:Conceptos>
  <cfdi:Concepto
    ClaveProdServ="84111506"
    NoIdentificacion="SKU-001"   <!-- Opcional -->
    Cantidad="2"
    ClaveUnidad="E48"
    Unidad="Servicio"            <!-- Opcional -->
    Descripcion="Descripción del producto o servicio"
    ValorUnitario="500.00"
    Importe="1000.00"
    Descuento="100.00"           <!-- Opcional -->
    ObjetoImp="02">

    <!-- Solo si ObjetoImp="02" -->
    <cfdi:Impuestos>
      <cfdi:Traslados>
        <cfdi:Traslado
          Base="900.00"
          Impuesto="002"
          TipoFactor="Tasa"
          TasaOCuota="0.160000"
          Importe="144.00"/>
      </cfdi:Traslados>
      <cfdi:Retenciones>
        <cfdi:Retencion
          Base="900.00"
          Impuesto="001"
          TipoFactor="Tasa"
          TasaOCuota="0.100000"
          Importe="90.00"/>
      </cfdi:Retenciones>
    </cfdi:Impuestos>

  </cfdi:Concepto>
</cfdi:Conceptos>
```

### Campos del Concepto

| Campo | Req. | Notas |
|---|---|---|
| ClaveProdServ | Sí | Del catálogo c_ClaveProdServ del SAT. En CFDI de Pago: `84111506` |
| NoIdentificacion | No | Identificador interno del emisor |
| Cantidad | Sí | Cantidad de bienes/servicios. En CFDI de Pago: `1` |
| ClaveUnidad | Sí | Del catálogo c_ClaveUnidad. En CFDI de Pago: `ACT` |
| Unidad | No | Descripción de la unidad |
| Descripcion | Sí | Descripción del bien o servicio. En CFDI de Pago: `Pago` |
| ValorUnitario | Sí | > 0 en I, E, N. = 0 en P |
| Importe | Sí | Cantidad × ValorUnitario. = 0 en P |
| Descuento | No | ≤ Importe. No en T ni P |
| ObjetoImp | Sí | **Nuevo en v4.0**. 01=no objeto, 02=sí objeto, 03=sí sin desglose |

### Traslados en concepto

| Campo | Req. | Notas |
|---|---|---|
| Base | Sí | > 0. Base del impuesto |
| Impuesto | Sí | 001/002/003 |
| TipoFactor | Sí | Tasa / Cuota / Exento |
| TasaOCuota | Condicional | Requerido si TipoFactor = Tasa o Cuota. **NO si Exento** |
| Importe | Condicional | Requerido si TipoFactor = Tasa o Cuota. **NO si Exento** |

### Retenciones en concepto

Igual que Traslados, excepto: **TipoFactor=Exento no está permitido en retenciones**.

---

## 7. Nodo Impuestos (Nivel Comprobante)

```xml
<cfdi:Impuestos
  TotalImpuestosRetenidos="90.00"
  TotalImpuestosTrasladados="160.00">

  <cfdi:Retenciones>
    <!-- Un nodo por tipo de impuesto retenido -->
    <cfdi:Retencion Impuesto="001" Importe="90.00"/>
  </cfdi:Retenciones>

  <cfdi:Traslados>
    <!-- Un nodo por combinación impuesto+factor+tasa -->
    <cfdi:Traslado
      Base="1000.00"
      Impuesto="002"
      TipoFactor="Tasa"
      TasaOCuota="0.160000"
      Importe="160.00"/>
  </cfdi:Traslados>

</cfdi:Impuestos>
```

**Reglas críticas:**
- **NO debe existir** cuando TipoDeComprobante es T, P o N → CFDI40201
- Solo **un** nodo Retencion por tipo de impuesto → CFDI40208
- Solo **un** nodo Traslado por combinación impuesto+factor+tasa → CFDI40218
- TotalImpuestosRetenidos = `ROUND(∑Retencion.Importe, decimales)` → CFDI40203
- TotalImpuestosTrasladados = `ROUND(∑Traslado.Importe, decimales)` → CFDI40205
- Base y Importe de traslados globales deben cuadrar con la suma de los conceptos → CFDI40215, CFDI40221

---

## 8. Nodo CfdiRelacionados

```xml
<cfdi:CfdiRelacionados TipoRelacion="04">
  <cfdi:CfdiRelacionado UUID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"/>
  <!-- Puede haber múltiples CfdiRelacionado -->
</cfdi:CfdiRelacionados>
```

| TipoRelacion | Uso |
|---|---|
| 01 | Nota de crédito |
| 02 | Nota de débito |
| 03 | Devolución de mercancía |
| 04 | Sustitución de CFDI previo (para corregir errores) |
| 05 | Traslados de mercancías facturados previamente |
| 06 | Factura generada por traslados previos |
| 07 | CFDI por aplicación de anticipo |

---

## 9. Nodo InformacionGlobal

Solo para facturas globales de operaciones con público en general (RFC=XAXX010101000).

```xml
<cfdi:InformacionGlobal
  Periodicidad="04"
  Meses="01"
  Año="2024"/>
```

**Requisitos:**
- RegimenFiscal del emisor debe ser `621` (Incorporación Fiscal) → CFDI40132
- Meses 01–12 para periodicidad mensual; 13–18 para bimestral
- Año = año en curso o inmediato anterior → CFDI40136

---

## 10. Restricciones por TipoDeComprobante

| Campo / Nodo | I (Ingreso) | E (Egreso) | T (Traslado) | N (Nómina) | P (Pago) |
|---|---|---|---|---|---|
| FormaPago | ✅ Requerido | ✅ Requerido | ❌ No existe | ❌ No existe | ❌ No existe |
| MetodoPago | ✅ Requerido | ✅ Requerido | ❌ No existe | Opcional | ❌ No existe |
| CondicionesDePago | ✅ Permitido | ✅ Permitido | ❌ No existe | ❌ No existe | ❌ No existe |
| SubTotal | Suma conceptos | Suma conceptos | Suma conceptos | Suma conceptos | **0** |
| Total | Calculado | Calculado | Calculado | Calculado | **0** |
| Moneda | Cualquiera | Cualquiera | Cualquiera | Cualquiera | **XXX** |
| TipoCambio | Si ≠ MXN | Si ≠ MXN | Si ≠ MXN | Si ≠ MXN | ❌ No existe |
| Descuento (conceptos) | ✅ Permitido | ✅ Permitido | ❌ No existe | — | ❌ No existe |
| ObjetoImp en conceptos | ✅ | ✅ | ✅ | ✅ | **01** siempre |
| Nodo Impuestos global | ✅ Condicional | ✅ Condicional | ✅ Condicional | ❌ No existe | ❌ No existe |
| UsoCFDI receptor | Cualquiera | Cualquiera | Cualquiera | **CN01** | **CP01** |
| Complemento Pagos | ❌ | ❌ | ❌ | ❌ | ✅ Requerido |

---

## 11. Complemento de Pagos 2.0

### ¿Cuándo se usa?

Cuando el pago de la contraprestación no ocurre al momento de emitir el CFDI:
- Pago en parcialidades (PPD): se emite factura por el total, luego un CFDI de Pago por cada cobro
- Pago diferido: igual que parcialidades pero se espera pago único posterior

### Estructura del CFDI "sobre" (tipo P)

El CFDI que contiene el Complemento de Pagos debe tener estos valores fijos:

| Campo | Valor | Error si incorrecto |
|---|---|---|
| TipoDeComprobante | P | CFDI40121 |
| SubTotal | 0 | CFDI40109 |
| Total | 0 | CFDI40119 |
| Moneda | XXX | CFDI40113 |
| FormaPago | **No debe existir** | CFDI40103 |
| MetodoPago | **No debe existir** | CFDI40125 |
| CondicionesDePago | **No debe existir** | — |
| TipoCambio | **No debe existir** | CFDI40116 |
| Nodo Impuestos | **No debe existir** | CFDI40201 |
| Receptor.UsoCFDI | CP01 | CFDI40161 |
| Concepto.ClaveProdServ | 84111506 | — |
| Concepto.Cantidad | 1 | — |
| Concepto.ClaveUnidad | ACT | — |
| Concepto.Descripcion | Pago | — |
| Concepto.ValorUnitario | 0 | — |
| Concepto.Importe | 0 | — |
| Concepto.ObjetoImp | 01 | — |

### Estructura del Complemento

```xml
<pago20:Pagos xmlns:pago20="http://www.sat.gob.mx/Pagos20" Version="2.0">

  <pago20:Totales
    MontoTotalPagos="15000.00"
    TotalTrasladosBaseIVA16="12931.03"
    TotalTrasladosImpuestoIVA16="2068.97"
    TotalRetencionesISR="..."
    TotalRetencionesIVA="..."/>

  <pago20:Pago
    FechaPago="2024-01-03T12:00:00"
    FormaDePagoP="03"
    MonedaP="MXN"
    TipoCambioP="1"
    Monto="15000.00"
    NumOperacion="SPEI-123456"
    RfcEmisorCtaOrd="BNM970805DQ4"
    CtaOrdenante="123456789012345678"
    RfcEmisorCtaBen="BNM970805DQ4"
    CtaBeneficiario="987654321098765432">

    <pago20:DoctoRelacionado
      IdDocumento="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
      Serie="A"
      Folio="100"
      MonedaDR="MXN"
      EquivalenciaDR="1"
      NumParcialidad="1"
      ImpSaldoAnt="15000.00"
      ImpPagado="15000.00"
      ImpSaldoInsoluto="0.00"
      ObjetoImpDR="02">

      <pago20:ImpuestosDR>
        <pago20:TrasladosDR>
          <pago20:TrasladoDR
            BaseDR="12931.03"
            ImpuestoDR="002"
            TipoFactorDR="Tasa"
            TasaOCuotaDR="0.160000"
            ImporteDR="2068.97"/>
        </pago20:TrasladosDR>
      </pago20:ImpuestosDR>

    </pago20:DoctoRelacionado>

    <pago20:ImpuestosP>
      <pago20:TrasladosP>
        <pago20:TrasladoP
          BaseP="12931.03"
          ImpuestoP="002"
          TipoFactorP="Tasa"
          TasaOCuotaP="0.160000"
          ImporteP="2068.97"/>
      </pago20:TrasladosP>
    </pago20:ImpuestosP>

  </pago20:Pago>
</pago20:Pagos>
```

### Reglas de cálculo del Complemento de Pagos

**MontoTotalPagos** = `ROUND(∑(Pago.Monto × Pago.TipoCambioP), 2)`

**TotalTrasladosBaseIVA16** = `ROUND(∑(TrasladoP.BaseP × TipoCambioP) donde ImpuestoP=002 y TasaOCuotaP=0.160000, 2)`

**TotalTrasladosImpuestoIVA16** = `ROUND(∑(TrasladoP.ImporteP × TipoCambioP) donde ImpuestoP=002 y TasaOCuotaP=0.160000, 2)`

(Equivalente para IVA 8%, IVA 0%, IVA Exento, ISR, IEPS)

**ImpSaldoInsoluto** = `ImpSaldoAnt - ImpPagado` (≥ 0)

### Plazo de emisión

El CFDI con Complemento de Pagos debe emitirse **a más tardar el 5° día natural del mes siguiente** al que se recibió el pago.

### Criterios de asignación de pago a documentos

1. Disposición jurídica expresa
2. Acuerdo explícito entre las partes
3. El pagador indica al receptor (dentro de 5 días naturales del pago)
4. Sin indicación: se aplica al CFDI pendiente más antiguo

---

## 12. Cadena Original y Firma Digital

### ¿Qué es?

La cadena original es la representación textual canónica del CFDI, usada para generar el Sello Digital del emisor.

### Proceso completo

```
XML del CFDI
     ↓
Transformación XSLT (cadenaoriginal_4_0.xslt)
     ↓
Cadena original (texto con campos separados por |)
     ↓
Hash SHA-256 de la cadena original
     ↓
Cifrado RSA con llave privada del CSD del emisor
     ↓
Sello Digital (base64) → atributo Sello en el CFDI
```

### Formato de la cadena original

```
||4.0|A|123|2024-01-15T10:30:00|03|20001000000300022815|MXN|1000.00|1160.00|I|01|PUE|06600||AAA010101AAA|EMPRESA EJEMPLO SA DE CV|601||BBB010101BBB|CLIENTE EJEMPLO SA DE CV|06700|601|G03||...||
```

- Separador de campos: `|` (pleca)
- Inicio y fin: `||`
- Campos opcionales ausentes: se omiten (no se pone `||` doble en su lugar)
- Sin espacios extras ni saltos de línea

### Archivos XSLT oficiales

| Comprobante | URL SAT | URL GNcys (espejo) |
|---|---|---|
| CFDI 4.0 | https://www.sat.gob.mx/sitio_internet/cfd/4/cadenaoriginal_4_0.xslt | https://www.gncys.com/cfd/cadenaoriginal_4_0.xslt |
| Complemento Pagos 2.0 | https://www.sat.gob.mx/sitio_internet/cfd/Pagos/Pagos20.xslt | https://www.gncys.com/cfd/Pagos20.xslt |
| Timbre Fiscal Digital 1.1 | https://www.sat.gob.mx/sitio_internet/cfd/TimbreFiscalDigital/TimbreFiscalDigitalv11.xslt | — |

---

## 13. XSLT — Problemas y Soluciones

### Causas más frecuentes de error

#### 1. Namespace incorrecto
El XSLT espera exactamente: `xmlns:cfdi="http://www.sat.gob.mx/cfd/4"`

```bash
# Verificar namespace del XML
grep -o 'xmlns:cfdi="[^"]*"' mi_cfdi.xml
# Debe mostrar: xmlns:cfdi="http://www.sat.gob.mx/cfd/4"
```

Si el XML tiene `cfd/3` o cualquier otro, el XSLT no encontrará ningún nodo y la cadena saldrá vacía `||`.

#### 2. XSLT 2.0/3.0 incompatible con el XSLT del SAT
El XSLT del SAT está escrito en **XSLT 1.0**. Si usas Saxon en modo XSLT 2.0 o 3.0, puede dar errores o resultados incorrectos.

```bash
# Con xsltproc (XSLT 1.0, correcto)
xsltproc cadenaoriginal_4_0.xslt mi_cfdi.xml

# Con Saxon forzando XSLT 1.0
java -jar saxon-he.jar -xsl:cadenaoriginal_4_0.xslt -s:mi_cfdi.xml -t:1.0
```

#### 3. BOM en el archivo XML (Byte Order Mark)
Un BOM al inicio del XML causa que el parser falle silenciosamente.

```bash
# Detectar BOM (si la primera línea empieza con EF BB BF)
hexdump -C mi_cfdi.xml | head -1

# Eliminar BOM
sed -i '1s/^\xEF\xBB\xBF//' mi_cfdi.xml
```

#### 4. Encoding que no es UTF-8
```bash
# Verificar encoding
file mi_cfdi.xml
# Convertir si es necesario
iconv -f ISO-8859-1 -t UTF-8 mi_cfdi.xml > mi_cfdi_utf8.xml
```

#### 5. Cadena original vacía `||`
Causas: namespace incorrecto (ver #1), o el XSLT no encontró el nodo raíz.

#### 6. Cadena original con campos en blanco inesperados
El XSLT incluye solo atributos presentes en el XML. Si un campo opcional está ausente, no aparece en la cadena. Esto es correcto.

#### 7. XSLT del Complemento de Pagos es diferente
El complemento tiene su propio XSLT (`Pagos20.xslt`). La cadena del complemento se genera **por separado** y se concatena a la del CFDI antes de firmar para el TFD.

### Snippets de transformación

**C# (.NET) — XslCompiledTransform (XSLT 1.0)**
```csharp
using System.Xml;
using System.Xml.Xsl;
using System.IO;

public string GenerarCadenaOriginal(string xmlCfdi, string rutaXslt)
{
    var xslt = new XslCompiledTransform();
    xslt.Load(rutaXslt);

    var xmlDoc = new XmlDocument();
    xmlDoc.LoadXml(xmlCfdi);

    using var sw = new StringWriter();
    using var xw = XmlWriter.Create(sw, xslt.OutputSettings);
    xslt.Transform(xmlDoc, null, xw);
    return sw.ToString();
}
```

**Python — lxml (XSLT 1.0)**
```python
from lxml import etree

def generar_cadena_original(xml_path: str, xslt_path: str) -> str:
    xml_doc = etree.parse(xml_path)
    xslt_doc = etree.parse(xslt_path)
    transform = etree.XSLT(xslt_doc)
    resultado = transform(xml_doc)
    return str(resultado)
```

**Bash — xsltproc**
```bash
xsltproc cadenaoriginal_4_0.xslt mi_cfdi.xml > cadena_original.txt
cat cadena_original.txt
```

### Verificación rápida de la cadena

Una cadena válida debe:
- Iniciar con `||4.0|`
- Terminar con `||`
- No contener saltos de línea
- Contener exactamente los campos presentes en el XML

---

## 14. XSD — Validación de Esquema

### Archivos XSD

| Archivo | Descripción | URL |
|---|---|---|
| cfdv40.xsd | Esquema principal del CFDI 4.0 | https://www.sat.gob.mx/sitio_internet/cfd/4/cfdv40.xsd |
| catCFDI.xsd | Tipos de catálogos usados en el CFDI | https://www.sat.gob.mx/sitio_internet/cfd/catalogos/catCFDI.xsd |
| Pagos10.xsd | Esquema del Complemento de Pagos 2.0 | https://www.gncys.com/complementos/pagos20/docs/Pagos10.xsd |
| catPagos.xsd | Catálogos del Complemento de Pagos | https://www.gncys.com/complementos/pagos20/docs/catPagos.xsd |
| tdCFDI.xsd | Tipos de datos comunes CFDI | https://www.gncys.com/complementos/pagos20/docs/tdCFDI.xsd |

### Validar con xmllint (Linux/Mac)
```bash
xmllint --noout --schema cfdv40.xsd mi_cfdi.xml
# Si es válido: mi_cfdi.xml validates
# Si tiene error: muestra la línea y el error
```

### Validar con Python (lxml)
```python
from lxml import etree

def validar_cfdi(xml_path: str, xsd_path: str) -> list[str]:
    with open(xsd_path, 'rb') as f:
        schema = etree.XMLSchema(etree.parse(f))
    with open(xml_path, 'rb') as f:
        xml_doc = etree.parse(f)
    if schema.validate(xml_doc):
        return []
    return [str(e) for e in schema.error_log]

errores = validar_cfdi('mi_cfdi.xml', 'cfdv40.xsd')
for e in errores:
    print(e)
```

### Validar con .NET
```csharp
using System.Xml;
using System.Xml.Schema;

var settings = new XmlReaderSettings();
settings.Schemas.Add("http://www.sat.gob.mx/cfd/4", "cfdv40.xsd");
settings.ValidationType = ValidationType.Schema;
settings.ValidationEventHandler += (s, e) =>
    Console.WriteLine($"Error XSD: {e.Message}");

using var reader = XmlReader.Create("mi_cfdi.xml", settings);
while (reader.Read()) { }
```

---

## 15. FAQ

**¿Cuándo empieza la vigencia de CFDI 4.0?**
Vigente desde 1 enero 2022; obligatorio desde 1 mayo 2022. No existe convivencia con v3.3 desde esa fecha.

**¿Qué datos mínimos necesito del receptor para facturar?**
RFC, Nombre exacto, RegimenFiscalReceptor, DomicilioFiscalReceptor (CP fiscal), UsoCFDI.

**¿Puede el receptor rechazar una solicitud de cancelación?**
Sí. En el esquema de cancelación v2.0, el receptor tiene 3 días hábiles para aceptar o rechazar. Si no responde, se acepta automáticamente en algunos motivos.

**¿FormaPago=99 siempre requiere Complemento de Pagos?**
Sí. FormaPago=99 + MetodoPago=PPD significa que el pago llegará después, y cada pago recibido debe documentarse con un CFDI tipo P con Complemento de Pagos.

**¿Puedo emitir un solo CFDI de Pagos para varios pagos del mismo mes?**
Sí, siempre que sean del mismo receptor. Plazo: máximo el 5° día natural del mes siguiente.

**¿El CFDI de Pagos puede relacionarse con múltiples facturas?**
Sí. Un solo nodo `Pago` puede tener múltiples `DoctoRelacionado`.

**¿Qué pasa si el Nombre del receptor tiene un acento diferente al del SAT?**
El PAC rechazará con CFDI40145. El nombre debe ser byte-a-byte idéntico al de la l_RFC.

**¿Cómo sé el nombre exacto registrado en el SAT?**
Descargando la Constancia de Situación Fiscal del contribuyente en: https://www.sat.gob.mx/aplicacion/login/53027/genera-tu-constancia-de-situacion-fiscal

**¿CFDI40999 qué significa?**
Error no clasificado. Validar el XML completo contra cfdv40.xsd para encontrar el problema estructural.

**¿Dónde verifico si un UUID es auténtico?**
En el verificador del SAT: https://verificacfdi.facturaelectronica.sat.gob.mx/

---

## 16. Glosario

| Término | Definición |
|---|---|
| CFDI | Comprobante Fiscal Digital por Internet |
| PAC | Proveedor Autorizado de Certificación — empresa que timbra CFDIs |
| SAT | Servicio de Administración Tributaria |
| TFD | Timbre Fiscal Digital — complemento que agrega el PAC al timbrar |
| UUID | Folio fiscal único asignado por el PAC al timbrar |
| CSD | Certificado de Sello Digital del contribuyente |
| l_RFC | Lista de RFC inscritos no cancelados publicada por el SAT |
| Cadena original | Representación canónica del CFDI para generar el sello |
| Sello Digital | Firma SHA-256+RSA del emisor sobre la cadena original |
| XSLT 1.0 | Lenguaje de transformación XML — la versión que usa el SAT |
| XSD | XML Schema Definition — define la estructura válida del XML |
| PPD | Pago en Parcialidades o Diferido |
| PUE | Pago en Una sola Exhibición |
| SPEI | Sistema de Pagos Electrónicos Interbancarios del Banco de México |
| Timbrado | Proceso de validación y sellado del CFDI por el PAC |
| RFC genérico | XAXX010101000 (nacional) o XEXX010101000 (extranjero) |
| CFF | Código Fiscal de la Federación |
| RMF | Resolución Miscelánea Fiscal |
| Anexo 20 | Anexo de la RMF con el estándar técnico del CFDI |
| Addenda | Sección libre del CFDI para datos adicionales (sin validación fiscal) |

---

## 17. URLs de Recursos Técnicos

### SAT — Fuente oficial
| Recurso | URL |
|---|---|
| Portal factura electrónica | https://www.sat.gob.mx/consultas/43074/actualizacion-factura-electronica---reforma-fiscal-2022- |
| Constancia de Situación Fiscal | https://www.sat.gob.mx/aplicacion/login/53027/genera-tu-constancia-de-situacion-fiscal |
| Verificador de CFDI (UUID) | https://verificacfdi.facturaelectronica.sat.gob.mx/ |
| Complemento Recepción de Pagos | https://www.sat.gob.mx/consultas/92764/comprobante-de-recepcion-de-pagos |

### Archivos XSD
| Archivo | URL SAT | URL GNcys |
|---|---|---|
| cfdv40.xsd | https://www.sat.gob.mx/sitio_internet/cfd/4/cfdv40.xsd | https://www.gncys.com/cfd/cfdv40.xsd |
| catCFDI.xsd | https://www.sat.gob.mx/sitio_internet/cfd/catalogos/catCFDI.xsd | https://www.gncys.com/cfd/catCFDI.xsd |
| Pagos10.xsd | — | https://www.gncys.com/complementos/pagos20/docs/Pagos10.xsd |
| catPagos.xsd | — | https://www.gncys.com/complementos/pagos20/docs/catPagos.xsd |
| tdCFDI.xsd | — | https://www.gncys.com/complementos/pagos20/docs/tdCFDI.xsd |

### Archivos XSLT
| Archivo | URL SAT | URL GNcys |
|---|---|---|
| cadenaoriginal_4_0.xslt | https://www.sat.gob.mx/sitio_internet/cfd/4/cadenaoriginal_4_0.xslt | https://www.gncys.com/cfd/cadenaoriginal_4_0.xslt |
| Pagos20.xslt | https://www.sat.gob.mx/sitio_internet/cfd/Pagos/Pagos20.xslt | https://www.gncys.com/cfd/Pagos20.xslt |
| TimbreFiscalDigitalv11.xslt | https://www.sat.gob.mx/sitio_internet/cfd/TimbreFiscalDigital/TimbreFiscalDigitalv11.xslt | — |

### Documentación GNcys
| Sección | URL |
|---|---|
| Estándar I.A — Comprobante | https://www.gncys.com/anexo20/4.0/estandar/i/a/ |
| Estándar I.B — Sellos digitales | https://www.gncys.com/anexo20/4.0/estandar/i/b/ |
| Estándar I.E — Cadena original | https://www.gncys.com/anexo20/4.0/estandar/i/e/ |
| Estándar III.B — TFD 1.1 | https://www.gncys.com/anexo20/4.0/estandar/iii/b/ |
| Guía de llenado I — CFDI | https://www.gncys.com/anexo20/4.0/guia-llenado-i.aspx |
| Apéndice 2 — Tipos de CFDI | https://www.gncys.com/anexo20/4.0/guia-llenado-apendice-2.aspx |
| Apéndice 5 — Egresos | https://www.gncys.com/anexo20/4.0/guia-llenado-apendice-5.aspx |
| Apéndice 6 — Anticipos | https://www.gncys.com/anexo20/4.0/guia-llenado-apendice-6.aspx |
| Apéndice 7 — Preguntas y respuestas | https://www.gncys.com/anexo20/4.0/guia-llenado-apendice-7.aspx |
| Complemento Pagos 2.0 — Estándar | https://www.gncys.com/complementos/pagos20/estandar.aspx |
| Complemento Pagos 2.0 — Guía llenado | https://www.gncys.com/complementos/pagos20/guia-llenado.aspx |
| Matriz de errores | https://www.gncys.com/anexo20/4.0/errores/ |
| Catálogos (índice) | https://www.gncys.com/anexo20/4.0/catalogos/ |
| Catálogos XLS descargable | https://www.gncys.com/anexo20/4.0/catalogos/docs/catCFDI_V4_19-10-2021.xls |
