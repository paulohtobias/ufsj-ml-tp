# -*- coding: utf-8 -*-

import urllib2
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import datetime
import os
import re

MAL_URL = "https://myanimelist.net"
ANIMES_PATH = "data/animes/"

class Avaliacao:
	def __init__(self, usuario, user_entry):
		self.user_name = usuario
		self.num_watched_episodes = user_entry["num_watched_episodes"]
		user_score = user_entry["score"]
		if user_score > 0:
			self.user_score = user_score
		else:
			self.user_score = None
		self.status = user_entry["status"]

		self.criar_nova_avaliacao(user_entry["anime_id"])

	def criar_nova_avaliacao(self, id_anime):
		file_json = json.dumps(self.__dict__, indent = 4)
		user_path = self.get_path()
		if not(os.path.exists(user_path)):
			os.makedirs(user_path)
		with open(user_path + "/" + str(id_anime) + ".json", "w") as arq:
			arq.write(file_json)

	def get_path(self):
		return "data/users/" + self.user_name

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

			#Super atoi
			def satoi(string):
				try:
					return int(filter(unicode.isdigit, string))
				except:
					return None

			#Information
			anime.licensors = Anime.get_info(soup, "Licensors", True)
			anime.studios = Anime.get_info(soup, "Studios", True)
			anime.source = Anime.get_info(soup, "Source", False)
			anime.genres = Anime.get_info(soup, "Genres", True)
			anime.duration = satoi(Anime.get_info(soup, "Duration", False))

			#Statistics
			try:
				anime.public_score = float(Anime.get_info(soup, "Score", False))
			except:
				anime.public_score = None
			anime.rank = satoi(Anime.get_info(soup, "Ranked", False))
			anime.popularity = satoi(Anime.get_info(soup, "Popularity", False))

			#Criar novo anime na cache
			anime.criar_novo_anime()

			return anime

	@staticmethod
	def from_user_entry(username, user_entry):
		anime = Anime.from_url(user_entry["anime_url"])

		if anime != None:
			try:
				#Criar nova avaliação do usuario para o anime
				Avaliacao(username, user_entry)
			except:
				return None

		return anime
	
	@staticmethod
	def from_file(username, filename):
		with open(ANIMES_PATH + filename) as f:
			url = json.loads(f.read())["url"]

			return Anime.from_url(url)
		
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

def get_lista(usuario, status = Status.todos, browser = None, force_update = False):
	if os.path.exists("data/users/" + usuario) and force_update == False:
		lista = []

		for (dirpath, dirnames, filenames) in os.walk("data/users/" + usuario):
			for filename in filenames:
				lista.append(Anime.from_file(usuario, filename))
			break

		return lista

	url = MAL_URL + "/animelist/" + usuario + "?status=" + status

	try:
		response = urllib2.urlopen(url)
	except:
		return None

	pagina = response.read()

	soup = BeautifulSoup(pagina, 'html5lib')
	try:
		lista = map(lambda ue: Anime.from_user_entry(usuario, ue), json.loads(soup.find(class_ = "list-table")["data-items"]))
	except:
		statuses = [status]
		if status == Status.todos:
			statuses = [Status.watching, Status.completed, Status.hold, Status.dropped, Status.plan]

		geckodriver = "./geckodriver"

		bq = False
		if browser == None:
			options = webdriver.FirefoxOptions()
			options.add_argument("-headless")

			browser = webdriver.Firefox(executable_path=geckodriver, firefox_options=options)
			bq = True

		lista = []

		for status in statuses:
			url = MAL_URL + "/animelist/" + usuario + "?status=" + status

			browser.get(url)

			pagina = browser.page_source

			soup = BeautifulSoup(pagina, "html5lib")

			tags = list(soup.find_all(class_="animetitle"))

			#Para cada anime
			for tag in tags:
				ts = list(tag.parent.next_siblings)
				user_entry = {}
				user_entry["anime_url"] = tag.get("href")
				user_entry["anime_id"] = user_entry["anime_url"].split("/")[2]
				user_entry["status"] = status

				try:
					user_entry["score"] = int(ts[1].string.strip())
				except:
					user_entry["score"] = 0

				try:
					user_entry["num_watched_episodes"] = int(ts[5].string.strip())
				except:
					try:
						user_entry["num_watched_episodes"] = int(ts[5].span.string.strip())
					except:
						user_entry["num_watched_episodes"] = 0

				lista.append(Anime.from_user_entry(usuario, user_entry))

		if bq:
			browser.quit()

	print url
	return lista

if __name__ == "__main__":
        arq = open("users.txt","r")
        lista = map(lambda s: s.strip(), set(arq.readlines()))
        for user in lista:
                get_lista(user)
        arq.close()
