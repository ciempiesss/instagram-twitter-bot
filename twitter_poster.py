# -*- coding: utf-8 -*-
"""
Módulo para publicar en Twitter
Usa Tweepy con API v2
"""
import sys
import io

# Fix UTF-8 para Windows (solo si es necesario)
if hasattr(sys.stdout, 'buffer') and not isinstance(sys.stdout, io.TextIOWrapper):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass

import tweepy
from pathlib import Path
import os

class TwitterPoster:
    def __init__(self, api_key, api_secret, access_token, access_secret, bearer_token=None):
        """
        Inicializa el cliente de Twitter

        Args:
            api_key: Consumer API Key
            api_secret: Consumer API Secret
            access_token: Access Token
            access_secret: Access Token Secret
            bearer_token: Bearer Token (opcional, para API v2)
        """
        # Cliente API v2 (para crear tweets)
        self.client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret,
            wait_on_rate_limit=True
        )

        # API v1.1 (necesaria para subir media)
        auth = tweepy.OAuth1UserHandler(
            api_key, api_secret, access_token, access_secret
        )
        self.api_v1 = tweepy.API(auth, wait_on_rate_limit=True)

        print("[OK] Cliente de Twitter inicializado")

    def upload_media(self, file_path):
        """
        Sube un archivo (imagen o video) a Twitter

        Args:
            file_path: Ruta al archivo

        Returns:
            Media ID de Twitter
        """
        try:
            file_path = Path(file_path)

            if not file_path.exists():
                print(f"❌ Archivo no encontrado: {file_path}")
                return None

            # Determinar si es video o imagen
            is_video = file_path.suffix.lower() in ['.mp4', '.mov', '.avi']

            print(f"📤 Subiendo {'video' if is_video else 'imagen'}: {file_path.name}...")

            if is_video:
                # Para videos, especificar categoría
                media = self.api_v1.media_upload(
                    filename=str(file_path),
                    media_category='tweet_video'
                )
            else:
                # Para imágenes
                media = self.api_v1.media_upload(filename=str(file_path))

            print(f"✅ Media subido con ID: {media.media_id}")
            return media.media_id

        except Exception as e:
            print(f"❌ Error subiendo media: {e}")
            return None

    def create_tweet(self, text, media_ids=None):
        """
        Crea un tweet

        Args:
            text: Texto del tweet
            media_ids: Lista de media IDs (opcional)

        Returns:
            ID del tweet creado
        """
        try:
            # Asegurar que el texto no exceda 280 caracteres
            if len(text) > 280:
                text = text[:277] + "..."

            print(f"🐦 Creando tweet...")
            print(f"   Texto: {text[:100]}...")

            # Crear tweet
            response = self.client.create_tweet(
                text=text,
                media_ids=media_ids
            )

            tweet_id = response.data['id']
            tweet_url = f"https://twitter.com/i/web/status/{tweet_id}"

            print(f"✅ Tweet publicado: {tweet_url}")
            return tweet_id

        except Exception as e:
            print(f"❌ Error creando tweet: {e}")
            return None

    def post_with_media(self, text, media_files):
        """
        Publica tweet con imágenes o video

        Args:
            text: Texto del tweet
            media_files: Lista de rutas de archivos (máximo 4 imágenes o 1 video)

        Returns:
            ID del tweet
        """
        if not media_files:
            # Si no hay media, solo texto
            return self.create_tweet(text)

        # Subir todos los archivos media
        media_ids = []

        for file_path in media_files:
            media_id = self.upload_media(file_path)
            if media_id:
                media_ids.append(media_id)

                # Twitter permite máximo 4 imágenes o 1 video
                if len(media_ids) >= 4:
                    break

        if not media_ids:
            print("⚠️ No se pudo subir ningún archivo, publicando solo texto")
            return self.create_tweet(text)

        # Crear tweet con media
        return self.create_tweet(text, media_ids=media_ids)

    def verify_credentials(self):
        """
        Verifica que las credenciales sean válidas

        Returns:
            True si son válidas, False si no
        """
        try:
            user = self.api_v1.verify_credentials()
            print(f"✅ Autenticado como: @{user.screen_name}")
            return True
        except Exception as e:
            print(f"❌ Error de autenticación: {e}")
            return False


# Prueba del módulo
if __name__ == "__main__":
    # IMPORTANTE: Reemplaza con tus credenciales reales
    poster = TwitterPoster(
        api_key="tu_api_key",
        api_secret="tu_api_secret",
        access_token="tu_access_token",
        access_secret="tu_access_secret"
    )

    # Verificar credenciales
    if poster.verify_credentials():
        # Ejemplo: publicar tweet de prueba
        # poster.create_tweet("Tweet de prueba desde Python!")

        # Ejemplo: publicar con imagen
        # poster.post_with_media(
        #     text="Mi primer tweet con imagen desde Python!",
        #     media_files=["ruta/a/tu/imagen.jpg"]
        # )
        pass
