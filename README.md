---
title: YT Downloader API
emoji: 🎬
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

API para descargar audio y video de YouTube usando FastAPI y yt-dlp.

## Render

YouTube puede bloquear las IPs compartidas de Render. Las cookies ayudan, pero no
garantizan el acceso y deben mantenerse vigentes.

1. Exporta las cookies de `youtube.com` en formato **Netscape** (no JSON) desde
   un navegador donde YouTube funcione.
2. En Render, crea un **Secret File** llamado `cookies.txt`. El contenido debe
   comenzar con `# Netscape HTTP Cookie File`.
3. Despliega de nuevo. Render monta ese archivo en
   `/etc/secrets/cookies.txt`, que es la ruta usada por defecto.
4. Si usas otro nombre o ruta, define `YTDLP_COOKIE_FILE` con la ruta absoluta.

No subas `cookies.txt` al repositorio ni lo incluyas en la imagen Docker. Las
cookies son credenciales y pueden caducar o ser revocadas. Si el bloqueo
persiste con cookies válidas, es una restricción de YouTube contra la IP de
Render; no existe una solución 100% gratuita y garantizada desde ese proveedor.