import argparse
from dotvault.core import manager

def main():
    parser = argparse.ArgumentParser(prog="dotvault", description="Gestor de perfiles de configuración")
    subparsers = parser.add_subparsers(dest="command", required=True)

    #link
    link_parser = subparsers.add_parser("link", help="Vincula un perfil")
    link_parser.add_argument("profile", help="Nombre del perfil a vincular")

    #unlink
    unlink_parser = subparsers.add_parser("unlink", help="Desvincula un perfil")
    unlink_parser.add_argument("profile", help="Nombre del perfil a desvincular")
    unlink_parser.add_argument("--dry-run", action="store_true", help="Simula la desvinculación sin borrar nada")
    unlink_parser.add_argument("--force", action="store_true", help="Elimina archivos reales (con precaución)")

    #status
    status_parser = subparsers.add_parser("status", help="Muestra el estado de todos los perfiles")

    args = parser.parse_args()

    # Ejecutar según el comando
    if args.command == "link":
        manager.link_profile(args.profile)

    elif args.command == "unlink":
        manager.unlink_profile(args.profile, dry_run=args.dry_run, force=args.force)

    elif args.command == "status":
        manager.loadStatus()

if __name__ == "__main__":
    main()
