# Complemento de Nómina 1.2 (Rev. E) — estructura, reglas y flujo

> Fuentes: `nomina12.xsd` + `catNomina.xsd` (SAT), Guía de llenado del comprobante del recibo de pago
> de nómina y su complemento (CFDI 4.0 + Nómina 1.2), Matriz de errores Nómina 1.2 Rev. E.
> Namespace: `http://www.sat.gob.mx/nomina12` · Versión fija del complemento: `1.2`
> XSD: `http://www.sat.gob.mx/sitio_internet/cfd/nomina/nomina12.xsd`
> XSLT cadena original: `http://www.sat.gob.mx/sitio_internet/cfd/nomina/nomina12.xslt` (se concatena dentro de la cadena del CFDI 4.0, no por separado como Pagos).
> Errores del PAC: `NOM1`–`NOM111` → matriz completa en `nomina-errores.md`.

## 1. Cuándo se usa

Obligatorio para todo pago de **sueldos y salarios** o **asimilados a salarios** (Art. 99 LISR, fracc. III).
Va dentro de un CFDI 4.0 **TipoDeComprobante = `N`**, un complemento por trabajador y periodo.
El CFDI de nómina sirve también como recibo/constancia laboral (Art. 132 y 804 LFT).

- **Plazo de emisión**: a más tardar en la fecha de pago (con facilidad de la regla 2.7.5.1 RMF: días hábiles según número de trabajadores).
- **Un CFDI puede llevar dos complementos Nomina** (caso: mismo periodo con pago ordinario + indemnización, TipoRegimen distinto en cada uno). Alternativa: dos CFDI.
- El RFC del trabajador debe estar inscrito y no cancelado (l_RFC). Validador: `https://portalsat.plataforma.sat.gob.mx/ConsultaRFC/`

## 2. CFDI "sobre" tipo N — valores fijos obligatorios (NOM1–NOM29)

```xml
<!-- Comprobante -->
Version="4.0"
TipoDeComprobante="N"
Moneda="MXN"                       <!-- NOM1: siempre MXN -->
Exportacion="01"                   <!-- NOM3 -->
MetodoPago="PUE"                   <!-- por guía de llenado -->
SubTotal={TotalPercepciones + TotalOtrosPagos}
Descuento={TotalDeducciones}       <!-- omitir si no hay deducciones -->
Total={SubTotal − Descuento}
<!-- NO incluir: FormaPago, CondicionesDePago, TipoCambio (NOM/guía) -->
<!-- NO incluir: InformacionGlobal (NOM4) -->

<!-- Emisor -->
<!-- FacAtrAdquirente NO debe existir (NOM7) -->
<!-- Si Emisor.Rfc de 13 (persona física) → nomina12:Emisor Curp obligatoria (NOM6);
     si de 12 (moral) → Curp NO debe existir (NOM5) -->

<!-- Receptor -->
Rfc={RFC del trabajador, 13 posiciones, en l_RFC}   <!-- NOM8/NOM9 -->
RegimenFiscalReceptor="605"        <!-- NOM11: incluso con RFC genérico -->
UsoCFDI="CN01"                     <!-- NOM12 -->
DomicilioFiscalReceptor={CP del trabajador según su constancia}
<!-- Trabajador fallecido: Rfc=XAXX010101000 y en nomina12:Receptor va la CURP del fallecido (NOM10) -->

<!-- Un solo Concepto, sin hijos (NOM13), con valores fijos: -->
ClaveProdServ="84111505"           <!-- NOM14 -->
Cantidad="1"                       <!-- NOM16: sin decimales -->
ClaveUnidad="ACT"                  <!-- NOM17 -->
Descripcion="Pago de nómina"       <!-- NOM19: texto exacto -->
ValorUnitario={TotalPercepciones + TotalOtrosPagos}   <!-- NOM20 -->
Importe={TotalPercepciones + TotalOtrosPagos}         <!-- NOM21 -->
Descuento={TotalDeducciones}       <!-- NOM22 -->
ObjetoImp="01"                     <!-- NOM23 -->
<!-- NO incluir en el concepto: NoIdentificacion, Unidad, Impuestos, ACuentaTerceros,
     InformacionAduanera, CuentaPredial, ComplementoConcepto, Parte (NOM15/18/24–29) -->
<!-- NO incluir nodo cfdi:Impuestos global (regla CFDI40201) -->
```

