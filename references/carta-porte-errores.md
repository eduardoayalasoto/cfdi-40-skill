# Matriz de errores — Complemento Carta Porte 3.1 (CP1xx)

> Fuente: `Matriz_Errores_CCP_V31.xls` (SAT). Códigos `CP101`–`CP204` + `CP999`.
> Úsala como diccionario: el PAC devuelve `CPxxx` → busca aquí el atributo, la regla y **cómo resolver**.
> Agrupada por sección del complemento (así se mapea 1:1 al wizard de captura).

## Cómo leer
Cada fila: `CÓDIGO — Elemento:Atributo — regla (caso de validación) → cómo resolver`.
La causa #1 de rechazo es **condicionalidad por modo de transporte** y **TranspInternac=Sí**: un atributo que "debe existir" en un caso y "no debe existir" en otro. Antes de timbrar, evalúa primero: TipoDeComprobante (T/I), modo(s) de transporte, TranspInternac, RegistroISTMO, SectorCOFEPRIS.

---

## A. Comprobante (CFDI que porta el complemento) — CP101–CP111
| Código | Atributo | Regla → cómo resolver |
|---|---|---|
| CP101 | Comprobante:Version | Debe ser `4.0`. |
| CP102 | Subtotal | Si TipoDeComprobante=`T` → Subtotal `0`. |
| CP103 | Moneda | Si `T` → Moneda `XXX`. |
| CP104 | Moneda | Si `I` → Moneda ≠ `XXX` (usa MXN, USD, etc.). |
| CP105 | Total | Si `T` → Total `0`. |
| CP106 | Concepto:ObjetoImp | Clave de c_ObjetoImp (01/02/03/04/05). Si `02` → desglosar impuestos a nivel concepto. |
| CP107 | Receptor:Rfc | Si `T` → Receptor.Rfc = Emisor.Rfc (te trasladas a ti mismo). |
| CP108 | Receptor:Rfc | Si `I` y no genérico → RFC debe estar en l_RFC (inscrito no cancelado). |
| CP109 | Concepto:ClaveProdServ | Si `I` → ClaveProdServ debe ser una clave de **servicio de transporte** permitida (78101500–78102205, 78121603, 78141500/01, 84121806, 92121800–02). |
| CP110 | Concepto:ClaveProdServ | Si `I` + clave intermodal (78101900–04) → deben existir **≥2 nodos de transporte**. |
| CP111 | Receptor:UsoCFDI | Si `T` → UsoCFDI = `S01` (Sin efectos fiscales). |

## B. Nodo CartaPorte (raíz del complemento) — CP112–CP127
| Código | Atributo | Regla → cómo resolver |
|---|---|---|
| CP112 | CartaPorte | Exactamente **un** nodo CartaPorte hijo de Complemento. |
| CP113 | (coexistencia) | Solo puede coexistir con: TimbreFiscalDigital, ComercioExterior, PersonaFisicaIntegranteCoordinado, ImpuestosLocales, LeyendasFiscales. |
| CP114 | (existencia) | El complemento solo aplica si TipoDeComprobante = `I` o `T`. |
| CP115 | CartaPorte:Version | Debe ser `3.1`. |
| CP116 | RegimenesAduaneros | Nodo existe **solo si** TranspInternac=`Sí`. |
| CP117/118/169 | RegimenAduanero | Clave de c_RegimenAduanero; debe coincidir con ImpoExpo: `Entrada`→importación (col Entrada/Salida,Entrada), `Salida`→exportación (col Salida/Salida,Entrada). |
| CP119 | EntradaSalidaMerc | Si TranspInternac=`Sí` → capturar (`Entrada`/`Salida`). |
| CP120 | EntradaSalidaMerc | Si TranspInternac=`No` → **no debe existir**. |
| CP121 | PaisOrigenDestino | Si TranspInternac=`Sí` → clave c_Pais. |
| CP122 | PaisOrigenDestino | Si TranspInternac=`No` → no debe existir. |
| CP123 | ViaEntradaSalida | Si TranspInternac=`Sí` → clave c_CveTransporte. |
| CP124 | ViaEntradaSalida | Si TranspInternac=`No` → no debe existir. |
| CP125 | TotalDistRec | Existe **solo si** hay Autotransporte o TransporteFerroviario; si no, omitir. |
| CP126 | TotalDistRec | Debe ser = Σ Ubicacion:DistanciaRecorrida (de las ubicaciones tipo Destino). |
| CP127 | UbicacionPoloOrigen/Destino | Existen **solo si** RegistroISTMO=`Sí`; si no, omitir. |

