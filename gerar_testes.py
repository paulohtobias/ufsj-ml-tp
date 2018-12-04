# -*- coding: utf-8 -*-

import os
import random
import json
import subprocess

separador = ", "

faixa = 0 # 0, 1 ou 2
qtd_usuarios = 50

nmin = 0
try:
	with open("resultados.csv", "r") as f:
		nmin = int(f.readlines()[-2].split(separador)[0]) + 1
except:
	pass

nmax = nmin + qtd_usuarios

print nmin, nmax
#exit()

with open("resultados.csv", "a") as f:
	for classificador in ["arvore", "mlp", "naive_bayes"]:
		f.write(classificador + "\n")
		f.write(separador.join(["numero", "username", "quantity", "accuracy", "score", "time"]) + "\n")
		for (dirpath, dirnames, filenames) in os.walk("data/users"):
			usuarios = sorted(dirnames)
			
			inicio = len(usuarios) / 3 * faixa
			fim = min([inicio + len(usuarios) / 3, len(usuarios)])

			i = 0
			for usuario in usuarios[inicio:fim][nmin:nmax]:
				print 'python2.7 tp_aprendizado.py -u "' + usuario + '" -m ' + classificador
				
				try:
					resultado = str(i) + separador + usuario + separador
					resultado += subprocess.check_output(["python", "tp_aprendizado.py", "-u", usuario, "-m", classificador, "-q"]).replace("\n", separador)
					resultado += "\n"

					f.write(resultado)
				except Exception as e:
					print "Erro no usuário " + usuario,
					print e

				i += 1

				#break #apague
			break
		f.write("\n")
