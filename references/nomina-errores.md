# Matriz de errores — Complemento de Nómina 1.2 Rev. E (NOMxxx)

> Fuente: `Matriz_Errores_Nomina_v12_Rev_E.xls` (SAT). Códigos `NOM1`–`NOM111` sobre CFDI 4.0.
> Úsala como diccionario: el PAC devuelve `NOMxxx` → busca aquí el atributo, la regla y **cómo resolver**.
> Agrupada por sección (así se mapea 1:1 al wizard de captura de `nomina.md` §8).

## Cómo leer
Cada fila: `CÓDIGO — Elemento:Atributo — regla → cómo resolver`.
Las dos causas #1 de rechazo: **valores fijos del CFDI sobre tipo N** (sección A) y
**condicionalidad TipoContrato/TipoRegimen/TipoPercepcion** (secciones D y E). Antes de timbrar,
evalúa el orden de decisión de `nomina.md` §4 y ejecuta los cuadres de §5.

---

## A. CFDI "sobre" (comprobante tipo N, valores fijos) — NOM1–NOM29
| Código | Atributo | Regla → cómo resolver |
|---|---|---|
| NOM1 | Comprobante:Moneda | Debe ser `MXN`. |
| NOM2 | TipoDeComprobante | Debe ser `N`. |
| NOM3 | Exportacion | Debe ser `01`. |
| NOM4 | InformacionGlobal | **No debe existir** (nómina nunca es factura global). |
| NOM5 | nomina12:Emisor:Curp | Emisor RFC de 12 (persona moral) → Curp del complemento **no debe existir**. |
| NOM6 | nomina12:Emisor:Curp | Emisor RFC de 13 (persona física) → Curp del complemento **debe existir**. |
| NOM7 | Emisor:FacAtrAdquirente | No debe existir. |
| NOM8 | Receptor:Rfc | Debe ser persona física (13 posiciones). |
| NOM9 | Receptor:Rfc | Debe estar en l_RFC (inscrito, no cancelado). |
| NOM10 | nomina12:Receptor:Curp | Si Receptor.Rfc = `XAXX010101000` (trabajador fallecido) → registrar la CURP del fallecido. |
| NOM11 | RegimenFiscalReceptor | Debe ser `605` (Sueldos y Salarios), incluso con RFC genérico. |
| NOM12 | Receptor:UsoCFDI | Debe ser `CN01`. |
| NOM13 | Conceptos:Concepto | Exactamente **un** concepto, sin elementos hijo. |
| NOM14 | Concepto:ClaveProdServ | Debe ser `84111505`. |
| NOM15 | Concepto:NoIdentificacion | No debe existir. |
| NOM16 | Concepto:Cantidad | Debe ser `1` (sin decimales). |
| NOM17 | Concepto:ClaveUnidad | Debe ser `ACT`. |
| NOM18 | Concepto:Unidad | No debe existir. |
| NOM19 | Concepto:Descripcion | Texto exacto `Pago de nómina`. |
| NOM20 | Concepto:ValorUnitario | = TotalPercepciones + TotalOtrosPagos. |
| NOM21 | Concepto:Importe | = TotalPercepciones + TotalOtrosPagos. |
| NOM22 | Concepto:Descuento | = Nomina:TotalDeducciones (omitir si no hay deducciones). |
| NOM23 | Concepto:ObjetoImp | Debe ser `01`. |
| NOM24 | Concepto:Impuestos | No debe existir. |
| NOM25 | Concepto:ACuentaTerceros | No debe existir. |
| NOM26 | Concepto:InformacionAduanera | No debe existir. |
| NOM27 | Concepto:CuentaPredial | No debe existir. |
| NOM28 | Concepto:ComplementoConcepto | No debe existir. |
| NOM29 | Concepto:Parte | No debe existir. |

