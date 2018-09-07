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
	def from_url(url, ingnore_cache = False):
		anime = Anime()

		anime.url = url
		anime.id = int(url.split("/")[2])

		#Verificar se o anime já está salvo na cache
		try:
			if ingnore_cache:
				raise Exception() #Pra cair no bloco ecxept
			with open(anime.get_nome_arq(), "r") as arquivo:
				#todo: isso é muito roubo e não sei se vai dar certo assim. Precisa testar mais.
				#Em último caso tem que setar cada atributo separadamente.
				anime.__dict__ = json.loads(arquivo.read())
				return anime
		except:
			try:
				pagina = urllib2.urlopen((MAL_URL + url).encode("UTF-8")).read()
				soup = BeautifulSoup(pagina, "html5lib")
			except:
				print "Erro ao realizar request na pagina"
				return None

			def get_year():
				s = Anime.get_info(soup, "Aired", False)
				if s == "Not available":
					return None
				i = s.find(",") + 2
				return int(s[i : i + 4])

			anime.title = soup.find(itemprop = "name").string

			anime.type = Anime.get_info(soup, "Type", False)
			anime.episodes = Anime.get_info(soup, "Episodes", False)
			anime.year = get_year()
			try:
				anime.rating = Anime.get_info(soup, "Rating", False).split(" - ")[0]
			except:
				anime.rating = None

			anime.update_from_url(soup, ingnore_cache)

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
		try:
			#Criar nova avaliação do usuario para o anime
			Avaliacao(user_entry, anime.id)
		
			anime.update_from_url()
		except:
			return None
			
		return anime

	def update_from_url(self, soup = None, ingnore_cache = False):
		#Verificar se o anime já está salvo na cache
		try:
			if ingnore_cache:
				raise Exception() #Pra cair no bloco ecxept
			with open(self.get_nome_arq()) as arquivo:
				#todo: isso é muito roubo e não sei se vai dar certo assim. Precisa testar mais.
				#Em último caso tem que setar cada atributo separadamente.
				self.__dict__ = json.loads(arquivo.read())
				return
		except:
			url = MAL_URL + self.url
			if soup == None:
				pagina = urllib2.urlopen(url.encode("UTF-8")).read()
				soup = BeautifulSoup(pagina, "html5lib")

			#Super atoi
			def satoi(string):
				try:
					return int(filter(unicode.isdigit, string))
				except:
					return None

			#Information
			self.licensors = Anime.get_info(soup, "Licensors", True)
			self.studios = Anime.get_info(soup, "Studios", True)
			self.source = Anime.get_info(soup, "Source", False)
			self.genres = Anime.get_info(soup, "Genres", True)
			self.duration = satoi(Anime.get_info(soup, "Duration", False))

			#Statistics
			try:
				self.public_score = float(Anime.get_info(soup, "Score", False))
			except:
				self.public_score = None
			self.rank = satoi(Anime.get_info(soup, "Ranked", False))
			self.popularity = satoi(Anime.get_info(soup, "Popularity", False))

			#Criar novo anime na cache
			self.criar_novo_anime()
		
	def criar_novo_anime(self):
		file_json = json.dumps(self.__dict__, indent = 4)
		if not(os.path.exists(ANIMES_PATH)):
			os.makedirs(ANIMES_PATH)
		with open(self.get_nome_arq(), "w") as arq:
			arq.write(file_json)

	def get_nome_arq(self):
		return ANIMES_PATH + str(self.id) + ".json"
	
	@staticmethod
	def get_info(soup, atributo, is_list):
		tag = soup.find(string = atributo + ":").parent

		#Funções úteis
		def strip(t):
			try:
				return t.string.strip(" ,\n")
			except:
				return ""
		filtro = lambda s: len(s) > 0 and s not in ["None found", "add some"]

		if is_list:
			info_list = filter(filtro, map(strip, list(tag.next_siblings)))
			if len(info_list) > 0:
				return info_list
			else:
				return None
		else:
			info = tag.next_sibling
			while not filtro(strip(info)):
				info = info.next_sibling
			
			sinfo = strip(info)
			if sinfo == "Unknown":
				return None
			else:
				return strip(info)

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

#u = get_lista(usuario)
