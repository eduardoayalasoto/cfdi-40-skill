# Matriz de Errores CFDI 4.0 — Referencia Completa

> Fuente: SAT — Matriz de Errores CFDI v4.0, versión 25/03/2026
> URL: https://www.gncys.com/anexo20/4.0/errores/

Cuando el PAC rechaza un CFDI, devuelve un código `CFDI40xxx`. Busca el código
aquí para entender la causa exacta y cómo corregirla.

---

## Cómo interpretar los errores

- Los errores **CFDI401xx** son del nodo `Comprobante` (campos raíz)
- Los errores **CFDI401xx–CFDI402xx** cubren Emisor, Receptor, Conceptos e Impuestos
- **CFDI40999** = error no clasificado; revisar XML completo contra XSD

---

## Tabla completa de errores

| Código | Atributo afectado | Descripción del error | Cómo corregir |
|---|---|---|---|
| CFDI40101 | Fecha | No cumple con el patrón requerido | Formato exacto: `AAAA-MM-DDThh:mm:ss` — sin zona horaria, hora local |
| CFDI40102 | Sello | El resultado de la digestión debe ser igual al resultado de la desencripción del sello | Regenerar cadena original y sello con el CSD correcto y vigente |
| CFDI40103 | FormaPago | Si TipoDeComprobante es T, N o P, FormaPago no debe existir | Eliminar el campo FormaPago del XML |
| CFDI40104 | FormaPago | No contiene un valor del catálogo c_FormaPago | Usar clave válida: 01, 02, 03, 04, 05, 06, 08, 12–17, 23–31, 99 |
| CFDI40105 | FormaPago | No contiene el valor "99" | Cuando MetodoPago=PPD, FormaPago debe ser "99" |
| CFDI40106 | Certificado | No cumple con alguno de los valores permitidos | Verificar que el certificado CSD esté vigente y en base64 correcto |
| CFDI40107 | SubTotal | Excede la cantidad de decimales que soporta la moneda | Redondear al número de decimales de la moneda (MXN=2, BHD=3, CLP=0) |
| CFDI40108 | SubTotal | TipoDeComprobante I/E/N: importe ≠ redondeo de suma de conceptos | SubTotal = ∑(Importe de conceptos), redondeado |
| CFDI40109 | SubTotal | TipoDeComprobante T o P: importe ≠ 0 | Poner SubTotal="0" en comprobantes de Traslado o Pago |
| CFDI40110 | Descuento | Descuento > SubTotal | El descuento total no puede superar el subtotal |
| CFDI40111 | Descuento | TipoDeComprobante no es I/E/N y un concepto incluye descuento | Eliminar descuentos de conceptos en comprobantes T y P |
| CFDI40112 | Descuento | Excede decimales soportados por la moneda | Redondear descuento igual que SubTotal |
| CFDI40113 | Moneda | No contiene valor del catálogo c_Moneda | Usar código ISO 4217 válido: MXN, USD, EUR, etc. |
| CFDI40114 | TipoCambio | Moneda=MXN pero TipoCambio ≠ "1" | Cuando Moneda=MXN, TipoCambio debe ser exactamente "1" |
| CFDI40115 | TipoCambio | Moneda ≠ MXN y ≠ XXX: TipoCambio no registrado | Agregar TipoCambio con el tipo de cambio FIX del día |
| CFDI40116 | TipoCambio | Moneda=XXX y existe TipoCambio | Eliminar TipoCambio cuando Moneda=XXX (CFDIs de Pago) |
| CFDI40117 | TipoCambio | No cumple el patrón requerido | Valor numérico positivo con hasta 6 decimales |
| CFDI40118 | TipoCambio | Fuera del rango permitido sin campo Confirmacion | Obtener clave Confirmacion del PAC o ajustar TipoCambio al rango |
| CFDI40119 | Total | Total ≠ SubTotal − Descuento + Traslados − Retenciones | Recalcular: Total = SubTotal - Descuento + TotalImpuestosTrasladados - TotalImpuestosRetenidos |
| CFDI40120 | Total | Fuera del límite establecido sin Confirmacion | Obtener clave Confirmacion del PAC si el total es inusualmente alto |
| CFDI40121 | TipoDeComprobante | No contiene valor del catálogo c_TipoDeComprobante | Usar: I, E, T, N, o P |
| CFDI40122 | Exportacion | Valor "02" sin Complemento para Comercio Exterior | Agregar el Complemento de Comercio Exterior o cambiar Exportacion a "01" |
| CFDI40123 | Exportacion | No contiene valor del catálogo c_Exportacion | Usar: 01 (no aplica), 02 (definitiva A1), 03 (temporal), 04 (definitiva otra) |
| CFDI40124 | MetodoPago | No contiene valor del catálogo c_MetodoPago | Usar: PUE o PPD |
| CFDI40125 | MetodoPago | TipoDeComprobante T o P y existe MetodoPago | Eliminar MetodoPago de comprobantes de Traslado y Pago |
| CFDI40126 | LugarExpedicion | No contiene valor del catálogo c_CodigoPostal | Verificar que el CP exista en el catálogo SAT y corresponda a la sucursal |
| CFDI40127 | Confirmacion | Existe Confirmacion pero TipoCambio/Total están dentro del rango | Eliminar el campo Confirmacion si no es necesario |
| CFDI40128 | Confirmacion | Número de confirmación inválido | La clave la asigna el PAC — solicitarla nuevamente |
| CFDI40129 | Confirmacion | Número de confirmación ya utilizado | Solicitar nueva clave Confirmacion al PAC |
| CFDI40130 | RFC/Nombre Receptor | RFC=XAXX010101000 pero Nombre ≠ "PUBLICO EN GENERAL" | Nombre debe ser exactamente `PUBLICO EN GENERAL` (mayúsculas, sin acento) |
| CFDI40131 | Periodicidad | No contiene valor del catálogo c_Periodicidad | Usar: 01 (Diario), 02 (Semanal), 03 (Quincenal), 04 (Mensual), 05 (Bimestral) |
| CFDI40132 | Periodicidad | RegimenFiscal del emisor ≠ 621 en factura global | Las facturas globales solo las emite el régimen 621 (Incorporación Fiscal) |
| CFDI40133 | Meses | No contiene valor del catálogo c_Meses | Usar claves 01–18 según el período de la factura global |
| CFDI40134 | Meses | Para periodicidad mensual, valor no es 01–12 | El campo Meses debe ser el mes correspondiente (01=Enero … 12=Diciembre) |
| CFDI40135 | Meses | Para periodicidad bimestral, valor no es 13–18 | Usar 13–18 para bimestres (13=Ene-Feb, 14=Mar-Abr … 18=Nov-Dic) |
| CFDI40136 | Año | No es el año en curso ni el año inmediato anterior | Verificar que el año de la factura global sea correcto |
| CFDI40137 | TipoRelacion | No contiene valor del catálogo c_TipoRelacion | Usar: 01–07 según el tipo de relación entre CFDIs |
| CFDI40138 | Nombre (Emisor) | Emisor no está en la lista de RFC inscritos no cancelados | El CSD del emisor puede estar revocado — verificar en el SAT |
| CFDI40139 | Nombre (Emisor) | Nombre no corresponde al RFC del Emisor | Copiar el nombre exacto de la Constancia de Situación Fiscal |
| CFDI40140 | RegimenFiscal | No contiene valor del catálogo c_RegimenFiscal | Ver catálogo completo en references/catalogos.md |
| CFDI40141 | RegimenFiscal | No corresponde al tipo de persona (física/moral) | 601/603/620/623/624 = solo moral; resto = física o ambas |
| CFDI40142 | FacAtrAdquirente | Número de operación inválido | Verificar el número de operación de facturación atribuible al adquirente |
| CFDI40143 | RFC (Receptor) | RFC del receptor no existe en la l_RFC del SAT | Verificar que el RFC esté activo; si es extranjero, usar XEXX010101000 |
| CFDI40144 | Nombre (Receptor) | Receptor no está en la lista de RFC inscritos no cancelados | El receptor puede tener el RFC cancelado — verificar con él |
| CFDI40145 | Nombre (Receptor) | Nombre no corresponde al RFC del Receptor | Copiar el nombre exacto de la Constancia de Situación Fiscal del receptor |
| CFDI40146 | Nombre (Receptor) | RFC receptor debe ser XAXX010101000 | Para público en general sin datos, usar RFC genérico XAXX010101000 |
| CFDI40147 | DomicilioFiscalReceptor | No está en la lista de RFC inscritos no cancelados | RFC del receptor no activo en el SAT |
| CFDI40148 | DomicilioFiscalReceptor | No corresponde al RFC del Receptor | El CP debe ser el del domicilio fiscal registrado en el SAT para ese RFC |
| CFDI40149 | DomicilioFiscalReceptor | No es igual al LugarExpedicion | **Nuevo en v4.0**: el CP del receptor debe coincidir con LugarExpedicion — aplicable solo cuando el receptor es el mismo que el emisor (autoconsumo) — *revisar interpretación según caso* |
| CFDI40150 | ResidenciaFiscal | No contiene valor del catálogo c_Pais | Usar código ISO 3166-1 alpha-3: USA, CAN, ESP, etc. |
| CFDI40151 | ResidenciaFiscal | RFC inscrito en SAT o RFC genérico nacional y existe ResidenciaFiscal | Eliminar ResidenciaFiscal si el receptor tiene RFC mexicano |
| CFDI40152 | ResidenciaFiscal | Valor = MEX | ResidenciaFiscal no puede ser México (MEX); solo extranjeros |
| CFDI40153 | ResidenciaFiscal | NumRegIdTrib existe pero no hay ResidenciaFiscal | Si hay número de registro tributario extranjero, también debe ir ResidenciaFiscal |
| CFDI40154 | NumRegIdTrib | RFC es mexicano o genérico nacional y existe NumRegIdTrib | Eliminar NumRegIdTrib si el receptor es mexicano |
| CFDI40155 | NumRegIdTrib | Requiere Complemento Comercio Exterior y RFC genérico extranjero | NumRegIdTrib solo aplica con XEXX010101000 y Complemento Comercio Exterior |
| CFDI40156 | NumRegIdTrib | No cumple el patrón del país correspondiente | Verificar formato del ID tributario según el país en c_Pais |
| CFDI40157 | RegimenFiscalReceptor | No contiene valor del catálogo c_RegimenFiscal | Campo obligatorio en v4.0 — ver catálogo en references/catalogos.md |
| CFDI40158 | RegimenFiscalReceptor | No corresponde al tipo de persona del receptor | Verificar si el receptor es física o moral y usar régimen compatible |
| CFDI40159 | RegimenFiscalReceptor | No corresponde al RFC del receptor | El régimen debe coincidir con el registrado en el SAT para ese RFC |
| CFDI40160 | UsoCFDI | No contiene valor del catálogo c_UsoCFDI | Ver catálogo completo en references/catalogos.md |
| CFDI40161 | UsoCFDI | No corresponde al tipo de persona y régimen del receptor | D01–D10 solo para personas físicas; CP01 obligatorio en tipo P; CN01 en tipo N |
| CFDI40162 | ClaveProdServ | No contiene valor del catálogo c_ClaveProdServ | Verificar clave en el catálogo SAT: https://www.gncys.com/anexo20/4.0/claveprodserv/ |
| CFDI40163 | ClaveProdServ | Requiere un complemento que no existe | Algunas claves de producto exigen complementos específicos |
| CFDI40164 | ClaveProdServ | Impuesto relacionado no declarado | La clave requiere declarar un impuesto que falta en el concepto |
| CFDI40165 | ClaveUnidad | No contiene valor del catálogo c_ClaveUnidad | Verificar clave en: https://www.gncys.com/anexo20/4.0/claveunidad/ |
| CFDI40166 | ValorUnitario | Debe ser > 0 para comprobantes I, E o N | No se puede facturar a $0 en ingresos, egresos o nómina |
| CFDI40167 | Importe (concepto) | Fuera del rango permitido | Verificar que Importe = Cantidad × ValorUnitario con decimales correctos |
| CFDI40168 | Descuento (concepto) | Más decimales que el campo Importe del concepto | El descuento no puede tener más decimales que el importe del concepto |
| CFDI40169 | Descuento (concepto) | Descuento > Importe del concepto | El descuento de un concepto no puede superar su importe |
| CFDI40170 | ObjetoImp | No contiene valor del catálogo c_ObjetoImp | Usar: 01 (no objeto), 02 (sí objeto), 03 (sí objeto sin desglose) |
| CFDI40171 | ObjetoImp | ObjetoImp=02 pero no existe nodo Impuestos en el concepto | Agregar el nodo Impuestos con Traslados y/o Retenciones |
| CFDI40172 | ObjetoImp | ObjetoImp=01 o 03 pero existe nodo Impuestos en el concepto | Eliminar el nodo Impuestos del concepto |
| CFDI40173 | Impuestos (concepto) | Nodo Impuestos existe pero sin traslados ni retenciones | El nodo Impuestos debe tener al menos un Traslado o una Retención |
| CFDI40174 | Base (Traslado) | Base ≤ 0 en traslado del concepto | La base del impuesto trasladado debe ser mayor que cero |
| CFDI40175 | Impuesto (Traslado) | No contiene valor de c_Impuesto | Usar: 001 (ISR), 002 (IVA), 003 (IEPS) |
| CFDI40176 | TipoFactor (Traslado) | No contiene valor de c_TipoFactor | Usar: Tasa, Cuota, o Exento |
| CFDI40177 | TipoFactor (Traslado) | TipoFactor=Exento pero existen TasaOCuota o Importe | Eliminar TasaOCuota e Importe cuando TipoFactor=Exento |
| CFDI40178 | TipoFactor (Traslado) | TipoFactor=Tasa o Cuota pero faltan TasaOCuota o Importe | Agregar TasaOCuota e Importe cuando TipoFactor es Tasa o Cuota |
| CFDI40179 | TasaOCuota (Traslado) | No contiene valor válido del catálogo o fuera de rango | IVA 16%=0.160000, IVA 8%=0.080000, IVA 0%=0.000000 — ver errores.md catálogo |
| CFDI40180 | Importe (Traslado) | Fuera del rango permitido | Importe = Base × TasaOCuota, con decimales de la moneda |
| CFDI40181 | Base (Retención) | Base ≤ 0 en retención del concepto | La base de retención debe ser mayor que cero |
| CFDI40182 | Impuesto (Retención) | No contiene valor de c_Impuesto | Usar: 001 (ISR), 002 (IVA), 003 (IEPS) |
| CFDI40183 | TipoFactor (Retención) | No contiene valor de c_TipoFactor | Usar: Tasa o Cuota — Exento no está permitido en retenciones |
| CFDI40184 | TipoFactor (Retención) | TipoFactor=Exento en una retención | Las retenciones no pueden ser Exentas — corregir a Tasa o Cuota |
| CFDI40185 | TasaOCuota (Retención) | No contiene valor válido del catálogo | Verificar que la tasa corresponda al impuesto y factor declarados |
| CFDI40186 | Importe (Retención) | Fuera del rango permitido | Importe = Base × TasaOCuota, con decimales de la moneda |
| CFDI40187 | RfcACuentaTerceros | No se encuentra en la lista l_LCO | El RFC del tercero no está en la Lista de Contribuyentes Obligados |
| CFDI40188 | RfcACuentaTerceros | Igual al RFC del Emisor o Receptor | El RFC del tercero debe ser diferente al del emisor y receptor |
| CFDI40189 | NombreACuentaTerceros | No está en la lista de RFC inscritos no cancelados | RFC del tercero no activo |
| CFDI40190 | NombreACuentaTerceros | No corresponde al RFC del tercero | Copiar nombre exacto de la Constancia de Situación Fiscal del tercero |
| CFDI40191 | RegimenFiscalACuentaTerceros | No contiene valor del catálogo c_RegimenFiscal | Ver catálogo en references/catalogos.md |
| CFDI40192 | DomicilioFiscalACuentaTerceros | No está en la lista de RFC inscritos no cancelados | RFC del tercero no activo |
| CFDI40193 | DomicilioFiscalACuentaTerceros | No corresponde al RFC del tercero | El CP debe ser el domicilio fiscal del tercero en el SAT |
| CFDI40194 | NumeroPedimento | Número de pedimento inválido (en concepto) | Formato: AA-ADUANA-PATENTE-XXXXXXXX — verificar estructura |
| CFDI40195 | NumeroPedimento | No debe existir si hay Complemento de Comercio Exterior | Eliminar NumeroPedimento del concepto cuando se usa el complemento |
| CFDI40196 | ClaveProdServ | No contiene valor del catálogo (en parte del concepto) | Igual que CFDI40162 pero en el nodo Parte |
| CFDI40197 | ValorUnitario | Debe ser > 0 (en parte del concepto) | Igual que CFDI40166 pero en el nodo Parte |
| CFDI40198 | Importe | Fuera del rango (en parte del concepto) | Igual que CFDI40167 pero en el nodo Parte |
| CFDI40199 | NumeroPedimento | Inválido (en parte del concepto) | Igual que CFDI40194 pero en el nodo Parte |
| CFDI40200 | NumeroPedimento | No debe existir con Complemento Comercio Exterior (en parte) | Igual que CFDI40195 pero en el nodo Parte |
| CFDI40201 | Impuestos (global) | TipoDeComprobante T o P y existe nodo Impuestos | Eliminar el nodo Impuestos del comprobante en tipo T o P |
| CFDI40202 | TotalImpuestosRetenidos | Más decimales de los soportados por la moneda | Redondear a los decimales de la moneda |
| CFDI40203 | TotalImpuestosRetenidos | ≠ suma de importes de los nodos Retencion | Recalcular: TotalImpuestosRetenidos = ∑(Importe de cada Retencion) |
| CFDI40204 | TotalImpuestosTrasladados | Más decimales de los soportados por la moneda | Redondear a los decimales de la moneda |
| CFDI40205 | TotalImpuestosTrasladados | ≠ suma de importes de los nodos Traslado | Recalcular: TotalImpuestosTrasladados = ∑(Importe de cada Traslado) |
| CFDI40206 | Retenciones | Existe nodo Retenciones sin TotalImpuestosRetenidos | Agregar el atributo TotalImpuestosRetenidos al nodo Impuestos |
| CFDI40207 | Impuesto (Retención global) | No contiene valor de c_Impuesto | Usar: 001 (ISR), 002 (IVA), 003 (IEPS) |
| CFDI40208 | Impuesto (Retención global) | Más de un registro por tipo de impuesto | Solo puede haber un nodo Retencion por tipo de impuesto; sumar importes |
| CFDI40209 | Importe (Retención global) | Existe sin TotalImpuestosRetenidos | Agregar el atributo TotalImpuestosRetenidos |
| CFDI40210 | Importe (Retención global) | Más decimales de los soportados por la moneda | Redondear |
| CFDI40211 | Importe (Retención global) | ≠ redondeo de suma de retenciones de conceptos del mismo tipo | El Importe global de cada retención debe = ∑(ImporteRetención en conceptos del mismo tipo) |
| CFDI40212 | Traslados | Existe nodo Traslados sin TotalImpuestosTrasladados | Agregar el atributo TotalImpuestosTrasladados al nodo Impuestos |
| CFDI40213 | Traslado (global) | Faltan campos Base, Impuesto o TipoFactor | Los tres campos son obligatorios en cada Traslado global |
| CFDI40214 | Base (Traslado global) | Más decimales de los soportados por la moneda | Redondear |
| CFDI40215 | Base (Traslado global) | ≠ redondeo de suma de bases de conceptos (mismo impuesto+tasa) | La Base global debe cuadrar con la suma de bases de conceptos |
| CFDI40216 | Base (Traslado global) | ≠ redondeo de suma de todas las bases trasladadas en conceptos | Error de suma en bases — revisar cada concepto |
| CFDI40217 | Impuesto (Traslado global) | No contiene valor de c_Impuesto | Usar: 001, 002, 003 |
| CFDI40218 | Impuesto (Traslado global) | Más de un registro con la misma combinación impuesto+factor+tasa | Consolidar traslados con la misma combinación en un solo nodo |
| CFDI40219 | TasaOCuota (Traslado global) | No corresponde al catálogo para ese impuesto y factor | Verificar que impuesto, factor y tasa sean combinación válida en c_TasaOCuota |
| CFDI40220 | Importe (Traslado global) | Más decimales de los soportados por la moneda | Redondear |
| CFDI40221 | Importe (Traslado global) | ≠ redondeo de suma de importes de conceptos (mismo impuesto+tasa) | El Importe global del traslado debe = ∑(Importe traslado en conceptos del mismo tipo y tasa) |
| CFDI40999 | No clasificado | Error no clasificado | Validar el XML completo contra cfdv40.xsd; revisar todos los nodos |