## 3. Estructura del complemento (árbol de nodos)

```
nomina12:Nomina  Version="1.2" TipoNomina FechaPago FechaInicialPago FechaFinalPago
│                NumDiasPagados [TotalPercepciones] [TotalDeducciones] [TotalOtrosPagos]
├── Emisor (0..1)            [Curp] [RegistroPatronal] [RfcPatronOrigen]
│   └── EntidadSNCF (0..1)   OrigenRecurso [MontoRecursoPropio]     ← solo entes públicos SNCF
├── Receptor (1)             Curp NumEmpleado TipoContrato TipoRegimen PeriodicidadPago ClaveEntFed
│   │                        [NumSeguridadSocial] [FechaInicioRelLaboral] [Antigüedad] [Sindicalizado]
│   │                        [TipoJornada] [Departamento] [Puesto] [RiesgoPuesto] [Banco]
│   │                        [CuentaBancaria] [SalarioBaseCotApor] [SalarioDiarioIntegrado]
│   └── SubContratacion (0..n)  RfcLabora PorcentajeTiempo          ← Σ% = 100 (NOM68)
├── Percepciones (0..1)      [TotalSueldos] [TotalSeparacionIndemnizacion]
│   │                        [TotalJubilacionPensionRetiro] TotalGravado TotalExento
│   ├── Percepcion (1..n)    TipoPercepcion Clave Concepto ImporteGravado ImporteExento
│   │   ├── AccionesOTitulos (0..1)   ValorMercado PrecioAlOtorgarse   ← solo TipoPercepcion 045
│   │   └── HorasExtra (0..n)         Dias TipoHoras HorasExtra ImportePagado ← solo 019
│   ├── JubilacionPensionRetiro (0..1)  [TotalUnaExhibicion]|[TotalParcialidad MontoDiario]
│   │                                   IngresoAcumulable IngresoNoAcumulable ← solo 039/044
│   └── SeparacionIndemnizacion (0..1)  TotalPagado NumAñosServicio UltimoSueldoMensOrd
│                                       IngresoAcumulable IngresoNoAcumulable ← solo 022/023/025
├── Deducciones (0..1)       [TotalOtrasDeducciones] [TotalImpuestosRetenidos]
│   └── Deduccion (1..n)     TipoDeduccion Clave Concepto Importe (>0, NOM96)
├── OtrosPagos (0..1)
│   └── OtroPago (1..n)      TipoOtroPago Clave Concepto Importe
│       ├── SubsidioAlEmpleo (0..1)          SubsidioCausado          ← obligatorio si tipo 002
│       └── CompensacionSaldosAFavor (0..1)  SaldoAFavor Año RemanenteSalFav ← obligatorio si 004
└── Incapacidades (0..1)
    └── Incapacidad (1..n)   DiasIncapacidad TipoIncapacidad [ImporteMonetario]
```

Atributos raíz clave:
- `TipoNomina`: `O` ordinaria → PeriodicidadPago ≠ 99 (NOM33) · `E` extraordinaria → PeriodicidadPago = `99` (NOM34). Aguinaldo, PTU, finiquitos, bonos = extraordinaria.
- `FechaPago` (fecha real de erogación), `FechaInicialPago` ≤ `FechaFinalPago` (NOM35). En extraordinarias las tres pueden coincidir.
- `NumDiasPagados`: 0.001–36160.000; en extraordinarias (aguinaldo/PTU) se puede usar `1`.
- Debe existir `TotalPercepciones` o `TotalOtrosPagos`, al menos uno (NOM31).

## 4. Orden de decisión (gobierna qué nodos son obligatorios)

