#Codigo complemetar_clientes()

def complementar_clientes(self):

            print("\n" + "=" * 80)
            print("[START] INICIANDO complementar_clientes")
            print("=" * 80)

            ruta_cliente = os.path.join(self.rutaSalida, "Cliente.csv")
            if not os.path.exists(ruta_cliente):
                print(f"[!] No existe el archivo Cliente.csv: {ruta_cliente}")
                return None

            try:
                dfc = pd.read_csv(ruta_cliente, sep=";", dtype=str, encoding="utf-8")
                print(f"[OK] Cliente.csv cargado | Filas: {len(dfc)}")
            except Exception as e:
                print(f"[X] Error al cargar Cliente.csv: {e}")
                return None

            PROMOTORAS = {
                "Arrendamiento Bogota": "2607",
                "A-Seguro": "2604",
                "Berrocal": "0003",
                "Bolivariana": "2597",
                "Business Partner": "0028",
                "Cabecera": "2629",
                "Cartago": "2634",
                "Chicamocha": "2630",
                "Enfoque": "2599",
                "Gestionarte": "2612",
                "Metropolitana": "2600",
                "Milan": "2638",
                "Panamericana": "2536",
                "Pena Clausen": "2615",
                "Piedra Pintada": "2645",
                "Poblado": "2598",
                "Programacion Administracion Seguros": "2617",
                "Prollano": "2620",
                "Prosear Seguros": "2608",
                "Samur Barranquilla": "2626",
                "Samur Cartagena": "2633",
                "Sevillas": "2632",
                "SotoMayor": "2631",
                "Su Aliado": "2614",
                "Torres Sierra": "2619",
                "VenSer": "2603",
                "Villaser": "4802",
                "Sigma": "2601",
            }

            cod_oficina_actual = PROMOTORAS.get(self.promotora, "")
            print(f" Promotora: {self.promotora} | CodOficina: {cod_oficina_actual}")

            ruta_busqueda = self.build_path("Datos", "seguros", "Produccion")
            if not os.path.exists(ruta_busqueda):
                print(f"[!] No existe la ruta de Producción histrica: {ruta_busqueda}")
                return dfc

            archivos_encontrados = []
            for raiz, _, archivos in os.walk(ruta_busqueda):
                for archivo in archivos:
                    if archivo.startswith("~$"):
                        continue
                    if archivo.lower().endswith((".xlsx", ".xls", ".csv")):
                        archivos_encontrados.append(os.path.join(raiz, archivo))

            if not archivos_encontrados:
                print(f"[!] No se encontraron archivos en Producción histrica: {ruta_busqueda}")
                return dfc

            def prioridad_archivo(ruta):
                nombre = os.path.basename(ruta).lower()
                for y in range(2035, 1999, -1):
                    if str(y) in nombre:
                        return -y
                return 0

            archivos_encontrados = sorted(archivos_encontrados, key=prioridad_archivo)
            print(f" Archivos de produccin encontrados: {len(archivos_encontrados)}")

            # ============================================================
            # FUENTE ADICIONAL: Informes.parquet
            # ============================================================
            ruta_informes_parquet = os.path.join(self.rutaSalida, "Informes.parquet")

            if os.path.exists(ruta_informes_parquet):
                print(f" Informes.parquet encontrado: {ruta_informes_parquet}")
            else:
                print(f"[!] La promotora {self.promotora} no tiene Informes.parquet")

            # FIX #1: Listas solo en ASCII (sin tildes).
            # Los nombres de columna se normalizarn a ASCII justo después de leer cada archivo,
            # por eso ya no necesitamos variantes con tilde aqu.
            posibles_cod = [  # CodCliente
                "Tomador Numero de Identificacion",  # 2025 / 2026
                "Tomador Numero ID",
                "CodCliente",
                "Cliente Numero ID",   # 2019 / 2022 / 2023 (llega como "N?mero" sin normalizar)
            ]

            posibles_nom = [  # Cliente
                "Tomador Nombre",          # 2025 / 2026
                "Cliente Nombre Completo", # 2019 / 2022 / 2023
                "Nombre Cliente",
                "Cliente",
                "Tomador",
            ]

            posibles_cod_agente = [  # CodAgente
                "Agente Lider Redir Codigo_Op",      # 2025 / 2026
                "Agente Lider Act Codigo Agente",    # 2019 / 2020 / 2023
                "Agente Lider Redir Codigo Op",      # variante sin guion bajo
                "CodAgente",
            ]

            lista_produccion = []

            # ============================================================
            # FUENTE ADICIONAL: Informes.parquet
            # ============================================================
            ruta_informes_parquet = os.path.join(self.rutaSalida, "Informes.parquet")

            if os.path.exists(ruta_informes_parquet):
                try:
                    df_inf = pd.read_parquet(ruta_informes_parquet)

                    if df_inf.empty:
                        print(f"[!] Informes.parquet est vaco para {self.promotora}")
                    else:
                        df_inf.columns = [
                            unicodedata.normalize('NFKD', str(c)).encode('ascii', 'ignore').decode('ascii').strip()
                            for c in df_inf.columns
                        ]

                        posibles_cod_inf = [
                            "Tomador Numero de Identificacion",
                            "Tomador Numero ID",
                            "CodCliente",
                            "Cliente Numero ID",
                        ]

                        posibles_nom_inf = [
                            "Tomador Nombre",
                            "Cliente Nombre Completo",
                            "Nombre Cliente",
                            "Cliente",
                            "Tomador",
                        ]

                        posibles_cod_agente_inf = [
                            "Agente Lider Redir Codigo_Op",
                            "Agente Lider Act Codigo Agente",
                            "Agente Lider Redir Codigo Op",
                            "CodAgente",
                            "CodAgentes",
                        ]

                        col_cod_inf = next((c for c in posibles_cod_inf if c in df_inf.columns), None)
                        col_nom_inf = next((c for c in posibles_nom_inf if c in df_inf.columns), None)
                        col_agente_inf = next((c for c in posibles_cod_agente_inf if c in df_inf.columns), None)

                        if not col_cod_inf or not col_nom_inf or not col_agente_inf:
                            print(f"[!] Informes.parquet no tiene las columnas necesarias para {self.promotora}")
                            print(f"Columnas disponibles: {list(df_inf.columns)}")
                        else:
                            df_temp_inf = df_inf[[col_cod_inf, col_nom_inf, col_agente_inf]].copy()
                            df_temp_inf.columns = ["CodCliente", "Cliente", "CodAgentes"]

                            df_temp_inf["CodCliente"] = df_temp_inf["CodCliente"].astype(str).str.extract(r"(\d+)", expand=False)
                            df_temp_inf["CodCliente"] = df_temp_inf["CodCliente"].astype(str).str.strip()
                            df_temp_inf["CodAgentes"] = df_temp_inf["CodAgentes"].astype(str).str.strip()
                            df_temp_inf["Cliente"] = df_temp_inf["Cliente"].astype(str).str.strip().str.title()

                            df_temp_inf["Carpeta"] = "Informes"
                            df_temp_inf["Ruta"] = ruta_informes_parquet
                            df_temp_inf["CodOficina"] = (
                                df_inf["CodOficina"].astype(str).str.strip()
                                if "CodOficina" in df_inf.columns
                                else cod_oficina_actual
                            )
                            df_temp_inf["Archivo"] = "Informes.parquet"
                            df_temp_inf["CodOficinaU"] = (
                                df_inf["CodOficinaU"].astype(str).str.strip()
                                if "CodOficinaU" in df_inf.columns
                                else (
                                    df_temp_inf["CodOficina"].astype(str).str.strip()
                                    + df_temp_inf["CodAgentes"].astype(str).str.strip()
                                )
                            )
                            df_temp_inf["CodCiudad"] = (
                                df_inf["CodCiudad"].astype(str).str.strip()
                                if "CodCiudad" in df_inf.columns
                                else ""
                            )

                            df_temp_inf = df_temp_inf[
                                df_temp_inf["CodCliente"].notna()
                                & (df_temp_inf["CodCliente"] != "")
                                & df_temp_inf["Cliente"].notna()
                                & (df_temp_inf["Cliente"] != "")
                                & (df_temp_inf["Cliente"].str.lower() != "nan")
                                & df_temp_inf["CodAgentes"].notna()
                                & (df_temp_inf["CodAgentes"] != "")
                                & (df_temp_inf["CodAgentes"].str.lower() != "nan")
                            ].copy()

                            if not df_temp_inf.empty:
                                filas_antes_dedup_inf = len(df_temp_inf)

                                df_temp_inf = df_temp_inf.drop_duplicates(
                                    subset=["CodCliente", "CodAgentes"]
                                )

                                filas_despues_dedup_inf = len(df_temp_inf)

                                lista_produccion.append(df_temp_inf)

                                print(f"[OK] Informes.parquet procesado para {self.promotora}")
                                print(f" Informes.parquet: {filas_antes_dedup_inf} filas útiles extraídas inicialmente.")
                                print(f" Informes.parquet: {filas_despues_dedup_inf} filas después de deduplicar.")
                            else:
                                print(f"[!] Informes.parquet no dej filas útiles para {self.promotora}")

                except Exception as e:
                    print(f"[!] Error leyendo Informes.parquet para {self.promotora}: {e}")

            else:
                print(f"[!] La promotora {self.promotora} no tiene Informes.parquet")

            for ruta_archivo in archivos_encontrados:
                archivo = os.path.basename(ruta_archivo)

                try:
                    if archivo.lower().endswith(".csv"):
                        df_hist = pd.read_csv(
                            ruta_archivo,
                            sep=None,
                            engine="python",
                            dtype=str,
                            encoding="utf-8",
                        )
                    else:
                        # FIX A: Detectar la fila real del encabezado.
                        # Algunos xlsx tienen filas de filtro/titulo antes de los datos
                        # (ej. 2025/2026 de Sigma tienen 2 filas extra al inicio).
                        # Probamos primero con header=0; si ninguna columna conocida aparece,
                        # escaneamos las primeras filas para encontrar el header real.
                        _todas_conocidas = (
                            set(posibles_cod) | set(posibles_nom) | set(posibles_cod_agente)
                        )

                        def _normalizar(c):
                            return unicodedata.normalize('NFKD', str(c)).encode('ascii', 'ignore').decode('ascii').strip()

                        def _tiene_cols(df_):
                            cols_norm = {_normalizar(c) for c in df_.columns}
                            return bool(cols_norm & _todas_conocidas)

                        df_hist = pd.read_excel(ruta_archivo, dtype=str, header=0)
                        if not _tiene_cols(df_hist):
                            # Escanear las primeras 15 filas buscando el header real
                            df_raw = pd.read_excel(ruta_archivo, header=None, nrows=15, dtype=str)
                            fila_header = None
                            for fila_idx in range(len(df_raw)):
                                candidatos = {_normalizar(str(v)) for v in df_raw.iloc[fila_idx].tolist()}
                                if candidatos & _todas_conocidas:
                                    fila_header = fila_idx
                                    break
                            if fila_header is not None:
                                df_hist = pd.read_excel(ruta_archivo, dtype=str, header=fila_header)
                                print(f" {archivo}: encabezado detectado en fila {fila_header}")
                            else:
                                print(f"[!] {archivo}: no se encontr fila de encabezado vlida")
                                continue
                except Exception as e:
                    print(f"[!] Error leyendo {archivo}: {e}")
                    continue

                if df_hist.empty:
                    continue

                # FIX #1: Normalizar columnas a ASCII para que tildes/caracteres rotos no impidan el match
                df_hist.columns = [
                    unicodedata.normalize('NFKD', str(c)).encode('ascii', 'ignore').decode('ascii').strip()
                    for c in df_hist.columns
                ]

                col_cod = next((c for c in posibles_cod if c in df_hist.columns), None)
                col_nom = next((c for c in posibles_nom if c in df_hist.columns), None)
                col_agente = next((c for c in posibles_cod_agente if c in df_hist.columns), None)

                if not col_cod or not col_nom or not col_agente:
                    continue

                print(f"  -> Columnas encontradas: Codigo='{col_cod}', Nombre='{col_nom}', Agente='{col_agente}'")

                df_temp = df_hist[[col_cod, col_nom, col_agente]].copy()
                df_temp.columns = ["CodCliente", "Cliente", "CodAgentes"]

                df_temp["CodCliente"] = df_temp["CodCliente"].astype(str).str.extract(r"(\d+)", expand=False)
                df_temp["CodCliente"] = df_temp["CodCliente"].astype(str).str.strip()
                df_temp["CodAgentes"] = df_temp["CodAgentes"].astype(str).str.strip()
                df_temp["Cliente"] = df_temp["Cliente"].astype(str).str.strip().str.title()

                print(f"[OK] {archivo}: columnas detectadas y limpiadas correctamente")

                # ===== CAMBIOS PARA COMPLEMENTAR CLIENTES =====
                df_temp["Carpeta"] = (
                    df_hist["Carpeta"].astype(str).str.strip()
                    if "Carpeta" in df_hist.columns
                    else "Produccion"
                )
                df_temp["Ruta"] = (
                    df_hist["Ruta"].astype(str).str.strip()
                    if "Ruta" in df_hist.columns
                    else ruta_archivo
                )
                df_temp["CodOficina"] = (
                    df_hist["CodOficina"].astype(str).str.strip()
                    if "CodOficina" in df_hist.columns
                    else cod_oficina_actual
                )
                df_temp["Archivo"] = (
                    df_hist["Archivo"].astype(str).str.strip()
                    if "Archivo" in df_hist.columns
                    else archivo
                )
                df_temp["CodOficinaU"] = (
                    df_hist["CodOficinaU"].astype(str).str.strip()
                    if "CodOficinaU" in df_hist.columns
                    else (
                        df_temp["CodOficina"].astype(str).str.strip()
                        + df_temp["CodAgentes"].astype(str).str.strip()
                    )
                )
                df_temp["CodCiudad"] = (
                    df_hist["CodCiudad"].astype(str).str.strip()
                    if "CodCiudad" in df_hist.columns
                    else ""
                )
                # ===== FIN CAMBIOS PARA COMPLEMENTAR CLIENTES =====

                df_temp = df_temp[
                    df_temp["CodCliente"].notna()
                    & (df_temp["CodCliente"] != "")
                    & df_temp["Cliente"].notna()
                    & (df_temp["Cliente"] != "")
                    & (df_temp["Cliente"].str.lower() != "nan")
                    & df_temp["CodAgentes"].notna()
                    & (df_temp["CodAgentes"] != "")
                    & (df_temp["CodAgentes"].str.lower() != "nan")
                ].copy()

                if df_temp.empty:
                    continue

                # FIX #2: Deduplicar por CodCliente+CodAgentes priorizando la fila ms completa
                filas_antes_dedup = len(df_temp)

                df_temp["_tiene_nombre"] = (
                    df_temp["Cliente"].fillna("").astype(str).str.strip().ne("")
                    & df_temp["Cliente"].fillna("").astype(str).str.lower().ne("nan")
                )

                df_temp["_metadata_score"] = 0
                for col in ["Archivo", "CodOficinaU", "CodCiudad", "Ruta", "CodOficina"]:
                    if col in df_temp.columns:
                        df_temp["_metadata_score"] += (
                            df_temp[col].fillna("").astype(str).str.strip().ne("")
                        ).astype(int)

                df_temp = df_temp.sort_values(
                    by=["CodCliente", "CodAgentes", "_tiene_nombre", "_metadata_score"],
                    ascending=[True, True, False, False]
                )

                df_temp = df_temp.drop_duplicates(
                    subset=["CodCliente", "CodAgentes"],
                    keep="first"
                )

                df_temp.drop(columns=["_tiene_nombre", "_metadata_score"], inplace=True, errors="ignore")

                filas_despues_dedup = len(df_temp)

                lista_produccion.append(df_temp)
                print(f" {archivo}: {filas_antes_dedup} filas útiles extraídas inicialmente.")
                print(f" {archivo}: {filas_despues_dedup} filas después de deduplicar internamente (CodCliente+CodAgentes).")
                print(f"[OK] {archivo}: procesado exitosamente")

            if not lista_produccion:
                print("[!] No se encontraron pares CodCliente-Cliente-CodAgente en Producción histrica")
                return dfc

            df_prod_clientes = pd.concat(lista_produccion, ignore_index=True) 
            
            df_prod_clientes["_tiene_nombre"] = (
                df_prod_clientes["Cliente"].fillna("").astype(str).str.strip().ne("")
                & df_prod_clientes["Cliente"].fillna("").astype(str).str.lower().ne("nan")
                )

            df_prod_clientes["_metadata_score"] = 0
            for col in ["Archivo", "CodOficinaU", "CodCiudad", "Ruta", "CodOficina"]:
                if col in df_prod_clientes.columns:
                    df_prod_clientes["_metadata_score"] += (
                        df_prod_clientes[col].fillna("").astype(str).str.strip().ne("")
                    ).astype(int)

            df_prod_clientes = df_prod_clientes.sort_values(
                by=["CodCliente", "CodAgentes", "_tiene_nombre", "_metadata_score"],
                ascending=[True, True, False, False]
            )        
            # FIX #2: Deduplicar histrico por CodCliente+CodAgentes
            df_prod_clientes = df_prod_clientes.drop_duplicates(
                subset=["CodCliente", "CodAgentes"],
                keep="first"
            )
            print(f"[OK] Filas nicas desde Producción: {len(df_prod_clientes)}")
            cols_demo = [c for c in ["CodCliente", "Cliente", "CodAgentes", "Archivo", "CodOficinaU", "CodCiudad"] if c in df_prod_clientes.columns]
            print("[DATA] Primeras filas de df_prod_clientes:")
            print(df_prod_clientes[cols_demo].head(5))

            def _count_valid(series):
                return series.fillna("").astype(str).str.strip().replace({"nan": "", "None": ""}).ne("").sum()

            print(
                f"[OK] Valores de produccin antes de unir: Archivo={_count_valid(df_prod_clientes['Archivo'])}, "
                f"CodOficinaU={_count_valid(df_prod_clientes['CodOficinaU'])}, "
                f"CodCiudad={_count_valid(df_prod_clientes['CodCiudad'])}"
            )

            columnas_necesarias = [
                "CodAgentes", "Cliente", "CodCliente", "Carpeta", "Ruta", "CodOficina"
            ]
            columnas_obligatorias = ["Archivo", "CodOficinaU", "CodCiudad"]

            # Conservar todas las columnas originales y garantizar las obligatorias.
            columnas_entrada = list(dfc.columns)
            for col in columnas_obligatorias:
                if col not in columnas_entrada:
                    columnas_entrada.append(col)

            for col in columnas_necesarias + columnas_obligatorias:
                if col not in dfc.columns:
                    dfc[col] = ""

            dfc["CodCliente"] = dfc["CodCliente"].astype(str).str.extract(r"(\d+)", expand=False)
            dfc["CodCliente"] = dfc["CodCliente"].astype(str).str.strip()
            dfc["Cliente"] = dfc["Cliente"].astype(str).str.strip().str.title()
            if "CodAgentes" in dfc.columns:
                dfc["CodAgentes"] = dfc["CodAgentes"].astype(str).str.strip()

            dfc_base = dfc.copy()

            # Traer las columnas originales de dfc al dataframe de produccin si existen.
            columnas_adicionales = [col for col in columnas_entrada if col not in columnas_necesarias]
            if columnas_adicionales:
                df_prod_clientes = df_prod_clientes.merge(
                    dfc_base[["CodCliente", "Cliente", "CodAgentes"] + columnas_adicionales].drop_duplicates(
                        subset=["CodCliente", "Cliente", "CodAgentes"]
                    ),
                    on=["CodCliente", "Cliente", "CodAgentes"],
                    how="left",
                    suffixes=("", "_orig")
                )
                for col in columnas_adicionales:
                    orig_col = f"{col}_orig"
                    if orig_col in df_prod_clientes.columns:
                        df_prod_clientes[col] = df_prod_clientes[col].fillna(df_prod_clientes[orig_col])
                        df_prod_clientes.drop(columns=[orig_col], inplace=True, errors="ignore")

            for col in columnas_entrada:
                if col not in df_prod_clientes.columns:
                    df_prod_clientes[col] = ""

            dfc_base["_source"] = 0
            df_prod_clientes["_source"] = 1

            # === ANTES DE CONCAT: Mostrar columnas ===
            print("\n" + "=" * 80)
            print("[DATA] ANLISIS DE COLUMNNAS ANTES DE CONCAT")
            print("=" * 80)
            print(f"\n[OK] dfc_base columnas ({len(dfc_base.columns)}): {list(dfc_base.columns)}")
            print(f"\n[OK] df_prod_clientes columnas DISPONIBLES ({len(df_prod_clientes.columns)}): {list(df_prod_clientes.columns)}")
            print(f"\n columnas_entrada ESPERADAS ({len(columnas_entrada)}): {columnas_entrada}")
            
            # Verificar qu columnas faltan en df_prod_clientes
            columnas_faltantes = [col for col in columnas_entrada if col not in df_prod_clientes.columns]
            if columnas_faltantes:
                print(f"\n[!]  COLUMNAS FALTANTES en df_prod_clientes: {columnas_faltantes}")
            else:
                print(f"\n[OK] Todas las columnas esperadas están en df_prod_clientes")

            # Usar reindex para garantizar que ambos DataFrames tengan exactamente las mismas columnas
            cols_para_concat = columnas_entrada + ["_source"]
            
            # Asegurar que df_prod_clientes tiene todas las columnas (rellenar con "" si falta)
            df_prod_clientes = df_prod_clientes.reindex(columns=cols_para_concat, fill_value="")
            
            print(f"\n[OK] df_prod_clientes después de reindex ({len(df_prod_clientes.columns)}): {list(df_prod_clientes.columns)}")
            print("=" * 80 + "\n")

            # ============================================================
            # NUEVA ESTRATEGIA:
            # Cliente.csv ya viene completo.
            # Solo agregamos combinaciones nuevas desde Producción histrica + Informes.parquet
            # y deduplicamos por CodCliente + CodAgentes.
            # ============================================================

            filas_base_antes = len(dfc_base)
            filas_nuevas_fuente = len(df_prod_clientes)

            print(f"[OK] Filas originales en Cliente.csv: {filas_base_antes}")
            print(f"[OK] Filas candidatas desde Producción/Informes.parquet: {filas_nuevas_fuente}")

            df_clientes_final = pd.concat(
                [dfc_base, df_prod_clientes],
                ignore_index=True,
                sort=False
            )

            filas_antes_dedup_final = len(df_clientes_final)

            df_clientes_final = df_clientes_final[
                df_clientes_final["CodCliente"].notna()
                & (df_clientes_final["CodCliente"].astype(str).str.strip() != "")
                & df_clientes_final["Cliente"].notna()
                & (df_clientes_final["Cliente"].astype(str).str.strip() != "")
                & (df_clientes_final["Cliente"].astype(str).str.strip().str.lower() != "nan")
                & df_clientes_final["CodAgentes"].notna()
                & (df_clientes_final["CodAgentes"].astype(str).str.strip() != "")
                & (df_clientes_final["CodAgentes"].astype(str).str.strip().str.lower() != "nan")
            ].copy()

            df_clientes_final["_tiene_nombre"] = (
                df_clientes_final["Cliente"].fillna("").astype(str).str.strip().ne("")
                & df_clientes_final["Cliente"].fillna("").astype(str).str.lower().ne("nan")
            )

            df_clientes_final["_metadata_score"] = 0
            for col in ["Archivo", "CodOficinaU", "CodCiudad", "Ruta", "CodOficina"]:
                if col in df_clientes_final.columns:
                    df_clientes_final["_metadata_score"] += (
                        df_clientes_final[col].fillna("").astype(str).str.strip().ne("")
                    ).astype(int)

            df_clientes_final = df_clientes_final.sort_values(
                by=["CodCliente", "CodAgentes", "_tiene_nombre", "_metadata_score", "_source"],
                ascending=[True, True, False, False, False]
            )

            df_clientes_final = df_clientes_final.drop_duplicates(
                subset=["CodCliente", "CodAgentes"],
                keep="first"
            )

            filas_despues_dedup_final = len(df_clientes_final)
            filas_agregadas = filas_despues_dedup_final - filas_base_antes

            df_clientes_final.drop(
                columns=["_source", "_invalid_agente", "_metadata_score", "_tiene_nombre"],
                inplace=True,
                errors="ignore"
            )

            print(f"[OK] Filas antes de deduplicación final: {filas_antes_dedup_final}")
            print(f"[OK] Filas después de deduplicación final: {filas_despues_dedup_final}")
            print(f"[OK] Nuevas combinaciones CodCliente+CodAgentes agregadas: {filas_agregadas}")

            def count_valid_non_blank(series):
                if series.name not in df_clientes_final.columns:
                    return 0
                cleaned = series.fillna("").astype(str).str.strip().replace({"nan": "", "None": ""})
                return cleaned.ne("").sum()

            num_archivo = count_valid_non_blank(df_clientes_final["Archivo"]) if "Archivo" in df_clientes_final.columns else 0
            num_cod_oficina_u = count_valid_non_blank(df_clientes_final["CodOficinaU"]) if "CodOficinaU" in df_clientes_final.columns else 0
            num_cod_ciudad = count_valid_non_blank(df_clientes_final["CodCiudad"]) if "CodCiudad" in df_clientes_final.columns else 0

            num_archivo_orig = count_valid_non_blank(dfc_base["Archivo"]) if "Archivo" in dfc_base.columns else 0
            num_cod_oficina_u_orig = count_valid_non_blank(dfc_base["CodOficinaU"]) if "CodOficinaU" in dfc_base.columns else 0
            num_cod_ciudad_orig = count_valid_non_blank(dfc_base["CodCiudad"]) if "CodCiudad" in dfc_base.columns else 0

            print(f"[OK] Filas finales después de unir y quitar duplicados: {len(df_clientes_final)}")
            print(f"[OK] Valores originales en Cliente.csv: Archivo={num_archivo_orig}, CodOficinaU={num_cod_oficina_u_orig}, CodCiudad={num_cod_ciudad_orig}")
            print(f"[OK] Valores conservados en salida: Archivo={num_archivo}, CodOficinaU={num_cod_oficina_u}, CodCiudad={num_cod_ciudad}")

            # === DESPUS DEL PROCESAMIENTO: Mostrar columnas finales ===
            print("\n" + "=" * 80)
            print("[DATA] ANLISIS DE COLUMNAS DESPUS DEL PROCESAMIENTO")
            print("=" * 80)
            print(f"\n[OK] df_clientes_final columnas FINALES ({len(df_clientes_final.columns)}): \n{list(df_clientes_final.columns)}")
            print(f"\n Cambio de columnas: {len(columnas_entrada)} esperadas  {len(df_clientes_final.columns)} finales")
            print("=" * 80 + "\n")

            ruta_cliente_actualizado = os.path.join(self.rutaSalida, "Cliente.csv")
            df_clientes_final.to_csv(ruta_cliente_actualizado, sep=";", encoding="utf-8", index=False)

            # === VERIFICACIN FINAL: Releer el archivo para confirmar columnas ===
            print("\n" + "=" * 80)
            print("[OK] VERIFICACIN FINAL DEL ARCHIVO EXPORTADO")
            print("=" * 80)
            df_verificacion = pd.read_csv(ruta_cliente_actualizado, sep=";", dtype=str, encoding="utf-8", nrows=0)
            print(f"\n[OK] Cliente.csv EXPORTADO contiene ({len(df_verificacion.columns)}) columnas:")
            print(f"{list(df_verificacion.columns)}")
            print(f"\n[DATA] Primera fila de datos (muestra):")
            df_muestra = pd.read_csv(ruta_cliente_actualizado, sep=";", dtype=str, encoding="utf-8", nrows=3)
            print(df_muestra.to_string())
            print("=" * 80 + "\n")

            print(f"[OK] Archivo Cliente.csv actualizado y guardado en: {ruta_cliente_actualizado}")
            print("=" * 80 + "\n")

            return df_clientes_final


