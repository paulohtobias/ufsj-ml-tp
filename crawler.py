# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import json
import datetime

MAL_URL = "https://myanimelist.net"

# futuro
class Anime:
    def __init__(self, user_entry):
        self.title = user_entry["anime_title"]
        self.url = user_entry["anime_url"] #Pode ser usado como "hash" na cache
        self.status = user_entry["status"]
        self.type = user_entry["anime_media_type_string"]
        self.episodes = user_entry["anime_num_episodes"]
        self.year = datetime.datetime.strptime(user_entry["anime_start_date_string"][-2:], "%y").year
        self.rating = user_entry["anime_mpaa_rating_string"]
        self.user_score = user_entry["score"] #LEMBRETE: score == 0 significa que ainda não foi avaliado.
        self.update_from_url()

    def update_from_url(self):
        #todo: olhar se já tem na cache pra evitar bobeira

        url = MAL_URL + self.url
        response = urllib2.urlopen(url.encode("UTF-8"))
        pagina = response.read()
        soup = BeautifulSoup(pagina, "lxml")

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
        satoi = lambda string: int(filter(unicode.isdigit, string))

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

        #todo: inserir o anime na cache

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

usuario = "Master_Exploder"

def get_lista(usuario, status = Status.todos):
    #todo: deixar retornar mais de um status por vez?
    url = MAL_URL + "/animelist/" + usuario + "?status=" + status

    response = urllib2.urlopen(url)
    pagina = response.read()

    soup = BeautifulSoup(pagina, 'lxml')
    return json.loads(soup.find(class_="list-table")["data-items"])

u = get_lista(usuario)
a = Anime(u[4])
print json.dumps(a.__dict__, indent=4)