Evaluar en este orden antes de armar el XML — cada switch obliga/prohíbe bloques:

1. **¿Asalariado o asimilado?** → `TipoContrato`:
   - `01`–`08` (relación laboral) → `TipoRegimen` debe ser `02`, `03` o `04` (NOM57) y `RegistroPatronal` **debe existir** (NOM42).
   - `09`, `10`, `99` (sin relación laboral / jubilación) → `TipoRegimen` `05`–`99` (NOM58) y `RegistroPatronal` **no debe existir** (NOM43).
2. **Si existe `RegistroPatronal`** → obligatorios: `NumSeguridadSocial`, `FechaInicioRelLaboral`, `Antigüedad`, `RiesgoPuesto`, `SalarioDiarioIntegrado` (NOM44).
3. **`TipoRegimen` = `02` (Sueldos)** → debe existir un OtroPago `002` (Subsidio al empleo), salvo que se registre `007`/`008` por ajuste (NOM105). Si TipoRegimen ≠ 02 → prohibidas las claves 002/007/008 (NOM106). Si el subsidio causado del periodo es 0, se registra OtroPago 002 con Importe 0.00 y SubsidioCausado 0.00.
4. **Emisor ente público SNCF**: si el RFC emisor tiene marca SNCF en l_RFC → `EntidadSNCF` obligatorio (NOM45), si no la tiene → prohibido (NOM46). `OrigenRecurso=IM` (mixto) → `MontoRecursoPropio` obligatorio y < TotalPercepciones+TotalOtrosPagos (NOM48–50).
5. **Por cada `TipoPercepcion`** (dispara nodos hijo):
   | Clave | Obliga | Prohíbe |
   |---|---|---|
   | `019` Horas extra | nodo `HorasExtra` (NOM84) | HorasExtra si clave ≠ 019 (NOM85) |
   | `014` Subsidios por incapacidad | nodo `Incapacidades` + Σ ImporteMonetario = gravado+exento de la percepción (NOM86/87) | — |
   | `022`/`023`/`025` separación | atributo `TotalSeparacionIndemnizacion` + nodo `SeparacionIndemnizacion` (NOM78) | — |
   | `039` jubilación 1 exhibición | `TotalJubilacionPensionRetiro` + nodo `JubilacionPensionRetiro` con `TotalUnaExhibicion` (NOM79/80) | `TotalParcialidad`, `MontoDiario` |
   | `044` jubilación parcialidades | ídem con `TotalParcialidad` + `MontoDiario` (NOM81) | `TotalUnaExhibicion` |
   | `045` acciones/títulos | nodo `AccionesOTitulos` (NOM82) | AccionesOTitulos si ≠ 045 (NOM83) |
   | `038` otros ingresos | `ImporteExento` = 0 obligatorio (NOM109; desde 2026 el 038 es 100% gravado — previsión social sin clave específica va en `056`) | — |
6. **Por cada `TipoOtroPago`**: `002` → nodo `SubsidioAlEmpleo` (NOM99) e Importe ≤ SubsidioCausado (NOM107); `004` → nodo `CompensacionSaldosAFavor` (NOM98) con SaldoAFavor ≥ RemanenteSalFav (NOM102) y Año = año anterior (o en curso si el periodo es diciembre) (NOM103); cualquier clave ≠ 002 → Importe > 0 (NOM100).
7. **Deducciones**: `002` ISR alimenta `TotalImpuestosRetenidos`; el resto `TotalOtrasDeducciones`. `006` (descuento por incapacidad) → nodo `Incapacidades` y Deduccion.Importe = Σ Incapacidad.ImporteMonetario (NOM94/95).
8. **Depósito**: `CuentaBancaria` de 10 (celular), 11 (cuenta), 16 (tarjeta) o 18 (CLABE) posiciones (NOM62). CLABE 18 → `Banco` **no** debe existir y el dígito verificador debe cuadrar (NOM63/64); 10/11/16 → `Banco` obligatorio (NOM65).
9. **`Antigüedad`** formato ISO 8601 duración: `P{n}W` (semanas: n ≤ (días transcurridos+1)/7, NOM54) o `P{a}Y{m}M{d}D` coherente con FechaInicioRelLaboral→FechaFinalPago (NOM55). `FechaInicioRelLaboral` ≤ FechaFinalPago (NOM53).

