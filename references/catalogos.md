# Catálogos CFDI 4.0 — Referencia Completa

> Fuente: GNcys / SAT, Anexo 20 v4.0 (01/01/2022)
> Índice de catálogos: https://www.gncys.com/anexo20/4.0/catalogos/
> Descarga XLS completo: https://www.gncys.com/anexo20/4.0/catalogos/docs/catCFDI_V4_19-10-2021.xls

---

## c_FormaPago — Formas de Pago
**URL:** https://www.gncys.com/anexo20/4.0/formapago/ | Rev. 0 | 01/01/2022

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
| 13 | Pago por subrogación | No |
| 14 | Pago por consignación | No |
| 15 | Condonación | No |
| 17 | Compensación | No |
| 23 | Novación | No |
| 24 | Confusión | No |
| 25 | Remisión de deuda | No |
| 26 | Prescripción o caducidad | No |
| 27 | A satisfacción del acreedor | No |
| 28 | Tarjeta de débito | Sí |
| 29 | Tarjeta de servicios | Sí |
| 30 | Aplicación de anticipos | No |
| 31 | Intermediario pagos | No |
| 99 | Por definir — usar con MetodoPago=PPD | Opcional |

**Regla crítica:** FormaPago=`99` requiere MetodoPago=`PPD`. Son inseparables.

---

## c_TipoDeComprobante — Tipos de Comprobante
**URL:** https://www.gncys.com/anexo20/4.0/tipodecomprobante/ | Rev. 1.0 | 01/01/2022

| Clave | Descripción | Valor máximo de Total | Vigencia |
|---|---|---|---|
| I | Ingreso | 999999999999999999.999999 | 01/01/2022 |
| E | Egreso | 999999999999999999.999999 | 01/01/2022 |
| T | Traslado | 0 | 01/01/2022 |
| N | Nómina | 999999999999999999.999999 | 01/01/2022 |
| P | Pago | 999999999999999999.999999 | 01/01/2022 |

---

## c_MetodoPago — Método de Pago
**URL:** https://www.gncys.com/anexo20/4.0/metodopago/ | Rev. 1.0 | 01/01/2022

| Clave | Descripción | Vigencia |
|---|---|---|
| PUE | Pago en una sola exhibición (se cobra al emitir) | 01/01/2022 |
| PPD | Pago en parcialidades o diferido (se cobra después) | 01/01/2022 |

**Nota:** PPD requiere emitir CFDI de Pago (tipo P) con Complemento de Pagos 2.0 al recibir cada cobro.

---

## c_Exportacion — Exportación
**URL:** https://www.gncys.com/anexo20/4.0/exportacion/ | Rev. 2.0 | 24/02/2022

| Clave | Descripción | Vigencia |
|---|---|---|
| 01 | No aplica — usar en la mayoría de CFDIs | 01/01/2022 |
| 02 | Definitiva con clave A1 — requiere Complemento Comercio Exterior | 01/01/2022 |
| 03 | Temporal | 01/01/2022 |
| 04 | Definitiva con clave distinta a A1 o sin enajenación en términos del CFF | 25/02/2022 |

**Nota:** Campo obligatorio en todos los CFDI. Si no aplica exportación, usar `01`.

---

## c_TipoRelacion — Tipo de Relación entre CFDI
**URL:** https://www.gncys.com/anexo20/4.0/tiporelacion/ | Rev. 1.0 | 01/01/2022

| Clave | Descripción | Vigencia |
|---|---|---|
| 01 | Nota de crédito de los documentos relacionados | 01/01/2022 |
| 02 | Nota de débito de los documentos relacionados | 01/01/2022 |
| 03 | Devolución de mercancía sobre facturas o traslados previos | 01/01/2022 |
| 04 | Sustitución de los CFDI previos | 01/01/2022 |
| 05 | Traslados de mercancías facturados previamente | 01/01/2022 |
| 06 | Factura generada por los traslados previos | 01/01/2022 |
| 07 | CFDI por aplicación de anticipo | 01/01/2022 |

---

