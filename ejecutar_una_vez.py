# -*- coding: utf-8 -*-
"""
Ejecuta el bot UNA sola vez (sin menú interactivo)
"""
import sys
import io
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except:
    pass

from main import InstagramTwitterBot

print("\n" + "=" * 60)
print("BOT INSTAGRAM → TWITTER - EJECUCIÓN DE PRUEBA")
print("=" * 60)

try:
    bot = InstagramTwitterBot()

    # Verificar Twitter
    if not bot.twitter.verify_credentials():
        print("\n❌ ERROR: Credenciales de Twitter inválidas")
        sys.exit(1)

    print("\n✅ Todo configurado correctamente!")
    print("\n🔍 Buscando posts nuevos en Instagram...")
    print("=" * 60)

    # Ejecutar UNA vez
    bot.run_once()

    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 60)

    # Mostrar estadísticas
    bot.show_stats()

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
