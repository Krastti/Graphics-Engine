import tkinter as tk

from tkinter import filedialog
from parameters import *

loaded_obj_model = None

def load_obj_file():
    vertices = []
    faces = []


    global loaded_obj_model

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title = "Выберите .obj файл",
        filetypes = [("OBJ файлы", "*.obj"), ("All Files", "*.*")],
    )

    root.destroy()

    if not file_path:
        print("Файл не выбран")
        return None

    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.split()
                if not parts:
                    continue

                if parts[0] == 'v':
                    vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
                elif parts[0] == 'f':
                    face = []
                    for i in range(1, len(parts)):
                        idx = int(parts[i].split('/')[0]) - 1
                        face.append(idx)

                    if len(face) >= 3:
                        faces.append(face)
                    else:
                        print(f"Предупреждение: Некорректная грань {faces}, пропущена")

    except FileNotFoundError:
        print(f"Ошибка: файл не найден: {file_path}")
        return None

    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return None

    if not vertices or not faces:
        print("Файл не содержит вершин или граней")
        loaded_obj_model = None
        return None

    face_colors = [GRAY] * len(faces)

    loaded_obj_model = {
        "vertices": vertices,
        "faces": faces,
        "colors": face_colors,
    }

    return loaded_obj_model

def get_loaded_model():
    return loaded_obj_model

def reset_loaded_model():
    global loaded_obj_model
    loaded_obj_model = None