import requests

URL_DISCORD_NOTICIAS = "https://discord.com/api/webhooks/1509192242563387455/V4hnU2XGCG8nt5YZUFAt7U6gUtaBq1eAawEL_w4w2o0WqE3rkPkah_XL7ozsTfdAKuhd"
# Las APIs de noticias suelen pedir una API Key gratuita que te dan al registrarte
API_KEY_NOTICIAS = "TU_API_KEY_AQUI" 

def obtener_noticias_globales():
    # Pedimos noticias internacionales en español ordenadas por relevancia
    url = f"https://newsapi.org/v2/top-headlines?language=es&pageSize=10&apiKey={API_KEY_NOTICIAS}"
    
    try:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            articulos = datos.get("articles", [])
            
            embeds = []
            # Tomamos solo las primeras 3 noticias de impacto
            for art in articulos[:3]:
                titulo = art.get("title")
                descripcion = art.get("description", "Sin descripción disponible.")
                enlace = art.get("url")
                imagen = art.get("urlToImage", "") # Foto de la noticia
                fuente = art.get("source", {}).get("name", "Noticias")
                
                # Diseñamos la tarjeta de la noticia
                embed = {
                    "title": f"📢 {titulo}",
                    "url": enlace,
                    "description": descripcion,
                    "color": 3447003, # Color azul informativo
                    "thumbnail": {"url": imagen},
                    "footer": {"text": f"Fuente: {fuente}"}
                }
                embeds.append(embed)
                
            payload = {
                "content": "🌍 📰 **¡EL REPORTE DE NOTICIAS INTERNACIONALES!** 📰 🌍",
                "embeds": embeds
            }
            
            requests.post(URL_DISCORD_NOTICIAS, json=payload)
            print("¡Noticias enviadas!")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    obtener_noticias_globales()