## c_RegimenFiscal — Régimen Fiscal
**URL:** https://www.gncys.com/anexo20/4.0/regimenfiscal/ | Rev. 1.0 | 01/01/2022

| Clave | Descripción | Física | Moral |
|---|---|---|---|
| 601 | General de Ley Personas Morales | No | Sí |
| 603 | Personas Morales con Fines no Lucrativos | No | Sí |
| 605 | Sueldos y Salarios e Ingresos Asimilados a Salarios | Sí | No |
| 606 | Arrendamiento | Sí | No |
| 607 | Régimen de Enajenación o Adquisición de Bienes | Sí | No |
| 608 | Demás ingresos | Sí | No |
| 610 | Residentes en el Extranjero sin Establecimiento Permanente en México | Sí | Sí |
| 611 | Ingresos por Dividendos (socios y accionistas) | Sí | No |
| 612 | Personas Físicas con Actividades Empresariales y Profesionales | Sí | No |
| 614 | Ingresos por intereses | Sí | No |
| 615 | Régimen de los ingresos por obtención de premios | Sí | No |
| 616 | Sin obligaciones fiscales — usar para XEXX010101000 | Sí | No |
| 620 | Sociedades Cooperativas de Producción que optan por diferir sus ingresos | No | Sí |
| 621 | Incorporación Fiscal — único que emite facturas globales | Sí | No |
| 622 | Actividades Agrícolas, Ganaderas, Silvícolas y Pesqueras | Sí | Sí |
| 623 | Opcional para Grupos de Sociedades | No | Sí |
| 624 | Coordinados | No | Sí |
| 625 | Régimen de las Actividades Empresariales con ingresos a través de Plataformas Tecnológicas | Sí | No |
| 626 | Régimen Simplificado de Confianza (RESICO) | Sí | Sí |

---

## c_UsoCFDI — Uso del CFDI
**URL:** https://www.gncys.com/anexo20/4.0/usocfdi/ | Rev. 1.0 | 01/01/2022

| Clave | Descripción | Física | Moral |
|---|---|---|---|
| G01 | Adquisición de mercancías | Sí | Sí |
| G02 | Devoluciones, descuentos o bonificaciones | Sí | Sí |
| G03 | Gastos en general | Sí | Sí |
| I01 | Construcciones | Sí | Sí |
| I02 | Mobiliario y equipo de oficina por inversiones | Sí | Sí |
| I03 | Equipo de transporte | Sí | Sí |
| I04 | Equipo de cómputo y accesorios | Sí | Sí |
| I05 | Dados, troqueles, moldes, matrices y herramental | Sí | Sí |
| I06 | Comunicaciones telefónicas | Sí | Sí |
| I07 | Comunicaciones satelitales | Sí | Sí |
| I08 | Otra maquinaria y equipo | Sí | Sí |
| D01 | Honorarios médicos, dentales y gastos hospitalarios | Sí | No |
| D02 | Gastos médicos por incapacidad o discapacidad | Sí | No |
| D03 | Gastos funerales | Sí | No |
| D04 | Donativos | Sí | No |
| D05 | Intereses reales efectivamente pagados por créditos hipotecarios (casa habitación) | Sí | No |
| D06 | Aportaciones voluntarias al SAR | Sí | No |
| D07 | Primas por seguros de gastos médicos | Sí | No |
| D08 | Gastos de transportación escolar obligatoria | Sí | No |
| D09 | Depósitos en cuentas para el ahorro, primas con base en planes de pensiones | Sí | No |
| D10 | Pagos por servicios educativos (colegiaturas) | Sí | No |
| S01 | Sin efectos fiscales | Sí | Sí |
| CP01 | Pagos — **obligatorio en CFDI tipo P** | Sí | Sí |
| CN01 | Nómina — **obligatorio en CFDI tipo N** | Sí | No |

---

## c_ObjetoImp — Objeto de Impuesto
**URL:** https://www.gncys.com/anexo20/4.0/objetoimp/ | Rev. 0 | 01/01/2022

