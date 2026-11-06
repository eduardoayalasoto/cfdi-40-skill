# Matriz de errores — Complemento de Pagos 2.0 (CRP)

> Fuente: `MatrizDeErrores_CRP_V20_RevB.xls` (SAT). Códigos `CRP201xx` (comprobante base P) y `CRP202xx` (complemento) + `CRP20999`.
> Diccionario para error handling: el PAC devuelve `CRPxxxxx` → busca aquí atributo, regla y **cómo resolver / qué mostrar al usuario**.
> Detalle de estructura del complemento Pagos 2.0: `guia.md` sección 11. Valores fijos del CFDI tipo P: `SKILL.md`.

## Para pantallas/usuarios
Casi todos estos errores se previenen en captura. El **CFDI "sobre" tipo P es 100% de valores fijos** (no lo escribe el usuario, lo arma el sistema) → grupo A debe estar correcto por construcción. Los grupos B–F dependen de lo que el usuario captura por **pago** y por **documento relacionado**; ahí va la validación de UI + los cuadres.

---

## A. Comprobante base (CFDI tipo P, valores fijos) — CRP20101–CRP20123
Si alguno falla, es bug del generador, no del usuario.
| Código | Atributo | Debe ser → |
|---|---|---|
| CRP20101 | TipoDeComprobante | `P` |
| CRP20102 | Exportacion | `01` |
| CRP20103 | SubTotal | `0` |
| CRP20104 | Moneda | `XXX` |
| CRP20105 | FormaPago | **no existir** |
| CRP20106 | MetodoPago | **no existir** |
| CRP20107 | CondicionesDePago | **no existir** |
| CRP20108 | Descuento (comprobante) | **no existir** |
| CRP20109 | TipoCambio | **no existir** |
| CRP20110 | Total | `0` |
| CRP20111 | Conceptos | **un solo** Concepto |
| CRP20112 | Concepto hijos | sin nodos hijo (salvo AcuentaTerceros) |
| CRP20113 | ClaveProdServ | `84111506` |
| CRP20114 | NoIdentificacion | no existir |
| CRP20115 | Cantidad | `1` |
| CRP20116 | ClaveUnidad | `ACT` |
| CRP20117 | Unidad | no existir |
| CRP20118 | Descripcion | `Pago` |
| CRP20119 | ValorUnitario | `0` |
| CRP20120 | Importe | `0` |
| CRP20121 | Descuento (concepto) | no existir |
| CRP20122 | ObjetoImp | `01` |
| CRP20123 | Concepto:Impuestos | **no existir** |

## B. Totales del nodo Pagos (cuadres) — CRP20201–CRP20211
Cada total = Σ del importe correspondiente de los DoctoRelacionado **× TipoCambioP** de su Pago, redondeado. Si rechaza, hay descuadre en la suma.
| Código | Atributo | Regla |
|---|---|---|
| CRP20201/02/03 | TotalRetencionesIVA / ISR / IEPS | = Σ ImporteP retenido (por impuesto) × TipoCambioP. |
| CRP20204/05 | TotalTrasladosBaseIVA16 / ImpuestoIVA16 | base/importe trasladado Tasa 0.160000 × TipoCambioP. |
| CRP20206/07 | …IVA8 (0.080000) | idem 8%. |
| CRP20208/09 | …IVA0 (0.000000) | idem 0%. |
| CRP20210 | TotalTrasladosBaseExento | base trasladada TipoFactor Exento × TipoCambioP. |
| CRP20211 | MontoTotalPagos | = Σ (Monto × TipoCambioP) de cada Pago. |

## C. Nodo Pago — CRP20212–CRP20235
| Código | Atributo | Regla → cómo resolver |
|---|---|---|
| CRP20212 | FormaDePagoP | ≠ `99` (debe ser la forma real: 01,02,03,04,28…). |
| CRP20213 | MonedaP | ≠ `XXX`. |
| CRP20214 | TipoCambioP | requerido si MonedaP ≠ MXN. |
| CRP20215 | TipoCambioP | = `1` si MonedaP = MXN. |
| CRP20216 | Confirmacion | requerido si TipoCambioP fuera de límites (clave la da el PAC). |
| CRP20217 | Monto | Σ ImpPagado (misma moneda) ≤ Monto. |
| CRP20218 | Monto | > 0. |
| CRP20219 | Monto | decimales según MonedaP. |
| CRP20220 | Confirmacion | requerido si Monto (en MXN) excede límite. |
| CRP20221/24/27/28 | RfcEmisorCtaOrd / CtaOrdenante / RfcEmisorCtaBen / CtaBeneficiario | **no existir** si FormaDePagoP no es bancarizada (02,03,04,05,06,28,29). |
| CRP20222 | RfcEmisorCtaOrd | en l_RFC (salvo genérico XEXX). |
| CRP20223 | NomBancoOrdExt | requerido si RfcEmisorCtaOrd = XEXX010101000. |
| CRP20225/26 | CtaOrdenante / CtaBeneficiario | deben cumplir el patrón de c_FormaPago. |
| CRP20229 | TipoCadPago | existe **solo si** FormaDePagoP = `03`. |
| CRP20230–35 | CertPago / CadPago / SelloPago | si hay TipoCadPago → los 3 obligatorios; si no → los 3 prohibidos. |

