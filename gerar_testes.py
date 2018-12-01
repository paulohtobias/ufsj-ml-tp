# -*- coding: utf-8 -*-

import os
import random
import json

total_animes = 10
faixa = 0 # 0, 1 ou 2

def cn(nota):
	return int((nota - 1) / 2 + 1)

def ftol(arquivo):
	with open("data/animes/" + arquivo) as f:
		anime = json.loads(f.read())
		return anime["url"]
	raise Exception("Problema ao pegar a url de " + str(arquivo))

animes_dict = {}
print "Listando os animes da base..."
for (dirpath, dirnames, filenames) in os.walk("data/animes"):
	for arquivo in filenames:
		animes_dict[arquivo] = ftol(arquivo)
	print "feito."
	break

for (dirpath, dirnames, filenames) in os.walk("data/users"):
	usuarios = sorted(dirnames)
	
	inicio = len(usuarios) / 3 * faixa
	fim = min([inicio + len(usuarios) / 3, len(usuarios)])
	
	for usuario in usuarios[inicio:fim]:
		for (dirpath2, dirnames2, filenames2) in os.walk("data/users/" + usuario):
			avaliacoes = {}
			notas = [0] * 6
			notas_existentes = []
			for arquivo in filenames2:
				try:
					with open("data/users/" + usuario + "/" + arquivo) as f:
						avaliacao = json.loads(f.read())
						nota = cn(int(avaliacao["user_score"]))

						avaliacao["user_score"] = nota
						avaliacao["url"] = animes_dict[arquivo]
						
						notas[nota] += 1
						
						if avaliacoes.has_key(nota) == False:
							avaliacoes[nota] = []
							notas_existentes.append(nota)

						avaliacoes[nota].append(avaliacao)
				except:
					pass
			
			# Usuários com poucos animes serão desconsiderados.
			if sum(notas) < total_animes / 2 + 1:
				continue

			# Lista de animes que serão avaliados para o usuário.
			animes = []

			# Pegando animes avaliados
			for i in range(1, total_animes / 2 + 1):
				if notas[i] > 0:
					animes.append(random.choice(avaliacoes[i])["url"])
				else:
					animes.append(random.choice(avaliacoes[random.choice(notas_existentes)])["url"])

			# Pegando animes não avaliados
			for i in range(1, total_animes / 2 + 1):
				anime = random.choice(animes_dict.values())
				while anime in animes:
					anime = random.choice(animes_dict.values())
				animes.append(anime)
			for classificador in ["arvore", "mlp", "naive_bayes"]:
				print 'python2.7 tp_aprendizado.py -u "' + usuario + '" -m ' + classificador + ' -a "' + " ".join(animes) + '"'
			break
		break #apague
	break
