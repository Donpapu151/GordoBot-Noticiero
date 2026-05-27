import requests

# 📊 CONFIGURACIÓN DE TUS ENLACES:
URL_DISCORD_NOTICIAS = "https://discord.com/api/webhooks/1509192242563387455/V4hnU2XGCG8nt5YZUFAt7U6gUtaBq1eAawEL_w4w2o0WqE3rkPkah_XL7ozsTfdAKuhd"  # <-- Pega aquí el webhook de tu canal de noticias
API_KEY_NOTICIAS = "a3218623d03747de97b5e4b1643f1fd2"      # <-- Pega aquí la clave larga que acabas de copiar

def obtener_noticias_globales():
    # Buscamos las noticias más importantes (top-headlines) en español
    url = f"https://newsapi.org/v2/top-headlines?language=es&pageSize=10&apiKey={API_KEY_NOTICIAS}"
    
    print("📰 Conectando con las agencias de noticias internacionales...")
    try:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            articulos = datos.get("articles", [])
            
            embeds = []
            contador = 0
            
            for art in articulos:
                # Solo queremos noticias completas que tengan título y descripción
                titulo = art.get("title")
                descripcion = art.get("description")
                enlace = art.get("url")
                imagen = art.get("urlToImage")
                fuente = art.get("source", {}).get("name", "Internacional")
                
                # Si a la noticia le falta el título o el resumen, nos la saltamos
                if not titulo or not descripcion or "Removed" in titulo:
                    continue
                
                # Diseñamos una tarjeta informativa azul para cada nota
                embed = {
                    "title": f"📢 {titulo}",
                    "url": enlace,
                    "description": descripcion,
                    "color": 3447003,  # Azul informativo brillante
                    "thumbnail": {"url": imagen} if imagen else None,
                    "footer": {
                        "text": f"📰 Fuente: {fuente} • Gordobot Noticiero"
                    }
                }
                embeds.append(embed)
                contador += 1
                
                # Para no saturar el canal, mandamos solo las 3 notas más importantes del momento
                if contador >= 3:
                    break
            
            if embeds:
                payload = {
                    "content": "🌍 📰 **¡ÚLTIMA HORA: BOLETÍN INFORMATIVO GLOBAL!** 📰 🌍\n*Aquí tienes los acontecimientos más importantes del mundo en este momento:*",
                    "embeds": embeds
                }
                requests.post(URL_DISCORD_NOTICIAS, json=payload)
                print("¡Boletín de noticias enviado con éxito a Discord! 🎉")
            else:
                print("No se encontraron noticias válidas en este momento.")
                
        else:
            print(f"Error con la API de noticias. Código: {respuesta.status_code}")
            print("Revisa si tu API_KEY_NOTICIAS es correcta.")
            
    except Exception as e:
        print(f"Error de conexión: {e}")

if __name__ == "__main__":
    obtener_noticias_globales()