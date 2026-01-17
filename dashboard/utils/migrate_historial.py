# -*- coding: utf-8 -*-
"""
Migration Script: historial.json -> SQLite
Migra el historial existente del bot a la base de datos SQLite
"""
import json
import sys
from pathlib import Path
from datetime import datetime

# Agregar parent directory al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dashboard.models.database import Session, Post, init_db


def migrate_historial_to_db(historial_path='historial.json', dry_run=False):
    """
    Migra historial.json a SQLite

    Args:
        historial_path: Ruta al archivo historial.json
        dry_run: Si es True, no hace cambios, solo muestra qué haría

    Returns:
        Tupla (posts_migrated, posts_skipped, errors)
    """
    historial_file = Path(__file__).parent.parent.parent / historial_path

    if not historial_file.exists():
        print(f"[ERROR] No se encontró {historial_file}")
        return 0, 0, 1

    # Cargar historial
    print(f"[FILE] Leyendo {historial_file}...")
    with open(historial_file, 'r', encoding='utf-8') as f:
        historial = json.load(f)

    print(f"[OK] Encontrados {len(historial)} posts en historial.json\n")

    if dry_run:
        print("🔍 Modo DRY RUN - No se harán cambios\n")

    # Inicializar DB
    init_db()
    session = Session()

    posts_migrated = 0
    posts_skipped = 0
    errors = 0

    try:
        for shortcode, data in historial.items():
            try:
                # Verificar si ya existe
                existing = session.query(Post).filter_by(shortcode=shortcode).first()
                if existing:
                    print(f"[SKIP]  Post {shortcode} ya existe en DB, saltando...")
                    posts_skipped += 1
                    continue

                # Parsear fecha
                try:
                    processed_at = datetime.fromisoformat(data['fecha_procesado'])
                except:
                    processed_at = datetime.utcnow()

                # Parsear media URLs
                media_urls_json = json.dumps(data.get('archivos_descargados', []))

                # Crear objeto Post
                post = Post(
                    shortcode=shortcode,
                    platform_source='instagram',
                    platform_target='twitter',  # Asumimos Twitter por ahora
                    post_url=data.get('instagram_url', ''),
                    caption=data.get('caption', '')[:500],  # Limitar a 500 chars
                    post_type=data.get('tipo', 'imagen'),
                    media_urls=media_urls_json,
                    created_at=processed_at,
                    processed_at=processed_at,
                    status='success'
                )

                if dry_run:
                    print(f"+ Post {shortcode} sería migrado")
                    print(f"  - URL: {post.post_url}")
                    print(f"  - Tipo: {post.post_type}")
                    print(f"  - Fecha: {post.processed_at}")
                else:
                    session.add(post)
                    print(f"[OK] Post {shortcode} migrado")

                posts_migrated += 1

            except Exception as e:
                print(f"[ERROR] Error migrando post {shortcode}: {e}")
                errors += 1
                continue

        if not dry_run:
            session.commit()
            print(f"\n[SAVE] Cambios guardados en la base de datos")

    except Exception as e:
        session.rollback()
        print(f"\n[ERROR] Error general: {e}")
        errors += 1

    finally:
        session.close()

    return posts_migrated, posts_skipped, errors


def main():
    """Función principal para ejecutar la migración"""
    import argparse

    parser = argparse.ArgumentParser(description='Migrar historial.json a SQLite')
    parser.add_argument('--dry-run', action='store_true',
                       help='Modo dry-run: muestra qué haría sin hacer cambios')
    parser.add_argument('--file', type=str, default='historial.json',
                       help='Ruta al archivo historial.json')

    args = parser.parse_args()

    print("=" * 70)
    print("MIGRACIÓN: historial.json -> SQLite")
    print("=" * 70)
    print()

    migrated, skipped, errors = migrate_historial_to_db(
        historial_path=args.file,
        dry_run=args.dry_run
    )

    print("\n" + "=" * 70)
    print("RESUMEN DE MIGRACIÓN")
    print("=" * 70)
    print(f"[OK] Posts migrados:  {migrated}")
    print(f"[SKIP]  Posts saltados:  {skipped}")
    print(f"[ERROR] Errores:         {errors}")
    print("=" * 70)

    if args.dry_run:
        print("\n[TIP] Para ejecutar la migracion real, ejecuta sin --dry-run")

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
