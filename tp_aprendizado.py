# -*- coding: utf-8 -*-

# Importa o pacote train_test_split
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

# Cria classificador
from sklearn import tree                    # Importa o pacote de arvore de decisao
clf = tree.DecisionTreeClassifier()         # Cria classificador

#Importa o crawler
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

# Dicionário com os gêneros genéricos
generos = []
estudios = []
super_generos = {
	"Action": "Action",
	"Adventure": "Adventure",
	"Comedy": "Comedy",
	"Drama": "Drama",
	"Sci-Fi": "Sci-Fi",
	"Space": "Sci-Fi",
	"Fantasy": "Fantasy",
	"Magic": "Fantasy",
	"Romance": "Romance",
	"Shoujo": "Romance",
	"Super Power": "Fantasy",
	"Seinen": "Seinen",
	"Supernatural": "Fantasy",
	"Dementia": "Horror",
	"Horror": "Horror",
	"Mecha": "Sci-Fi",
	"Shounen": "Adventure",
	"Parody": "Comedy",
	"Historical": "Seinen",
	"Game": "Adventure",
	"Martial Arts": "Action",
	"Slice of Life": "Slice of Life",
	"School": "Slice of Life",
	"Music": "Slice of Life",
	"Psychological": "Thriller",
	"Hentai": "Adult",
	"Ecchi": "Adult",
	"Military": "Seinen",
	"Samurai": "Action",
	"Yaoi": "Adult",
	"Demons": "Fantasy",
	"Kids": "Kids",
	"Shoujo Ai": "Romance",
	"Harem": "Romance",
	"Mystery": "Thriller",
	"Vampire": "Fantasy",
	"Police": "Action",
	"Sports": "Sports",
	"Josei": "Seinen",
	"Thriller": "Thriller",
	"Shounen Ai": "Romance",
	"Cars": "Sports",
	"Yuri": "Adult"
}

def anime_to_df(usuario, anime, atributos_anime = atributos_anime_padrao, atributos_avaliacao = atributos_avaliacao_padrao):
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
	
	for atributo in atributos_anime:
		if atributo == "genres":
			for genero in generos:
				genero_bool = "Genre:" + super_generos[genero]
				if dado["genres"] != None and genero in dado["genres"]:
					dado_filtrado[genero_bool] = 1
				elif dado_filtrado.has_key(genero_bool) == False:
					dado_filtrado[genero_bool] = -1
			continue

		if atributo == "studios":
			for estudio in estudios:
				if dado["studios"] != None and estudio in dado["studios"]:
					dado_filtrado["Studio:" + estudio] = 1
				else:
					dado_filtrado["Studio:" + estudio] = -1
			continue

		if "episodes" in atributo:
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
				continue
			except:
				dado_filtrado[atributo] = dado[atributo]
				continue

		if dado[atributo] == None:
			dado_filtrado[atributo] = 0
		else:
			dado_filtrado[atributo] = dado[atributo]

	for atributo in atributos_avaliacao:
		if dado[atributo] == None:
			dado_filtrado[atributo] = 0
		else:
			dado_filtrado[atributo] = dado[atributo]
	
	dado_filtrado_json = "[" + json.dumps(dado_filtrado) + "]"
	df = pd.read_json(dado_filtrado_json)
	df = df.iloc[[0]]

	data = df.drop('user_score', axis = 1)

	le = preprocessing.LabelEncoder()
	for attr in data.columns:
		if data[attr].dtype == object:
			data[attr] = le.fit_transform(data[attr])
	
	return data