## B. Nodo Nomina — totales y fechas — NOM30–NOM40
| Código | Atributo | Regla → cómo resolver |
|---|---|---|
| NOM30 | Nomina | Debe ir como hijo de `cfdi:Complemento`, nunca dentro de ComplementoConcepto. |
| NOM31 | TotalPercepciones / TotalOtrosPagos | Debe existir al menos uno de los dos. |
| NOM32 | TipoNomina | Clave del catálogo c_TipoNomina (`O`/`E`). |
| NOM33 | PeriodicidadPago | TipoNomina=`O` → Periodicidad ≠ `99`. |
| NOM34 | PeriodicidadPago | TipoNomina=`E` → Periodicidad = `99`. |
| NOM35 | FechaInicialPago | Debe ser ≤ FechaFinalPago. |
| NOM36 | TotalPercepciones | Si no existe nodo Percepciones → **no debe existir**. |
| NOM37 | TotalPercepciones | = TotalSueldos + TotalSeparacionIndemnizacion + TotalJubilacionPensionRetiro. |
| NOM38 | TotalDeducciones | Si no existe nodo Deducciones → **no debe existir**. |
| NOM39 | TotalDeducciones | = TotalOtrasDeducciones + TotalImpuestosRetenidos. |
| NOM40 | TotalOtrosPagos | Si existe nodo OtrosPagos → debe existir y ser = Σ OtroPago.Importe. |

## C. Emisor (RegistroPatronal, SNCF) — NOM41–NOM50
| Código | Atributo | Regla → cómo resolver |
|---|---|---|
| NOM41 | Emisor:RfcPatronOrigen | Debe estar en l_RFC (inscrito, no cancelado). |
| NOM42 | Emisor:RegistroPatronal | TipoContrato `01`–`08` → **debe existir**. |
| NOM43 | Emisor:RegistroPatronal | TipoContrato `09`/`10`/`99` → **no debe existir**. |
| NOM44 | Receptor (bloque IMSS) | Si existe RegistroPatronal → obligatorios: NumSeguridadSocial, FechaInicioRelLaboral, Antigüedad, RiesgoPuesto y SalarioDiarioIntegrado. |
| NOM45 | Emisor:EntidadSNCF | RFC emisor con marca SNCF en l_RFC → el nodo **debe existir**. |
| NOM46 | Emisor:EntidadSNCF | RFC emisor sin marca SNCF → el nodo **no debe existir**. |
| NOM47 | EntidadSNCF:OrigenRecurso | Clave del catálogo c_OrigenRecurso (IP/IF/IM). |
| NOM48 | EntidadSNCF:MontoRecursoPropio | OrigenRecurso=`IM` → debe existir. |
| NOM49 | EntidadSNCF:MontoRecursoPropio | OrigenRecurso≠`IM` → no debe existir. |
| NOM50 | EntidadSNCF:MontoRecursoPropio | Debe ser < (TotalPercepciones + TotalOtrosPagos). |

## D. Receptor (contrato, régimen, cuenta, antigüedad) — NOM51–NOM68
| Código | Atributo | Regla → cómo resolver |
|---|---|---|
| NOM51 | Receptor:TipoContrato | Clave del catálogo c_TipoContrato. |
| NOM52 | Receptor:TipoJornada | Clave del catálogo c_TipoJornada. |
| NOM53 | Receptor:FechaInicioRelLaboral | Debe ser ≤ FechaFinalPago. |
| NOM54 | Receptor:Antigüedad | Patrón `P{n}W` → n ≤ (días entre FechaInicioRelLaboral y FechaFinalPago + 1) ÷ 7. |
| NOM55 | Receptor:Antigüedad | Patrón `P{a}Y{m}M{d}D` → debe corresponder a los años/meses/días entre FechaInicioRelLaboral y FechaFinalPago. |
| NOM56 | Receptor:TipoRegimen | Clave del catálogo c_TipoRegimen. |
| NOM57 | Receptor:TipoRegimen | TipoContrato `01`–`08` → régimen `02`, `03` o `04`. |
| NOM58 | Receptor:TipoRegimen | TipoContrato `09` o superior → régimen `05`–`99`. |
| NOM59 | Receptor:RiesgoPuesto | Clave del catálogo c_RiesgoPuesto (1–5, 99). |
| NOM60 | Receptor:PeriodicidadPago | Clave del catálogo c_PeriodicidadPago. |
| NOM61 | Receptor:Banco | Clave del catálogo c_Banco. |
| NOM62 | Receptor:CuentaBancaria | Longitud 10 (celular), 11 (cuenta), 16 (tarjeta) o 18 (CLABE). |
| NOM63 | Receptor:Banco | Con CLABE (18) → Banco **no debe existir** (la CLABE ya identifica al banco). |
| NOM64 | Receptor:CuentaBancaria | CLABE → verificar dígito de control (algoritmo módulo 10 ponderado 3-7-1). |
| NOM65 | Receptor:Banco | Cuenta a 10/11/16 posiciones → Banco **debe existir**. |
| NOM66 | Receptor:ClaveEntFed | Clave de c_Estado con país `MEX` (entidad donde el trabajador prestó el servicio). |
| NOM67 | SubContratacion:RfcLabora | Debe estar en l_RFC. |
| NOM68 | SubContratacion:PorcentajeTiempo | La suma de todos los PorcentajeTiempo debe ser 100. |

