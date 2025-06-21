# core/manager.py

import os
from pathlib import Path
from . import profiles # Importa el módulo de perfiles que acabamos de definir

# La ruta a la carpeta raíz del proyecto para resolver las rutas de origen
PROJECT_ROOT = Path(__file__).parent.parent
REPOSITORY_DIR = PROJECT_ROOT / "repository"

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

        # 3. Lógica de creación del enlace
        print(f"  Procesando: {destination_absolute}")
        # --- (Aquí iría la lógica de detección de conflictos) ---

        if not dry_run:
            # Asegurarse de que el directorio de destino exista
            destination_absolute.parent.mkdir(parents=True, exist_ok=True)
            # Crear el enlace simbólico
            os.symlink(source_absolute, destination_absolute)
            print(f"    -> Enlace creado: {destination_absolute} -> {source_absolute}")
        else:
            print(f"    -> [DRY RUN] Se crearía el enlace: {destination_absolute} -> {source_absolute}")


def unlink_profile(profile_name, dry_run= False):
    """
    Busca un perfil y elimina de forma segura los enlaces simbólicos asociados.

    Verifica que la ruta de destino sea un enlace simbólico y que apunte
    al archivo correcto en el repositorio antes de eliminarlo.
    """
    print(f"Iniciando desvinculación para el perfil: '{profile_name}'...")
    files_to_process = profiles.get_profile_files(profile_name)

    if files_to_process is None:
        print(f"  ERROR: Perfil '{profile_name}' no encontrado.")
        return

    for file_info in files_to_process:
        # Construir las rutas absolutas de origen y destino
        source_path = REPOSITORY_DIR / file_info["source"]
        destination_path = Path(file_info["destination"]).expanduser()

        print(f"  Verificando: {destination_path}")

        # --- Lógica de Verificación y Borrado Seguro ---

        # 1. Primero, verificar si la ruta es un enlace simbólico
        if not destination_path.is_symlink():
            if destination_path.exists():
                # Si existe pero no es un enlace (es un archivo/directorio real), no se toca.
                print("    -> ADVERTENCIA: La ruta es un archivo o directorio real. No se tocará.")
            else:
                # Si la ruta ni siquiera existe.
                print("    -> INFO: La ruta no existe. No hay nada que hacer.")
            continue # Pasa al siguiente archivo del perfil

        # 2. Si es un enlace, verificar a dónde apunta
        try:
            target_of_link = Path(os.readlink(destination_path))
            
            # Comparamos la ruta absoluta del objetivo del enlace con la ruta que esperamos
            # Usamos .resolve() para obtener la ruta canónica y evitar problemas
            if target_of_link.resolve() == source_path.resolve():
                # 3. Si apunta al lugar correcto, es seguro eliminarlo
                if not dry_run:        
                    destination_path.unlink()
                    print("    -> ÉXITO: Enlace simbólico correcto eliminado.")
                else:
                    print(f"    -> [DRY RUN] Se borraria el enlace: {destination_path} -> {source_path}")
            else:
                # Si apunta a otro lugar, no se toca por seguridad.
                print(f"    -> ADVERTENCIA: El enlace apunta a '{target_of_link}'. No se tocará.")

        except OSError as e:
            print(f"    -> ERROR: No se pudo leer o eliminar el enlace. {e}")

    print("\nDesvinculación completada.")