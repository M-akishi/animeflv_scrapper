from playwright.sync_api import sync_playwright
import re
import subprocess
import shutil
import sys

BASE_URL = "https://www3.animeflv.net"

def check_dependencies():
    for dep in ["mpv", "yt-dlp"]:
        if not shutil.which(dep):
            print(f"[ERROR] No se encontró '{dep}' en el PATH.")
            print(f"Por favor instala '{dep}', por ejemplo usando: scoop install {dep}")
            sys.exit(1)

def crear_navegador_headless():
    p = sync_playwright().start()
    browser = p.firefox.launch(headless=True)
    context = browser.new_context(user_agent="Mozilla/5.0")
    page = context.new_page()
    return p, browser, context, page

def buscar_series(nombre):
    p, browser, context, page = crear_navegador_headless()
    resultados = []
    try:
        url = f"{BASE_URL}/browse?q=" + nombre.replace(" ", "+")
        page.goto(url, timeout=15000)
        page.wait_for_selector("ul.ListAnimes li article.Anime", timeout=10000)
        articulos = page.query_selector_all("ul.ListAnimes li article.Anime")
        for a in articulos:
            titulo = a.query_selector("h3.Title").inner_text()
            href = a.query_selector("a").get_attribute("href")
            resultados.append({"titulo": titulo, "url": BASE_URL + href})
    except Exception as e:
        print(f"❌ Error al buscar series: {e}")
    finally:
        browser.close()
        p.stop()
    return resultados

def obtener_episodios(url_serie):
    p, browser, context, page = crear_navegador_headless()
    episodios = []
    try:
        page.goto(url_serie, timeout=15000)
        page.wait_for_selector("ul#episodeList li.fa-play-circle:not(.Next) a", timeout=10000)
        items = page.query_selector_all("ul#episodeList li.fa-play-circle:not(.Next) a")
        for item in items:
            titulo = item.query_selector("h3.Title").inner_text()
            p_text = item.query_selector("p").inner_text()
            match = re.search(r'Episodio\s+(\d+)', p_text, re.IGNORECASE)
            numero = match.group(1) if match else "Desconocido"
            href = item.get_attribute("href")
            episodios.append({"titulo": titulo, "numero": numero, "link": BASE_URL + href})
    except Exception as e:
        print(f"❌ Error al obtener episodios: {e}")
    finally:
        browser.close()
        p.stop()
    return episodios

def obtener_link_maru(url_episodio):
    p, browser, context, page = crear_navegador_headless()
    try:
        page.goto(url_episodio, timeout=15000)
        page.wait_for_selector("ul.CapiTnv li", timeout=10000)
        tabs = page.query_selector_all("ul.CapiTnv li")

        for tab in tabs:
            try:
                tab.click()
                page.wait_for_selector("div.CapiTcn div.tab-pane.active iframe", timeout=5000)
                iframe = page.query_selector("div.CapiTcn div.tab-pane.active iframe")
                src = iframe.get_attribute("src")
                if src.startswith("https://my.mail.ru"):
                    return src
            except:
                continue

        print("❌ No se encontró un iframe con host my.mail.ru.")
        return None
    except Exception as e:
        print(f"❌ Error al obtener link del episodio: {e}")
        return None
    finally:
        browser.close()
        p.stop()

def reproducir_en_mpv(url):
    try:
        subprocess.run(["mpv", url], check=True)
    except FileNotFoundError:
        print("Error: mpv no está instalado o no está en el PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar mpv: {e}")

def main():
    while True:
        nombre = input("\nIntroduce el nombre de la serie para buscar (o Enter para salir): ").strip()
        if not nombre:
            print("Saliendo del programa.")
            break

        resultados = buscar_series(nombre)
        if not resultados:
            print("No se encontraron resultados.")
            continue

        print("\nResultados encontrados:")
        for i, serie in enumerate(resultados, 1):
            print(f"{i}. {serie['titulo']}")

        eleccion = input("\nElige la serie (número): ").strip()
        if not eleccion.isdigit() or not (1 <= int(eleccion) <= len(resultados)):
            print("Elección inválida.")
            continue

        url_serie = resultados[int(eleccion) - 1]["url"]
        episodios = obtener_episodios(url_serie)

        if not episodios:
            print("No se encontraron episodios.")
            continue

        while True:
            print("\nLista de episodios:")
            for ep in episodios:
                print(f"{ep['numero']}: {ep['titulo']}")

            numero = input("\nIngresa el número del episodio que quieres ver (Enter para volver a buscar otra serie): ").strip()
            if not numero:
                break

            if not numero.isdigit():
                print("Entrada inválida.")
                continue

            episodio = next((ep for ep in episodios if ep["numero"] == numero), None)
            if not episodio:
                print("Episodio no encontrado.")
                continue

            print(f"\nObteniendo enlace Maru del episodio {numero}...")
            link_maru = obtener_link_maru(episodio["link"])
            if link_maru:
                reproducir_en_mpv(link_maru)
            else:
                print("No se encontró el enlace Maru para este episodio.")

if __name__ == "__main__":
    check_dependencies()
    main()