| Clave | Descripción | Nodo Impuestos en concepto | Vigencia |
|---|---|---|---|
| 01 | No objeto de impuesto | **No debe existir** | 01/01/2022 |
| 02 | Sí objeto de impuesto | **Debe existir** con Traslados o Retenciones | 01/01/2022 |
| 03 | Sí objeto del impuesto y no obligado al desglose | **No debe existir** | 01/01/2022 |

---

## c_Impuesto — Impuestos
**URL:** https://www.gncys.com/anexo20/4.0/Impuesto/

| Clave | Descripción |
|---|---|
| 001 | ISR — Impuesto Sobre la Renta |
| 002 | IVA — Impuesto al Valor Agregado |
| 003 | IEPS — Impuesto Especial sobre Producción y Servicios |

---

## c_TipoFactor — Tipo de Factor
**URL:** https://www.gncys.com/anexo20/4.0/TipoFactor/

| Clave | Descripción | En Traslados | En Retenciones |
|---|---|---|---|
| Tasa | Porcentaje sobre la base (ej. 0.160000 = 16%) | Permitido | Permitido |
| Cuota | Monto fijo por unidad de medida | Permitido | Permitido |
| Exento | Exento de impuesto — sin TasaOCuota ni Importe | Permitido | **Prohibido** |

---

## c_TasaOCuota — Tasas o Cuotas de Impuestos
**URL:** https://www.gncys.com/anexo20/4.0/TasaOCuota/ | Rev. 0 | 01/01/2022

| Tipo | Valor mín. | Valor máx. | Impuesto | Factor | Uso más común |
|---|---|---|---|---|---|
| Fijo | — | 0.000000 | IVA | Tasa | IVA 0% (exportaciones, alimentos, medicamentos) |
| Fijo | — | 0.080000 | IVA | Tasa | IVA 8% (zona fronteriza norte) |
| Fijo | — | 0.160000 | IVA | Tasa | **IVA 16% (tasa general)** |
| Rango | 0 | 0.160000 | IVA | Tasa | Tasa variable entre 0% y 16% |
| Fijo | — | 0.265000 | IEPS | Tasa | Cervezas y bebidas alcohólicas |
| Fijo | — | 0.300000 | IEPS | Tasa | Bebidas alcohólicas (> 20° GL) |
| Fijo | — | 0.530000 | IEPS | Tasa | Tabacos labrados |
| Fijo | — | 0.500000 | IEPS | Tasa | Cigarrillos |
| Fijo | — | 1.600000 | IEPS | Tasa | Cigarros (por unidad) |
| Fijo | — | 0.304000 | IEPS | Tasa | Bebidas energizantes |
| Fijo | — | 0.250000 | IEPS | Tasa | Bebidas saborizadas |
| Fijo | — | 0.090000 | IEPS | Tasa | Alimentos de alto valor calórico |
| Fijo | — | 0.080000 | IEPS | Tasa | Combustibles automotrices |
| Fijo | — | 0.070000 | IEPS | Tasa | Plaguicidas categoría 5 |
| Fijo | — | 0.060000 | IEPS | Tasa | Plaguicidas categoría 4 |
| Fijo | — | 0.030000 | IEPS | Tasa | Plaguicidas categoría 3 |
| Fijo | — | 0.000000 | IEPS | Tasa | IEPS exento (tasa 0%) |
| Rango | 0 | 59.1449 | IEPS | Cuota | Cuota por litro/unidad (combustibles, etc.) |
| Rango | 0 | 0.350000 | ISR | Tasa | Retención ISR (variable según tabla de tarifas) |

---

## c_Periodicidad — Periodicidad (facturas globales)
**URL:** https://www.gncys.com/anexo20/4.0/periodicidad/ | Rev. 2.0 | 24/02/2022

| Clave | Descripción | Vigencia |
|---|---|---|
| 01 | Diario | 01/01/2022 |
| 02 | Semanal | 01/01/2022 |
| 03 | Quincenal | 01/01/2022 |
| 04 | Mensual | 01/01/2022 |
| 05 | Bimestral | 01/01/2022 |

---

