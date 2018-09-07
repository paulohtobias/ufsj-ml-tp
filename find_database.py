# -*- coding: utf-8 -*-

import os
import sys
import crawler
import urllib2
from bs4 import BeautifulSoup as bs

# definicoes
MAL_URL = crawler.MAL_URL

def fill_database(start_page, num_pages):
	anime_links = []

	# Paginas a serem analisadas
	paginas = [x * 50 for x in range(start_page, start_page + num_pages)]

	for i in paginas:
		print "Pagina " + str(i / 50) + ": " + str(i)
		# Capturando a pagina do MyAnimeList
		url = MAL_URL + "/topanime.php?limit=" + str(i)
		try:
			response = urllib2.urlopen(url.encode("UTF-8"))
			pagina = response.read()
			soup = bs(pagina, "html5lib")
		except:
			print "Erro ao realizar request na pagina " + str(i / 50) 
			continue
		

		# Capturando todos os links com o link dos animes
		links = soup.find_all("a", {"class":"hoverinfo_trigger fl-l ml12 mr8"})

		# Adicionando lista de animes na pagina atual a 
		# lista global de animes
		anime_links.extend([x.get("href")[len(MAL_URL):] for x in links])

	overwrite_cache = False #Ignora um possível cache hit e força a atualização da cache.
	stop_on_error = False #Interrompe a execução da "thread" caso dê algum erro.
	
	# Debug
	k = 1
	pid = os.getpid()
	for link in anime_links:
		current_page = start_page + int((k - 1) / 50)
		link_index = k % 50
		info = "Page %d: %d/50 # %s" % (current_page, link_index, link)
		print "#%d | %s" % (pid, info)
		k += 1
		
		if crawler.Anime.from_url(link, overwrite_cache) == None:
			print "\033[91m#%d | Error on %s\033[0m" % (pid, info)
			log_dir = "log"
			if not(os.path.exists(log_dir)):
				os.makedirs(log_dir)
			with open("%s/p_%04d.txt" % (log_dir, current_page), "a") as f:
				f.write(info.encode('utf8') + "\n")
			
			if stop_on_error == True:
				exit(1)

if __name__ == "__main__":
	pagina_inicial = int(sys.argv[1])
	qtd_paginas = int(sys.argv[2])
	fill_database(pagina_inicial, qtd_paginas)