## 5. Cuadres numéricos (validar antes de timbrar)

```
Nomina.TotalPercepciones  = Percepciones.TotalSueldos + TotalSeparacionIndemnizacion
                            + TotalJubilacionPensionRetiro                      (NOM37)
Percepciones.TotalSueldos = Σ (ImporteGravado+ImporteExento) de claves ∉ {022,023,025,039,044}  (NOM70)
Percepciones.TotalSeparacionIndemnizacion = Σ claves ∈ {022,023,025}            (NOM71)
Percepciones.TotalJubilacionPensionRetiro = Σ claves ∈ {039,044}                (NOM72)
Percepciones.TotalGravado = Σ Percepcion.ImporteGravado                         (NOM73)
Percepciones.TotalExento  = Σ Percepcion.ImporteExento                          (NOM74)
TotalSueldos+TotalSepInd+TotalJubPR = TotalGravado + TotalExento                (NOM69)

Nomina.TotalDeducciones   = Deducciones.TotalOtrasDeducciones + TotalImpuestosRetenidos  (NOM39)
TotalImpuestosRetenidos   = Σ Deduccion.Importe donde TipoDeduccion = 002; si no hay 002,
                            el atributo NO debe existir                          (NOM91/92)
Nomina.TotalOtrosPagos    = Σ OtroPago.Importe                                   (NOM40)

CFDI: SubTotal = TotalPercepciones + TotalOtrosPagos
      Descuento = TotalDeducciones
      Total = SubTotal − Descuento

Reglas por percepción: no puede haber gravado=0 y exento=0 a la vez
  (si exento=0 → gravado>0, NOM75; si gravado=0 → exento>0, NOM110).
Subsidio (Rev. E): SubsidioCausado ≤ 628.00 si NumDiasPagados ≤ 31 (NOM101);
  si NumDiasPagados > 31 → SubsidioCausado ≤ 20.66 × NumDiasPagados (NOM108).
  ⚠ Estos topes derivan del decreto de subsidio/UMA vigente y cambian por año — tratarlos
  como parámetro configurable, no como constante.
Si el nodo Percepciones/Deducciones no existe → su Total correspondiente NO debe existir (NOM36/38).
```

## 6. Catálogos (catNomina) con descripción

### c_TipoNomina · c_PeriodicidadPago
`O` Ordinaria · `E` Extraordinaria (aguinaldo, PTU, finiquito, bonos → Periodicidad `99`)

| Per. | Desc. | Per. | Desc. |
|---|---|---|---|
| 01 | Diario | 06 | Bimestral |
| 02 | Semanal | 07 | Unidad obra |
| 03 | Catorcenal | 08 | Comisión |
| 04 | Quincenal | 09 | Precio alzado |
| 05 | Mensual | 10 | Decenal |
| | | 99 | Otra Periodicidad (solo TipoNomina=E) |

### c_TipoContrato

| Clave | Descripción | Clave | Descripción |
|---|---|---|---|
| 01 | Por tiempo indeterminado | 06 | Con capacitación inicial |
| 02 | Para obra determinada | 07 | Por pago de hora laborada |
| 03 | Por tiempo determinado | 08 | Por comisión laboral |
| 04 | Por temporada | 09 | Sin relación de trabajo (asimilados) |
| 05 | Sujeto a prueba | 10 | Jubilación, pensión, retiro |
| | | 99 | Otro contrato |

### c_TipoRegimen

