"""
Script de prueba simplificado (sin emojis para Windows)
"""
import sys

print("=" * 60)
print("PROBANDO CONFIGURACION DEL BOT")
print("=" * 60)

# 1. Python
print("\n1. Verificando Python...")
v = sys.version_info
if v.major >= 3 and v.minor >= 8:
    print(f"   OK - Python {v.major}.{v.minor}.{v.micro}")
else:
    print(f"   ERROR - Python {v.major}.{v.minor} (se requiere 3.8+)")
    sys.exit(1)

# 2. Dependencias
print("\n2. Verificando dependencias...")
packages = ['playwright', 'tweepy', 'requests', 'PIL', 'instaloader']
missing = []

for pkg in packages:
    try:
        if pkg == 'PIL':
            __import__('PIL')
        else:
            __import__(pkg)
        print(f"   OK - {pkg}")
    except ImportError:
        print(f"   FALTA - {pkg}")
        missing.append(pkg)

if missing:
    print(f"\n   Instala: pip install {' '.join(missing)}")
    sys.exit(1)

# 3. Configuración
print("\n3. Verificando config.py...")
try:
    import config

    if config.INSTAGRAM_USERNAME == "tu_usuario_instagram":
        print("   ADVERTENCIA - INSTAGRAM_USERNAME no configurado")
    else:
        print(f"   OK - Instagram: @{config.INSTAGRAM_USERNAME}")

    if config.TWITTER_API_KEY == "tu_api_key":
        print("   ADVERTENCIA - Credenciales de Twitter no configuradas")
    else:
        print("   OK - Twitter: Credenciales configuradas")

        # Probar Twitter
        print("\n4. Probando conexion a Twitter...")
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
                print("   OK - Conexion exitosa!")
            else:
                print("   ERROR - Autenticacion fallida")
        except Exception as e:
            print(f"   ERROR - {str(e)[:100]}")

except Exception as e:
    print(f"   ERROR leyendo config.py: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("RESUMEN: Tu entorno esta listo!")
print("=" * 60)
print("\nProximos pasos:")
print("1. Asegurate de configurar config.py con tus credenciales")
print("2. Ejecuta: python main.py")
print("=" * 60)
