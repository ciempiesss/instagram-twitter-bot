"""
Módulo para descargar contenido de Instagram
Usa Instaloader - no requiere API oficial
"""
import instaloader
from pathlib import Path
from datetime import datetime
import time

class InstagramScraper:
    def __init__(self, username, password=None, download_folder="media"):
        """
        Inicializa el scraper de Instagram

        Args:
            username: Usuario de Instagram a monitorear
            password: Contraseña (solo si quieres hacer login, opcional)
            download_folder: Carpeta donde guardar las descargas
        """
        self.username = username
        self.download_folder = Path(download_folder)
        self.download_folder.mkdir(exist_ok=True)

        # Configurar Instaloader
        self.L = instaloader.Instaloader(
            download_pictures=True,
            download_videos=True,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False,
            dirname_pattern=str(self.download_folder)
        )

        # Login opcional (permite acceder a más contenido)
        if password:
            try:
                self.L.load_session_from_file(username)
                print(f"✅ Sesión cargada para {username}")
            except FileNotFoundError:
                print(f"🔐 Iniciando sesión como {username}...")
                self.L.login(username, password)
                self.L.save_session_to_file()
                print("✅ Sesión guardada")

    def get_recent_posts(self, max_posts=5):
        """
        Obtiene los posts más recientes del perfil

        Args:
            max_posts: Número máximo de posts a obtener

        Returns:
            Lista de diccionarios con información de los posts
        """
        posts_data = []

        try:
            print(f"🔍 Obteniendo posts de @{self.username}...")
            profile = instaloader.Profile.from_username(self.L.context, self.username)

            for index, post in enumerate(profile.get_posts()):
                if index >= max_posts:
                    break

                post_info = {
                    'shortcode': post.shortcode,
                    'post_id': post.mediaid,
                    'url': f"https://www.instagram.com/p/{post.shortcode}/",
                    'caption': post.caption if post.caption else "",
                    'date': post.date_utc.isoformat(),
                    'is_video': post.is_video,
                    'likes': post.likes,
                    'comments': post.comments,
                    'typename': post.typename,  # GraphImage, GraphVideo, GraphSidecar
                }

                posts_data.append(post_info)

            print(f"✅ Encontrados {len(posts_data)} posts")
            return posts_data

        except Exception as e:
            print(f"❌ Error obteniendo posts: {e}")
            return []

    def download_post(self, shortcode):
        """
        Descarga un post específico (imagen o video)

        Args:
            shortcode: Código del post de Instagram

        Returns:
            Dict con rutas de archivos descargados
        """
        try:
            print(f"📥 Descargando post {shortcode}...")

            # Obtener el post
            post = instaloader.Post.from_shortcode(self.L.context, shortcode)

            # Descargar directamente en download_folder
            # Instaloader usa el patrón de fecha: YYYY-MM-DD_HH-MM-SS_UTC
            self.L.download_post(post, target=str(self.download_folder))

            # Encontrar los archivos descargados
            downloaded_files = {
                'images': [],
                'videos': [],
                'caption': post.caption if post.caption else "",
                'url': f"https://www.instagram.com/p/{shortcode}/"
            }

            # Instaloader nombra archivos como: YYYY-MM-DD_HH-MM-SS_UTC.jpg
            # Convertir la fecha del post a ese formato
            date_str = post.date_utc.strftime('%Y-%m-%d_%H-%M-%S_UTC')

            # Buscar archivos que coincidan con esta fecha
            for file in self.download_folder.iterdir():
                if file.is_file() and file.stem == date_str:
                    if file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                        downloaded_files['images'].append(str(file))
                    elif file.suffix.lower() in ['.mp4']:
                        downloaded_files['videos'].append(str(file))

            print(f"✅ Descargado: {len(downloaded_files['images'])} imágenes, {len(downloaded_files['videos'])} videos")

            return downloaded_files

        except Exception as e:
            print(f"❌ Error descargando post: {e}")
            return None

    def get_latest_post(self):
        """
        Obtiene solo el post más reciente

        Returns:
            Dict con info del post más reciente
        """
        posts = self.get_recent_posts(max_posts=1)
        return posts[0] if posts else None


# Prueba del módulo
if __name__ == "__main__":
    # Test
    scraper = InstagramScraper(
        username="tu_usuario_aqui",  # Cambia esto
        password=None  # Opcional: agrega tu contraseña
    )

    # Obtener posts recientes
    posts = scraper.get_recent_posts(max_posts=3)

    for post in posts:
        print(f"\n📸 Post: {post['url']}")
        print(f"   Caption: {post['caption'][:50]}...")
        print(f"   Es video: {post['is_video']}")

    # Descargar el primero
    if posts:
        files = scraper.download_post(posts[0]['shortcode'])
        print(f"\n✅ Archivos descargados: {files}")
