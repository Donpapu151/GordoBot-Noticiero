import requests

# 📊 CONFIGURACIÓN DE TUS ENLACES (Pega tus datos dentro de las comillas):
URL_DISCORD_NOTICIAS = "https://discord.com/api/webhooks/1509192242563387455/V4hnU2XGCG8nt5YZUFAt7U6gUtaBq1eAawEL_w4w2o0WqE3rkPkah_XL7ozsTfdAKuhd" # <-- Pon aquí tu webhook completo
API_KEY_NOTICIAS = "a3218623d03747de97b5e4b1643f1fd2" # <-- Pon aquí tu clave de NewsAPI sin corchetes ni llaves

def obtener_noticias_globales():
    # Buscamos las noticias más importantes de impacto general en español
    url = f"https://newsapi.org/v2/top-headlines?language=es&pageSize=15&apiKey={API_KEY_NOTICIAS}"
    
    print("📰 Conectando con las agencias de noticias internacionales...")
    try:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            articulos = datos.get("articles", [])
            
            embeds = []
            contador = 0
            
            for art in articulos:
                titulo = art.get("title")
                descripcion = art.get("description")
                enlace = art.get("url")
                imagen = art.get("urlToImage")
                fuente = art.get("source", {}).get("name", "Internacional")
                
                # Nos saltamos noticias rotas, eliminadas o vacías
                if not titulo or not descripcion or "[Removed]" in titulo or "Removed" in descripcion:
                    continue
                
                # Diseñamos la tarjeta azul estética
                embed = {
                    "title": f"📢 {titulo}",
                    "url": enlace,
                    "description": descripcion,
                    "color": 3447003, # Azul informativo
                    "thumbnail": {"url": imagen} if imagen else None,
                    "footer": {
                        "text": f"📰 Fuente: {fuente} • Gordobot Noticiero"
                    }
                }
                embeds.append(embed)
                contador += 1
                
                # Mandamos las 3 más importantes
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
                print("⚠️ No se encontraron noticias válidas filtradas en esta tanda de la API.")
                
        else:
            print(f"❌ Error con la API de noticias. Código: {respuesta.status_code}")
            print("Verifica que tu API_KEY_NOTICIAS esté bien copiada y no tenga espacios.")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    obtener_noticias_globales()