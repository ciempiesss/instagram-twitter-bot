"""
Script de prueba para verificar que todo funciona
Ejecuta este script ANTES de usar el bot completo
"""
import sys
from pathlib import Path

print("🧪 PROBANDO CONFIGURACIÓN DEL BOT")
print("=" * 60)

# 1. Verificar Python
print("\n1️⃣  Verificando versión de Python...")
python_version = sys.version_info
if python_version.major >= 3 and python_version.minor >= 8:
    print(f"   ✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
else:
    print(f"   ❌ Python {python_version.major}.{python_version.minor} - Se requiere 3.8+")
    sys.exit(1)

# 2. Verificar dependencias
print("\n2️⃣  Verificando dependencias...")

required_packages = [
    'playwright',
    'tweepy',
    'requests',
    'PIL'  # Pillow
]

missing_packages = []

for package in required_packages:
    try:
        if package == 'PIL':
            __import__('PIL')
        else:
            __import__(package)
        print(f"   ✅ {package}")
    except ImportError:
        print(f"   ❌ {package} - NO INSTALADO")
        missing_packages.append(package)

if missing_packages:
    print(f"\n   ⚠️  Instala los paquetes faltantes con:")
    print(f"   pip install -r requirements.txt")
    sys.exit(1)

# 3. Verificar Playwright
print("\n3️⃣  Verificando Playwright...")
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        browser.close()
    print("   ✅ Playwright configurado correctamente")
except Exception as e:
    print(f"   ❌ Error con Playwright: {e}")
    print(f"   💡 Ejecuta: playwright install chromium")
    sys.exit(1)

# 4. Verificar configuración
print("\n4️⃣  Verificando config.py...")
try:
    import config

    # Instagram
    if config.INSTAGRAM_USERNAME == "tu_usuario_instagram":
        print("   ⚠️  INSTAGRAM_USERNAME no configurado")
    else:
        print(f"   ✅ Instagram: @{config.INSTAGRAM_USERNAME}")

    # Twitter
    if config.TWITTER_API_KEY == "tu_api_key":
        print("   ❌ Credenciales de Twitter NO configuradas")
        print("   💡 Edita config.py con tus credenciales")
    else:
        print("   ✅ Twitter: Credenciales configuradas")

    # Carpetas
    if config.MEDIA_FOLDER.exists():
        print(f"   ✅ Carpeta media: {config.MEDIA_FOLDER}")
    else:
        print(f"   ℹ️  Carpeta media se creará: {config.MEDIA_FOLDER}")

except Exception as e:
    print(f"   ❌ Error leyendo config.py: {e}")
    sys.exit(1)

# 5. Probar Twitter (si está configurado)
print("\n5️⃣  Probando conexión a Twitter...")
if config.TWITTER_API_KEY != "tu_api_key":
    try:
        from twitter_poster import TwitterPoster

        poster = TwitterPoster(
            api_key=config.TWITTER_API_KEY,
            api_secret=config.TWITTER_API_SECRET,
            access_token=config.TWITTER_ACCESS_TOKEN,
            access_secret=config.TWITTER_ACCESS_SECRET,
            bearer_token=config.TWITTER_BEARER_TOKEN
        )

        if poster.verify_credentials():
            print("   ✅ Conexión a Twitter exitosa")
        else:
            print("   ❌ Error de autenticación con Twitter")
    except Exception as e:
        print(f"   ❌ Error conectando a Twitter: {e}")
else:
    print("   ⏭️  Saltando (credenciales no configuradas)")

# 6. Probar Instagram (básico)
print("\n6️⃣  Probando scraper de Instagram...")
if config.INSTAGRAM_USERNAME != "tu_usuario_instagram":
    try:
        from instagram_scraper_playwright import InstagramScraperPlaywright

        print(f"   🔍 Intentando acceder a @{config.INSTAGRAM_USERNAME}...")
        scraper = InstagramScraperPlaywright(
            username=config.INSTAGRAM_USERNAME,
            download_folder=str(config.MEDIA_FOLDER),
            headless=True
        )

        # Intentar obtener el perfil (no descargar nada aún)
        print("   ℹ️  Esto puede tomar unos segundos...")
        posts = scraper.get_recent_posts(max_posts=1)

        if posts:
            print(f"   ✅ Perfil accesible - {len(posts)} post(s) detectado(s)")
            print(f"      Último post: {posts[0]['url']}")
        else:
            print("   ⚠️  No se pudieron obtener posts (puede ser cuenta privada)")

    except Exception as e:
        print(f"   ❌ Error: {e}")
        print(f"   💡 Verifica que el usuario exista y sea público")
else:
    print("   ⏭️  Saltando (usuario no configurado)")

# Resumen final
print("\n" + "=" * 60)
print("📊 RESUMEN")
print("=" * 60)

all_ok = (
    python_version.major >= 3 and
    python_version.minor >= 8 and
    not missing_packages
)

if all_ok:
    print("✅ Tu entorno está listo para ejecutar el bot!")
    print("\n🚀 Próximos pasos:")
    print("   1. Configura tus credenciales en config.py")
    print("   2. Ejecuta: python main.py")
else:
    print("⚠️  Hay problemas que resolver antes de ejecutar el bot")
    print("   Revisa los errores arriba ⬆️")

print("=" * 60)
