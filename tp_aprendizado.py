# -*- coding: utf-8 -*-

from optparse import OptionParser

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

# Opções da linha de comando
verbose = False
gerar_arvore = False

def anime_to_dict(usuario, anime, atributos_anime = atributos_anime_padrao, atributos_avaliacao = atributos_avaliacao_padrao, f_selecao = None):
	dado = {}
	dado_filtrado = {}

	# Pegando os dados do anime
	for atributo in atributos_anime_todos:
		dado[atributo] = anime.__dict__[atributo]

	if "user_score" not in atributos_avaliacao:
		atributos_avaliacao.append("user_score")
	# Pegando os dados da avaliação
	try:
		with open("data/users/" + usuario + "/" + str(anime.id) + ".json") as f:
			avaliacao = json.loads(f.read())
	except:
		avaliacao = {
			"user_name": usuario,
			"num_watched_episodes": 0,
			"user_score": None,
			"status": int(crawler.Status.plan)
		}

	for atributo in atributos_avaliacao_todos:
		dado[atributo] = avaliacao[atributo]
	
	if f_selecao == None or f_selecao(dado) == True:
		for atributo in atributos_anime:
			if atributo == "genres":
				for genero in generos:
					try:
						genero_bool = "Genre:" + super_generos[genero]
					except:
						print genero + "n ta na lista de super generos?"
						print anime.id
						exit()
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
					dado_filtrado[atributo] = 0
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
		
		return dado_filtrado
	
	return None

def anime_to_df(usuario, anime, atributos_anime = atributos_anime_padrao, atributos_avaliacao = atributos_avaliacao_padrao, f_selecao = None):
	anime_dict = anime_to_dict(usuario, anime, atributos_anime, atributos_avaliacao, f_selecao)
	anime_dict_json = "[" + json.dumps(anime_dict, indent=4) + "]"

	df = pd.read_json(anime_dict_json)
	df = df.iloc[[0]]

	data = df.drop('user_score', axis = 1)

	le = preprocessing.LabelEncoder()
	for attr in data.columns:
		if data[attr].dtype == object:
			data[attr] = le.fit_transform(data[attr])
	
	return data

def filtro(usuario, f_selecao, atributos_anime = atributos_anime_padrao, atributos_avaliacao = atributos_avaliacao_padrao, force_update = False):
	dados = []
	lista_animes = crawler.get_lista(usuario)
    
	#print lista_animes

	global generos
	global estudios

	for anime in lista_animes:
		if anime.genres != None and "No genres have been added yet." not in anime.genres:
			generos.extend(anime.genres)
		if anime.studios != None:
			estudios.extend(anime.studios)

	# Removendo cópias
	generos = list(set(generos))
	estudios = list(set(estudios))

	for anime in lista_animes:
		dado = anime_to_dict(usuario, anime, atributos_anime, atributos_avaliacao, f_selecao)
		if dado != None:
			dados.append(dado)

	return dados

def carregar_dataset(usuario, f_selecao, atributos_anime = atributos_anime_padrao, atributos_avaliacao = atributos_avaliacao_padrao, force_update = False):
	lista_final = filtro(usuario, f_selecao, atributos_anime, atributos_avaliacao, force_update)

	df = pd.read_json(json.dumps(lista_final))

	target = df['user_score']
	data = df.drop('user_score', axis = 1)

	le = preprocessing.LabelEncoder()
	for attr in data.columns:
		if data[attr].dtype == object:
			data[attr] = le.fit_transform(data[attr])
	
	return data, target

def selecao_completos(anime_dict):
	return anime_dict["status"] == 2 or anime_dict["status"] == "2"

def arvore_decisao(usuario, anime, atributos_anime = atributos_anime_padrao, atributos_avaliacao = atributos_avaliacao_padrao, f_selecao = selecao_completos, force_update = False):
	# Carregar Dataset
	x, y = carregar_dataset(usuario, f_selecao, atributos_anime, atributos_avaliacao, force_update)

	if verbose:
		cont = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

		for c in y.values:
			cont[c] += 1

		for i in range(11):
			print i, " - ", class_names[i] + ": ", cont[i]

	# Criar classificador
	from sklearn import tree                    # Importa o pacote de arvore de decisao
	clf = tree.DecisionTreeClassifier()         # Cria classificador

	# Criar Grid Search Cross Validation
	from sklearn.model_selection import GridSearchCV
	parameters = {'max_depth': range(2, 20)}
	best_clf = GridSearchCV(clf, parameters)
	best_clf.fit(x, y)

	# Resultados
	means = best_clf.cv_results_['mean_test_score']
	stds = best_clf.cv_results_['std_test_score']
	if verbose:
		for mean, std, params in zip(means, stds, best_clf.cv_results_['params']):
			print("%0.3f (+/-%0.03f) for %r"
				% (mean, std * 2, params))
		
		print 'Melhor max_depth:', best_clf.best_params_['max_depth']

	# Apresentacao dos resultados
	if verbose:
		max_depth = best_clf.best_params_['max_depth']
		print 'Accuracy: %0.2f (+/- %0.2f)' % (means[max_depth], stds[max_depth] * 2)

	# Visualizacao da Arvore do Modelo 1
	if gerar_arvore:
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
	
	return best_clf

def mlp(usuario, anime, atributos_anime = atributos_anime_padrao, atributos_avaliacao = atributos_avaliacao_padrao, f_selecao = selecao_completos, force_update = False):
	from sklearn.preprocessing import StandardScaler
	from sklearn.neural_network import MLPClassifier
	from sklearn.metrics import classification_report,confusion_matrix
	
	# Carregar Dataset
	X, y = carregar_dataset(usuario, f_selecao, atributos_anime, atributos_avaliacao, force_update)

	X_train, X_test, y_train, y_test = train_test_split(X, y)

	scaler = StandardScaler()

	# Fit only to the training data
	scaler.fit(X_train)

	StandardScaler(copy=True, with_mean=True, with_std=True)

	# Now apply the transformations to the data:
	X_train = scaler.transform(X_train)
	X_test = scaler.transform(X_test)

	mlp = MLPClassifier(hidden_layer_sizes=(13,13,13),max_iter=500)
	mlp.fit(X_train,y_train)

	return mlp

if __name__ == "__main__":
	# Option handling
	parser = OptionParser()
	parser.add_option("-q", action = "store_false", dest = "verbose", default = True)
	parser.add_option("-u", "--usuario", dest = "usuario")
	parser.add_option("-a", "--anime", dest = "anime_url")
	parser.add_option("-m", "--metodo", dest = "metodo")
	parser.add_option("-f", "--force_update", action="store_true", dest="force_update", default = False)

	(options, args) = parser.parse_args()

	verbose = options.verbose
	usuario = options.usuario
	anime_url = options.anime_url
	metodo = options.metodo
	force_update = options.force_update

	if metodo == None:
		print "Método necessário"
		exit()

	metodos = {
		"arvore": arvore_decisao,
		"mlp": mlp
	}
	anime = crawler.Anime.from_url(anime_url, True)
	preditor = metodos[metodo](usuario, anime, force_update=force_update)

	anime_df = anime_to_df(usuario, anime)

	nota = preditor.predict(anime_df.values)
	if verbose:
		print nota[0]

	with open("nota.txt", "w") as f:
		saida_json = '{"nota": ' + str(nota[0]) + ', "anime": ' + json.dumps(anime.__dict__) + '}'
		f.write(saida_json)