## E. Percepciones — NOM69–NOM90, NOM109, NOM110
| Código | Atributo | Regla → cómo resolver |
|---|---|---|
| NOM69 | Percepciones (totales) | TotalSueldos + TotalSeparacionIndemnizacion + TotalJubilacionPensionRetiro = TotalGravado + TotalExento. |
| NOM70 | TotalSueldos | = Σ (gravado+exento) de percepciones con clave ∉ {022, 023, 025, 039, 044}. |
| NOM71 | TotalSeparacionIndemnizacion | = Σ (gravado+exento) de claves {022, 023, 025}. |
| NOM72 | TotalJubilacionPensionRetiro | = Σ (gravado+exento) de claves {039, 044}. |
| NOM73 | TotalGravado | = Σ Percepcion.ImporteGravado. |
| NOM74 | TotalExento | = Σ Percepcion.ImporteExento. |
| NOM75 | Percepcion:ImporteGravado | Si ImporteExento = 0 → ImporteGravado > 0 (no ambos en cero). |
| NOM76 | Percepcion:TipoPercepcion | Clave del catálogo c_TipoPercepcion. |
| NOM77 | TotalSueldos | Si hay percepción con clave ∉ {022,023,025,039,044} → TotalSueldos debe existir. |
| NOM78 | TotalSeparacionIndemnizacion + SeparacionIndemnizacion | Clave 022/023/025 → ambos deben existir; sin esas claves → no deben existir. |
| NOM79 | TotalJubilacionPensionRetiro + JubilacionPensionRetiro | Clave 039/044 → ambos deben existir; sin esas claves → no deben existir. |
| NOM80 | JubilacionPensionRetiro | Clave `039` (una exhibición) → TotalUnaExhibicion existe; TotalParcialidad y MontoDiario **no**. |
| NOM81 | JubilacionPensionRetiro | Clave `044` (parcialidades) → TotalParcialidad y MontoDiario existen; TotalUnaExhibicion **no**. |
| NOM82 | AccionesOTitulos | Clave `045` → el nodo debe existir. |
| NOM83 | AccionesOTitulos | Clave ≠ `045` → el nodo no debe existir. |
| NOM84 | HorasExtra | Clave `019` → el nodo debe existir. |
| NOM85 | HorasExtra | Clave ≠ `019` → el nodo no debe existir. |
| NOM86 | Incapacidades | Clave `014` (subsidios por incapacidad) → nodo Incapacidades debe existir. |
| NOM87 | Incapacidad:ImporteMonetario | Clave `014` → Σ ImporteMonetario = ImporteGravado + ImporteExento de esa percepción. |
| NOM88 | HorasExtra:TipoHoras | Clave del catálogo c_TipoHoras (01 dobles / 02 simples / 03 triples). |
| NOM89 | JubilacionPensionRetiro | Con valor en TotalUnaExhibicion → MontoDiario y TotalParcialidad no deben existir. |
| NOM90 | JubilacionPensionRetiro | Con valor en TotalParcialidad → MontoDiario debe existir y TotalUnaExhibicion no. |
| NOM109 | Percepcion:ImporteExento | Clave `038` (Otros ingresos por salarios) → ImporteExento = 0. Previsión social sin clave específica → usar `056`. |
| NOM110 | Percepcion:ImporteExento | Si ImporteGravado = 0 → ImporteExento > 0 (no ambos en cero). |