| Clave | Descripción | Clave | Descripción |
|---|---|---|---|
| 02 | Sueldos (incluye fracc. I Art. 94 LISR) | 08 | Asimilados comisionistas |
| 03 | Jubilados | 09 | Asimilados Honorarios |
| 04 | Pensionados | 10 | Asimilados Acciones |
| 05 | Asimilados Miembros Soc. Coop. Producción | 11 | Asimilados Otros |
| 06 | Asimilados Integrantes Soc. Asoc. Civiles | 12 | Jubilados o Pensionados |
| 07 | Asimilados Miembros consejos | 13 | Indemnización o Separación |
| | | 99 | Otro Régimen |

Regla cruzada: TipoContrato 01–08 → régimen 02/03/04 · TipoContrato ≥ 09 → régimen 05–99.
Pagos por indemnización/separación → régimen `13`.

### c_TipoJornada · c_RiesgoPuesto · c_TipoIncapacidad · c_TipoHoras · c_OrigenRecurso

| Jornada | | Riesgo (Art. 196 RACERF) | | Incapacidad | | Horas | | Origen |
|---|---|---|---|---|---|---|---|---|
| 01 Diurna | 05 Reducida | 1 Clase I | | 01 Riesgo de trabajo | | 01 Dobles | | IP Ingresos propios |
| 02 Nocturna | 06 Continuada | 2 Clase II | | 02 Enfermedad en general | | 02 Simples | | IF Ingresos federales |
| 03 Mixta | 07 Partida | 3 Clase III | | 03 Maternidad | | 03 Triples | | IM Ingresos mixtos |
| 04 Por hora | 08 Por turnos | 4 Clase IV | | 04 Licencia cuidados médicos hijos con cáncer | | | | |
| | 99 Otra | 5 Clase V · 99 | | | | | | |

### c_TipoPercepcion (completo)

| Clave | Descripción | Clave | Descripción |
|---|---|---|---|
| 001 | Sueldos, Salarios Rayas y Jornales | 029 | Vales de despensa |
| 002 | Gratificación Anual (Aguinaldo) | 030 | Vales de restaurante |
| 003 | Participación de los Trabajadores en las Utilidades PTU | 031 | Vales de gasolina |
| 004 | Reembolso de Gastos Médicos Dentales y Hospitalarios | 032 | Vales de ropa |
| 005 | Fondo de Ahorro | 033 | Ayuda para renta |
| 006 | Caja de ahorro | 034 | Ayuda para artículos escolares |
| 009 | Contribuciones a Cargo del Trabajador Pagadas por el Patrón | 035 | Ayuda para anteojos |
| 010 | Premios por puntualidad | 036 | Ayuda para transporte |
| 011 | Prima de Seguro de vida | 037 | Ayuda para gastos de funeral |
| 012 | Seguro de Gastos Médicos Mayores | 038 | Otros ingresos por salarios (**exento = 0**, NOM109) |
| 013 | Cuotas Sindicales Pagadas por el Patrón | 039 | Jubilaciones, pensiones o haberes de retiro (una exhibición) |
| 014 | Subsidios por incapacidad | 044 | Jubilaciones, pensiones o haberes de retiro (parcialidades) |
| 015 | Becas para trabajadores y/o hijos | 045 | Ingresos en acciones o títulos valor que representan bienes |
| 019 | Horas extra | 046 | Ingresos asimilados a salarios |
| 020 | Prima dominical | 047 | Alimentación diferente a la del Art. 94 último párrafo LISR |
| 021 | Prima vacacional | 048 | Habitación |
| 022 | Prima por antigüedad | 049 | Premios por asistencia |
| 023 | Pagos por separación | 050 | Viáticos |
| 024 | Seguro de retiro | 051 | Pagos a extrabajadores (gratificaciones/primas/compensaciones) derivados de jubilación en parcialidades |
| 025 | Indemnizaciones | 052 | Pagos a extrabajadores — jubilación en parcialidades por resolución judicial o laudo |
| 026 | Reembolso por funeral | 053 | Pagos a extrabajadores — jubilación en una exhibición por resolución judicial o laudo |
| 027 | Cuotas de seguridad social pagadas por el patrón | 054 | Días de descanso laborados (alta dic-2025) |
| 028 | Comisiones | 055 | Días de descanso obligatorios laborados (alta dic-2025) |
| | | 056 | Previsión social sin clave específica (alta dic-2025; sustituye el uso de 038 para previsión social) |
| | | 057 | Premios por concursos científicos, artísticos o literarios / otorgados por la Federación (alta jun-2026) |

