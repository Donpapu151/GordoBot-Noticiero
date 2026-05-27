import requests
from datetime import datetime

# 📊 CONFIGURACIÓN DE TUS ENLACES:
URL_DISCORD_NOTICIAS = "https://discord.com/api/webhooks/1509192242563387455/V4hnU2XGCG8nt5YZUFAt7U6gUtaBq1eAawEL_w4w2o0WqE3rkPkah_XL7ozsTfdAKuhd"
API_KEY_NOTICIAS = "a3218623d03747de97b5e4b1643f1fd2"

def obtener_noticias_globales():
    # Pedimos una tanda buena de 25 noticias populares del mundo
    url = f"https://newsapi.org/v2/everything?q=(mundo OR internacional OR global)&language=es&sortBy=popularity&pageSize=25&apiKey={API_KEY_NOTICIAS}"
    
    print("🎨 Diseñando boletín informativo ultra-estético...")
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
                autor = art.get("author", "Redacción")
                fecha_raw = art.get("publishedAt", "")
                
                # Descartamos si viene incompleto o roto
                if not titulo or not descripcion or "[Removed]" in titulo or "Removed" in descripcion:
                    continue
                
                # Estética 1: Formatear la fecha para que se vea limpia (Día/Mes/Año)
                try:
                    fecha_objeto = datetime.strptime(fecha_raw, "%Y-%m-%dT%H:%M:%SZ")
                    fecha_limpia = fecha_objeto.strftime("%d/%m/%Y")
                except:
                    fecha_limpia = "Reciente"
                
                # Estética 2: Limitar tamaño de textos para evitar saturar la vista
                if len(titulo) > 85:
                    titulo = titulo[:82] + "..."
                if len(descripcion) > 160:
                    descripcion = descripcion[:157] + "..."
                
                # Estética 3: Si el autor es una URL o es gigante, lo limpiamos
                if "http" in autor or len(autor) > 25:
                    autor = "Corresponsal"

                # 🎨 CONSTRUCCIÓN DE LA TARJETA PREMIUM
                embed = {
                    "author": {
                        "name": f"📰 {fuente.upper()}",
                        "icon_url": "https://i.imgur.com/wSTFk6v.png" # Icono estético de periódico para el encabezado
                    },
                    "title": titulo,
                    "url": enlace,
                    "description": f"*{descripcion}*", # Texto en cursiva para elegancia
                    "color": 2123412,  # Un azul oscuro sofisticado tipo Cyberpunk/Premium
                    "image": {"url": imagen} if imagen else None, # Imagen en grande abajo para máximo impacto visual
                    "fields": [
                        {
                            "name": "✍️ Autor",
                            "value": f"`{autor}`",
                            "inline": True
                        },
                        {
                            "name": "📅 Publicado",
                            "value": f"`{fecha_limpia}`",
                            "inline": True
                        }
                    ],
                    "footer": {
                        "text": "🌐 GORDOBOT NEWS • SISTEMA DE INFORMACIÓN GLOBAL 24/7",
                        "icon_url": "https://i.imgur.com/OcMRbT8.png" # Mini logo en el pie de página
                    }
                }
                
                embeds.append(embed)
                contador += 1
                
                # 🌟 ¡Subimos la dosis a las 5 mejores noticias del día!
                if contador >= 5:
                    break
            
            if embeds:
                payload = {
                    "content": "📡 ✨ **【 BOLETÍN GLOBAL DE ÚLTIMA HORA 】** ✨ 📡\n*Las 5 coberturas internacionales más destacadas e importantes del momento.*",
                    "embeds": embeds
                }
                requests.post(URL_DISCORD_NOTICIAS, json=payload)
                print("¡Boletín premium de 5 noticias enviado! 🎉")
            else:
                print("⚠️ No pasaron el filtro de calidad en esta tanda.")
        else:
            print(f"❌ Error API: {respuesta.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    obtener_noticias_globales()