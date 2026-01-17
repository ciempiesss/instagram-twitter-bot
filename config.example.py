"""
Configuración del Bot Instagram → Twitter
COPIA ESTE ARCHIVO A config.py Y EDITA CON TUS CREDENCIALES
"""
import os
from pathlib import Path

# ====================
# CONFIGURACIÓN INSTAGRAM
# ====================
INSTAGRAM_USERNAME = "usuario_a_monitorear"  # Usuario de Instagram a monitorear
INSTAGRAM_PASSWORD = ""  # Solo si usas método con login (opcional)

# ====================
# CONFIGURACIÓN TWITTER
# ====================
# Obtén estas credenciales en: https://developer.twitter.com/en/portal/dashboard
TWITTER_API_KEY = "tu_api_key"
TWITTER_API_SECRET = "tu_api_secret"
TWITTER_ACCESS_TOKEN = "tu_access_token"
TWITTER_ACCESS_SECRET = "tu_access_secret"
TWITTER_BEARER_TOKEN = "tu_bearer_token"  # Opcional para API v2

# ====================
# CONFIGURACIÓN GENERAL
# ====================
# Carpeta donde se guardarán las imágenes/videos descargados
MEDIA_FOLDER = Path(__file__).parent / "media"
MEDIA_FOLDER.mkdir(exist_ok=True)

# Archivo para trackear qué posts ya se publicaron
HISTORIAL_FILE = Path(__file__).parent / "historial.json"

# Intervalo de verificación (en minutos)
CHECK_INTERVAL = 15

# Número máximo de posts a revisar en cada ejecución
MAX_POSTS_TO_CHECK = 5

# Prefijo para los tweets (opcional)
TWEET_PREFIX = ""  # Ejemplo: "Nuevo en Instagram: "

# Incluir enlace al post de Instagram en el tweet
INCLUDE_INSTAGRAM_LINK = True

# Límite de caracteres para el caption (Twitter permite 280)
MAX_CAPTION_LENGTH = 250
