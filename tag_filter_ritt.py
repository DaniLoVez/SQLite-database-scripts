import sqlite3
import os
import json
from collections import Counter

# Función para conectar a la base de datos SQLite
def connect_to_db(db_path):
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"El archivo no existe en la ruta especificada: {db_path}")
    conn = sqlite3.connect(db_path)
    return conn

# Función para obtener archivos .mp4 con múltiples etiquetas especificadas
def get_files_by_tags(conn, tags):
    cursor = conn.cursor()
    placeholders = ' OR '.join('Content LIKE ?' for _ in tags)
    query = f"""
    SELECT Name, Content
    FROM RittMainGraph
    WHERE {placeholders}
    """
    like_tags = [f'%{tag}%' for tag in tags]
    cursor.execute(query, like_tags)
    rows = cursor.fetchall()
    return rows

# Función para obtener los nombres de archivos basados en IDs
def get_filenames_by_ids(conn, ids):
    cursor = conn.cursor()
    query = """
    SELECT ID, Name
    FROM RittMainGraph
    WHERE ID IN ({})
    """.format(','.join('?' for _ in ids))
    cursor.execute(query, ids)
    rows = cursor.fetchall()
    return {row[0]: row[1] for row in rows}

# Función para buscar archivos .mp4 recursivamente en un directorio
def find_mp4_files(base_path):
    mp4_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.mp4'):
                mp4_files.append(os.path.join(root, file))
    return mp4_files

# Función para extraer archivos .mp4 de los resultados
def extract_mp4_files(rows, conn, base_path):
    mp4_files = []
    for name, content in rows:
        try:
            data = json.loads(content)
            ids = data.get('l', [])
            filenames = get_filenames_by_ids(conn, ids)
            for file_id, filename in filenames.items():
                file_found = False
                for file_path in find_mp4_files(base_path):
                    if os.path.basename(file_path) == filename:
                        mp4_files.append(file_path)
                        file_found = True
                        break
                if not file_found:
                    continue
                    #print(f"Archivo no encontrado para ID {file_id}: {filename}")
        except json.JSONDecodeError:
            print(f"Error al decodificar JSON en el contenido de {name}")
            continue  # Si el contenido no es JSON, pasa al siguiente registro
    return mp4_files

# Cerrar la conexión a la base de datos
def close_connection(conn):
    conn.close()


if __name__ == "__main__":

    # CONFIGURACION
    db_path = r'***************************'  # Reemplaza con la ruta al archivo .ritt
    footage_base_path = r'***************************'  # Ruta base donde se encuentran los videos .mp4

    tags_to_filter = ['***************************']  # Reemplaza con las etiquetas que deseas filtrar

    try:
        conn = connect_to_db(db_path)
        rows = get_files_by_tags(conn, tags_to_filter)
        mp4_files = extract_mp4_files(rows, conn, footage_base_path)

        c = dict(Counter(mp4_files))
        for elemento, cuenta in c.items():
            if cuenta == len(tags_to_filter):
                print(f'Elemento: {elemento}, Repeticiones: {cuenta}')

        close_connection(conn)
    except FileNotFoundError as e:
        print(e)
    except sqlite3.OperationalError as e:
        print(f"Error al abrir la base de datos: {e}")
