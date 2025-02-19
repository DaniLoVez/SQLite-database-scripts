import sqlite3
import os
import json
import csv

# Función para conectar a la base de datos SQLite
def connect_to_db(db_path):
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"El archivo no existe en la ruta especificada: {db_path}")
    conn = sqlite3.connect(db_path)
    return conn

# Función para obtener los nombres de archivos y sus IDs
def get_videos_and_ids(conn):
    cursor = conn.cursor()
    query = """
    SELECT Name, Content
    FROM RittMainGraph
    WHERE json_extract(Content, '$.m.t') = 2
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    videos = {}
    for name, content in rows:
        data = json.loads(content)
        video_id = data.get('i', None)
        if video_id is not None:
            videos[video_id] = name
    return videos

# Función para obtener los tags y sus IDs
def get_tags_and_ids(conn):
    cursor = conn.cursor()
    query = """
    SELECT Name, Content
    FROM RittMainGraph
    WHERE json_extract(Content, '$.m.t') = 1
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    tags = {}
    for name, content in rows:
        data = json.loads(content)
        tag_ids = data.get('l', [])
        tags[name] = tag_ids
    return tags

# Función para obtener la familia de un tag dado (ejemplo)
def get_tag_family(tag_name):
    tag_families = {
        'Angle': ['orbital', 'higher', 'normal', 'lower', 'bottom'],
        'shot': ['close-up', 'medium', 'full', 'general', 'panoramic', 'american'],
        'indoor': ['outdoor', 'indoor'],
        'light_issue': ['none', 'shadows', 'backlight', 'night', 'poorlighting', 'weather'],
        'quality': ['poor', 'average', 'best'],
        'dynamic_camera': ['static', 'dynamic'],
        'density': ['low', 'mid', 'high', 'very-high']
    }
    for family, members in tag_families.items():
        if tag_name in members:
            return family
    return None

# Función para buscar archivos .mp4 recursivamente en un directorio
def find_mp4_files(base_path):
    mp4_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.mp4'):
                mp4_files.append(os.path.join(root, file))
    return mp4_files

# Función para extraer los tags de cada video
def extract_video_tags(videos, tags, base_path):
    mp4_files = find_mp4_files(base_path)
    video_tags = {}
    for tag_name, tag_ids in tags.items():
        for video_id in tag_ids:
            if video_id in videos:
                video_name = os.path.splitext(videos[video_id])[0]  # Eliminar la extensión del archivo
                family = get_tag_family(tag_name)
                if family is not None:
                    for file_path in mp4_files:
                        if os.path.basename(file_path) == f"{video_name}.mp4":
                            if video_name not in video_tags:
                                video_tags[video_name] = {}
                            video_tags[video_name][family] = tag_name
                            break
    return video_tags

# Función para escribir el resultado en un archivo CSV
def write_to_csv(video_tags, csv_path):
    fieldnames = ["Filename", "Angle", "shot", "indoor", "light_issue", "quality", "dynamic_camera", "density"]
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for video_name, tags in video_tags.items():
            row = {"Filename": video_name}
            row.update(tags)
            writer.writerow(row)

# Cerrar la conexión a la base de datos
def close_connection(conn):
    conn.close()

if __name__ == "__main__":

    db_path = r'***************************'  # Reemplaza con la ruta al archivo .ritt

    # ---Configuration---
    footage_base_path = r'***************************'  # Cambia esta ruta según sea necesario
    csv_output_path = 'output.csv'  # Ruta donde se guardará el archivo CSV

    try:
        conn = connect_to_db(db_path)
        videos = get_videos_and_ids(conn)
        tags = get_tags_and_ids(conn)
        video_tags = extract_video_tags(videos, tags, footage_base_path)
        write_to_csv(video_tags, csv_output_path)
        close_connection(conn)
        print(f"Archivo CSV generado exitosamente en {csv_output_path}")
    except FileNotFoundError as e:
        print(e)
    except sqlite3.OperationalError as e:
        print(f"Error al abrir la base de datos: {e}")
