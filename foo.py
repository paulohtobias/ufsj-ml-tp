# -*- coding: utf-8 -*-

import os
intervalo = 5

pagina_inicio = 0
pagina_fim = pagina_inicio + 100

paginas = range(pagina_inicio, pagina_fim, intervalo)

paginas_faltando = sorted(map(lambda n: int(filter(str.isdigit, n)), os.listdir("log")))

if len(paginas_faltando) > 0:
	paginas = paginas_faltando

print pagina_inicio, pagina_fim, intervalo

for pagina_base in paginas_faltando:
	print "################### PAGINA BASE: " + str(pagina_base) + " ###################"
	comando = "./anime_crawler.sh %d %d" % (pagina_base, pagina_base + intervalo)
	
	os.system(comando)
	
	# Executa uma segunda vez para pegar os animes que faltam. É mais rápido.
	os.system(comando)
