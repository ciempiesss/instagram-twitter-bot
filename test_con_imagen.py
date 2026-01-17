# -*- coding: utf-8 -*-
"""
Test: Publicar UN solo post con imagen en Twitter
"""
import sys
import io
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except:
    pass

from instagram_scraper import InstagramScraper
from twitter_poster import TwitterPoster
import config

print("\n" + "=" * 60)
print("TEST: Publicar post con IMAGEN en Twitter")
print("=" * 60)

# Inicializar
ig = InstagramScraper(
    username=config.INSTAGRAM_USERNAME,
    download_folder=str(config.MEDIA_FOLDER)
)

tw = TwitterPoster(
    api_key=config.TWITTER_API_KEY,
    api_secret=config.TWITTER_API_SECRET,
    access_token=config.TWITTER_ACCESS_TOKEN,
    access_secret=config.TWITTER_ACCESS_SECRET,
    bearer_token=config.TWITTER_BEARER_TOKEN
)

# Verificar Twitter
if not tw.verify_credentials():
    print("❌ Error con Twitter")
    sys.exit(1)

print("\n🔍 Obteniendo último post de Instagram...")
posts = ig.get_recent_posts(max_posts=1)

if not posts:
    print("❌ No se encontraron posts")
    sys.exit(1)

post = posts[0]
print(f"\n📸 Post encontrado: {post['url']}")
print(f"   Caption: {post['caption'][:50]}...")

# Descargar
print("\n📥 Descargando...")
files = ig.download_post(post['shortcode'])

if not files:
    print("❌ Error descargando")
    sys.exit(1)

print(f"\n✅ Archivos descargados:")
print(f"   Imágenes: {files['images']}")
print(f"   Videos: {files['videos']}")

# Preparar tweet
tweet_text = f"TEST: Post desde Instagram\n\n{post['url']}"

# Publicar
print(f"\n🐦 Publicando en Twitter...")
media_files = files['videos'] if files['videos'] else files['images']

if media_files:
    print(f"   📎 Con {len(media_files)} archivo(s) adjunto(s)")
    tweet_id = tw.post_with_media(tweet_text, media_files[:1])  # Solo el primero
else:
    print("   ⚠️ Sin archivos, solo texto")
    tweet_id = tw.create_tweet(tweet_text)

if tweet_id:
    print(f"\n" + "=" * 60)
    print(f"✅ ÉXITO!")
    print(f"=" * 60)
    print(f"Tweet: https://twitter.com/i/web/status/{tweet_id}")
    print(f"=" * 60)
else:
    print("\n❌ Error publicando")