## D. DoctoRelacionado — CRP20236–CRP20247, CRP20275–CRP20279
| Código | Atributo | Regla → cómo resolver |
|---|---|---|
| CRP20236 | MonedaDR | ≠ `XXX`. |
| CRP20237 | EquivalenciaDR | requerido si MonedaDR ≠ MonedaP. |
| CRP20238 | EquivalenciaDR | = `1` si MonedaDR = MonedaP (10 decimales `1.0000000000` en cálculo de márgenes, CRP20277). |
| CRP20239/41 | ImpSaldoAnt / ImpPagado | > 0. |
| CRP20240/42/43 | ImpSaldoAnt / ImpPagado / ImpSaldoInsoluto | decimales según MonedaDR. |
| CRP20244 | ImpSaldoInsoluto | ≥ 0 y = ImpSaldoAnt − ImpPagado. |
| CRP20245 | ObjetoImpDR | valor de c_ObjetoImp. |
| CRP20246 | ObjetoImpDR=`02` | → nodo ImpuestosDR **debe existir**. |
| CRP20247 | ObjetoImpDR ∈ {01,03,04,05} | → ImpuestosDR **no debe existir**. |
| CRP20278 | ObjetoImpDR ∈ {06,08} | sin RetencionDR/TrasladoDR con ImpuestoDR 002/003 (IVA/IEPS); puede RetencionDR 001 (ISR). |
| CRP20279 | ObjetoImpDR=`07` | sin IVA(002); debe haber TrasladoDR 003(IEPS); puede RetencionDR 001/003. |
| CRP20275 | ImpPagado (multimoneda) | dentro de límites inferior/superior por margen de variación. |
| CRP20276 | Monto (multimoneda) | entre Σ límites inferiores y Σ superiores de ImpPagado. |

## E. ImpuestosDR (impuestos del documento relacionado) — CRP20248–CRP20261
| Código | Atributo | Regla → cómo resolver |
|---|---|---|
| CRP20248 | ImpuestosDR | si existe → incluir traslados y/o retenciones. |
| CRP20249 | RetencionDR:BaseDR | > 0. |
| CRP20250 | RetencionDR:ImpuestoDR | valor de c_Impuesto. |
| CRP20251/52 | RetencionDR:TipoFactorDR | de c_TipoFactor, **≠ Exento**. |
| CRP20253 | RetencionDR:TasaOCuotaDR | de c_TasaOCuota (coherente impuesto+factor). |
| CRP20254 | RetencionDR:ImporteDR | entre límite inferior y superior. |
| CRP20255 | TrasladoDR:BaseDR | > 0. |
| CRP20256/57 | TrasladoDR:ImpuestoDR / TipoFactorDR | de c_Impuesto / c_TipoFactor. |
| CRP20258 | TrasladoDR Exento | sin TasaOCuotaDR ni ImporteDR. |
| CRP20259 | TrasladoDR Tasa/Cuota | con TasaOCuotaDR e ImporteDR. |
| CRP20260 | TrasladoDR:TasaOCuotaDR | de c_TasaOCuota (coherente). |
| CRP20261 | TrasladoDR:ImporteDR | entre límites. |

## F. ImpuestosP (impuestos totalizados del Pago) — CRP20262–CRP20274
| Código | Atributo | Regla → cómo resolver |
|---|---|---|
| CRP20262 | RetencionP:ImpuestoP | de c_Impuesto. |
| CRP20263 | RetencionP | un solo registro por tipo de impuesto retenido. |
| CRP20264 | RetencionP:ImporteP | exige al menos uno de TotalRetencionesIVA/ISR/IEPS. |
| CRP20265 | RetencionP:ImporteP | = Σ retenciones de los DR con el mismo ImpuestoP. |
| CRP20266 | TrasladoP (todo Exento) | solo BaseP, ImpuestoP, TipoFactorP. |
| CRP20267 | TrasladoP:BaseP (IVA 002) | exige al menos un TotalTrasladosBaseIVA16/8/0/Exento. |
| CRP20268 | TrasladoP:BaseP | = Σ BaseDR de DR con mismo ImpuestoP + TasaOCuotaP. |
| CRP20269 | TrasladoP:BaseP (todo Exento) | = Σ BaseDR. |
| CRP20270 | TrasladoP:ImpuestoP | de c_Impuesto. |
| CRP20271 | TrasladoP | un registro por combinación impuesto+factor+tasa. |
| CRP20272 | TrasladoP:TasaOCuotaP | de c_TasaOCuota (coherente). |
| CRP20273 | TrasladoP:ImporteP (IVA, no exento) | exige TotalTrasladosImpuestoIVA16/8/0. |
| CRP20274 | TrasladoP:ImporteP | = Σ ImporteDR de DR con mismo ImpuestoP + TasaOCuotaP. |

## Z. Catch-all
| CRP20999 | — | Error no clasificado: revisar XSD/estructura/orden de nodos del complemento. |

---

## Patrón de error handling (pantallas)
1. **El "sobre" P es fijo** → grupo A nunca debe llegar al usuario; si aparece, es bug.
2. **Por pago**: valida FormaDePagoP≠99, MonedaP/TipoCambioP, Monto>0 y cuentas según bancarización (grupo C) en el form.
3. **Por documento relacionado**: ObjetoImpDR gobierna si va ImpuestosDR (CRP20246/47/78/79); EquivalenciaDR según monedas; ImpSaldoInsoluto = ImpSaldoAnt − ImpPagado (calcúlalo, no lo pidas).
4. **Cuadres (B/E/F)**: calcula los totales TotalRetenciones*/TotalTraslados* y los BaseP/ImporteP **en el servidor** a partir de los DR; no dejes que el usuario los teclee → elimina CRP20201–20211 y CRP20265/268/274.
5. Traduce `CRPxxxxx` → sección del wizard (Pago / Documento / Impuestos) y resalta el campo.
