# -*- coding: utf-8 -*-

import sys
import crawler
import urllib2
from bs4 import BeautifulSoup as bs

#definicoes
MAL_URL = "https://myanimelist.net"

def fill_database(start_page, num_pages):
	anime_links = []

	for i in [x*50 for x in range(start_page,start_page + num_pages)]:
		# Capturando a pagina do MyAnimeList
		url = MAL_URL + "/topanime.php?limit=" + str(i)
		response = urllib2.urlopen(url.encode("UTF-8"))
		pagina = response.read()
		soup = bs(pagina, "html5lib")

		# Capturando todos os links com o link dos animes
		links = soup.find_all("a", {"class":"hoverinfo_trigger fl-l ml12 mr8"})

		# Adicionando lista de animes na pagina atual a 
		# lista global de animes
		anime_links.extend([x.get("href")[len(MAL_URL):] for x in links])

	return anime_links

if __name__ == "__main__":
	pagina_inicial = int(sys.argv[1])
	qtd_paginas = int(sys.argv[2])
	print fill_database(pagina_inicial, qtd_paginas)
