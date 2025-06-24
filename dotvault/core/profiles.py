# core/profiles.py

import json
from pathlib import Path

# La ruta al archivo de configuración
PROFILES_PATH = Path(__file__).parent.parent / "config" / "profiles.json"

def load_all_profiles():
    """Carga y devuelve todos los perfiles desde el archivo JSON."""
    try:
        with open(PROFILES_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Manejar el caso en que el archivo no existe
        return {}
    except json.JSONDecodeError:
        # Manejar el caso en que el JSON está mal formado
        return {}

def get_profile_files(profile_name):
    """
    Busca un perfil por su nombre y devuelve su lista de archivos.
    Devuelve None si el perfil no se encuentra.
    """
    all_profiles = load_all_profiles()
    profile = all_profiles.get(profile_name)
    if profile:
        return profile.get("files", []) # Devuelve la lista de archivos o una lista vacía
    return None