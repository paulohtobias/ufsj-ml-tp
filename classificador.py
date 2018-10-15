# -*- coding: utf-8 -*-

import json
import crawler
import pandas as pd

class_names = ["No Score", "Appalling", "Horrible", "Very Bad", "Bad", "Average", "Fine", "Good", "Very Good", "Great", "Masterpiece"]

# Listas com todos os atributos disponíveis
atributos_anime_todos = ["title", "duration", "episodes", "genres", "popularity", "public_score", "rank", "rating", "source", "studios", "type", "year"]
atributos_avaliacao_todos = ["num_watched_episodes", "user_score", "status"]

# Listas com alguns atributos mais relevantes
atributos_anime_padrao = ["duration", "episodes", "genres", "type", "year"]
atributos_avaliacao_padrao = ["user_score"]

def filtro(usuario, f_selecao, atributos_anime = atributos_anime_padrao, atributos_avaliacao = atributos_avaliacao_padrao, agrupar_episodios = False, force_update = False):
	if "user_score" not in atributos_avaliacao:
		atributos_avaliacao.append("user_score")

	dados = []
	lista_animes = crawler.get_lista(usuario)

	generos = []
	estudios = []
	for anime in lista_animes:
		if anime.genres != None:
			generos.extend(anime.genres)
		if anime.studios != None:
			estudios.extend(anime.studios)

	generos = list(set(generos))
	estudios = list(set(estudios))

	for anime in lista_animes:
		dado = {}
		dado_filtrado = {}

		# Pegando os dados do anime
		for atributo in atributos_anime_todos:
			dado[atributo] = anime.__dict__[atributo]

		# Pegando os dados da avaliação
		with open("data/users/" + usuario + "/" + str(anime.id) + ".json") as f:
			avaliacao = json.loads(f.read())

			for atributo in atributos_avaliacao_todos:
				dado[atributo] = avaliacao[atributo]

		if f_selecao == None or f_selecao(dado):
			dado_filtrado = {}
			
			for atributo in atributos_anime:
				if atributo == "genres":
					for genero in generos:
						if genero in dado["genres"]:
							dado_filtrado["Genre:" + genero] = 1
						else:
							dado_filtrado["Genre:" + genero] = -1
					continue

				if atributo == "studios":
					for estudio in estudios:
						if estudio in dado["studios"]:
							dado_filtrado["Studio:" + estudio] = 1
						else:
							dado_filtrado["Studio:" + estudio] = -1
					continue

				if agrupar_episodios and "episodes" in atributo:
					try:
						epis = int(dado[atributo])
						if epis <= 6:
							dado_filtrado[atributo] = 1
						elif epis <= 14:
							dado_filtrado[atributo] = 2
						elif epis <= 26:
							dado_filtrado[atributo] = 3
						elif epis <= 70:
							dado_filtrado[atributo] = 4
						else:
							dado_filtrado[atributo] = 5
					except:
						dado_filtrado[atributo] = dado[atributo]

			for atributo in atributos_avaliacao:
				dado_filtrado[atributo] = dado[atributo]

			dados.append(dado_filtrado)
	
	return dados


# params: "jusaragu", lambda d: d["status"] == 2, force_update=True

def carregar_dataset(usuario, f_selecao, atributos_anime = atributos_anime_padrao, atributos_avaliacao = atributos_avaliacao_padrao, agrupar_episodios = False, force_update = False):
	lista_final = filtro("jusaragu", lambda d: d["status"] == 2, force_update=True)

	df = pd.read_json(json.dumps(lista_final))

	target = df['user_score']
	data = df.drop('user_score', axis = 1)

	from sklearn import preprocessing
	le = preprocessing.LabelEncoder()
	for attr in data.columns:
		if data[attr].dtype == object:
			data[attr] = le.fit_transform(data[attr])
	
	return data, target

from sklearn import tree
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x_train, y_train)

# Visualizacao da Arvore
import graphviz
cn = []
for v in sorted(set(y_train.values)):
    cn.append(str(v) + ": " + class_names[v])
dot_data = tree.export_graphviz(clf, out_file=None,
     feature_names=x_train.columns,
     class_names=cn,
     filled=True, rounded=True,
     special_characters=True)
graph = graphviz.Source(dot_data, format='png')
graph.render('arvore', view=True)

# Teste da Arvore de Decisao
y_predicted = clf.predict(x_train)                # Realiza predicao no conjunto de testes

# Conferir os resultados das predicoes
import numpy as np                                  # Importa o pacote numpy, para consolidar os resultados
classes = np.array([y_train]).T                 # Obtem um array das classes indicadas na base, para concatenar
predicao = np.array([y_predicted]).T                # Obtem um array das predicoes na base, para concatenar
print np.concatenate(                               # Concatena os atributos, classe indicada e predicao do classificador
    (x_train, classes, predicao), axis=1)         # para cada instancia

# Avaliando o modelo criado
clf.score(x_train, y_train)                   # Utiliza a metrica padrao de avaliacao do classificador
