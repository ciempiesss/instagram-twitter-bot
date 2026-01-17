# -*- coding: utf-8 -*-
"""
Bot de Auto-Posting: Instagram → Twitter
Monitorea un perfil de Instagram y replica posts en Twitter automáticamente
"""
import json
import time
from pathlib import Path
from datetime import datetime
import sys

# Importar módulos
from instagram_scraper import InstagramScraper  # Usando Instaloader (más confiable)
from twitter_poster import TwitterPoster
import config

class InstagramTwitterBot:
    def __init__(self):
        """Inicializa el bot con la configuración"""
        print("🤖 Inicializando bot Instagram → Twitter")
        print("=" * 50)

        # Inicializar scraper de Instagram
        self.ig_scraper = InstagramScraper(
            username=config.INSTAGRAM_USERNAME,
            download_folder=str(config.MEDIA_FOLDER)
        )

        # Inicializar poster de Twitter
        self.twitter = TwitterPoster(
            api_key=config.TWITTER_API_KEY,
            api_secret=config.TWITTER_API_SECRET,
            access_token=config.TWITTER_ACCESS_TOKEN,
            access_secret=config.TWITTER_ACCESS_SECRET,
            bearer_token=config.TWITTER_BEARER_TOKEN
        )

        # Cargar historial
        self.historial_file = config.HISTORIAL_FILE
        self.historial = self.load_historial()

        print("✅ Bot inicializado correctamente\n")

    def load_historial(self):
        """Carga el historial de posts ya procesados"""
        if self.historial_file.exists():
            with open(self.historial_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_historial(self):
        """Guarda el historial de posts"""
        with open(self.historial_file, 'w', encoding='utf-8') as f:
            json.dump(self.historial, f, indent=2, ensure_ascii=False)

    def format_caption(self, caption, instagram_url):
        """
        Formatea el caption para Twitter

        Args:
            caption: Caption original de Instagram
            instagram_url: URL del post de Instagram

        Returns:
            Texto formateado para Twitter
        """
        # Añadir prefijo si está configurado
        text = config.TWEET_PREFIX + caption if config.TWEET_PREFIX else caption

        # Calcular espacio disponible
        available_chars = config.MAX_CAPTION_LENGTH

        if config.INCLUDE_INSTAGRAM_LINK:
            # Reservar espacio para el link (23 caracteres en Twitter)
            available_chars -= 25  # 23 + espacio + salto de línea

        # Truncar si es necesario
        if len(text) > available_chars:
            text = text[:available_chars - 3] + "..."

        # Añadir link al post original si está configurado
        if config.INCLUDE_INSTAGRAM_LINK:
            text += f"\n\n{instagram_url}"

        return text

    def process_new_posts(self):
        """
        Busca y procesa posts nuevos de Instagram
        """
        print(f"\n{'='*50}")
        print(f"🔍 Buscando nuevos posts de @{config.INSTAGRAM_USERNAME}")
        print(f"   Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}\n")

        try:
            # Obtener posts recientes
            posts = self.ig_scraper.get_recent_posts(max_posts=config.MAX_POSTS_TO_CHECK)

            if not posts:
                print("ℹ️  No se encontraron posts nuevos")
                return

            # Procesar cada post
            nuevos_posts = 0

            for post in posts:
                shortcode = post['shortcode']

                # Verificar si ya fue procesado
                if shortcode in self.historial:
                    print(f"⏭️  Post {shortcode} ya procesado anteriormente")
                    continue

                nuevos_posts += 1
                print(f"\n{'─'*50}")
                print(f"📸 NUEVO POST DETECTADO")
                print(f"{'─'*50}")
                print(f"URL: {post['url']}")
                print(f"Caption: {post['caption'][:100]}...")
                print(f"Tipo: {'Video' if post['is_video'] else 'Imagen'}")

                # Descargar el post
                print(f"\n📥 Descargando contenido...")
                downloaded = self.ig_scraper.download_post(shortcode)

                if not downloaded:
                    print(f"❌ Error descargando post {shortcode}")
                    continue

                # Preparar archivos para Twitter
                media_files = []

                if downloaded['videos']:
                    # Si hay video, solo subir el primero
                    media_files = [downloaded['videos'][0]]
                elif downloaded['images']:
                    # Si hay imágenes, máximo 4
                    media_files = downloaded['images'][:4]

                # Formatear caption
                tweet_text = self.format_caption(
                    downloaded['caption'],
                    post['url']
                )

                # Publicar en Twitter
                print(f"\n🐦 Publicando en Twitter...")
                tweet_id = self.twitter.post_with_media(
                    text=tweet_text,
                    media_files=media_files
                )

                if tweet_id:
                    # Guardar en historial
                    self.historial[shortcode] = {
                        'fecha_procesado': datetime.now().isoformat(),
                        'instagram_url': post['url'],
                        'tweet_id': tweet_id,
                        'tweet_url': f"https://twitter.com/i/web/status/{tweet_id}",
                        'caption': post['caption'][:200],
                        'tipo': 'video' if post['is_video'] else 'imagen',
                        'archivos_descargados': media_files
                    }
                    self.save_historial()

                    print(f"\n{'='*50}")
                    print(f"✅ POST PUBLICADO EXITOSAMENTE")
                    print(f"{'='*50}")
                    print(f"Instagram: {post['url']}")
                    print(f"Twitter: https://twitter.com/i/web/status/{tweet_id}")
                    print(f"{'='*50}\n")

                else:
                    print(f"❌ Error publicando en Twitter")

                # Delay entre posts para no saturar
                time.sleep(5)

            if nuevos_posts == 0:
                print("ℹ️  No hay posts nuevos para procesar")
            else:
                print(f"\n✨ Procesados {nuevos_posts} posts nuevos")

        except Exception as e:
            print(f"\n❌ Error durante el procesamiento: {e}")
            import traceback
            traceback.print_exc()

    def run_once(self):
        """Ejecuta el bot una sola vez"""
        self.process_new_posts()

    def run_loop(self, interval_minutes=None):
        """
        Ejecuta el bot en loop continuo

        Args:
            interval_minutes: Intervalo en minutos (usa config si no se especifica)
        """
        interval = interval_minutes or config.CHECK_INTERVAL

        print(f"\n🔄 Bot en modo continuo")
        print(f"⏱️  Verificando cada {interval} minutos")
        print(f"⌨️  Presiona Ctrl+C para detener\n")

        try:
            while True:
                self.process_new_posts()

                print(f"\n⏳ Esperando {interval} minutos hasta la próxima verificación...")
                print(f"   Próxima ejecución: {self._get_next_run_time(interval)}")
                print(f"   (Presiona Ctrl+C para detener)\n")

                time.sleep(interval * 60)

        except KeyboardInterrupt:
            print(f"\n\n{'='*50}")
            print("🛑 Bot detenido por el usuario")
            print(f"{'='*50}")
            print(f"Posts procesados en esta sesión: {len(self.historial)}")
            print("¡Hasta luego! 👋\n")

    def _get_next_run_time(self, minutes):
        """Calcula la hora de la próxima ejecución"""
        from datetime import datetime, timedelta
        next_time = datetime.now() + timedelta(minutes=minutes)
        return next_time.strftime('%H:%M:%S')

    def show_stats(self):
        """Muestra estadísticas del bot"""
        print(f"\n{'='*50}")
        print("📊 ESTADÍSTICAS DEL BOT")
        print(f"{'='*50}")
        print(f"Total de posts procesados: {len(self.historial)}")

        if self.historial:
            print(f"\nÚltimos 5 posts:")
            for i, (shortcode, data) in enumerate(list(self.historial.items())[-5:], 1):
                print(f"\n{i}. Post {shortcode}")
                print(f"   Fecha: {data['fecha_procesado']}")
                print(f"   Instagram: {data['instagram_url']}")
                print(f"   Twitter: {data['tweet_url']}")

        print(f"{'='*50}\n")


def main():
    """Función principal"""
    # Verificar configuración
    if config.INSTAGRAM_USERNAME == "tu_usuario_instagram":
        print("❌ ERROR: Configura tu usuario de Instagram en config.py")
        return

    if config.TWITTER_API_KEY == "tu_api_key":
        print("❌ ERROR: Configura tus credenciales de Twitter en config.py")
        return

    # Crear bot
    bot = InstagramTwitterBot()

    # Verificar credenciales de Twitter
    if not bot.twitter.verify_credentials():
        print("❌ ERROR: Credenciales de Twitter inválidas")
        return

    # Mostrar menú
    print("\n╔════════════════════════════════════════╗")
    print("║  Bot Instagram → Twitter               ║")
    print("╚════════════════════════════════════════╝")
    print("\n¿Cómo quieres ejecutar el bot?")
    print("\n1. Ejecutar UNA VEZ (revisar ahora)")
    print("2. Ejecutar en LOOP (cada X minutos)")
    print("3. Ver ESTADÍSTICAS")
    print("4. Salir")

    choice = input("\nElige una opción (1-4): ").strip()

    if choice == "1":
        bot.run_once()
    elif choice == "2":
        minutes = input(f"¿Cada cuántos minutos? (default: {config.CHECK_INTERVAL}): ").strip()
        interval = int(minutes) if minutes else config.CHECK_INTERVAL
        bot.run_loop(interval_minutes=interval)
    elif choice == "3":
        bot.show_stats()
    elif choice == "4":
        print("👋 ¡Hasta luego!")
    else:
        print("❌ Opción inválida")


if __name__ == "__main__":
    main()
