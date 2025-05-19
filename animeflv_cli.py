from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import re
import os
import subprocess

def crear_driver_headless():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    service = Service()
    service.creationflags = subprocess.CREATE_NO_WINDOW
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def buscar_series(nombre):
    driver = crear_driver_headless()
    driver.get("https://www3.animeflv.net/browse?q=" + nombre.replace(" ", "+"))
    time.sleep(5)
    resultados = []
    try:
        articulos = driver.find_elements(By.CSS_SELECTOR, "ul.ListAnimes li article.Anime")
        for a in articulos:
            titulo = a.find_element(By.CSS_SELECTOR, "h3.Title").text
            url = a.find_element(By.TAG_NAME, "a").get_attribute("href")
            resultados.append({"titulo": titulo, "url": url})
    finally:
        driver.quit()
    return resultados

def obtener_episodios(url_serie):
    driver = crear_driver_headless()
    driver.get(url_serie)
    time.sleep(5)
    episodios = []
    try:
        items = driver.find_elements(By.CSS_SELECTOR, "ul#episodeList li.fa-play-circle:not(.Next) a")
        for item in items:
            titulo = item.find_element(By.CSS_SELECTOR, "h3.Title").text
            p_text = item.find_element(By.CSS_SELECTOR, "p").text
            match = re.search(r'Episodio\s+(\d+)', p_text, re.IGNORECASE)
            numero = match.group(1) if match else "Desconocido"
            link = item.get_attribute("href")
            episodios.append({"titulo": titulo, "numero": numero, "link": link})
    finally:
        driver.quit()
    return episodios

def obtener_link_maru(url_episodio):
    driver = crear_driver_headless()
    driver.get(url_episodio)
    time.sleep(5)
    try:
        tabs = driver.find_elements(By.CSS_SELECTOR, 'ul.CapiTnv li')
        for tab in tabs:
            tooltip = tab.get_attribute('data-original-title') or tab.get_attribute('title')
            if tooltip and 'maru' in tooltip.strip().lower():
                tab.click()
                time.sleep(2)
                iframe = driver.find_element(By.CSS_SELECTOR, 'div.CapiTcn.tab-content div[role="tabpanel"].tab-pane.active iframe')
                return iframe.get_attribute('src')
        return None
    finally:
        driver.quit()

def reproducir_en_mpv(url):
    try:
        subprocess.run(["mpv", url], check=True)
    except FileNotFoundError:
        print("Error: mpv no está instalado o no está en el PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar mpv: {e}")

def main():
    nombre = input("Introduce el nombre de la serie para buscar: ").strip()
    resultados = buscar_series(nombre)

    if not resultados:
        print("No se encontraron resultados.")
        return

    print("\nResultados encontrados:")
    for i, serie in enumerate(resultados, 1):
        print(f"{i}. {serie['titulo']}")

    eleccion = input("\nElige la serie (número): ").strip()
    if not eleccion.isdigit() or not (1 <= int(eleccion) <= len(resultados)):
        print("Elección inválida.")
        return

    url_serie = resultados[int(eleccion) - 1]["url"]
    episodios = obtener_episodios(url_serie)

    if not episodios:
        print("No se encontraron episodios.")
        return

    print("\nLista de episodios:")
    for ep in episodios:
        print(f"{ep['numero']}: {ep['titulo']} -> {ep['link']}")

    numero = input("\nIngresa el número del episodio que quieres ver (o Enter para salir): ").strip()
    if not numero.isdigit():
        print("Entrada inválida o vacía. Saliendo.")
        return

    episodio = next((ep for ep in episodios if ep["numero"] == numero), None)
    if not episodio:
        print("Episodio no encontrado.")
        return

    print(f"\nObteniendo enlace Maru del episodio {numero}...")
    link_maru = obtener_link_maru(episodio["link"])
    if link_maru:
        reproducir_en_mpv(link_maru)
    else:
        print("No se encontró el enlace Maru para este episodio.")

if __name__ == "__main__":
    main()
