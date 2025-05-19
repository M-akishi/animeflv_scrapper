# AnimeFLV Scrapper CLI

Este proyecto permite buscar y reproducir anime desde [AnimeFLV](https://www3.animeflv.net/) directamente en tu reproductor MPV

---

## Requisitos

* [Python 3.11 o superior](https://www.python.org/)
* [mpv](https://mpv.io/) (recomendado instalar con [Scoop](https://scoop.sh/))
* [yt-dlp](https://github.com/yt-dlp/yt-dlp) (también recomendado con Scoop)
* [Anime4K](https://github.com/bloc97/Anime4K) (para mejorar la resolucion)

---

## Instalación

1. Clona o descarga este repositorio:

   ```bash
   git clone https://github.com/tu-usuario/animeflv_scrapper.git
   cd animeflv_scrapper
   ```

2. (Opcional) Agrega la carpeta del proyecto al PATH poder ejecutar el comando desde cualquier ubicación:

   ```powershell
   .\agregar_al_path.ps1
   ```

   Esto registrará la ruta donde está el script `animeflv_cli.bat` en el PATH.

3. Prepara el entorno e instala dependencias, y lanza el scrapper con el archivo por lotes:

   ```bash
   .\animeflv_cli.bat
   ```

   El script hará lo siguiente:

   * Verificará y creará (si no existe) el entorno virtual (`venv`).
   * Activará el `venv` y, solo la primera vez, instalará las dependencias en `requirements.txt`.
   * Verificará que `mpv` y `yt-dlp` estén instalados; en caso contrario sugerirá instalarlos con Scoop.
   * Ejecutará `animeflv_cli.py` con los argumentos que pases.

---

## Uso

Con todo listo, puedes ejecutar:

```bash
animeflv_cli  # si agregaste al PATH
o
.\animeflv_cli.bat      # desde la carpeta del proyecto
```

## Y seguir las indicaciones para buscar tu serie, elegir capítulo y reproducirlo en MPV


## Licencia

Este proyecto es software libre y de código abierto bajo la licencia MIT.