### c_TipoDeduccion (núcleo 001–023 + ajustes)

| Clave | Descripción | Clave | Descripción |
|---|---|---|---|
| 001 | Seguridad social | 013 | Pagos hechos con exceso al trabajador |
| 002 | ISR | 014 | Errores |
| 003 | Aportaciones a retiro, cesantía en edad avanzada y vejez | 015 | Pérdidas |
| 004 | Otros | 016 | Averías |
| 005 | Aportaciones a Fondo de vivienda | 017 | Adquisición de artículos producidos por la empresa |
| 006 | Descuento por incapacidad (→ nodo Incapacidad) | 018 | Cuotas para sociedades cooperativas y cajas de ahorro |
| 007 | Pensión alimenticia | 019 | Cuotas sindicales |
| 008 | Renta | 020 | Ausencia (Ausentismo) |
| 009 | Préstamos del FONACOT/INFONAVIT (Fondo Nac. Vivienda) | 021 | Cuotas obrero patronales |
| 010 | Pago por crédito de vivienda | 022 | Impuestos Locales |
| 011 | Pago de abonos INFONACOT | 023 | Aportaciones voluntarias |
| 012 | Anticipo de salarios | | |

Claves `024`–`102`: **ajustes espejo** — "Ajuste en {percepción} gravado/exento" por cada clave de
percepción (p.ej. 065/066 y 069/070 jubilaciones — si se usaron mal, cancelar y reexpedir;
071 Ajuste en subsidio efectivamente entregado; 080/081 ajustes de viáticos). Claves recientes:
`101` ISR retenido de ejercicio anterior (Art. 97 LISR) · `102` Ajuste a pagos por gratificaciones a
extrabajadores · `107` Ajuste al Subsidio Causado (Apéndice 7) · `108`/`109` Ajuste a días de descanso
laborados gravado/exento · `110`/`111` ídem días de descanso obligatorios · `112`/`113` Ajuste a previsión
social 056 gravado/exento · `114`/`115` Ajuste a premios 057 gravado/exento.
Catálogo completo vigente: `http://omawww.sat.gob.mx/tramitesyservicios/Paginas/documentos/catNomina.xls`

### c_TipoOtroPago

| Clave | Descripción |
|---|---|
| 001 | Reintegro de ISR pagado en exceso (no enterado al SAT) |
| 002 | Subsidio para el empleo efectivamente entregado al trabajador (→ nodo SubsidioAlEmpleo) |
| 003 | Viáticos entregados al trabajador |
| 004 | Aplicación de saldo a favor por compensación anual (→ nodo CompensacionSaldosAFavor) |
| 005 | Reintegro de ISR retenido en exceso de ejercicio anterior (no enterado al SAT) |
| 006 | Alimentos en bienes (servicios de comedor y comida) Art. 94 último párrafo LISR |
| 007 | ISR ajustado por subsidio (solo con ajuste del Apéndice 7) |
| 008 | Subsidio efectivamente entregado que no correspondía (solo con ajuste del Apéndice 7) |
| 009 | Reembolso de descuentos efectuados para el crédito de vivienda |
| 999 | Pagos distintos a los listados que no son ingreso por sueldos/asimilados |

**Los importes de OtrosPagos no son ingreso acumulable ni exento** — no son sueldo (por eso el
subsidio entregado suma al neto pero no a percepciones).

### c_Banco
Solo claves numéricas (002 Banamex, 012 BBVA, 014 Santander, 021 HSBC, 072 Banorte…).
Catálogo completo en `catNomina.xsd`/`catNomina.xls` — validar contra la clave, no el nombre.

## 7. Casos especiales (apéndices de la guía de llenado)

