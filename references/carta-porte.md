# Complemento Carta Porte 3.1 — estructura, reglas y flujo

> Fuente: instructivos SAT (`Instructivo_ComplementoCartaPorte_{Autotransporte,Maritimo,Aereo,Ferroviario}_31.pdf`), `CatalogosCartaPorte31.xls`, `Preguntas_frecuentes_CartaPorte_31.pdf`.
> Vigente: **CCP 3.1** (única timbrable). Namespace `http://www.sat.gob.mx/CartaPorte31`. Va dentro de un CFDI 4.0 tipo `T` (Traslado) o `I` (Ingreso).
> Para la lista de errores de validación: `carta-porte-errores.md`.

## 1. Cuándo se usa
Acredita el **transporte/tenencia legal** de bienes o mercancías en territorio nacional. Dos modalidades de emisión:
- **Tipo T (Traslado)** — el dueño traslada con medios propios. Moneda `XXX`, Subtotal/Total `0`, Receptor.Rfc = Emisor.Rfc, UsoCFDI `S01`.
- **Tipo I (Ingreso)** — transportista que cobra el flete. Con importes/impuestos; ClaveProdServ de servicio de transporte (ver CP109).

## 2. Estructura (árbol de nodos)
```
CFDI 4.0 (T o I)
└─ Complemento → cartaporte31:CartaPorte  (Version=3.1, IdCCP, TranspInternac, [TotalDistRec], [RegistroISTMO], [RegimenesAduaneros], [EntradaSalidaMerc, PaisOrigenDestino, ViaEntradaSalida])
   ├─ Ubicaciones → Ubicacion[]   (TipoUbicacion Origen/Destino, IDUbicacion, RFCRemitenteDestinatario, [DistanciaRecorrida], Domicilio)
   ├─ Mercancias  (PesoBrutoTotal, [PesoNetoTotal], UnidadPeso, NumTotalMercancias)
   │   ├─ Mercancia[]  (BienesTransp=ClaveProdServCP, Descripcion, Cantidad, ClaveUnidad, PesoEnKg, [MaterialPeligroso, CveMaterialPeligroso, Embalaje], [SectorCOFEPRIS...], [ValorMercancia, Moneda])
   │   │   ├─ DocumentacionAduanera[]   (solo TranspInternac=Sí)
   │   │   ├─ GuiasIdentificacion[]
   │   │   ├─ CantidadTransporta[]      (IDOrigen, IDDestino, Cantidad, [CvesTransporte])
   │   │   └─ DetalleMercancia          (solo Marítimo)
   │   └─ UN nodo de transporte (o varios si intermodal):
   │       ├─ Autotransporte → IdentificacionVehicular, Seguros, [Remolques[]]
   │       ├─ TransporteMaritimo → Contenedor[], [RemolqueCCP[]]
   │       ├─ TransporteAereo
   │       └─ TransporteFerroviario → DerechosDePaso[], Carro[] → Contenedor[]
   └─ FiguraTransporte → TiposFigura[]   (TipoFigura, RFCFigura/NumRegIdTrib, [NumLicencia], [Domicilio], [PartesTransporte[]])
```

## 3. Selección de modo de transporte (mutuamente excluyente, salvo intermodal)
`c_CveTransporte`: `01` Autotransporte · `02` Marítimo · `03` Aéreo · `04` Ferroviario.
- **Intermodal**: >1 nodo de transporte → obliga `CantidadTransporta:CvesTransporte` (CP180) y ClaveProdServ intermodal (CP110).
- Conteo mínimo de Ubicaciones por modo: Auto/Marítimo/Aéreo → ≥2 (1 Origen + 1 Destino, CP130). Ferroviario → ≥1 Origen + ≥5 Destino (CP128/129).

## 4. Catálogos con columna de decisión (gobiernan obligatoriedad)
Estos son chicos y su **columna extra** decide si un nodo es obligatorio/opcional/prohibido. Embébelos en la lógica; los grandes van a BD.

**c_RegimenAduanero** (col ImpoExpo) — Entrada=importación, Salida=exportación, Salida,Entrada=ambos:
`IMD` Def. importación (Entrada) · `EXD` Def. exportación (Salida) · `ITR`/`ITE` temporales import (Entrada) · `ETR`/`ETE` temporales export (Salida) · `DFI` Depósito Fiscal · `RFE` · `RFS` · `TRA` Tránsitos (los 4 últimos: Salida,Entrada).

**c_TipoDeServicio** (col Contenedor) — `1`→Carro:Contenedor obligatorio (CP192):
`TS01` Carros Ferroviarios (0) · `TS02` …intermodal (1) · `TS03` Tren unitario (0) · `TS04` Tren unitario intermodal (1).

**c_ConfigAutotransporte** (col Remolque) — `1`→Remolques obligatorio, `0,1`→opcional, `0`→omitir (CP184). Catálogo grande (config vehiculares VL/C2/C3/T3S2…), la columna Remolque es la clave.

**c_ClaveProdServCP** (col "Material peligroso") — `1` o `0,1`→ habilita Mercancia:MaterialPeligroso (CP155). Catálogo grande (miles de claves) → BD.

**c_FiguraTransporte**: `01` Operador (obliga NumLicencia, CP196; obligatorio en Autotransporte, CP194) · `02` Propietario · `03` Arrendador · `04` Notificado · `05` Integrante de Coordinados. Tipos 02/03 → obligan PartesTransporte (CP199).

