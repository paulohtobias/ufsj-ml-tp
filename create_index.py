# -*- coding: UTF-8 -*-
import os
import json

# Não adicion animes que existem 
def append_animes(anime_dict, index="index.json"):
	# Buscando o arquivo existente
	anime_index = {}
	try: anime_index = json.load(open(index,"r"))
	except: pass

	# Para todos os animes nao adicionados
	for anime in anime_dict.keys():
		if anime not in anime_index:
			anime_index[anime] = anime_dict[anime]

	anime_json = json.dumps(anime_index,indent=True)
	open(index, "w").write(anime_json.encode("utf8"))

def index_from_db(db_in='data/animes',db_out="index.json"):
	animes = {}

	for root, folder, files in os.walk(db_in):
		for elmnt in files:
			anime = json.load(open(os.path.join(root, elmnt)))
			animes[anime["title"]] = anime["id"];

	append_animes(animes,db_out)

index_from_db("./data/animes")