- **Viáticos (Apéndice 4)** — 3 momentos: (1) entrega → OtroPago `003` por el monto depositado;
  (2) comprobación → Percepcion `050` Viáticos con importes comprobados/exentos en ImporteExento
  y Deduccion `081` (Ajuste de viáticos entregados) por el mismo total, para netear;
  (3) lo no comprobado y no devuelto que exceda los límites → gravado.
- **Ajuste mensual del subsidio (Apéndice 7)** — cuando se pagó subsidio en quincena 1 pero al
  cierre del mes el subsidio causado es 0: en el último CFDI del mes registrar
  Deduccion `107` (Ajuste al Subsidio Causado, por el subsidio causado previo), Deduccion `002` ISR
  (por el ISR que se dejó de retener), Deduccion `071` (subsidio entregado a revertir),
  OtroPago `007` (ISR ajustado por subsidio, mismo importe que la 002 del ajuste) y
  OtroPago `008` (subsidio entregado que no correspondía, mismo importe que la 071).
- **Diferencia de ISR anual (Apéndice 8)** — retención por cálculo anual: Deduccion `002` en el CFDI
  donde se entera, o `101` si es de ejercicio anterior; saldo a favor compensado → OtroPago `004`.
- **Separación + última nómina ordinaria**: dos complementos en un CFDI o dos CFDI; el de
  indemnización con TipoRegimen `13` y nodo SeparacionIndemnizacion.
- **Trabajador fallecido**: Rfc receptor `XAXX010101000`, RegimenFiscalReceptor `605`,
  CURP del fallecido en nomina12:Receptor (NOM10/11).
- **Asimilados a salarios**: TipoContrato `09`/`99`, TipoRegimen `05`–`11`, sin RegistroPatronal,
  sin NSS/SDI, sin subsidio (NOM106), percepción típica `046`.
- **Sustitución de un CFDI de nómina con errores**: cancelar con motivo `01` relacionando el
  sustituto (TipoRelacion `04`); si el pago no varió, conservar FechaPago original.

## 8. Flujo de captura recomendado (wizard)

1. Datos del periodo: TipoNomina → Periodicidad → fechas → días pagados.
2. Empleador: ¿física/moral? (Curp emisor) · ¿ente SNCF? · RegistroPatronal según TipoContrato.
3. Trabajador: RFC/CURP → validar en l_RFC · TipoContrato → TipoRegimen (validar cruce) →
   bloque IMSS si hay RegistroPatronal → depósito (CuentaBancaria/Banco) → ClaveEntFed.
4. Percepciones: por cada clave, disparar sub-nodos requeridos (§4.5) y validar gravado/exento.
5. Deducciones: separar ISR (002) del resto; incapacidades ligadas.
6. Otros pagos: subsidio obligatorio si régimen 02.
7. Ejecutar todos los cuadres de §5 **en servidor** antes de firmar y timbrar.
8. Si el PAC devuelve `NOMxxx` → mapear con `nomina-errores.md` a la sección del wizard.

## 9. Errores frecuentes de integración

- Redondeos: los totales del complemento y del CFDI se comparan a 2 decimales — sumar sobre los
  importes ya redondeados de cada nodo, no recalcular desde tasas.
- `Antigüedad` calculada con la fecha de emisión en lugar de `FechaFinalPago` (NOM54/55).
- Enviar `TotalPercepciones`/`TotalDeducciones` cuando el nodo correspondiente no existe (NOM36/38).
- Subsidio con Importe > SubsidioCausado (NOM107) o registrar OtroPago 002 sin nodo SubsidioAlEmpleo (NOM99).
- CLABE con Banco (NOM63) o tarjeta/cuenta sin Banco (NOM65).
- Usar `038` con parte exenta (NOM109) — desde 2026 la previsión social sin clave va en `056`.
- Nombre del receptor no idéntico al de la constancia (regla CFDI40145, aplica igual en nómina).
- El complemento se registra en `cfdi:Complemento`, nunca en `ComplementoConcepto` (NOM30).
