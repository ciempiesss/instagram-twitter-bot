# 🤖 Bot Instagram → Twitter Auto-Poster

Bot automatizado que monitorea un perfil de Instagram y replica los posts en Twitter automáticamente.

## ✨ Características

- ✅ Detecta automáticamente posts nuevos en Instagram
- ✅ Descarga imágenes y videos
- ✅ Publica en Twitter con el caption original
- ✅ Soporta múltiples imágenes y videos
- ✅ Sistema de historial para no duplicar posts
- ✅ Modo continuo con intervalo configurable
- ✅ Usa Playwright para simular navegador real

## 📋 Requisitos

- Python 3.8 o superior
- Cuenta de Twitter con acceso a Developer API
- Conexión a internet

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

Ya tienes los archivos en: `C:\Users\disoc\instagram-twitter-bot\`

### 2. Instalar Python (si no lo tienes)

Descarga desde: https://www.python.org/downloads/

### 3. Instalar dependencias

Abre PowerShell o CMD en la carpeta del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

### 4. Instalar navegadores para Playwright

```bash
playwright install chromium
```

## ⚙️ Configuración

### 1. Configurar Instagram

Edita `config.py` y cambia:

```python
INSTAGRAM_USERNAME = "nombre_del_usuario_a_monitorear"
```

### 2. Obtener Credenciales de Twitter

#### Paso a paso:

1. **Ir a Twitter Developer Portal:**
   - https://developer.twitter.com/en/portal/dashboard
   - Inicia sesión con tu cuenta de Twitter

2. **Crear una App:**
   - Click en "Create Project"
   - Nombre del proyecto: "Instagram Twitter Bot"
   - Caso de uso: "Making a bot"

3. **Obtener Keys y Tokens:**
   - Ve a la pestaña "Keys and tokens"
   - Genera:
     - API Key y API Secret
     - Access Token y Access Secret
     - Bearer Token

4. **Configurar Permisos:**
   - Ve a "User authentication settings"
   - Habilita "Read and Write" permissions
   - Guarda cambios

5. **Copiar credenciales en config.py:**

```python
TWITTER_API_KEY = "tu_api_key_aqui"
TWITTER_API_SECRET = "tu_api_secret_aqui"
TWITTER_ACCESS_TOKEN = "tu_access_token_aqui"
TWITTER_ACCESS_SECRET = "tu_access_secret_aqui"
TWITTER_BEARER_TOKEN = "tu_bearer_token_aqui"
```

### 3. Ajustar Configuraciones Opcionales

En `config.py` puedes modificar:

```python
# Intervalo de verificación (en minutos)
CHECK_INTERVAL = 15

# Número de posts a revisar
MAX_POSTS_TO_CHECK = 5

# Prefijo para los tweets
TWEET_PREFIX = "Nuevo post: "

# Incluir link al post original de Instagram
INCLUDE_INSTAGRAM_LINK = True

# Longitud máxima del caption
MAX_CAPTION_LENGTH = 250
```

## 🎮 Uso

### Ejecutar el bot

```bash
python main.py
```

### Menú de opciones:

```
1. Ejecutar UNA VEZ (revisar ahora)
   → Revisa Instagram una sola vez y publica si hay posts nuevos

2. Ejecutar en LOOP (cada X minutos)
   → Revisa continuamente cada X minutos

3. Ver ESTADÍSTICAS
   → Muestra historial de posts procesados

4. Salir
```

### Ejemplo de ejecución:

```bash
C:\Users\disoc\instagram-twitter-bot> python main.py

🤖 Inicializando bot Instagram → Twitter
==================================================
✅ Cliente de Twitter inicializado
✅ Bot inicializado correctamente

╔════════════════════════════════════════╗
║  Bot Instagram → Twitter               ║
╚════════════════════════════════════════╝

¿Cómo quieres ejecutar el bot?

1. Ejecutar UNA VEZ (revisar ahora)
2. Ejecutar en LOOP (cada X minutos)
3. Ver ESTADÍSTICAS
4. Salir

Elige una opción (1-4): 2
¿Cada cuántos minutos? (default: 15): 10

🔄 Bot en modo continuo
⏱️  Verificando cada 10 minutos
⌨️  Presiona Ctrl+C para detener

🔍 Buscando nuevos posts de @instagram...
```

## 📁 Estructura de Archivos

```
instagram-twitter-bot/
├── main.py                          # Script principal
├── instagram_scraper_playwright.py  # Módulo Instagram (Playwright)
├── twitter_poster.py                # Módulo Twitter
├── config.py                        # Configuración
├── requirements.txt                 # Dependencias
├── historial.json                  # Historial (se crea automáticamente)
└── media/                          # Descargas (se crea automáticamente)
    └── [shortcode]/
        ├── imagen.jpg
        └── video.mp4
```

## 🔧 Solución de Problemas

### Error: "Instagram no carga"
- Instagram puede detectar bots
- Solución: Cambia `headless=False` en main.py para ver qué pasa
- Añade más `time.sleep()` entre acciones

### Error: "Twitter API 401"
- Verifica que las credenciales sean correctas
- Asegúrate de tener permisos de Read and Write

### Error: "No se encontró Playwright"
```bash
playwright install chromium
```

### Videos no se suben a Twitter
- Twitter tiene límite de 512MB para videos
- Los videos deben ser menos de 2:20 minutos

## ⚠️ Advertencias

- **Uso Responsable**: No abuses del bot. Instagram puede banear tu IP.
- **Términos de Servicio**: Verifica que cumples con los TOS de Instagram y Twitter.
- **Rate Limits**: Twitter tiene límites de publicación (300 tweets/3 horas).
- **Privacidad**: Solo monitorea cuentas públicas.

## 🔐 Seguridad

- **NUNCA** compartas tu `config.py` con credenciales
- Añade `config.py` a `.gitignore` si usas Git
- Considera usar variables de entorno en producción

## 📊 Características Avanzadas

### Ejecutar como servicio en Windows

1. Crea un archivo `run_bot.bat`:
```bat
@echo off
cd C:\Users\disoc\instagram-twitter-bot
python main.py
pause
```

2. Crea una tarea programada en Windows para ejecutarlo al inicio

### Ejecutar en la nube

- Puedes usar Replit, PythonAnywhere, o un servidor VPS
- Para servidores sin interfaz gráfica, asegúrate que `headless=True`

## 📝 Registro de Cambios

### v1.0 (2026-01-17)
- ✅ Versión inicial
- ✅ Soporte para imágenes y videos
- ✅ Sistema de historial
- ✅ Modo continuo

## 🤝 Contribuciones

Mejoras bienvenidas:
- Soporte para carruseles de Instagram
- Notificaciones por email
- Dashboard web
- Soporte para múltiples cuentas

## 📄 Licencia

Uso educativo y personal. Úsalo bajo tu propia responsabilidad.

---

**¿Problemas?** Revisa los logs en la consola o abre un issue.

**¡Disfruta del bot!** 🚀
