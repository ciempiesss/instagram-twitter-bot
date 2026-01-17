# -*- coding: utf-8 -*-
"""
Prueba rapida del scraper de Instagram
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from instagram_scraper_playwright import InstagramScraperPlaywright
import config

print("=" * 60)
print("PROBANDO SCRAPER DE INSTAGRAM")
print("=" * 60)

scraper = InstagramScraperPlaywright(
    username=config.INSTAGRAM_USERNAME,
    headless=True  # Sin mostrar navegador
)

print(f"\nBuscando posts de @{config.INSTAGRAM_USERNAME}...")
print("(Esto puede tardar 10-15 segundos...)\n")

try:
    posts = scraper.get_recent_posts(max_posts=3)

    if posts:
        print(f"\n[OK] Encontrados {len(posts)} posts recientes:\n")

        for i, post in enumerate(posts, 1):
            print(f"{i}. Post: {post['url']}")
            print(f"   Tipo: {'Video' if post['is_video'] else 'Imagen'}")
            caption = post['caption'][:80].replace('\n', ' ')
            print(f"   Caption: {caption}...")
            print()

        print("=" * 60)
        print("[OK] El bot puede acceder a Instagram correctamente!")
        print("=" * 60)
    else:
        print("[ADVERTENCIA] No se encontraron posts")
        print("Verifica que la cuenta sea publica")

except Exception as e:
    print(f"[ERROR] {e}")
    print("\nPosibles causas:")
    print("1. La cuenta no existe")
    print("2. La cuenta es privada")
    print("3. Instagram bloqueo temporalmente el acceso")
