# core/manager.py

import os
import json
from pathlib import Path
from . import profiles # Importa el módulo de perfil

REPOSITORY_DIR = Path(__file__).resolve().parent.parent / "repository"
PROJECT_ROOT = Path(__file__).parent.parent


def link_profile(profile_name, dry_run=False):
    """
    Crea enlaces simbólicos para todos los archivos de un perfil dado.
    """
    files_to_link = profiles.get_profile_files(profile_name)

    if files_to_link is None:
        print(f"Error: El perfil '{profile_name}' no fue encontrado.")
        return

    print(f"Vinculando el perfil: {profile_name}")
    for file_info in files_to_link:
        # 1. Obtener la ruta de origen y destino del JSON
        source_relative = file_info["source"]
        destination_tilde = file_info["destination"]

        # 2. Construir las rutas absolutas y limpias
        #    Ej: "work/.bashrc" -> "/ruta/completa/a/dotvault/repository/work/.bashrc"
        source_absolute = REPOSITORY_DIR / source_relative
        #    Ej: "~/.bashrc" -> "/home/usuario/.bashrc"
        destination_absolute = Path(destination_tilde).expanduser()

        # 3. Lógica de creación
        print(f"  Procesando: {destination_absolute}")

        if not dry_run:
            # Asegurarse de que el directorio de destino exista
            destination_absolute.parent.mkdir(parents=True, exist_ok=True)
            # Crear el enlace simbólico
            os.symlink(source_absolute, destination_absolute)
            print(f"    -> Enlace creado: {destination_absolute} -> {source_absolute}")
        else:
            print(f"    -> [DRY RUN] Se crearía el enlace: {destination_absolute} -> {source_absolute}")


def unlink_profile(profile_name, dry_run=False, force=False):
    """
    Busca un perfil y elimina de forma segura los enlaces simbólicos asociados.

    Verifica que la ruta de destino sea un enlace simbólico y que apunte
    al archivo correcto en el repositorio antes de eliminarlo.

    Si 'force' es True, elimina también archivos o directorios reales.
    """
    print(f"Iniciando desvinculación para el perfil: '{profile_name}'...")
    files_to_process = profiles.get_profile_files(profile_name)

    if files_to_process is None:
        print(f"  ERROR: Perfil '{profile_name}' no encontrado.")
        return

    for file_info in files_to_process:
        source_path = REPOSITORY_DIR / file_info["source"]
        destination_path = Path(file_info["destination"]).expanduser()

        print(f"  Verificando: {destination_path}")

        if destination_path.is_symlink():
            try:
                target_of_link = Path(os.readlink(destination_path))
                if target_of_link.resolve() == source_path.resolve():
                    if not dry_run:
                        destination_path.unlink()
                        print("    -> ÉXITO: Enlace simbólico correcto eliminado.")
                    else:
                        print(f"    -> [DRY RUN] Se borraría el enlace: {destination_path} -> {source_path}")
                else:
                    print(f"    -> ADVERTENCIA: El enlace apunta a '{target_of_link}'. No se tocará.")
            except OSError as e:
                print(f"    -> ERROR: No se pudo leer o eliminar el enlace. {e}")
        elif destination_path.exists():
            if force:
                if not dry_run:
                    try:
                        if destination_path.is_dir():
                            destination_path.rmdir()  # solo si está vacía
                        else:
                            destination_path.unlink()
                        print("    -> ⚠ ARCHIVO REAL eliminado por 'force'.")
                    except Exception as e:
                        print(f"    -> ERROR al eliminar archivo real: {e}")
                else:
                    print(f"    -> [DRY RUN] Se eliminaría archivo real: {destination_path}")
            else:
                print("    -> ADVERTENCIA: La ruta es un archivo o directorio real. No se tocará.")
        else:
            print("    -> INFO: La ruta no existe. No hay nada que hacer.")

    print("\nDesvinculación completada.")


def showList():
    BASE_DIR = Path(__file__).resolve().parent.parent  

    config_path = BASE_DIR / "config" / "profiles.json"

    with open(config_path, "r") as f:
        data = json.load(f)
        print("Perfiles disponibles: ")
        for profileName in data:
            print("Perfil: " + profileName + " y los archivos que configura: ")
            files= [entry["source"].split("/")[-1] for entry in data[profileName]["files"]]
            for filename in files:
                print(filename)

def loadStatus():
    BASE_DIR = Path(__file__).resolve().parent.parent  

    config_path = BASE_DIR / "config" / "profiles.json"

    with open(config_path, "r") as f:
        data = json.load(f)
    for name, profileData in data.items():
        print(f"Perfil : {name}")
        for entry in profileData["files"]:
            source = entry["source"]
            destination = entry["destination"]
            status = check_file_status(source, destination)
            print(f"{destination}->{status}")

def check_file_status(source, destination):
    source_path = (REPOSITORY_DIR / source).resolve()
    destination_path = Path(destination).expanduser()
    if not destination_path.exists():
        return "MISSING"
    elif destination_path.is_symlink():
        try:
            target = os.readlink(destination_path)
            target_path = (destination_path.parent / target).resolve()
            if target_path == source_path:
                return "LINKED"
            else:
                print(f"    ↪ DEBUG: esperado = {source_path}, apuntado = {target_path}")
                return "CONFLICT"
        except OSError:
            return "CONFLICT"
    else:
        return "CONFLICT"



