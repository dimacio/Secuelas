# Secuelas/evaluation.py

def _normalize_row(row_dict, column_names_ordered):
    """
    Convierte una fila de diccionario a una tupla de valores en el orden especificado
    por column_names_ordered. Maneja valores None consistentemente.
    """
    if not isinstance(row_dict, dict):
        # Podría ser una tupla/lista si SQLAlchemy devuelve eso directamente
        # bajo ciertas circunstancias, aunque usualmente es un RowProxy que se comporta como dict.
        # Para estar seguros, si no es un dict, intentamos usarlo como una secuencia.
        # Esto es menos robusto que esperar siempre dicts.
        return tuple(row_dict) if hasattr(row_dict, '__iter__') else tuple()

    return tuple(row_dict.get(col_name) for col_name in column_names_ordered)

def compare_results(user_results, user_columns, correct_results, correct_columns, eval_options):
    """
    Compara los resultados de la consulta del usuario con los resultados correctos.
    Devuelve (bool_es_correcto, mensaje_string)
    """
    user_results = user_results or []
    correct_results = correct_results or []
    user_columns_processed = [str(c).lower() for c in (user_columns or [])] # Nombres de columna a minúsculas
    correct_columns_processed = [str(c).lower() for c in (correct_columns or [])]

    # 1. Comprobar nombres de columnas (si es necesario)
    if eval_options.get('check_column_names', True):
        if eval_options.get('column_order_matters', True):
            if user_columns_processed != correct_columns_processed:
                return False, f"Error: Los nombres o el orden de las columnas no coinciden. Se esperaba: {correct_columns}, Resultado: {user_columns}"
        else:  # El orden de las columnas no importa, pero los nombres deben coincidir
            if set(user_columns_processed) != set(correct_columns_processed):
                # Proporcionar más detalles sobre qué columnas faltan o sobran
                missing_in_user = set(correct_columns_processed) - set(user_columns_processed)
                extra_in_user = set(user_columns_processed) - set(correct_columns_processed)
                error_msg = "Error: El conjunto de nombres de columna no coincide."
                if missing_in_user:
                    error_msg += f" Faltan columnas en tu resultado: {missing_in_user}."
                if extra_in_user:
                    error_msg += f" Hay columnas adicionales en tu resultado: {extra_in_user}."
                return False, error_msg
    
    # Usar correct_columns_processed como el orden canónico para la comparación de datos
    # si check_column_names es falso, o si el orden de columnas del usuario no importa pero los nombres sí.
    # Si el orden de columnas del usuario importa y los nombres también, ya se validó arriba.
    # Si los nombres de las columnas no importan en absoluto (raro, pero posible), la comparación de datos es más compleja.
    # Por ahora, asumimos que si check_column_names es True, correct_columns_processed es la referencia.
    # Si check_column_names es False, la comparación de datos es inherentemente más ambigua sin un mapeo.
    # Para este juego, es probable que check_column_names sea casi siempre True.

    # Normalizar filas a tuplas para comparación, usando el orden de correct_columns_processed
    try:
        # Asegurarse de que las filas del usuario se normalizan usando el orden de las columnas correctas,
        # especialmente si el orden de las columnas del usuario no importaba pero los nombres sí.
        # Si los nombres de las columnas del usuario eran diferentes y check_column_names era False, esto fallaría.
        # Asumimos que si check_column_names es True, las columnas del usuario (potencialmente reordenadas) coinciden con las correctas.
        
        # Para la normalización de user_results, necesitamos usar user_columns para extraer los datos
        # y luego, si column_order_matters es False, reordenarlos según correct_columns.
        # Si column_order_matters es True, user_columns ya debe ser igual a correct_columns.

        # Normalizamos los datos del usuario según SUS PROPIAS columnas primero.
        temp_user_data_tuples = []
        for row in user_results:
            # Convertir RowProxy a dict si es necesario, o manejarlo directamente
            row_dict = row if isinstance(row, dict) else dict(row._mapping if hasattr(row, '_mapping') else row)
            temp_user_data_tuples.append(tuple(row_dict.get(str(col).lower()) for col in user_columns))

        # Si el orden de las columnas del usuario no importa pero los nombres sí,
        # necesitamos remapear las tuplas del usuario al orden de las columnas correctas.
        user_data_tuples_for_comparison = []
        if not eval_options.get('column_order_matters', True) and eval_options.get('check_column_names', True):
            # Crear un mapeo de índice de columna correcta a índice de columna de usuario
            user_col_idx_map = {name: i for i, name in enumerate(user_columns_processed)}
            for user_tuple in temp_user_data_tuples:
                reordered_tuple = []
                for correct_col_name in correct_columns_processed:
                    user_idx = user_col_idx_map.get(correct_col_name)
                    if user_idx is not None:
                         reordered_tuple.append(user_tuple[user_idx])
                    else: # Esto no debería pasar si los sets de columnas coinciden
                         reordered_tuple.append(None) 
                user_data_tuples_for_comparison.append(tuple(reordered_tuple))
        else: # El orden de columnas del usuario importa (o no se chequean nombres)
            user_data_tuples_for_comparison = temp_user_data_tuples


        correct_data_tuples = []
        for row in correct_results:
            row_dict = row if isinstance(row, dict) else dict(row._mapping if hasattr(row, '_mapping') else row)
            correct_data_tuples.append(tuple(row_dict.get(str(col).lower()) for col in correct_columns))

    except Exception as e:
        return False, f"Error interno al procesar los resultados para comparación: {e}"

    # 2. Comprobar número de filas si el orden no importa (si importa, se comprueba con la igualdad de listas)
    if not eval_options.get('order_matters', True):
        if len(user_data_tuples_for_comparison) != len(correct_data_tuples):
            return False, f"Error: El número de filas no coincide. Se esperaba: {len(correct_data_tuples)}, Resultado: {len(user_data_tuples_for_comparison)}"

    # 3. Comparar datos
    if eval_options.get('order_matters', True):
        if user_data_tuples_for_comparison != correct_data_tuples:
            # Encontrar la primera diferencia para un mensaje más útil
            for i in range(min(len(user_data_tuples_for_comparison), len(correct_data_tuples))):
                if user_data_tuples_for_comparison[i] != correct_data_tuples[i]:
                    return False, f"Error: Datos incorrectos en la fila {i+1} (considerando el orden). Se esperaba: {correct_data_tuples[i]}, Resultado: {user_data_tuples_for_comparison[i]}"
            if len(user_data_tuples_for_comparison) != len(correct_data_tuples): # Diferencia de longitud
                 return False, f"Error: El número de filas no coincide. Se esperaba: {len(correct_data_tuples)}, Resultado: {len(user_data_tuples_for_comparison)}"
            return False, "Error: Los datos no coinciden (considerando el orden)."
    else:
        # El orden no importa, comparar como multiconjuntos (listas de tuplas ordenadas internamente y luego la lista de listas)
        # Convertir a una forma canónica para comparación de multiconjuntos: ordenar cada tupla y luego ordenar la lista de tuplas.
        # No, las tuplas internas no deben ordenarse, solo la lista externa de tuplas.
        # Usar contadores para manejar duplicados correctamente es más robusto para multiconjuntos.
        from collections import Counter
        user_counts = Counter(user_data_tuples_for_comparison)
        correct_counts = Counter(correct_data_tuples)

        if user_counts != correct_counts:
            # Encontrar diferencias para dar feedback
            for item_tuple, count in correct_counts.items():
                if user_counts[item_tuple] != count:
                    return False, f"Error: Discrepancia en la fila de datos '{item_tuple}'. Se esperaba {count} vez/veces, se encontró {user_counts[item_tuple]} vez/veces."
            # Chequear si hay items extra en el resultado del usuario
            for item_tuple, count in user_counts.items():
                if correct_counts[item_tuple] != count: # Ya cubierto arriba, pero por si acaso
                     return False, f"Error: Discrepancia en la fila de datos '{item_tuple}'. Se esperaba {correct_counts[item_tuple]} vez/veces, se encontró {count} vez/veces."
            return False, "Error: El contenido de los datos no coincide (sin considerar el orden de las filas, pero sí los duplicados)."

    return True, "¡Correcto!" # Mensaje de éxito genérico, la vista puede usar el de la misión