## C. Ubicaciones (Origen/Destino + Domicilio) — CP128–CP147
| Código | Atributo | Regla → cómo resolver |
|---|---|---|
| CP128 | Ubicacion (Ferroviario) | Si Ferroviario → ≥1 Ubicacion tipo `Origen`. |
| CP129 | Ubicacion (Ferroviario) | Si Ferroviario → ≥5 Ubicaciones tipo `Destino`. |
| CP130 | Ubicacion (Auto/Marítimo/Aéreo) | ≥2 Ubicaciones: al menos una `Origen` y una `Destino`. |
| CP131 | Ubicacion:IDUbicacion | Requerido si existe Mercancia:CantidadTransporta. |
| CP132 | RFCRemitenteDestinatario | Si no es genérico → debe estar en l_RFC. |
| CP133 | NumRegIdTrib | Requerido si RFC = `XEXX010101000` (extranjero). |
| CP134 | ResidenciaFiscal | Requerido si hay NumRegIdTrib; clave c_Pais ≠ `MEX`. |
| CP135 | NumEstacion | Si Autotransporte → **omitir** NumEstacion. |
| CP136 | NumEstacion | Clave de c_Estaciones según modo (02 marítimo / 03 aéreo / 04 ferroviario). |
| CP137/138 | NombreEstacion | Requerido si hay NumEstacion; para estación extranjera, texto libre (no "Extranjera"). |
| CP139 | NavegacionTrafico | Existe **solo si** TransporteMaritimo. |
| CP140 | TipoEstacion | Clave c_TipoEstacion si Ferroviario/Marítimo/Aéreo; si Autotransporte → no existe; estación extranjera → no existe. |
| CP141 | DistanciaRecorrida | Existe si Auto/Ferroviario **y** TipoUbicacion=`Destino`; en `Origen` no aplica. |
| CP142 | Domicilio | Si Ferroviario y TipoEstacion=`02` (Intermedia) → Domicilio **no debe existir**; si no, sí. |
| CP143 | Domicilio:Colonia | MEX → clave c_Colonia que case con CodigoPostal; extranjero → texto libre. |
| CP144 | Domicilio:Localidad | MEX → clave c_Localidad que case con Estado; extranjero → texto libre. |
| CP145 | Domicilio:Municipio | MEX → clave c_Municipio que case con Estado; extranjero → texto libre. |
| CP146 | Domicilio:Estado | MEX/USA/CAN → clave c_Estado que case con Pais; otro → texto libre. |
| CP147 | Domicilio:CodigoPostal | MEX → clave c_CodigoPostal que case con Estado/Municipio/Localidad; otro → texto libre. |

