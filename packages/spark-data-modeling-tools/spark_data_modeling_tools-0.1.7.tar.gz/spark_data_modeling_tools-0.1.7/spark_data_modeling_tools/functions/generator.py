def normalize_data(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b)
    return s


def remove_accents_data(input_str):
    import unicodedata
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    new_str = str(nfkd_form).lower().replace(" ", "_")
    new_str = normalize_data(new_str.replace("\n", "").replace("-", "_"))
    return new_str


def dm_generated_table_refused(path_bui=None,
                               path_tables=None,
                               nro_sda=None,
                               project_name=None,
                               sprint_name=None,
                               nro_q=None,
                               scrum_master=None,
                               collaborator_dm=None,
                               comment_resolution=None,
                               comment_history=None,
                               add_dashboard_ingesta_procesamiento=None):
    import pandas as pd
    from datetime import date, datetime

    data_fuentes = pd.read_excel(path_bui, sheet_name='ID Fuentes (Source)', skiprows=[0, 1], dtype=str)
    data_columns = [f"f_{remove_accents_data(col)}" for col in list(data_fuentes.columns)]
    data_fuentes.columns = data_columns
    data_fuentes['f_id2'] = data_fuentes['f_id'].astype(float)

    data_fuentes["f_master_registrado_en_el_tablero_ingesta"] = data_fuentes["f_master_registrado_en_el_tablero_ingesta"].str.split('/').str[-1]
    data_fuentes['f_master_registrado_en_el_tablero_ingesta'] = data_fuentes['f_master_registrado_en_el_tablero_ingesta'].str.lower()
    data_fuentes['f_master_registrado_en_el_tablero_ingesta'] = data_fuentes['f_master_registrado_en_el_tablero_ingesta'].str.strip()
    data_fuentes = data_fuentes[(data_fuentes['f_master_registrado_en_el_tablero_ingesta'].notna()) &
                                (data_fuentes['f_master_registrado_en_el_tablero_ingesta'].notnull())]
    data_fuentes['f_descripcion_de_la_tds'] = data_fuentes['f_descripcion_de_la_tds'].str.lower()
    data_fuentes['f_descripcion_de_la_tds'] = data_fuentes['f_descripcion_de_la_tds'].str.strip()
    data_fuentes2 = data_fuentes[['f_id', 'f_id2', 'f_descripcion_de_la_tds', 'f_fuente_tds',
                                  'f_fuente_origen', 'f_periodicidad', 'f_status', 'f_tipología',
                                  'f_deuda_de_dictamen_o_sustento_tds', 'f_master_registrado_en_el_tablero_ingesta',
                                  'f_comentarios_deuda_de_dictamen_o_sustento_tds']]
    data_fuentes2 = data_fuentes2.sort_values(by="f_id2", ascending=False)
    with open(path_tables) as f:
        tables_lines = [line.rstrip('\n') for line in f]
    data_fuentes3 = data_fuentes2[data_fuentes2["f_master_registrado_en_el_tablero_ingesta"].isin(tables_lines)]
    data_fuentes4 = data_fuentes3.drop_duplicates(["f_master_registrado_en_el_tablero_ingesta"])

    data_bui = pd.read_excel(path_bui, sheet_name='Base única de Ingesta (BUI)', skiprows=[0, 1], dtype=str)
    data_bui_columns_original = [remove_accents_data(col) for col in list(data_bui.columns)]
    data_bui_columns = [f"b_{remove_accents_data(col)}" for col in list(data_bui.columns)]
    data_bui.columns = data_bui_columns
    data_bui['b_resolucion'] = data_bui['b_resolucion'].str.lower()
    data_bui['b_resolucion'] = data_bui['b_resolucion'].str.strip()
    data_bui2 = data_bui[data_bui['b_resolucion'].str.contains('se ingesta tabla dictaminada', regex=True, na=True)]
    data_bui3 = data_bui2[['b_#folio', 'b_resolucion', 'b_tipo', 'b_id', 'b_nombre_tabla_o_descarga_(si_existiera)']]
    data_bui4 = data_bui3.drop_duplicates(["b_id"])

    data_join = data_fuentes4.merge(data_bui4, left_on=['f_id'], right_on=['b_id'], how='left')
    data_join.drop(['f_id2', 'f_fuente_origen', 'b_id'], axis=1, inplace=True)

    project_sda = f"{nro_sda}-{project_name}"
    year = date.today().year
    anio_sprint = f"{nro_q}-{year}-{sprint_name}"
    comment_resolution = f"{date.today()} {comment_resolution}"
    comment_history = f"{date.today()} {comment_history}"

    frame = pd.DataFrame(columns=data_bui_columns_original)
    frame["#folio"] = " "
    frame["nombre_tabla,_fichero_o_concepto_original"] = data_join["f_fuente_tds"]
    frame["descripcion_tabla,_fichero_o_concepto_original"] = data_join["f_descripcion_de_la_tds"]
    frame["sdatool_nombre_proyecto"] = str(project_sda)
    frame["historico_solicitado_(meses)"] = "0"
    frame["periodicidad_solicitada"] = data_join["f_periodicidad"]
    frame["q_año_sp_de_registro_folio"] = str(anio_sprint)
    frame["fecha_de_registro_folio"] = str(date.today().strftime("%d/%m/%Y"))
    frame["estatus_resolucion"] = "En proceso"
    frame["analista_del_proyecto_que_realizo_el_dictamen"] = str(scrum_master)
    frame["colaborador_core_data_que_aprobo_el_dictamen"] = str(collaborator_dm)
    frame["resolucion"] = str("Se atendió con otro folio")
    frame["fecha_de_cierre_de_dictamen"] = str(date.today().strftime("%d/%m/%Y"))
    frame["#_folio_(si_se_atiende_con_otro_folio_o_ya_esta_ingestado)"] = data_join["b_#folio"]
    frame["comentario_resolucion"] = str(comment_resolution)
    frame["tipo"] = data_join["b_tipo"]
    frame["id"] = data_join["f_id"]
    frame["nombre_tabla_o_descarga_(si_existiera)"] = data_join["f_master_registrado_en_el_tablero_ingesta"]
    frame["#_campos_ingestados"] = "0"
    frame["historia_a_ingestar(período:_desde___hasta)"] = str("No requiere")
    frame["comentarios_/_depuracion_y/o_ruta_de_historia"] = str(comment_history)
    frame["persistencia_destino"] = "Datio"
    frame["q_año_sp_de_cierre_de_dictamen"] = str(anio_sprint)
    frame["pasa_a_dashboard_de_ingesta/procesam."] = str(add_dashboard_ingesta_procesamiento)
    frame["fecha_pase_a_dashboard_de_ingesta/procesam."] = str(datetime.now().strftime("%d/%m/%Y %H:%M"))
    frame["comentarios_generales(colocar_fecha_del_comentario)ver_excepcion"] = " "
    frame["sdatool"] = f"SDATOOL-{nro_sda}"
    frame["catálogo_dictaminado"] = " "
    frame["valida_tds_dictaminada_(no_descentralizado)"] = " "
    frame["status_table"] = data_join["f_status"]
    frame["tipologia_table"] = data_join["f_tipología"]
    frame["deuda_sustento_table"] = data_join["f_deuda_de_dictamen_o_sustento_tds"]
    frame["comentarios_deuda_de_dictamen_o_sustento_tds"] = data_join["f_comentarios_deuda_de_dictamen_o_sustento_tds"]

    frame.to_excel('BUIv2.xlsx', sheet_name='Base única de Ingesta (BUI)', index=False)
