# -*- coding: utf-8 -*-
"""
SQLite Database Models for Social Media Dashboard
Schema for posts, analytics, and bot runs
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from pathlib import Path

# Base para modelos
Base = declarative_base()

# Path al archivo de base de datos
DB_PATH = Path(__file__).parent.parent.parent / 'data' / 'analytics.db'
DB_PATH.parent.mkdir(exist_ok=True)

# Engine de SQLite
engine = create_engine(
    f'sqlite:///{DB_PATH}',
    echo=False,  # Cambiar a True para debugging
    connect_args={'check_same_thread': False}  # Necesario para Streamlit
)

# Session factory
Session = sessionmaker(bind=engine)


class Post(Base):
    """Modelo de Posts procesados"""
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    shortcode = Column(String(20), unique=True, nullable=False, index=True)
    platform_source = Column(String(20), nullable=False)  # 'instagram'
    platform_target = Column(String(20), nullable=False)  # 'twitter', 'facebook'
    post_url = Column(String(500))
    caption = Column(Text)
    post_type = Column(String(10))  # 'image', 'video'
    media_urls = Column(Text)  # JSON array serializado
    created_at = Column(DateTime, nullable=False, index=True)
    processed_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String(20), default='success')  # 'success', 'failed', 'pending'

    # Relación con analytics
    analytics = relationship('Analytics', back_populates='post', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Post(shortcode='{self.shortcode}', platform='{self.platform_target}', status='{self.status}')>"


class Analytics(Base):
    """Modelo de Métricas de Engagement"""
    __tablename__ = 'analytics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False, index=True)
    platform = Column(String(20), nullable=False)  # 'instagram', 'twitter', 'facebook'
    metric_name = Column(String(50), nullable=False)  # 'likes', 'retweets', 'views', 'comments'
    metric_value = Column(Integer)
    collected_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    # Relación con post
    post = relationship('Post', back_populates='analytics')

    def __repr__(self):
        return f"<Analytics(post_id={self.post_id}, metric='{self.metric_name}', value={self.metric_value})>"


class BotRun(Base):
    """Modelo de Ejecuciones del Bot"""
    __tablename__ = 'bot_runs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    ended_at = Column(DateTime)
    status = Column(String(20))  # 'running', 'stopped', 'error'
    posts_processed = Column(Integer, default=0)
    errors_count = Column(Integer, default=0)
    error_message = Column(Text)

    def __repr__(self):
        return f"<BotRun(id={self.id}, status='{self.status}', posts={self.posts_processed})>"


# Crear todas las tablas
def init_db():
    """Inicializa la base de datos creando todas las tablas"""
    Base.metadata.create_all(engine)
    print(f"[OK] Database initialized at: {DB_PATH}")


# Función helper para obtener sesión
def get_session():
    """Retorna una nueva sesión de base de datos"""
    return Session()


# Inicializar DB al importar el módulo
if __name__ != "__main__":
    init_db()


# Si se ejecuta directamente, mostrar info
if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE SCHEMA INITIALIZATION")
    print("=" * 60)

    init_db()

    # Mostrar tablas creadas
    print("\nTablas creadas:")
    for table in Base.metadata.tables.keys():
        print(f"  + {table}")

    # Contar registros
    session = get_session()
    post_count = session.query(Post).count()
    analytics_count = session.query(Analytics).count()
    bot_runs_count = session.query(BotRun).count()
    session.close()

    print(f"\nRegistros actuales:")
    print(f"  Posts: {post_count}")
    print(f"  Analytics: {analytics_count}")
    print(f"  Bot Runs: {bot_runs_count}")
    print("\n" + "=" * 60)