## D. Mercancías — CP148–CP181
| Código | Atributo | Regla → cómo resolver |
|---|---|---|
| CP148 | Mercancias | ≥1 Mercancia **y** ≥1 nodo de transporte (Auto/Marítimo/Aéreo/Ferroviario). |
| CP149 | PesoBrutoTotal | Auto/Aéreo/Ferroviario → = Σ Mercancia:PesoEnKg. |
| CP150 | PesoBrutoTotal | Marítimo → = Σ DetalleMercancia:PesoBruto. |
| CP151 | PesoNetoTotal | Marítimo → = Σ DetalleMercancia:PesoNeto. |
| CP152 | PesoNetoTotal | Ferroviario → = Σ Carro:ToneladasNetasCarro. |
| CP153 | LogisticaInversaRecoleccionDevolucion | Solo puede existir si Autotransporte. |
| CP154 | NumTotalMercancias | = número de nodos Mercancia. |
| CP155 | Mercancia:MaterialPeligroso | Existe **solo si** la BienesTransp (c_ClaveProdServCP) tiene flag Material Peligroso `0,1` o `1`. |
| CP156 | CveMaterialPeligroso | Si MaterialPeligroso=`Sí` → clave c_MaterialPeligroso; si no, no existe. |
| CP157 | Embalaje | Requerido si hay CveMaterialPeligroso (clave c_TipoEmbalaje). |
| CP158 | SectorCOFEPRIS | Clave de c_SectorCOFEPRIS (opcional). |
| CP159 | SectorCOFEPRIS=01 Medicamentos | Requeridos: DenominacionGenericaProd, DenominacionDistintivaProd, Fabricante, FechaCaducidad, LoteMedicamento, FormaFarmaceutica, CondicionesEspTransp, RegistroSanitarioFolioAutorizacion. |
| CP160 | SectorCOFEPRIS=02 Precursores | Requeridos: NombreIngredienteActivo, NomQuimico, Fabricante, FechaCaducidad, LoteMedicamento, FormaFarmaceutica, CondicionesEspTransp. |
| CP161 | SectorCOFEPRIS=03 Psicotrópicos | Mismos que 01. |
| CP162 | SectorCOFEPRIS=04 Sustancias tóxicas | Requeridos: NomQuimico, NumCAS. |
| CP163 | SectorCOFEPRIS=05 Plaguicidas/fertilizantes | Requeridos: NombreIngredienteActivo, NumRegSanPlagCOFEPRIS, DatosFabricante, DatosFormulador, DatosMaquilador, UsoAutorizado. |
| CP164 | PermisoImportacion | Solo si TranspInternac=`Sí` + EntradaSalidaMerc=`Entrada` + SectorCOFEPRIS ∈ {01,02,03}. |
| CP165 | FolioImpoVUCEM | Solo si TranspInternac=`Sí` + `Entrada` + SectorCOFEPRIS ∈ {01,02,04,05}. |
| CP166 | RazonSocialEmpImp | Solo si TranspInternac=`Sí` + `Entrada` + SectorCOFEPRIS=`04`. |
| CP167 | ValorMercancia | Requerido si TransporteAereo. |
| CP168 | Moneda (mercancia) | Requerido si hay ValorMercancia. |
| CP170 | TipoMateria | Requerido si TranspInternac=`Sí` (clave c_TipoMateria). |
| CP171 | DescripcionMateria | Requerido si TipoMateria=`05` (Otra). |
| CP172 | DocumentacionAduanera | Si TranspInternac=`Sí`+`Entrada` → debe existir; +`Salida` → puede; si `No` → no existe. |
| CP173 | DocAduanera:TipoDocumento | Si EntradaSalidaMerc=`Salida` → TipoDocumento ≠ `01` (no Pedimento). |
| CP174 | DocAduanera:NumPedimento | Si `Entrada` + TipoDocumento=`01` → estructura de pedimento válida (año, aduana c_Aduanas, patente c_PatenteAduanal, consecutivo c_NumPedimentoAduana). |
| CP175 | DocAduanera:IdentDocAduanero | Requerido si TipoDocumento ≠ `01`. |
| CP176 | DocAduanera:RFCImpo | Requerido si hay NumPedimento; en l_RFC o genérico. |
| CP177 | GuiasIdentificacion | Si `T` + ClaveProdServ ∈ {31181701 Empaques, 24112700 Estibas} → debe existir. |
| CP178 | CantidadTransporta:IDOrigen | Debe coincidir con un IDUbicacion tipo Origen. |
| CP179 | CantidadTransporta:IDDestino | Debe coincidir con un IDUbicacion tipo Destino. |
| CP180 | CantidadTransporta:CvesTransporte | Requerido si **>1** nodo de transporte (intermodal); clave c_CveTransporte. |
| CP181 | DetalleMercancia | Existe **solo si** TransporteMaritimo. |

## E. Autotransporte — CP182–CP184
| Código | Atributo | Regla → cómo resolver |
|---|---|---|
| CP182 | Seguros:AseguraMedAmbiente | Requerido si Mercancia:MaterialPeligroso=`Sí`. |
| CP183 | Seguros:PolizaMedAmbiente | Requerido si hay AseguraMedAmbiente. |
| CP184 | Remolques | Según col Remolque de c_ConfigAutotransporte de ConfigVehicular: `1`→obligatorio, `0,1`→opcional, `0`→omitir. |