## c_Meses — Meses (facturas globales)
**URL:** https://www.gncys.com/anexo20/4.0/meses/ | Rev. 1.0 | 01/01/2022

| Clave | Descripción | Periodicidad |
|---|---|---|
| 01 | Enero | Mensual |
| 02 | Febrero | Mensual |
| 03 | Marzo | Mensual |
| 04 | Abril | Mensual |
| 05 | Mayo | Mensual |
| 06 | Junio | Mensual |
| 07 | Julio | Mensual |
| 08 | Agosto | Mensual |
| 09 | Septiembre | Mensual |
| 10 | Octubre | Mensual |
| 11 | Noviembre | Mensual |
| 12 | Diciembre | Mensual |
| 13 | Enero-Febrero | Bimestral |
| 14 | Marzo-Abril | Bimestral |
| 15 | Mayo-Junio | Bimestral |
| 16 | Julio-Agosto | Bimestral |
| 17 | Septiembre-Octubre | Bimestral |
| 18 | Noviembre-Diciembre | Bimestral |

---

## c_Estado — Estados de México (c_Pais = MEX)
**URL:** https://www.gncys.com/anexo20/4.0/estado/ | Rev. 0 | 01/01/2022
> El catálogo completo incluye también estados de USA (50) y Canada (13).

| Clave | Estado |
|---|---|
| AGU | Aguascalientes |
| BCN | Baja California |
| BCS | Baja California Sur |
| CAM | Campeche |
| CHP | Chiapas |
| CHH | Chihuahua |
| COA | Coahuila |
| COL | Colima |
| CMX | Ciudad de México |
| DUR | Durango |
| GUA | Guanajuato |
| GRO | Guerrero |
| HID | Hidalgo |
| JAL | Jalisco |
| MEX | Estado de México |
| MIC | Michoacán |
| MOR | Morelos |
| NAY | Nayarit |
| NLE | Nuevo León |
| OAX | Oaxaca |
| PUE | Puebla |
| QUE | Querétaro |
| ROO | Quintana Roo |
| SLP | San Luis Potosí |
| SIN | Sinaloa |
| SON | Sonora |
| TAB | Tabasco |
| TAM | Tamaulipas |
| TLA | Tlaxcala |
| VER | Veracruz |
| YUC | Yucatán |
| ZAC | Zacatecas |

---

## RFC Genéricos

| RFC | Descripción | Nombre obligatorio |
|---|---|---|
| XAXX010101000 | Público en General (nacional) | `PUBLICO EN GENERAL` (exacto, mayúsculas) |
| XEXX010101000 | Extranjero | Nombre de la empresa/persona extranjera |

---

## Catálogos de Alto Volumen — Solo por URL

Estos catálogos tienen miles de registros y no se incluyen aquí. Consultarlos en línea o en la BD.

| Catálogo | Registros aprox. | URL |
|---|---|---|
| c_ClaveProdServ | ~55,000 | https://www.gncys.com/anexo20/4.0/claveprodserv/ |
| c_ClaveUnidad | ~2,500 | https://www.gncys.com/anexo20/4.0/claveunidad/ |
| c_CodigoPostal | ~100,000 | https://www.gncys.com/anexo20/4.0/codigopostal/ |
| c_Colonia | ~100,000 | https://www.gncys.com/anexo20/4.0/colonia/ |
| c_Municipio | ~2,500 | https://www.gncys.com/anexo20/4.0/municipio/ |
| c_Localidad | miles | https://www.gncys.com/anexo20/4.0/localidad |
| c_Moneda | 177 | https://www.gncys.com/anexo20/4.0/moneda/ |
| c_Pais | ~250 | https://www.gncys.com/anexo20/4.0/pais/ |
| c_Aduana | ~50 | https://www.gncys.com/anexo20/4.0/aduana/ |
| c_PatenteAduanal | ~1,000+ | https://www.gncys.com/anexo20/4.0/patenteaduanal/ |
| c_NumPedimentoAduana | miles | https://www.gncys.com/anexo20/4.0/numpedimentoaduana/ |