**c_SectorCOFEPRIS**: `01` Medicamento · `02` Precursores/químicos uso dual · `03` Psicotrópicos/estupefacientes · `04` Sustancias tóxicas · `05` Plaguicidas/fertilizantes. Cada uno obliga un set distinto de atributos (CP159–CP163).

**c_TipoMateria**: `01` Materia prima · `02` procesada · `03` terminada · `04` industria manufacturera · `05` Otra (→ DescripcionMateria, CP171). Obligatorio si TranspInternac=Sí (CP170).

**c_DocumentoAduanero**: `01` Pedimento (estructura validada, CP174) · `02`–`20` otros (→ IdentDocAduanero, CP175). En Salida no puede ser `01` (CP173).

**c_TipoEstacion**: `01` Origen Nacional · `02` Intermedia · `03` Destino Final Nacional (solo modos 02/03/04; Autotransporte no lleva estación, CP135/140).

**c_RegistroISTMO** (Polos): `01` Coatzacoalcos I … `06` San Blas Atempa. Solo si RegistroISTMO=Sí (CP127).

**c_TipoDeTrafico** (ferroviario): `TT01` local · `TT02` interlineal remitido · `TT03` recibido · `TT04` en tránsito.

Catálogos grandes (→ BD, no embeber): `c_ClaveProdServCP`, `c_Estaciones`, `c_Colonia_*`, `c_Localidad`, `c_Municipio`, `c_ClaveUnidadPeso`, `c_MaterialPeligroso`, `c_TipoEmbalaje`, `c_TipoPermiso`, `c_ContenedorMaritimo`, `c_NumAutorizacionNaviero`, `c_CodigoTransporteAereo`, `c_SubTipoRem`, `c_ConfigMaritima`, `c_ClaveTipoCarga`, `c_DerechosDePaso`, `c_TipoCarro`, `c_Contenedor`, `c_FormaFarmaceutica`, `c_CondicionesEspeciales`, `c_ParteTransporte`.

## 5. Cuadres numéricos (validar antes de timbrar)
- `TotalDistRec` = Σ `Ubicacion:DistanciaRecorrida` (solo ubicaciones Destino). Existe solo con Auto o Ferroviario.
- `Mercancias:PesoBrutoTotal`: Auto/Aéreo/Ferroviario = Σ `Mercancia:PesoEnKg`; Marítimo = Σ `DetalleMercancia:PesoBruto`.
- `Mercancias:PesoNetoTotal`: Marítimo = Σ `DetalleMercancia:PesoNeto`; Ferroviario = Σ `Carro:ToneladasNetasCarro`.
- `NumTotalMercancias` = número de nodos `Mercancia`.
- `Carro:ToneladasNetasCarro` = Σ `Contenedor:PesoNetoMercancia` (kg→ton) si hay contenedor.

## 6. Domicilio (cascada MEX) — aplica a Ubicacion y a TiposFigura
Si Pais=`MEX`: Estado(c_Estado)→Municipio(c_Municipio)→Localidad(c_Localidad)→CodigoPostal(c_CodigoPostal)→Colonia(c_Colonia), cada nivel debe casar con el padre (CP143–147 y CP200–204). Si extranjero: texto libre (Estado solo catálogo para MEX/USA/CAN).

## 7. Flujo de captura recomendado (wizard)
Orden que minimiza recapturas (cada paso habilita el siguiente):
1. **Comprobante/Receptor** — TipoComprobante (T/I) + (si I) ClaveProdServ de transporte, impuestos. Fija aquí Moneda/Subtotal/Total por T vs I.
2. **Datos CCP** — TranspInternac, RegistroISTMO, (si internac) RegimenesAduaneros/EntradaSalidaMerc/PaisOrigenDestino/ViaEntradaSalida.
3. **Ubicaciones** — Origen(es) y Destino(s) con su mínimo por modo; Domicilio en cascada; DistanciaRecorrida en Destinos.
4. **Mercancías** — por mercancía: BienesTransp, peso, (si peligroso) CveMaterialPeligroso+Embalaje, (si COFEPRIS) set correspondiente, CantidadTransporta (IDOrigen/IDDestino válidos), (Marítimo) DetalleMercancia, (internac) DocumentacionAduanera + TipoMateria.
5. **Transporte** — el/los nodos del modo elegido con sus condicionales (Remolques, Contenedor, Carro, etc.).
6. **Figuras** — Operador(es) con NumLicencia; Propietario/Arrendador con PartesTransporte; domicilio en cascada.
7. **Revisión + cuadres** — corre la pre-validación local (sección 5 + matriz de errores) antes de enviar al PAC.

## 8. Errores frecuentes en migración / integración
- Olvidar que **T** fuerza Moneda `XXX`, totales `0`, UsoCFDI `S01`, Receptor=Emisor.
- Atributos condicionales que "no deben existir" (CP120/122/124/127/135/142/153…): enviarlos vacíos = rechazo. Hay que **omitir el nodo/atributo**, no mandarlo en blanco.
- `IdCCP`: folio único del complemento (patrón SAT), distinto del UUID del CFDI.
- Cascada de domicilio: mandar CP que no case con Estado/Municipio = CP147/204.
- Intermodal: olvidar `CvesTransporte` en CantidadTransporta (CP180).