## F. Transporte Marítimo — CP185–CP187
| Código | Atributo | Regla → cómo resolver |
|---|---|---|
| CP185 | PermisoTempNavegacion | Requerido si NacionalidadEmbarc ≠ `MEX`. |
| CP186 | Contenedor:TipoContenedor | Si `CM011` (Ferri): Matricula/NumPrecinto **no existen**, pero IdCCPRelacionado/PlacaVMCCP/FechaCertificacionCCP **sí**; si ≠ CM011: al revés. |
| CP187 | Contenedor:RemolquesCCP | Puede existir solo si TipoContenedor=`CM011`. |

## G. Transporte Aéreo — CP188–CP190
| Código | Atributo | Regla → cómo resolver |
|---|---|---|
| CP188 | RFCEmbarcador | En l_RFC; excluyente con NumRegIdTribEmbarc. |
| CP189 | NumRegIdTribEmbarc | Requerido si no hay RFCEmbarcador. |
| CP190 | ResidenciaFiscalEmbarc | Requerido si hay NumRegIdTribEmbarc; c_Pais ≠ MEX. |

## H. Transporte Ferroviario — CP191–CP192
| Código | Atributo | Regla → cómo resolver |
|---|---|---|
| CP191 | Carro:ToneladasNetasCarro | Si hay Carro:Contenedor → = Σ Contenedor:PesoNetoMercancia (kg→ton); si no, valor directo. |
| CP192 | Carro:Contenedor | Existe **solo si** TipoDeServicio (c_TipoDeServicio) col Contenedor=`1` (TS02, TS04 intermodal). |

## I. Figura de Transporte — CP193–CP204
| Código | Atributo | Regla → cómo resolver |
|---|---|---|
| CP193 | FiguraTransporte | Requerido si Autotransporte. |
| CP194 | TiposFigura | Si Autotransporte → ≥1 con TipoFigura=`01` (Operador). |
| CP195 | RFCFigura | En l_RFC; excluyente con NumRegIdTribFigura. |
| CP196 | NumLicencia | Requerido si TipoFigura=`01` (Operador). |
| CP197 | NumRegIdTribFigura | Requerido si no hay RFCFigura. |
| CP198 | ResidenciaFiscalFigura | Requerido si hay NumRegIdTribFigura; c_Pais ≠ MEX. |
| CP199 | PartesTransporte | Existe **solo si** TipoFigura ∈ {02, 03}. |
| CP200–204 | TiposFigura:Domicilio:* | Misma cascada de domicilio que Ubicaciones (Colonia/Localidad/Municipio/Estado/CodigoPostal por país MEX vs libre). |

## Z. Catch-all
| CP999 | — | Error no clasificado. Revisa el XSD y el detalle del PAC; suele ser estructura/orden de nodos. |

---

## Patrón de error handling recomendado (app)
1. **Pre-validación local antes de timbrar** (no esperar el rechazo del PAC): evalúa en este orden — TipoComprobante(T/I) → modo(s) transporte → TranspInternac → RegistroISTMO → SectorCOFEPRIS → MaterialPeligroso. Cada condición habilita/deshabilita y vuelve obligatorios bloques completos.
2. **Cuadres numéricos**: TotalDistRec=Σ DistanciaRecorrida(Destino); PesoBrutoTotal/PesoNetoTotal según modo; NumTotalMercancias=conteo.
3. **Mapea CPxxx → campo del wizard**: cuando el PAC rechace, traduce el código a la sección/paso y resalta el campo (no solo mostrar el texto del SAT).
4. **Catálogos con columna de decisión** (ver `carta-porte.md`): c_ConfigAutotransporte.Remolque, c_TipoDeServicio.Contenedor, c_ClaveProdServCP.MaterialPeligroso, c_RegimenAduanero.ImpoExpo — el valor de la columna gobierna si un nodo es obligatorio/opcional/prohibido.