## F. Deducciones — NOM91–NOM96
| Código | Atributo | Regla → cómo resolver |
|---|---|---|
| NOM91 | Deducciones:TotalImpuestosRetenidos | = Σ Deduccion.Importe con TipoDeduccion `002` (ISR). |
| NOM92 | Deducciones:TotalImpuestosRetenidos | Sin deducciones `002` → el atributo **no debe existir**. |
| NOM93 | Deduccion:TipoDeduccion | Clave del catálogo c_TipoDeduccion. |
| NOM94 | Incapacidades | Deducción `006` (descuento por incapacidad) → nodo Incapacidades debe existir. |
| NOM95 | Deduccion:Importe | Deducción `006` → Importe = Σ Incapacidad.ImporteMonetario. |
| NOM96 | Deduccion:Importe | Debe ser > 0 (una deducción en ceros se omite). |

## G. OtrosPagos y subsidio al empleo — NOM97–NOM103, NOM105–NOM108
| Código | Atributo | Regla → cómo resolver |
|---|---|---|
| NOM97 | OtroPago:TipoOtroPago | Clave del catálogo c_TipoOtroPago. |
| NOM98 | CompensacionSaldosAFavor | TipoOtroPago `004` → el nodo debe existir. |
| NOM99 | SubsidioAlEmpleo | TipoOtroPago `002` → el nodo debe existir (aunque el subsidio sea 0.00). |
| NOM100 | OtroPago:Importe | TipoOtroPago ≠ `002` → Importe > 0. (El `002` sí puede ser 0.00.) |
| NOM101 | SubsidioAlEmpleo:SubsidioCausado | NumDiasPagados ≤ 31 → SubsidioCausado ≤ 628.00 (tope Rev. E; cambia con el decreto/UMA vigente). |
| NOM102 | CompensacionSaldosAFavor:SaldoAFavor | Debe ser ≥ RemanenteSalFav. |
| NOM103 | CompensacionSaldosAFavor:Año | = año inmediato anterior, o año en curso solo si el periodo de pago es diciembre (referencia: FechaPago). |
| NOM105 | OtroPago (subsidio) | TipoRegimen `02` → debe existir OtroPago `002`, salvo que se registre `007`/`008` (ajuste Apéndice 7). |
| NOM106 | OtroPago (subsidio) | TipoRegimen ≠ `02` → prohibidas las claves `002`, `007` y `008`. |
| NOM107 | OtroPago:Importe | TipoOtroPago `002` → Importe ≤ SubsidioCausado. |
| NOM108 | SubsidioAlEmpleo:SubsidioCausado | NumDiasPagados > 31 → SubsidioCausado ≤ 20.66 × NumDiasPagados (factor Rev. E; parametrizable). |

## H. Incapacidades — NOM104
| Código | Atributo | Regla → cómo resolver |
|---|---|---|
| NOM104 | Incapacidad:TipoIncapacidad | Clave del catálogo c_TipoIncapacidad (01 riesgo de trabajo / 02 enfermedad general / 03 maternidad / 04 licencia cuidados hijos con cáncer). |

## Z. Catch-all
| Código | Regla |
|---|---|
| NOM111 | Error no clasificado — el PAC lo usa para cualquier validación no tipificada. Revisar el mensaje textual del PAC y validar contra XSD + orden de decisión de `nomina.md` §4. |

---

## Patrón de error handling (pantallas)

1. **Pre-validar local** antes de enviar al PAC, en este orden: valores fijos del sobre (A) →
   totales/fechas (B) → contrato/régimen (C/D) → percepciones y sus nodos hijo (E) →
   deducciones (F) → subsidio (G). Es el mismo orden de la matriz: el primer error que regresa
   el PAC suele ser el primero de esta lista que esté mal.
2. **Cuadres en servidor**: nunca dejar que el usuario capture TotalPercepciones, TotalGravado,
   TotalDeducciones, etc. — calcularlos siempre a partir de los renglones (fórmulas en `nomina.md` §5).
3. Cuando el PAC devuelva `NOMxxx`, traducir el código → sección/campo del wizard y resaltar el
   campo, en lugar de mostrar solo el texto del SAT.
4. Los topes de subsidio (NOM101/NOM108) cambian con el decreto y la UMA de cada año:
   mantenerlos en configuración, no en código.