---

## Errores más frecuentes y su solución rápida

### "El Nombre del emisor/receptor no corresponde" (CFDI40139 / CFDI40145)
El nombre en el XML debe ser **byte-a-byte idéntico** al de la l_RFC del SAT.
Pasos: 1) Descargar la Constancia de Situación Fiscal del contribuyente, 2) Copiar el nombre exactamente como aparece, 3) Evitar caracteres extra, espacios al final, o diferencias de mayúsculas/minúsculas.

### "SubTotal no es igual a la suma de conceptos" (CFDI40108)
El valor debe ser el **redondeo** de la suma, no la suma aritmética exacta.
Fórmula: `SubTotal = ROUND(∑(Concepto.Importe), decimales_moneda)`

### "TotalImpuestosTrasladados no es igual..." (CFDI40205 / CFDI40221)
Causa más común: el redondeo se aplicó mal. El total de impuestos debe calcularse como suma de los importes **ya redondeados** de cada Traslado, no como redondeo de la suma de bases × tasa.

### "La digestión no coincide con el sello" (CFDI40102)
Causas: 1) Cadena original mal generada (problema de XSLT o namespace), 2) CSD caducado o revocado, 3) XML modificado después de firmar, 4) Encoding incorrecto (BOM en UTF-8).

### Errors en serie P (Complemento Pagos)
Si ves múltiples errores en un CFDI tipo P, verificar primero:
- SubTotal ≠ 0 → CFDI40109
- Total ≠ 0 → CFDI40119  
- Moneda ≠ XXX → CFDI40113
- Existe FormaPago → CFDI40103
- Existe nodo Impuestos → CFDI40201
- UsoCFDI ≠ CP01 → CFDI40161
