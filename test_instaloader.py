# -*- coding: utf-8 -*-
"""
Prueba con Instaloader (más confiable que Playwright)
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from instagram_scraper import InstagramScraper
import config

print("=" * 60)
print("PROBANDO INSTALOADER (sin navegador)")
print("=" * 60)

scraper = InstagramScraper(
    username=config.INSTAGRAM_USERNAME,
    download_folder=str(config.MEDIA_FOLDER)
)

print(f"\nBuscando posts de @{config.INSTAGRAM_USERNAME}...\n")

try:
    posts = scraper.get_recent_posts(max_posts=3)

    if posts:
        print(f"\n[OK] Encontrados {len(posts)} posts recientes:\n")

        for i, post in enumerate(posts, 1):
            print(f"{i}. Post: {post['url']}")
            print(f"   Tipo: {'Video' if post['is_video'] else 'Imagen'}")
            caption = post['caption'][:80].replace('\n', ' ')
            print(f"   Caption: {caption}...")
            print(f"   Likes: {post['likes']}")
            print()

        print("=" * 60)
        print("[OK] ¡El bot puede acceder a Instagram!")
        print("=" * 60)

        # Probar descarga
        print(f"\n[TEST] Descargando primer post...")
        result = scraper.download_post(posts[0]['shortcode'])
        if result:
            print(f"[OK] Descarga exitosa!")
            print(f"    Imagenes: {len(result['images'])}")
            print(f"    Videos: {len(result['videos'])}")
    else:
        print("[ADVERTENCIA] No se encontraron posts")

except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