def filtro(usuario, f_selecao, atributos_anime = atributos_anime_padrao, atributos_avaliacao = atributos_avaliacao_padrao, agrupar_episodios = False, force_update = False):
	if "user_score" not in atributos_avaliacao:
		atributos_avaliacao.append("user_score")

	dados = []
	lista_animes = crawler.get_lista(usuario)
    
	#print lista_animes

	global generos
	global estudios

	for anime in lista_animes:
		if anime.genres != None:
			generos.extend(anime.genres)
		if anime.studios != None:
			estudios.extend(anime.studios)

	# Removendo cópias
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
						genero_bool = "Genre:" + super_generos[genero]
						if dado["genres"] != None and genero in dado["genres"]:
							dado_filtrado[genero_bool] = 1
						elif dado_filtrado.has_key(genero_bool) == False:
							dado_filtrado[genero_bool] = -1
					continue

				if atributo == "studios":
					for estudio in estudios:
						if dado["studios"] != None and estudio in dado["studios"]:
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
						continue
					except:
						dado_filtrado[atributo] = dado[atributo]
						continue

				if dado[atributo] == None:
					dado_filtrado[atributo] = 0
				else:
					dado_filtrado[atributo] = dado[atributo]

			for atributo in atributos_avaliacao:
				if dado[atributo] == None:
					dado_filtrado[atributo] = 0
				else:
					dado_filtrado[atributo] = dado[atributo]

			dados.append(dado_filtrado)

	return dados

def carregar_dataset(usuario, f_selecao, atributos_anime = atributos_anime_padrao, atributos_avaliacao = atributos_avaliacao_padrao, agrupar_episodios = False, force_update = False):
	lista_final = filtro(usuario, f_selecao, atributos_anime, atributos_avaliacao, agrupar_episodios, force_update)

	df = pd.read_json(json.dumps(lista_final))

	target = df['user_score']
	data = df.drop('user_score', axis = 1)

	from sklearn import preprocessing
	le = preprocessing.LabelEncoder()
	for attr in data.columns:
		if data[attr].dtype == object:
			data[attr] = le.fit_transform(data[attr])
	
	return data, target

def teste():
	usuario = "zarem101"
	x, y = carregar_dataset(usuario, lambda d: (d["status"] == 2 or d["status"] == "2"), force_update=False)
	anime = crawler.Anime.from_file(usuario, "43.json")
	anime_df = anime_to_df(usuario, anime)

	x_df = x.iloc[[27]]
	print x_df.columns
	print anime_df.columns
	#print x_df == anime_df


if __name__ == "__main__":
	teste()



























def bla():
	x, y = carregar_dataset("Master_Exploder", lambda d: d["status"] == 2 or d["status"] == "2", force_update=False)

	cont = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	for c in y.values:
		cont[c] += 1

	for i in range(11):
		print i, " - ", class_names[i] + ": ", cont[i]

	# MODELO 1

	# Dividir conjuntos de treinamento e teste
	x_train, x_test, y_train, y_test = train_test_split(    # Divide conjuntos nao-aleatoriamente
		x, y, shuffle=False)

	# Treinamento da Arvore de Decisao
	from sklearn import tree                    # Importa o pacote de arvore de decisao
	clf = tree.DecisionTreeClassifier()         # Cria classificador
	clf = clf.fit(x_train, y_train)             # Treina o classificador

	# Avaliacao dos resultados
	clf.score(x_test, y_test)

	# Calcula validacao cruzada
	from sklearn.model_selection import cross_val_score             # Importa o pacote de validacao cruzada
	scores = cross_val_score(clf, x, y, cv=3)                       # Calcula os scores de 5-folds estratificados
	print scores

	# Apresentacao dos resultados
	print 'Accuracy: %0.2f (+/- %0.2f)' % (scores.mean(), scores.std() * 2)

	# Visualizacao da Arvore do Modelo 1
	import graphviz

	cn = []
	for v in sorted(set(y_train.values)):
		cn.append(str(v) + ": " + class_names[v])

	dot_data = tree.export_graphviz(clf, out_file=None,
		feature_names=x.columns,
		class_names=cn,
		filled=True, rounded=True,
		special_characters=True)
	graph = graphviz.Source(dot_data, format='png')
	graph.render('modelo_1', view=True)