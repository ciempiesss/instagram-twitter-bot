"""
Módulo para descargar contenido de Instagram usando Playwright
Más robusto y simula un navegador real
"""
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from pathlib import Path
import time
import re
import json
import requests
from datetime import datetime

class InstagramScraperPlaywright:
    def __init__(self, username, download_folder="media", headless=True):
        """
        Inicializa el scraper de Instagram con Playwright

        Args:
            username: Usuario de Instagram a monitorear
            download_folder: Carpeta donde guardar las descargas
            headless: Si es True, el navegador se ejecuta sin interfaz
        """
        self.username = username
        self.download_folder = Path(download_folder)
        self.download_folder.mkdir(exist_ok=True)
        self.headless = headless
        self.profile_url = f"https://www.instagram.com/{username}/"

    def get_recent_posts(self, max_posts=5):
        """
        Obtiene los posts más recientes del perfil

        Args:
            max_posts: Número máximo de posts a obtener

        Returns:
            Lista de diccionarios con información de los posts
        """
        posts_data = []

        with sync_playwright() as p:
            print(f"🌐 Abriendo navegador...")
            browser = p.chromium.launch(headless=self.headless)

            # Usar user agent real
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080}
            )

            page = context.new_page()

            try:
                print(f"🔍 Navegando a {self.profile_url}...")
                page.goto(self.profile_url, wait_until='networkidle', timeout=30000)

                # Esperar a que carguen los posts
                time.sleep(3)

                # Rechazar cookies si aparece el diálogo
                try:
                    reject_button = page.locator('button:has-text("Decline optional cookies")').first
                    if reject_button.is_visible(timeout=2000):
                        reject_button.click()
                        time.sleep(1)
                except:
                    pass

                # Obtener posts desde el HTML
                # Instagram carga posts iniciales en el HTML
                posts = page.locator('article a[href*="/p/"]').all()[:max_posts]

                print(f"✅ Encontrados {len(posts)} posts")

                for index, post_link in enumerate(posts):
                    try:
                        href = post_link.get_attribute('href')

                        # Extraer shortcode del href
                        match = re.search(r'/p/([^/]+)/', href)
                        if not match:
                            continue

                        shortcode = match.group(1)
                        post_url = f"https://www.instagram.com/p/{shortcode}/"

                        # Navegar al post para obtener más detalles
                        print(f"📸 Obteniendo detalles del post {index+1}/{len(posts)}...")
                        page.goto(post_url, wait_until='networkidle', timeout=15000)
                        time.sleep(2)

                        # Obtener caption
                        caption = ""
                        try:
                            caption_elem = page.locator('h1').first
                            if caption_elem.is_visible(timeout=2000):
                                caption = caption_elem.inner_text()
                        except:
                            pass

                        # Detectar si es video
                        is_video = page.locator('video').count() > 0

                        # Obtener URL de la imagen o video
                        media_url = None
                        if is_video:
                            video_elem = page.locator('video').first
                            media_url = video_elem.get_attribute('src')
                        else:
                            img_elem = page.locator('article img[src*="instagram"]').first
                            media_url = img_elem.get_attribute('src')

                        post_info = {
                            'shortcode': shortcode,
                            'url': post_url,
                            'caption': caption,
                            'date': datetime.now().isoformat(),
                            'is_video': is_video,
                            'media_url': media_url,
                            'typename': 'video' if is_video else 'image'
                        }

                        posts_data.append(post_info)

                        # Volver al perfil
                        page.goto(self.profile_url, wait_until='networkidle')
                        time.sleep(2)

                    except Exception as e:
                        print(f"⚠️ Error procesando post: {e}")
                        continue

            except Exception as e:
                print(f"❌ Error general: {e}")

            finally:
                browser.close()

        return posts_data

    def download_media(self, media_url, shortcode, is_video=False):
        """
        Descarga imagen o video desde URL

        Args:
            media_url: URL del archivo
            shortcode: Código del post
            is_video: Si es video o imagen

        Returns:
            Ruta del archivo descargado
        """
        try:
            # Crear carpeta para el post
            post_folder = self.download_folder / shortcode
            post_folder.mkdir(exist_ok=True)

            # Determinar extensión
            extension = '.mp4' if is_video else '.jpg'
            filename = f"{shortcode}{extension}"
            filepath = post_folder / filename

            # Descargar
            print(f"📥 Descargando {filename}...")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(media_url, headers=headers, stream=True)
            response.raise_for_status()

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"✅ Descargado: {filepath}")
            return str(filepath)

        except Exception as e:
            print(f"❌ Error descargando: {e}")
            return None

    def download_post(self, shortcode):
        """
        Descarga un post completo (con Playwright para obtener URLs)

        Args:
            shortcode: Código del post

        Returns:
            Dict con información y archivos descargados
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = context.new_page()

            try:
                post_url = f"https://www.instagram.com/p/{shortcode}/"
                print(f"🌐 Abriendo post: {post_url}")

                page.goto(post_url, wait_until='networkidle', timeout=30000)
                time.sleep(3)

                # Rechazar cookies
                try:
                    page.locator('button:has-text("Decline")').first.click(timeout=2000)
                except:
                    pass

                # Caption
                caption = ""
                try:
                    caption = page.locator('h1').first.inner_text(timeout=2000)
                except:
                    pass

                # Detectar tipo
                is_video = page.locator('video').count() > 0

                downloaded_files = {
                    'images': [],
                    'videos': [],
                    'caption': caption,
                    'url': post_url
                }

                if is_video:
                    # Descargar video
                    video_url = page.locator('video').first.get_attribute('src')
                    filepath = self.download_media(video_url, shortcode, is_video=True)
                    if filepath:
                        downloaded_files['videos'].append(filepath)
                else:
                    # Descargar imagen(es)
                    images = page.locator('article img[src*="instagram"]').all()
                    for img in images[:5]:  # Máximo 5 imágenes
                        img_url = img.get_attribute('src')
                        filepath = self.download_media(img_url, shortcode, is_video=False)
                        if filepath:
                            downloaded_files['images'].append(filepath)

                return downloaded_files

            except Exception as e:
                print(f"❌ Error: {e}")
                return None

            finally:
                browser.close()

    def get_latest_post(self):
        """Obtiene el post más reciente"""
        posts = self.get_recent_posts(max_posts=1)
        return posts[0] if posts else None


# Prueba del módulo
if __name__ == "__main__":
    # Test
    scraper = InstagramScraperPlaywright(
        username="instagram",  # Cambia por el usuario que quieras
        headless=False  # False para ver el navegador
    )

    # Obtener posts recientes
    posts = scraper.get_recent_posts(max_posts=3)

    for post in posts:
        print(f"\n📸 Post: {post['url']}")
        print(f"   Caption: {post['caption'][:100]}...")
        print(f"   Es video: {post['is_video']}")

    # Descargar el primero
    if posts:
        print("\n🔽 Descargando primer post...")
        files = scraper.download_post(posts[0]['shortcode'])
        if files:
            print(f"\n✅ Archivos descargados:")
            print(f"   Imágenes: {files['images']}")
            print(f"   Videos: {files['videos']}")
