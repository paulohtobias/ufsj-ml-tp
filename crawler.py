# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import json
import datetime
import os

MAL_URL = "https://myanimelist.net"
ANIMES_PATH = "data/animes/"
usuario = "Zarem101"
USER_PATH = "data/users/" + usuario + "/"

class Avaliacao:
	def __init__(self, user_entry, id_anime):
		self.num_watched_episodes = user_entry["num_watched_episodes"]
		self.user_score = user_entry["score"] #LEMBRETE: score == 0 significa que ainda não foi avaliado.
		self.status = user_entry["status"]
		
		self.criar_nova_avaliacao(id_anime)
	
	def criar_nova_avaliacao(self, id_anime):
		file_json = json.dumps(self.__dict__, indent = 4)
		if not(os.path.exists(USER_PATH)):
			os.makedirs(USER_PATH)
		with open(USER_PATH + str(id_anime) + ".json", "w") as arq:
			arq.write(file_json)

class Anime:
	@staticmethod
	def from_url(url):
		anime.url = url

		#todo: pegar title, type, episodes, year, rating e id direto da página do anime

		anime.update_from_url()

		return anime

	@staticmethod
	def from_user_entry(user_entry):
		anime = Anime()

		anime.title = user_entry["anime_title"]
		anime.url = user_entry["anime_url"] #Pode ser usado como "hash" na cache
		anime.type = user_entry["anime_media_type_string"]
		anime.episodes = user_entry["anime_num_episodes"]
		anime.year = datetime.datetime.strptime(user_entry["anime_start_date_string"][-2:], "%y").year
		anime.rating = user_entry["anime_mpaa_rating_string"]
		anime.id = user_entry["anime_id"]
		
		#Criar nova avaliação do usuario para o anime
		Avaliacao(user_entry, anime.id)
		
		anime.update_from_url()

		return anime

	def update_from_url(self):
		#Verificar se o anime já está salvo na cache
		try:
			with open(ANIMES_PATH + str(self.id) + ".json", "r") as arquivo:
				#todo: isso é muito roubo e não sei se vai dar certo assim. Precisa testar mais.
				#Em último caso tem que setar cada atributo separadamente.
				self.__dict__ = json.loads(arquivo.read())
				return
		except:
			url = MAL_URL + self.url
			response = urllib2.urlopen(url.encode("UTF-8"))
			pagina = response.read()
			soup = BeautifulSoup(pagina, "html5lib")

			def get_info(atributo, is_list):
				tag = soup.find(string = atributo + ":").parent

				#Funções úteis
				strip = lambda t: t.string.strip(" ,\n")
				filtro = lambda s: len(s) > 0 and s not in ["None found", "add some"]

				if is_list:
					return filter(filtro, map(strip, list(tag.next_siblings)))
				else:
					return strip(tag.next_sibling)

			#Super atoi
			def satoi(string):
				try:
					return int(filter(unicode.isdigit, string))
				except:
					return None

			#Information
			self.licensors = get_info("Licensors", True)
			self.studios = get_info("Studios", True)
			self.source = get_info("Source", False)
			self.genres = get_info("Genres", True)
			self.duration = satoi(get_info("Duration", False))

			#Statistics
			self.public_score = float(soup.find(itemprop = "ratingValue").string)
			self.rank = satoi(get_info("Ranked", False))
			self.popularity = satoi(get_info("Popularity", False))

			#Criar novo anime na cache
			self.criar_novo_anime()
		
	def criar_novo_anime(self):
		file_json = json.dumps(self.__dict__, indent = 4)
		if not(os.path.exists(ANIMES_PATH)):
			os.makedirs(ANIMES_PATH)
		with open(self.get_nome_arq(), "w") as arq:
			arq.write(file_json)
			print self.title.encode("utf-8")

	def get_nome_arq(self):
		return ANIMES_PATH + str(self.id) + ".json"
	#todo
	#def __str__(self):

"""
atributos iniciais
  status (animes que tão no dropped sofrem punição?)
  type
  episodes (total)
  year (ver se a tag anime_start_date_string corresponde à data de lançamento)
  licensors (? pode ser ultil em uma possível oficialização onde a disponibilidade de transmissão local oficial é um fator)
  studios
  source (imagino que vai ter pouco impacto)
  genres
  duration
  rating
  public_score
  rank
  popularity
  user_score (OBJETIVO)
"""

"""
todo:? criar filtros
  eg.: numero minimo (e maximo) de episódios (total ou assistidos),
	   casamento de caracteres pros fitros comuns
	   exigir que um atributo contenha um valor (nota do usuário)
	   etc
"""

#Status
class Status:
	watching = "1"
	completed = "2"
	hold = "3"
	dropped = "4"
	plan = "6" #Não sei nem se faz sentido esse.
	todos = "7"

def get_lista(usuario, status = Status.todos):
	#todo: deixar retornar mais de um status por vez?
	url = MAL_URL + "/animelist/" + usuario + "?status=" + status

	response = urllib2.urlopen(url)
	pagina = response.read()

	soup = BeautifulSoup(pagina, 'lxml')
	return map(lambda ue: Anime.from_user_entry(ue), json.loads(soup.find(class_ = "list-table")["data-items"]))

u = get_lista(usuario)
