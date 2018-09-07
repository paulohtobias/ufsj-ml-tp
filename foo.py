# -*- coding: utf-8 -*-

import os
intervalo = 5

for pagina_base in range(0, 100, intervalo):
	print "################### PAGINA BASE: " + str(pagina_base) + " ###################"
	comando = "./anime_crawler.sh %d %d" % (pagina_base, pagina_base + intervalo)
	
	os.system(comando)
	
	# Executa uma segunda vez para pegar os animes que faltam. É mais rápido.
	os.system(comando)
