import requests

# 📊 CONFIGURACIÓN DE TUS ENLACES:
URL_DISCORD_NOTICIAS = "https://discord.com/api/webhooks/1509192242563387455/V4hnU2XGCG8nt5YZUFAt7U6gUtaBq1eAawEL_w4w2o0WqE3rkPkah_XL7ozsTfdAKuhd"
API_KEY_NOTICIAS = "a3218623d03747de97b5e4b1643f1fd2"

def obtener_noticias_globales():
    # 🌟 CAMBIO CLAVE: Usamos 'everything' con palabras de búsqueda amplias en español y ordenado por popularidad
    url = f"https://newsapi.org/v2/everything?q=(mundo OR internacional OR global)&language=es&sortBy=popularity&pageSize=20&apiKey={API_KEY_NOTICIAS}"
    
    print("📰 Conectando con el satélite de noticias mundiales...")
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
                fuente = art.get("source", {}).get("name", "Mundo")
                
                # Descartamos si falta información clave o si la noticia fue removida
                if not titulo or not descripcion or "[Removed]" in titulo or "Removed" in descripcion:
                    continue
                
                # Recortamos la descripción si es exageradamente larga para que quepa en Discord
                if len(descripcion) > 200:
                    descripcion = descripcion[:197] + "..."
                
                # Diseñamos la tarjeta azul informativa
                embed = {
                    "title": f"📢 {titulo}",
                    "url": enlace,
                    "description": descripcion,
                    "color": 3447003,  # Azul informativo elegante
                    "thumbnail": {"url": imagen} if imagen else None,
                    "footer": {
                        "text": f"📰 Fuente: {fuente} • Gordobot Noticiero"
                    }
                }
                embeds.append(embed)
                contador += 1
                
                # Con 3 noticias de impacto es suficiente para el boletín
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
                print("⚠️ La API devolvió datos, pero ninguno pasó el filtro de calidad.")
                
        else:
            print(f"❌ Error con la API de noticias. Código: {respuesta.status_code}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    obtener_noticias_globales()